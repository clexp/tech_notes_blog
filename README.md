# Tech Blog

A professional technical blog built with [Zola](https://www.getzola.org/) static site generator, demonstrating modern web development practices, infrastructure automation, and complex deployment workflows.

## 🚀 Live Site

**[https://blog.clexp.net](https://blog.clexp.net)**

## ✨ Features

### Frontend Excellence

- **Modern SASS Architecture**: Organized with variables, mixins, and modular stylesheets
- **Real-time Search**: Dropdown search with Elasticlunr.js integration
- **Responsive Design**: Mobile-first approach with professional styling
- **Tag System**: Categorized posts with visual tag display
- **SEO Optimized**: Clean URLs, meta descriptions, and semantic HTML

### Technical Implementation

- **Static Site Generation**: Zola with template inheritance
- **Asset Pipeline**: Automatic SASS compilation and optimization
- **Search Index**: Client-side search with full-text indexing
- **Performance**: Lightweight, fast-loading pages

## 🛠 Tech Stack

- **[Zola](https://www.getzola.org/)**: Modern static site generator in Rust
- **SASS**: CSS preprocessing with advanced features
- **JavaScript**: Vanilla JS for search functionality
- **Elasticlunr.js**: Client-side search indexing
- **HTML5/CSS3**: Modern web standards

## 📁 Project Structure

```
Tech_Blog/
├── config.toml           # Zola configuration (dev default, base_url = "/")
├── config.prod.toml      # Production override (base_url = https://blog.clexp.net)
├── content/              # Markdown blog posts (the only folder Zola builds from)
├── raw_blogs/            # Ingestion folder: plain-markdown source material, pre-front-matter
├── templates/            # Jinja2 templates
├── sass/                 # SASS stylesheets
│   ├── _variables.scss   # Design tokens
│   ├── _base.scss        # Base styles
│   ├── _layout.scss      # Layout components
│   └── main.scss         # Main entry point
├── static/               # Static assets
├── archive/              # Retired docs/scripts/media, kept for reference only
└── public/               # Generated site (ignored, built by zola)
```

## 🚧 Development

### Prerequisites

- [Zola](https://www.getzola.org/documentation/getting-started/installation/) installed

### Local Development

```bash
# Serve locally with hot reload (drafts hidden by default)
zola serve

# Preview drafts too
zola serve --drafts

# Build for production (only non-draft content, correct base_url)
zola -c config.prod.toml build
```

See [WORK_FLOW.md](./WORK_FLOW.md) for the full draft → production workflow,
and how to tell a draft post from a published one.

### Content Management

See [WORK_FLOW.md](./WORK_FLOW.md) for the full pipeline from `raw_blogs/` to a
published post. Short version:

1. Drop raw material in `raw_blogs/` (plain markdown, no front matter needed).
2. Write the post in `content/<section>/<slug>.md` with `draft = true` in the
   front matter while you work on it.
3. Preview with `zola serve --drafts`.
4. Remove `draft = true` when it's ready to publish.

## 🌐 Deployment

```
Internet → OpenBSD VPS (relayd + TLS) → WireGuard → rtr04 → DNAT → MilkV nginx
```

Deployment is one command, run from either this repo or `~/MilkV`:

```bash
~/MilkV/lab/deploy-blog.sh
```

This builds `~/Tech_Blog` with `config.prod.toml` and rsyncs `public/` to the
MilkV nginx docroot (`/var/www/blog`). The old `deploy.sh` in this repo targeted
a retired FreeBSD jail host and has been archived to `archive/deploy.sh` — do
not use it.

TLS termination, DNS, and the WireGuard/VLAN network path are owned by sibling
projects (`~/OpenBSD_web`, `~/MilkV`) and are out of scope for this repo.

## 🎯 Key Learning Outcomes

### SASS Architecture

- **Variables**: Centralized design tokens
- **Mixins**: Reusable CSS components
- **Nesting**: Organized, maintainable stylesheets
- **Functions**: Dynamic color manipulation
- **Responsive Design**: Mobile-first breakpoints

### Search Implementation

- **Index Generation**: Zola's built-in search index
- **Client-side Search**: JavaScript with Elasticlunr
- **UX Patterns**: Dropdown results with keyboard navigation
- **Performance**: Minimal payload, fast search

### Infrastructure Skills

- **FreeBSD Administration**: Jail management, permissions
- **OpenBSD Security**: pf firewall, relayd configuration
- **Network Troubleshooting**: VPN tunnels, health checks
- **Service Management**: Process monitoring, log analysis

## 🔧 Technical Challenges Solved

1. **SASS Compilation Issues**: Fixed template paths and build process
2. **Search Functionality**: Implemented dropdown search with proper state management
3. **Network Connectivity**: Debugged firewall rules and VPN routing
4. **Load Balancer Health Checks**: Configured proper service monitoring
5. **IPv6 Deployment**: Full dual-stack network configuration

## 📊 Performance

- **Fast Loading**: Optimized static assets and minimal JavaScript
- **Search Performance**: < 100ms query response time
- **Mobile Optimized**: Responsive design with touch-friendly interface
- **SEO Ready**: Semantic HTML and proper meta tags

## 🎨 Design Philosophy

This project demonstrates:

- **Clean, Professional Design**: Minimal, content-focused interface
- **Performance First**: Optimized for speed and accessibility
- **Semantic HTML**: Proper document structure and SEO
- **Progressive Enhancement**: Works with JavaScript disabled
- **Mobile-First**: Responsive design from small screens up

## 🔒 Security & Best Practices

- **Static Site Security**: No server-side vulnerabilities
- **Firewall Configuration**: pf on the OpenBSD VPS, DNAT-only path to MilkV
- **Version Control**: Professional Git workflow
- **Documentation**: Comprehensive project documentation

## 📈 Skills Demonstrated

### Web Development

- Modern CSS architecture with SASS
- JavaScript DOM manipulation and event handling
- Responsive design and mobile optimization
- SEO and performance optimization
- Static site generation workflows

### System Administration

- FreeBSD jail management
- OpenBSD server configuration
- Network security and firewalls
- Service monitoring and health checks
- Log analysis and troubleshooting

### DevOps & Infrastructure

- Automated deployment pipelines
- VPN tunnel configuration
- Load balancer setup
- DNS management (IPv4/IPv6)
- Version control best practices

## 🤝 Contributing

This is a personal portfolio project showcasing professional development practices. The code demonstrates various techniques and patterns that may be useful for learning purposes.

## 📄 License

See [COPYRIGHT.md](./COPYRIGHT.md) for usage rights and restrictions.

---

**Built with attention to detail and professional development practices.**

_This project represents a complete full-stack development workflow, from initial design and implementation through complex infrastructure deployment and ongoing maintenance._
