+++
title = "Building and Deploying a Zola Site"
date = "2024-12-19"
description = "Static site generators promise simplicity: write markdown, get a website. But building a professional blog with modern styling, search functionality, and deploying it through a complex home lab infrastructure proved to be anything but simple..."
tags = ["zola", "sass", "css", "web-development", "freebsd", "openbsd", "nginx", "wireguard", "networking", "deployment", "debugging", "tutorial", "architecture"]
categories = ["technical"]
+++

## Building and Deploying a Zola Site: From SASS to Production

_By clexp, documenting a real static site deployment journey_

---

## Overview

Static site generators promise simplicity: write markdown, get a website. But building a professional blog with modern styling, search functionality, and deploying it through a complex home lab infrastructure proved to be anything but simple. This post documents the complete journey from broken SASS imports to a production-ready blog accessible at `https://blog.clexp.net`, deployed through a FreeBSD jail, WireGuard tunnel, and OpenBSD VPS relay.

The goal wasn't just to get Zola working—it was to build something that showcases both technical content and professional web development skills.

---

## The Setup

- **Local Development:** macOS with Zola static site generator
- **Target Platform:** FreeBSD 14.2 jail running nginx
- **Network Path:** Home lab → WireGuard tunnel → OpenBSD VPS → Internet
- **Requirements:** Modern SASS styling, search functionality, professional design

The infrastructure topology:

```markdown
[Internet] ← HTTPS → [OpenBSD VPS] ← WireGuard → [FreeBSD Box] ← LAN → [Ubuntu Router] ← VLAN → [macOS Development]
(relayd) (nginx jail)
```

---

## Phase 1: The SASS Crisis

### The Problem

Starting with what appeared to be a working Zola setup, the first issue emerged immediately: SASS wasn't compiling properly. The templates referenced `css/main.css`, but Zola was outputting `main.css` directly in the public directory.

```bash
## Templates were looking for:
<link rel="stylesheet" href="&lbrace;&lbrace; get_url(path="css/main.css") &rbrace;&rbrace;">

## But Zola generated:
public/main.css
```

More critically, the SASS organization was a mess. Everything was crammed into a single `main.scss` file instead of using proper SASS architecture.

### The Solution: Proper SASS Architecture

The fix required restructuring the entire SASS codebase:

**File Organization:**

```
sass/
├── _variables.scss    # Color palette, spacing, breakpoints
├── _base.scss        # Typography, resets, basic styles
├── _layout.scss      # Header, footer, containers, grid
└── main.scss         # Entry point that imports everything
```

**Variables file (`_variables.scss`):**

```scss
// Colors
$primary-color: #2563eb;
$secondary-color: #64748b;
$background-color: #ffffff;
$text-color: #1e293b;

// Typography
$font-family: "Inter", sans-serif;
$font-size-base: 16px;
$line-height: 1.6;

// Spacing system
$spacing-sm: 0.5rem;
$spacing-md: 1rem;
$spacing-lg: 1.5rem;

// Responsive breakpoints
$mobile: 768px;
$desktop: 1024px;
```

**Main entry point (`main.scss`):**

```scss
// Import order matters!
@import "variables"; // First - used by other files
@import "base"; // Basic styles and resets
@import "layout"; // Layout components

// Page-specific styles here
.hero {
  background: linear-gradient(
    135deg,
    lighten($primary-color, 45%) 0%,
    lighten($primary-color, 50%) 100%
  );

  &-title {
    font-size: 3rem;

    @include mobile {
      font-size: 2rem; // Responsive design
    }
  }
}
```

**Template fix** - updating all template files:

```html
<!-- Changed from: -->
<link rel="stylesheet" href="&lbrace;&lbrace; get_url(path="css/main.css")
&rbrace;&rbrace;">

<!-- To: -->
<link rel="stylesheet" href="&lbrace;&lbrace; get_url(path="main.css")
&rbrace;&rbrace;">
```

---

## Phase 2: Modern Web Features

### Adding Search Functionality

Zola comes with built-in search index generation, but implementing the frontend required custom JavaScript:

**Zola configuration (`config.toml`):**

```toml
build_search_index = true
```

**Search UI and JavaScript:**

```html
<input
  type="search"
  id="search"
  placeholder="Search posts..."
  class="search-input"
/>

<div id="search-results" class="search-results hidden">
  <div class="search-results-content">
    <div class="search-results-header">
      <h3>Search Results</h3>
      <button id="close-search">&times;</button>
    </div>
    <div id="search-results-list"></div>
  </div>
</div>
```

**Search implementation:**

```javascript
// Initialize search index
window.addEventListener("DOMContentLoaded", function () {
  if (typeof window.searchIndex !== "undefined") {
    searchIndex = elasticlunr.Index.load(window.searchIndex);
  }
});

// Real-time search
searchInput.addEventListener("input", function (e) {
  const query = e.target.value.trim();

  if (query.length >= 1) {
    const results = searchIndex.search(query, {
      fields: {
        title: { boost: 2 },
        body: { boost: 1 },
      },
      expand: true,
    });
    displayResults(results.slice(0, 10));
    searchResults.classList.remove("hidden");
  }
});
```

### Navigation Overhaul

Replaced broken category/tag pages with functional navigation:

```html
<div class="nav-menu">
  <a href="&lbrace;&lbrace; config.base_url &rbrace;&rbrace;" class="nav-link">Home</a>
  <a href="&lbrace;&lbrace; get_url(path="about") &rbrace;&rbrace;" class="nav-link">About</a>
  <input type="search" id="search" placeholder="Search posts..." class="search-input">
</div>
```

---

## Phase 3: Production Deployment Challenge

### The FreeBSD Target

The target deployment environment: a FreeBSD 14.2 system running nginx in a jail. The jail structure:

```bash
## FreeBSD host: tb02 (10.0.0.50)
jls
## JID  IP Address      Hostname                      Path
## 4  10.100.0.5      nginx.clexp.internal          /usr/jails/nginx
```

### Network Discovery

First challenge: finding the FreeBSD box on the `10.0.0.0/24` subnet:

```bash
## From Ubuntu router (rtr02)
ip neigh show | grep "10.0.0"
## Output: 10.0.0.50 dev enp3s0f0 lladdr 00:e0:4c:02:0a:b4 STALE
```

SSH access confirmed:

```bash
ssh clexp@10.0.0.50
## Success! FreeBSD 14.2-RELEASE-p1 GENERIC
```

### Deployment Process

**Step 1: Build locally**

```bash
cd /Users/clexp/Sync/Tech_Blog
zola build
```

**Step 2: Copy to FreeBSD**

```bash
## Direct copy to FreeBSD box
scp -r public/* clexp@10.0.0.50:/tmp/blog-files/
```

**Step 3: Move to nginx jail**

```bash
## On FreeBSD host
doas cp -r /tmp/blog-files/* /usr/jails/nginx/usr/local/www/nginx-dist/
doas chown -R www:www /usr/jails/nginx/usr/local/www/nginx-dist/
```

**Step 4: Restart nginx in jail**

```bash
doas jexec nginx service nginx restart
```

---

## Phase 4: The VPS Relay Problem

### The Infrastructure

The blog needed to be accessible from the internet through a complex path:

- OpenBSD VPS (`cl_vps_01`) with public IPv4/IPv6
- WireGuard tunnel between VPS and FreeBSD box
- relayd on VPS forwarding HTTPS traffic through tunnel

### The Health Check Failure

Initial relayd status showed the problem:

```bash
doas relayctl show summary
## Id    Type      Name        Avlblty Status
## 4     relay     blog                active
## 4     table     blog:80             empty   ← Problem!
## 4     host      10.100.0.5          unknown ← Problem!
```

The table was "empty" because relayd's default ICMP health checks were failing—ICMP was blocked from the jail.

### The Firewall Detective Work

Two interconnected issues emerged:

**Issue 1: Wrong subnet in pf.conf**

```bash
## VPS firewall was allowing:
pass out on wg0 proto tcp to 10.0.0.2 port 80 keep state

## But the jail was at:
10.100.0.5  # Different subnet!
```

**Fix:**

```bash
## Updated to:
pass out on wg0 proto tcp to 10.100.0.0/24 port 80 keep state
```

**Issue 2: Health check method**

Changed relayd from ICMP to HTTP health checks:

```bash
## In /etc/relayd.conf, changed:
table <blog> { 10.100.0.5 }

## To:
table <blog> { 10.100.0.5 } check http "/" code 200
```

### The Moment of Truth

After applying both fixes:

```bash
doas pfctl -f /etc/pf.conf
doas relayctl reload
doas relayctl show summary

## Success!
## 4     table     blog:80             active (1 hosts)
## 4     host      10.100.0.5   100.00% up
```

---

## Phase 5: DNS and Final Testing

### DNS Configuration

Added AAAA record at Namecheap:

```
Type: AAAA
Host: blog
Value: 2a03:6000:95f4:618::224
```

### Verification

```bash
## DNS resolution working
dig AAAA blog.clexp.net
## blog.clexp.net. 1664 IN AAAA 2a03:6000:95f4:618::224

## Connectivity from internet
curl https://blog.clexp.net
## Returns full blog HTML!
```

---

## Key SASS Concepts Learned

### 1. File Organization

- **Partials**: Files starting with `_` for importing
- **Main entry**: Single file that imports all partials
- **Logical separation**: Variables, base styles, layout, components

### 2. Variables and Functions

```scss
$primary-color: #2563eb;
background: lighten($primary-color, 45%);
border: darken($secondary-color, 10%);
```

### 3. Nesting and BEM-style Organization

```scss
.post-card {
  padding: $spacing-lg;

  &:hover {
    transform: translateY(-2px);
  }

  &-title {
    font-size: 1.5rem;
  }
}
```

### 4. Mixins for Reusability

```scss
@mixin button($bg-color: $primary-color) {
  padding: $spacing-sm $spacing-md;
  background-color: $bg-color;
  border-radius: 4px;
}

.btn {
  @include button;
}
```

### 5. Responsive Design

```scss
@mixin mobile {
  @media (max-width: $mobile) {
    @content;
  }
}

.hero-title {
  font-size: 3rem;

  @include mobile {
    font-size: 2rem;
  }
}
```

---

## Lessons Learned

### SASS Architecture Matters

- **Proper organization** from the start saves refactoring pain
- **Variables and mixins** make maintenance exponentially easier
- **Import order** is critical—variables must come first

### Static Site Deployment

- **Test the full path** from development to production
- **Health checks** should match your actual service capabilities
- **Firewall rules** need to be precise—wrong subnets cause mysterious failures

### Debugging Complex Systems

- **Layer by layer**: Test each component independently
- **Status commands**: `relayctl show summary`, `jls`, `pfctl -sr`
- **Logs matter**: Always check service logs when troubleshooting

### Infrastructure as Code Benefits

- **Reproducible**: Clear documentation of every configuration
- **Maintainable**: Changes can be tracked and reverted
- **Educational**: Forces understanding of each component

---

## Epilogue

The blog is now live at `https://blog.clexp.net`, serving real traffic through a sophisticated infrastructure chain. What started as a simple "fix the SASS" task became a comprehensive lesson in modern web development, system administration, and network engineering.

The final stack demonstrates enterprise-level capabilities:

- **Modern frontend**: SASS-powered responsive design with JavaScript search
- **Secure hosting**: FreeBSD jail isolation with nginx
- **Privacy-focused networking**: WireGuard tunneling
- **Professional TLS**: OpenBSD relayd with Let's Encrypt certificates
- **High availability**: Health-checked load balancing

Most importantly, the blog now showcases both technical content expertise and practical implementation skills—exactly what was needed for a professional portfolio.

Sometimes the best way to learn a technology stack is to deploy something real through it.
