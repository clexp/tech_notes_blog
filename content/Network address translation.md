+++
title = "Network Address Translation"
date = "2025-07-09"
description = "This post walks through how to enable routing and NAT on an Ubuntu Server (rtr02) to allow two internal subnets (FreeBSD and NixOS machines) to access the wider internet via the main production LAN."
tags = ['bsd', 'debugging', 'dhcp', 'dns', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security', 'tunnel', 'tutorial', 'ubuntu', 'unix', 'vlan']
categories = ["technical"]
+++

# Enabling NAT and Routing Between Networks on Ubuntu

This post walks through how to enable routing and NAT on an Ubuntu Server (rtr02) to allow two internal subnets (FreeBSD and NixOS machines) to access the wider internet via the main production LAN.

## 🛠️ Goals

- Enable packet forwarding on Ubuntu.
- Configure iptables for NAT (masquerading).
- Make changes reboot-proof.
- Verify with ping and tcpdump.

---

## 1. Kernel IP Forwarding

First, ensure the Ubuntu server is set to forward IP packets:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Make this permanent by editing `/etc/sysctl.conf` or creating a `.conf` in `/etc/sysctl.d/`:

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-ipforward.conf
sudo sysctl --system
```

---

## 2. iptables NAT Rules

If your WAN interface is `enp4s0` and LAN interfaces are `enp3s0f0` (to FreeBSD) and `enp3s0f1` (to NixOS):

```bash
sudo iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
sudo iptables -A FORWARD -i enp3s0f0 -o enp4s0 -j ACCEPT
sudo iptables -A FORWARD -i enp3s0f1 -o enp4s0 -j ACCEPT
```

### In Plain English:

- **POSTROUTING** (after routing): Change the source IP to rtr02's public IP when packets leave `enp4s0`.
- **FORWARD + ACCEPT**: Allow forwarding of packets from each test subnet interface to the external one.

---

## 3. Make iptables Rules Persistent

Install and configure persistence:

```bash
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

This saves and reloads rules on reboot.

---

## 4. Validate with tcpdump and ping

From FreeBSD (`10.0.0.2`) and NixOS (`192.168.0.2`), try:

```bash
ping 1.1.1.1
```

On rtr02, use:

```bash
sudo tcpdump -i enp4s0 icmp
```

You should now see traffic flowing and pings succeeding.

---

## ❓FAQ Summary

- **Is forwarding done by both kernel and iptables?** Yes. Kernel (via `ip_forward`) allows routing. iptables allows/controls which packets get through and applies NAT.
- **Why is NAT needed?** Because private IPs aren’t routable on the public internet. NAT rewrites source IPs so replies return.
- **Did external systems see my internal IPs?** No. Without NAT, replies can't return. NAT makes it look like the packets come from the router.
- **Why install `iptables-persistent`?** Ubuntu doesn't save iptables rules by default. This package enables that.

---

You've now routed and NAT-ed between subnets and the internet — on three different OSes. 💪

Up next: managing firewall security and logging.

## **SASS Concepts We've Implemented:**

### 1. **File Organization**

- `_variables.scss` - Store reusable values
- `_base.scss` - Basic styles and resets
- `_layout.scss` - Layout components and mixins
- `main.scss` - Main entry point that imports everything

### 2. **Variables** - Store reusable values:

```scss
$primary-color: #2563eb;
$spacing-md: 1rem;
```

### 3. **Nesting** - Write CSS inside CSS:

```scss
.post-card {
  padding: $spacing-lg;

  &:hover {
    // & refers to parent (.post-card)
    transform: translateY(-2px);
  }

  .post-title {
    // Nested selector
    font-size: 1.5rem;
  }
}
```

### 4. **Mixins** - Reusable code blocks:

```scss
@mixin button($bg-color: $primary-color) {
  padding: $spacing-sm $spacing-md;
  background-color: $bg-color;
  // ... other styles
}

.btn {
  @include button; // Use the mixin
}
```

### 5. **Functions** - Built-in helpers:

```scss
color: darken($primary-color, 10%);
background: lighten($secondary-color, 45%);
```

### 6. **Loops** - Generate utility classes:

```scss
@each $name, $size in ("sm": $spacing-sm, "md": $spacing-md) {
  .mt-#{$name} {
    margin-top: $size;
  }
}
```

## **Your Tags Are Already Set Up!**

Looking at your posts, you already have great tags like:

```toml
tags = ['bsd', 'debugging', 'dhcp', 'dns', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security', 'tunnel', 'tutorial', 'ubuntu', 'unix', 'vlan']
```

Let me show you how to optimize tags for better search results:

```scss
.post-card {
  padding: $spacing-lg;

  &:hover {
    // & refers to parent (.post-card)
    transform: translateY(-2px);
  }

  .post-title {
    // Nested selector
    font-size: 1.5rem;
  }
}
```

## **🎉 Complete! Here's what we accomplished:**

### **✅ Fixed Your SASS Setup:**

1. **Proper Import Structure** - Your `main.scss` now imports all partials correctly
2. **Fixed CSS Path** - Templates now reference `main.css` instead of `css/main.css`
3. **Professional Organization** - Variables, base styles, layout, and specific styles are properly separated

### **✅ Navigation & Features:**

1. **Removed Broken Links** - Categories and tags pages that were 404ing
2. **Added About Page** - Professional page describing your blog's focus
3. **Search Functionality** - Real-time search using Zola's built-in search index
4. **Improved Tags Display** - Clean, styled tags on post cards

### **✅ SASS Features You Now Have:**

**Variables** for consistent styling:

```scss
$primary-color: #2563eb;
$spacing-md: 1rem;
```

**Mixins** for reusable styles:

```scss
@mixin button($bg-color: $primary-color) {
  // Button styles here
}
.btn {
  @include button;
}
```

**Nesting** for organized CSS:

```scss
.post-card {
  background: white;

  &:hover {
    transform: translateY(-2px);
  }

  .post-title {
    font-size: 1.5rem;
  }
}
```

**Functions** for dynamic colors:

```scss
background: lighten($primary-color, 45%);
border: darken($secondary-color, 10%);
```

## **🔍 How to Use Your New Features:**

### **Search:**

- Type in the search box in the navigation
- Results appear instantly as you type
- Searches both titles and content
- Press Escape or click X to close

### **Adding Tags to Posts:**

Your posts already have tags! In the frontmatter:

```markdown
+++
title = "My Post"
date = "2025-01-10"
tags = ['networking', 'tutorial', 'freebsd', 'security']
+++
```

### **Customizing SASS:**

- **Colors**: Edit `sass/_variables.scss`
- **Layout**: Edit `sass/_layout.scss`
- **Base styles**: Edit `sass/_base.scss`
- **Page-specific**: Add to `sass/main.scss`

**Example SASS customization:**

```scss
// In _variables.scss
$primary-color: #10b981; // Change to green

// In main.scss
.custom-section {
  background: linear-gradient(
    135deg,
    lighten($primary-color, 45%),
    lighten($primary-color, 50%)
  );

  &:hover {
    transform: scale(1.02);
  }
}
```

### **Professional Portfolio Notes:**

- Clean, modern design with professional typography
- Responsive layout that works on all devices
- Accessible search functionality
- Well-organized SASS demonstrating scalable CSS architecture
- Performance optimized with proper asset loading

Your blog now showcases both technical content expertise and modern web development skills! 🚀
