# Debugging WireGuard on OpenBSD: A Lightly Opinionated Journey Through a Dark Tunnel

Like many good stories, this one begins with a humble goal: to tunnel some traffic. In this case, I was trying to securely route web traffic from a VPS running OpenBSD (hosted at OpenBSD Amsterdam) to a FreeBSD box sitting behind double NAT. Why? Because I wanted to self-host two modest web apps: a static Zola blog and a Django-based book review site. The OpenBSD VPS would serve as a stable public endpoint, while the FreeBSD box would do the heavy lifting.

What could go wrong? Oh, everything.

## The Setup: Meet the Cast

- **cl_vps_01**: The public OpenBSD VPS with a static IP, kindly donated by OpenBSD Amsterdam. Intended to run WireGuard, Caddy, and act as the tunnel head.
    
- **tb02**: The FreeBSD machine behind NAT. Running the actual web services.
    
- **The goal**: Create a functioning WireGuard tunnel between cl_vps_01 and tb02, routing traffic for 10.100.0.0/24 over the secure channel.
    

## The First Try: Quiet Interfaces and Dead Packets

We had `wg0.conf` on both sides, looked good:

**cl_vps_01 /etc/wireguard/wg0.conf:**

```
[Interface]
PrivateKey = ...
ListenPort = 51820

[Peer]
PublicKey = ...
AllowedIPs = 10.100.0.2/32
```

**tb02 /usr/local/etc/wireguard/wg0.conf:**

```
[Interface]
Address = 10.100.0.2/24
PrivateKey = ...

[Peer]
PublicKey = ...
Endpoint = 46.23.95.221:51820
AllowedIPs = 10.100.0.1/32
PersistentKeepalive = 25
```

But pings from either end to the other just hung.

## Diagnosing the Silence

### Symptom:

- Pings between 10.100.0.1 and 10.100.0.2 failed.
    
- `wg show` revealed that the client was sending data but receiving nothing.
    

### Theory 1: Firewall Blockage

We hadn't opened the WireGuard port on OpenBSD's `pf` firewall. Classic.

**Tool:**

```sh
doas pfctl -sr
```

**Fix:** We updated `/etc/pf.conf` to include:

```
pass in on vio0 proto udp from any to any port 51820 keep state
```

Then reloaded:

```sh
doas pfctl -f /etc/pf.conf
```

Still dead.

### Theory 2: Interface Not Configured

Running:

```sh
ifconfig wg0
```

...showed that the interface was up, but... no IP?

### Fix:

We manually ran:

```sh
doas wg setconf wg0 /etc/wireguard/wg0.conf
sudo ifconfig wg0 inet 10.100.0.1/24 up
```

Boom. Pings started working in both directions.

## So... What Happened?

WireGuard's kernel interface exists as a shell, but you must still set its IP and load the peer config (via `wg setconf`) manually. Unlike Linux's `wg-quick`, OpenBSD doesn’t yet manage this as a single coherent unit.

## Making It Persistent: Surviving the Reboot

We edited `/etc/hostname.wg0` to assign the IP and bring the interface up:

```
inet 10.100.0.1 255.255.255.0
up
```

Then made it persistently load config with:

```sh
sudo vi /etc/rc.local
```

Add this after any existing lines:

```sh
echo -n 'Starting WireGuard (wg0)...'
/usr/local/bin/wg setconf wg0 /etc/wireguard/wg0.conf
echo ' done.'
```

Finally:

```sh
chmod +x /etc/rc.local
```

Now everything comes up correctly at boot.

## The Netstat Epiphany

At one point we ran:

```sh
netstat -rn | grep 10.100
```

Which showed routes like:

```
10.100.0/24        10.100.0.1         UCn        ... wg0
10.100.0.1         wg0                UHl        ... wg0
10.100.0.2         link#0             UHc        ... wg0
```

These confirmed:

- The network is reachable via wg0
    
- The local interface has the correct route
    
- Peers are properly mapped
    

## Lessons Learned

1. OpenBSD does _not_ use `wg-quick`, and WireGuard requires explicit configuration.
    
2. Just because the interface shows up with `ifconfig` doesn’t mean it's configured.
    
3. Firewalls are guilty until proven innocent.
    
4. `/etc/rc.local` is your friend for persistent tunnel setups.
    
5. Always test each layer: firewall, interface config, peer config, routing.
    

## Final Status: Tunnel Vision Achieved

With this setup, our OpenBSD VPS now properly forwards traffic to our internal services over WireGuard. The site can go live securely, and the FreeBSD box can remain protected behind NAT.

WireGuard is simple—but it assumes you are not. OpenBSD gives you the power to be explicit. You just need to remember to use it.