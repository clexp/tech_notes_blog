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
- **Python**: Content processing and conversion scripts

## 📁 Project Structure

```
Tech_Blog/
├── config.toml           # Zola configuration
├── content/              # Markdown blog posts
├── templates/            # Jinja2 templates
├── sass/                 # SASS stylesheets
│   ├── _variables.scss   # Design tokens
│   ├── _base.scss        # Base styles
│   ├── _layout.scss      # Layout components
│   └── main.scss         # Main entry point
├── static/               # Static assets
├── convert_blogs.py      # Content processing script
└── public/               # Generated site (ignored)
```

## 🚧 Development

### Prerequisites

- [Zola](https://www.getzola.org/documentation/getting-started/installation/) installed
- Python 3.7+ (for content processing)

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/tech-blog.git
cd tech-blog

# Serve locally with hot reload
zola serve

# Build for production
zola build

# Clean build (removes public directory)
rm -rf public && zola build
```

### Content Management

```bash
# Convert raw blog posts to Zola format
python3 convert_blogs.py

# Add new post
# 1. Create markdown file in content/
# 2. Add front matter with title, date, tags
# 3. Build and test locally
```

## 🌐 Deployment Infrastructure

This project showcases a complex, production-ready deployment pipeline:

### Network Architecture

```
Internet → OpenBSD VPS → WireGuard Tunnel → FreeBSD Box → nginx Jail
```

### Components

- **OpenBSD VPS**: Public-facing server with relayd load balancer
- **WireGuard VPN**: Secure tunnel between VPS and home lab
- **FreeBSD Host**: Home lab server with jail-based services
- **nginx Jail**: Containerized web server for security isolation
- **IPv6 Ready**: Full dual-stack IPv4/IPv6 support

### Deployment Process

1. **Local Build**: `zola build` generates static site
2. **File Transfer**: `scp` to FreeBSD staging area
3. **Jail Deployment**: Copy files to nginx jail with proper permissions
4. **Service Management**: Restart nginx within jail
5. **Load Balancer**: OpenBSD relayd with health checks
6. **DNS**: AAAA records for IPv6 connectivity

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
- **Jail-based Deployment**: Containerized web server
- **Firewall Configuration**: Proper network security
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
