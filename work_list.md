# Work List

## Completed ✅

### Blog Infrastructure (2024-12-19)

- [x] **Add a search bar** - Implemented dropdown search with Elasticlunr.js
- [x] **Add an about page** - Created professional about page with technical background
- [x] **Make this a git repo** - Initialized Git repository with proper .gitignore
- [x] **Push to production** - Deployed to blog.clexp.net via FreeBSD/OpenBSD infrastructure
- [x] **Push to GitHub** - Repository hosted on GitHub for version control
- [x] **Update production server** - Configured nginx, WireGuard tunnel, and relayd
- [x] **Add a contact page** - Created contact page with professional layout
- [x] **Add a categories/sections page** - Implemented section-based navigation

### Content Organization (2024-12-19)

- [x] **Implement Zola sections** - Created 5 organized sections (Networking, System Admin, Security, Home Lab, Web Dev)
- [x] **Move all content to sections** - Reorganized 25+ posts into appropriate sections
- [x] **Create section navigation** - Added sidebar navigation with icons and active states
- [x] **Fix section pagination** - Resolved issues with posts not showing in sections
- [x] **Create Web Dev section** - Added dedicated section for web development content

### Image Processing System (2024-12-19)

- [x] **Design image specifications** - Created comprehensive image size and format guidelines
- [x] **Build image processing shortcodes** - Developed 4 specialized shortcodes (image, post_image, responsive_image, gallery)
- [x] **Implement professional styling** - Added SASS styling with hover effects and responsive layouts
- [x] **Create image directory structure** - Organized static/images/ with section-specific folders
- [x] **Document image strategy** - Created detailed documentation and quick reference guides

### Performance & Features (2024-12-19)

- [x] **Fix local development** - Corrected zola serve command with proper base URL
- [x] **Implement SASS architecture** - Professional CSS with variables, mixins, and responsive design
- [x] **Add responsive design** - Mobile-first approach with proper breakpoints
- [x] **Optimize search functionality** - Fixed search to work with local development

## Current Priorities 🎯

### Phase 1: Visual Enhancement (Next 1-2 weeks)

- [x] **site is live, edit to minimize security risks** - Enhanced 4 high-impact posts with professional polish, consistent sanitization, and authentic learning reflections while maintaining technical depth. Added RFC references, security considerations, and honest "What I Learned" sections. _(2025-07-16)_
- [x] Fix left sidebar navigation to appear on all pages
- [ ] **Create default section images** - Design 10 default images (5 heroes + 5 thumbnails)
- [ ] **Add page header images** - Create banners for About, Contact, and main pages
- [ ] **Design site logo and favicon** - Professional branding elements
- [ ] **Replace emoji icons with professional icons** - Create 5 section icons (SVG preferred)
- [x] **Fix search URL issue** - Fixed both dropdown and Enter key navigation to use relative URLs for local development _(2024-12-19)_
- [ ] **Add hero/thumbnail to top 5 posts** - Start with most important content

### Phase 2: Content Enhancement (Next 2-4 weeks)

- [ ] **Add images to all posts** - Hero + thumbnail for remaining 20+ posts
- [ ] **Create content images** - 2-3 inline images per post (diagrams, screenshots)
- [ ] **Optimize existing content** - Update post descriptions and formatting
- [ ] **Add more Web Dev content** - Document more site-building processes

### Phase 3: Advanced Features (Next 1-2 months)

- [ ] **Implement comment system** - Add Giscus or similar for engagement
- [ ] **Convert contact to form** - Functional contact form with validation
- [ ] **Add tags page** - Organize content by tags in addition to sections
- [ ] **Create post series** - Link related posts together
- [ ] **Add reading time estimates** - Improve user experience

## Under Consideration 🤔

### Social & Community

- [ ] **Add social media integration** - GitHub, LinkedIn, Twitter links
- [ ] **Create blogroll** - List of other technical blogs and resources
- [ ] **Add RSS feeds** - Section-specific and global feeds
- [ ] **Implement newsletter signup** - Email list for updates

### Technical Enhancements

- [ ] **Add syntax highlighting themes** - Dark/light mode code blocks
- [ ] **Implement dark mode** - User preference for dark/light themes
- [ ] **Add table of contents** - Auto-generated TOC for long posts
- [ ] **Create related posts** - Suggest similar content
- [ ] **Add print stylesheets** - Professional printing layout

### Content Features

- [ ] **Add post templates** - Standardized formats for different post types
- [ ] **Create content calendar** - Plan future posts and topics
- [ ] **Add post analytics** - Track popular content and engagement
- [ ] **Implement content series** - Multi-part tutorials and guides

### Infrastructure

- [ ] **Add CDN integration** - Faster global content delivery
- [ ] **Implement caching strategy** - Edge caching for better performance
- [ ] **Add monitoring** - Uptime and performance monitoring
- [ ] **Create staging environment** - Safe testing before production

## Recently Moved Content 📁

### Web Dev Section (2024-12-19)

- **Building and Deploying a Zola Site** - Moved from system-admin to web-dev
- **Image Processing with Zola: A Complete Guide** - Moved from system-admin to web-dev
- **Professional Image Processing for Web Development** - New comprehensive article

## Next Steps 🚀

1. **Start with images** - Create the 10 default section images to improve visual appeal
2. **Polish top content** - Add hero images to the 5 most important posts
3. **Document the journey** - Continue adding Web Dev posts about building this site
4. **Gather feedback** - Share with colleagues for input on priorities
5. **Plan content calendar** - Decide on future topics and posting schedule

---

_Last updated: 2024-12-19_
_Status: Active development - Blog foundation complete, focusing on visual enhancement_

## 🔍 **Comment System Options for Static Sites**

### 1. **Staticman** - The Static-First Approach

[Staticman](https://staticman.net/) is specifically designed for static sites and has some unique advantages:

**Pros:**

- ✅ **Keeps content in your repo** - Comments become data files in your GitHub repository
- ✅ **No external dependencies** - Your site remains truly static
- ✅ **Full ownership** - You own all the data
- ✅ **GitHub Pages friendly** - Works perfectly with your current setup
- ✅ **Moderation options** - Can create pull requests for approval before publishing

**Cons:**

- ❌ **Requires server setup** - Needs a Staticman instance (Heroku, Vercel, etc.)
- ❌ **No real-time updates** - Comments only appear after site rebuild
- ❌ **Limited features** - No threading, reactions, or advanced features

### 2. **Disqus** - The Traditional Approach

The most widely-used commenting system for static sites:

**Pros:**

- ✅ **Zero setup** - Just add a JavaScript snippet
- ✅ **Rich features** - Threading, moderation, spam protection
- ✅ **Real-time** - Comments appear immediately
- ✅ **Mobile apps** - Full ecosystem

**Cons:**

- ❌ **External dependency** - Your content depends on Disqus
- ❌ **Privacy concerns** - Tracks users across sites
- ❌ **Performance impact** - Adds JavaScript bloat
- ❌ **Data ownership** - You don't own the comment data

### 3. **Talkyard** - The Modern Alternative

[Talkyard](https://github.com/debiki/talkyard) is an interesting open-source option:

**Pros:**

- ✅ **Self-hosted** - Full control over your data
- ✅ **Rich features** - Comments, forum, chat, Q&A
- ✅ **Open source** - No vendor lock-in
- ✅ **Modern UI** - Clean, responsive design

**Cons:**

- ❌ **Complex setup** - Requires Docker and server management
- ❌ **Resource intensive** - Needs a proper server
- ❌ **Overkill** - Might be too much for simple blog comments

## 🎯 **Recommendation for Your Blog**

Given your technical background and the fact that you're already using GitHub Pages, I'd recommend **Staticman** for these reasons:

### **Why Staticman Fits Your Blog:**

1. **Philosophical alignment** - Keeps everything in your Git repo
2. **Technical fit** - Works perfectly with your Zola + GitHub Pages setup
3. **Learning opportunity** - Demonstrates advanced static site techniques
4. **Portfolio value** - Shows you can solve complex problems elegantly

### **Implementation Strategy:**

```yaml
<code_block_to_apply_changes_from>
```

## 🚀 **Next Steps**

Would you like me to:

1. **Implement Staticman** - Set up the full commenting system with moderation
2. **Create a hybrid approach** - Start with Disqus for immediate results, plan migration to Staticman
3. **Explore Talkyard** - Set up a self-hosted solution if you want more features
4. **Research alternatives** - Look at other options like Giscus (GitHub Discussions)

The choice depends on your priorities:

- **Quick setup**: Disqus
- **Full control**: Staticman
- **Rich features**: Talkyard
- **GitHub integration**: Giscus

What's your preference? I can help implement whichever approach you choose!

## 🚀 **Production Deployment & Marketing**

### Phase 1: Production Deployment (Immediate)

- [ ] **Deploy to production server** - Push current site to blog.clexp.net
- [ ] **Test all functionality** - Search, navigation, responsive design
- [ ] **Verify SSL certificates** - Ensure HTTPS is working properly
- [ ] **Check performance** - Run Lighthouse tests, optimize if needed
- [ ] **Update DNS if needed** - Ensure domain points to correct server

### Phase 2: LinkedIn Profile Integration (Next 1-2 weeks)

- [ ] **Create LinkedIn profile section** - Add blog to professional profile
- [ ] **Write professional summary** - Include link to blog and technical focus
- [ ] **Add featured posts** - Link to 3-5 best technical posts
- [ ] **Update experience section** - Mention blog as ongoing technical project
- [ ] **Network with tech community** - Connect with other sysadmins, network engineers
- [ ] **Share blog posts** - Post updates about new content on LinkedIn

### Phase 3: Content Marketing Strategy (Next 2-4 weeks)

- [ ] **Create content calendar** - Plan future posts and topics
- [ ] **Cross-post to other platforms** - Reddit (r/sysadmin, r/networking), Hacker News
- [ ] **Engage with community** - Comment on other blogs, participate in discussions
- [ ] **Track analytics** - Monitor traffic, engagement, popular posts
- [ ] **Optimize based on data** - Focus on content that performs well

### Phase 4: Advanced Features (Future)

- [ ] **Implement comments system** - Choose between Staticman, Disqus, or Giscus
- [ ] **Add newsletter signup** - Email list for updates
- [ ] **Create post series** - Multi-part tutorials and guides
- [ ] **Add related posts** - Suggest similar content
- [ ] **Implement dark mode** - User preference for dark/light themes

## 🎯 **Success Metrics**

- **Traffic**: 100+ monthly visitors within 3 months
- **Engagement**: Comments and social shares on posts
- **Professional opportunities**: Job inquiries, collaboration requests
- **Community building**: Regular readers and repeat visitors
- **Portfolio value**: Demonstrates technical writing and web development skills

---

_Last updated: 2025-01-19_
_Status: Ready for production deployment and LinkedIn integration_
