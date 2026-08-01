# From Caddy to Clarity: Serving HTTPS the OpenBSD Way

Like many self-hosters and indie developers, I started my latest web project with a clear, modern goal: use [Caddy](https://caddyserver.com/) to serve a static site and a Django-powered book review app. The idea was simple—Caddy would handle HTTPS, reverse proxying, and all the delightful HTTP bits in a single binary. Clean. Modern. Easy.

But there was a twist: the project was running on a VPS hosted by the excellent folks at [OpenBSD Amsterdam](https://openbsd.amsterdam/). And if you know OpenBSD, you know it doesn’t exactly roll out the red carpet for software that expects Linux-like behaviors.

## The Setup: A Clean VPS and a Clear Plan

The environment was as follows:

- **Host**: OpenBSD 7.5 running on a VM named `cl_vps_01`
    
- **Domain**: `clexp.net`, pointed via DNS to the VPS's public IP
    
- **Goal**: Serve a public-facing site over HTTPS, using Caddy for automatic TLS and reverse proxying to internal services via WireGuard
    

Initially, we planned to:

1. Expose ports 80 and 443 for HTTP/S traffic
    
2. Run Caddy on high ports like 8080 and 8443 (the "OpenBSD way")
    
3. Use PF to forward traffic from ports 80/443 to those high ports
    

Simple, right? Let's walk through what actually happened.

---

## Step One: Install and Configure Caddy

We started by installing Caddy via OpenBSD packages:

```
doas pkg_add caddy
```

Then we wrote a minimal Caddyfile:

```caddyfile
{
  admin 127.0.0.1:3020
  log {
    output file /var/log/caddy/access.log
  }
}
clexp.net:8443 {
  respond "Hello, World."
}
```

To avoid running Caddy as root (since OpenBSD disallows non-root daemons from binding to ports <1024), we had it listen on 8443. Then we added PF rules to redirect traffic:

```pf
pass in proto tcp from any to any port 80 rdr-to 127.0.0.1 port 8080
pass in proto tcp from any to any port 443 rdr-to 127.0.0.1 port 8443
```

We reloaded the PF configuration:

```
doas pfctl -f /etc/pf.conf
```

---

## First Sign of Trouble: HTTPS Certificate Fails

### Symptom:

Caddy logs showed it was trying to get a certificate from Let's Encrypt, but failed.

### Diagnosis:

Let’s Encrypt performs an HTTP-01 challenge by making a request to port 80 on the server. But PF redirection doesn’t rewrite the **destination IP**, so from Caddy’s perspective, the challenge request doesn’t match the domain.

### Tools Used:

- `tcpdump`: To inspect whether the request was hitting the loopback interface
    
- Caddy’s logs: For verbose TLS error messages
    

```sh
doas tcpdump -ni lo0 port 80 or port 443
```

**Bad output**: No traffic seen

**Good output**: Traffic to `127.0.0.1.8080`

---

## The Realization: Caddy Needs Direct Access to Ports 80/443

Caddy must bind directly to these ports to handle ACME HTTP challenges. Port forwarding isn’t good enough.

### Workaround Attempted:

We considered running Caddy as root to bind to 80/443 directly. But this is against both Caddy’s design and OpenBSD’s philosophy. OpenBSD expects daemons to run unprivileged. And even if we ran Caddy as root, the port binding might have worked, but the package was not designed with root-executed service in mind.

---

## The Lightbulb Moment: Use the OpenBSD Stack Instead

We took a step back. What were we really trying to achieve?

- Serve HTTPS
    
- Host a static site
    
- Reverse proxy to a backend app (Django)
    

OpenBSD has tools that do all of this:

|Function|Tool|
|---|---|
|Serve web|`httpd`|
|TLS certificates|`acme-client`|
|Reverse proxy|`relayd`|

### We Decided: Go Full Native

---

## Setting Up `acme-client` and `httpd`

### Step 1: TLS Certificates

Create `/etc/acme-client.conf`:

```conf
domain "clexp.net" {
    domain key "/etc/ssl/private/clexp.net.key"
    domain fullchain "/etc/ssl/clexp.net.fullchain.pem"
    sign with letsencrypt
}
```

Then run:

```sh
doas acme-client -v clexp.net
```

Check `/etc/ssl/` for the key and cert.

### Step 2: Web Server Configuration

Create `/etc/httpd.conf`:

```httpd
server "clexp.net" {
    listen on * port 80
    listen on * tls port 443
    tls {
        certificate "/etc/ssl/clexp.net.fullchain.pem"
        key "/etc/ssl/private/clexp.net.key"
    }

    location "/" {
        root "/htdocs"
        directory index "index.html"
    }
}
```

Enable and start the service:

```sh
doas rcctl enable httpd
sudo rcctl start httpd
```

Now visiting [https://clexp.net](https://clexp.net/) shows our static page with a valid TLS cert.

---

## Lessons Learned

### What Didn’t Work

- Using PF to redirect ports to high-numbered ones for Caddy
    
- Letting Caddy fetch certs when it doesn’t control port 80
    

### What Did Work

- Using `acme-client` to handle certs the OpenBSD way
    
- Letting `httpd` serve content directly over HTTPS
    

---

## Final Thoughts

Caddy is great—on Linux. It simplifies HTTPS setup tremendously. But on OpenBSD, it clashes with the base system’s design. Instead of bending the system to fit Caddy, we learned to let OpenBSD lead the way.

By using `httpd` and `acme-client`, we achieved everything we set out to do, but with better integration, fewer moving parts, and total harmony with the operating system.

Sometimes, the right tool isn’t the most popular one—it’s the one that speaks the same language as your platform.