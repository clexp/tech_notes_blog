+++
title = "Dual Homed Nas For Backup"
date = "2025-07-09"
description = "Debugging DNS and NAT in a Multi-NIC Home Lab: A Case Study"
tags = ['architecture', 'backup', 'bsd', 'containers', 'debugging', 'devops', 'dns', 'docker', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'security', 'storage', 'troubleshooting', 'ubuntu', 'unix', 'vlan']
categories = ["technical"]
+++

Debugging DNS and NAT in a Multi-NIC Home Lab: A Case Study

Here’s a detailed blog post draft based on your experience debugging the DNS and NAT issues with your FreeBSD backup box (`bub03`) and Docker-based Pi-hole on `nas04`. The style assumes a technical audience familiar with networking and Unix/Linux/BSD systems.

---

## **Debugging DNS and NAT in a Multi-NIC Home Lab: A Case Study**

In this post, I’ll walk through a recent real-world debugging session from my home lab. The core issue: a FreeBSD ZFS backup box (`bub03`) behind a dual-homed Ubuntu server (`nas04`) couldn't resolve DNS or access the internet—despite everything _looking_ correct.

## 🧩 **Symptoms**

The main symptoms:

- `dig` and `ping` to public addresses failed on `bub03`/FreeBSD.
- However `drill bbc.co.uk` works
    
- DNS queries to the local Pi-hole (`192.168.178.52`) worked but to 8.8.8.8 did not.
    
- `nc` (netcat) to port 53 showed no response.
    
- Local ping to gateway (`192.168.177.1`) and LAN (`192.168.178.1`) sometimes worked.
    
- Outbound HTTPS connections (e.g. to `pkg.freebsd.org`) failed.
    
- Docker container (`pihole`) was running with `-p 192.168.178.52:53:53`, so DNS _should_ have been reachable.
    

At first glance, everything seemed correct:

- `bub03` was configured with a static IP, default route, and proper nameserver.
    
- `nas04` had IP forwarding and MASQUERADE enabled.
    
- Pi-hole was listening on the published IP and port.
    

So why were DNS and HTTP(S) timing out?

---

## 🏗️ **Architecture Overview**

Here's the network layout:

```
[LAN: 192.168.178.0/24]
        |
     FritzBox
        |
     nas04
     ├── enp3s0: 192.168.178.52 (LAN, Docker Pi-hole bound here)
     └── enp4s0: 192.168.177.1 (backup subnet, gateway for bub03)
            |
         bub03
         └── re0: 192.168.177.2 (FreeBSD box)
```

- `nas04` acts as a NAT gateway for the internal `192.168.177.0/24` subnet.
    
- Docker is running Pi-hole in bridge mode, binding to `192.168.178.52:53`.
    

---

## 💡 **Initial Theories**

Several culprits came to mind:

1. **Firewall or NAT misconfiguration**:
    
    - MASQUERADE rules may not cover traffic from 192.168.177.0/24.
        
    - iptables FORWARD or INPUT chains might be blocking traffic.
        
2. **Docker networking oddities**:
    
    - Docker bridge mode’s userland proxy may not be handling traffic properly.
        
    - Binding to the host interface (`192.168.178.52`) might not behave as expected for NATed traffic.
        
3. **Loopback routing**:
    
    - NAT replies to forwarded traffic might be misrouted if replies go via loopback instead of external interface.
        
4. **FreeBSD resolver behavior**:
    
    - `resolv.conf` might not be correctly written.
        
    - DNS might be bypassing the configured resolver due to `resolvconf` vs manual config.
        

---

## 🔍 **Debugging Process and Tools**

### ✅ Step 1: Confirm IP Routing

On `bub03`:

```sh
netstat -rn
```

Output:

```
Destination        Gateway            Flags
default            192.168.177.1      UGSc
```

This confirms `nas04` is the default gateway. Ping worked:

```sh
ping 192.168.177.1
```

### ✅ Step 2: Confirm DNS Settings

```sh
cat /etc/resolv.conf
```

Revealed:

```
nameserver 192.168.178.52
```

This _looked_ correct, but DNS queries still timed out.

### ✅ Step 3: Use `dig` and `nc`

```sh
dig @192.168.178.52 google.com
```

→ Timed out.

```sh
nc -v 192.168.178.52 53
```

→ No response.

### ✅ Step 4: Inspect NAT with `conntrack`

On `nas04`:

```sh
sudo conntrack -L | grep 192.168.177.2
```

Key entry:

```
tcp 6 86 TIME_WAIT src=192.168.177.2 dst=85.30.190.140 sport=37479 dport=443 ...
src=85.30.190.140 dst=192.168.178.52 sport=443 dport=37479 [ASSURED]
```

This told us:

- NAT rewrote the source of `bub03` traffic to `192.168.178.52` (as expected).
    
- Return traffic is arriving and being matched.
    
- NAT _is working_.
    

But... DNS traffic didn’t appear here.

### ✅ Step 5: Check Docker Bindings

On `nas04`:

```sh
sudo ss -lntup | grep 53
```

Output showed:

```
udp   UNCONN  0      0    192.168.178.52:53    *:*    users:(("docker-proxy", ...))
```

Pi-hole is bound correctly, but possibly not accessible from NATed clients because Docker’s userland proxy doesn't always handle NAT MASQUERADE traffic well—especially when the destination is the _same machine_ doing the NAT.

### ✅ Step 6: Test External Traffic

Back on `bub03`:

```sh
nc -v pkg.freebsd.org 443
```

→ ❌ Initially failed.

After the fix down below: Eventually:

```
Connection to pkg.freebsd.org 443 port [tcp/https] succeeded!
```

This meant **internet access worked**, and NAT replies were routed correctly!

### ✅ Step 7: Use `traceroute`

```sh
traceroute -n 8.8.8.8
```

Showed:

```
1  192.168.177.1
2  192.168.178.1
3  <ISP backbone...>
```

This proved the routing path from `bub03` to the outside world was intact.

---

## 🧠 **The Root Cause**

The issue was **not** with routing or NAT.

The problem was with **Docker and DNS on the host**:

- Docker's userland proxy did **not handle NATed requests** to port 53 well.
    
- Despite publishing `192.168.178.52:53:53`, NATed DNS queries from `bub03` silently failed.
    
- This is a known quirk in Docker’s networking when the host is both source of NAT _and_ target of traffic.
    

---

## 🛠️ **Workarounds and Fixes**

Here are some things that resolved or sidestepped the issue:

1. ✅ **Test with `tcpdump`** to confirm UDP 53 traffic reached the interface:
    
    ```sh
    sudo tcpdump -ni enp3s0 port 53
    ```
    
2. ✅ **Switch Docker to macvlan** or run Pi-hole directly on the host to avoid Docker NAT complexities.
    
3. ✅ **Add a MASQUERADE rule for internal subnet:**
    
    ```sh
    iptables -t nat -A POSTROUTING -s 192.168.177.0/24 -o enp3s0 -j MASQUERADE
    ```
    
4. ✅ **Use a simpler upstream DNS for `bub03`** temporarily to rule out Pi-hole:
    
    ```sh
    echo 'nameserver 1.1.1.1' > /etc/resolv.conf
    ```
    

---

## 🧪 **Lessons Learned**

- Docker's networking stack is surprisingly leaky and opaque when used on systems doing NAT.
    
- Diagnosing NAT issues _requires visibility_, and tools like `conntrack`, `tcpdump`, and `traceroute` are essential.
    
- Always test connectivity from the perspective of each interface (client, gateway, and destination).
    
- Pi-hole in Docker is powerful, but can be problematic when tightly coupled with complex network architectures.
    

---

## 🧭 **Next Steps**

Now that routing and DNS are fixed, we’ll move on to:

- Setting up Wake-on-LAN for `bub03`
    
- Automating ZFS snapshots and replication with `sanoid` and `syncoid`
    
- Scheduling nightly backup + shutdown routines
    

Stay tuned for Part 2: **Automated, Low-Power ZFS Backups in a Home Lab.**

---

Would you like this exported as Markdown or HTML for your blog engine (Zola, Pelican, etc.)?
