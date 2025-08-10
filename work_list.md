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
- [x] **Implement collapsible sidebar** - Added organized sidebar with Infrastructure, Development, and Home & Lab groups _(2025-08-02)_
- [x] **Add AI transparency disclaimer** - Implemented honest disclaimer about AI assistance on all pages _(2025-08-02)_
- [x] **Create dynamic color palette system** - Built 3 professional palettes (Industrial Blue-Gray, Technical Dark, Engineering Green) with real-time switching _(2025-08-02)_
- [x] **Fix text contrast issues** - Resolved readability problems across all palettes _(2025-08-02)_
- [x] **Implement night mode with blueprint transformation** - Added dark mode toggle with CSS filters for blueprint effect on technical drawings _(2025-01-19)_
- [x] **Remove palette toggles, keep night mode** - Simplified to single P7 palette with night mode functionality _(2025-01-19)_
- [x] **Add light color fills to post cards** - Applied secondary color backgrounds to post cards, category cards, and tag cards _(2025-01-19)_
- [x] **Fix night mode sidebar text contrast** - Maintained dark text in sidebar for proper contrast in both day and night modes _(2025-01-19)_
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
- [x] **Add Electronics section** - Created new section for Arduino, ESP32, and hardware projects _(2025-08-02)_
- [ ] Add a C++ section
- [ ] add an arduino section
- [ ] add an ESP32 section
- [ ] add a rust section
- [ ] add a hardware and hard disks section

### Phase 3: Advanced Features (Next 1-2 months)

- [x] **Implement comment system** - Giscus integration ready, requires GitHub repo setup _(2025-08-02)_
- [x] **Convert contact to form** - Formspree integration with email delivery _(2025-08-02)_
- [x] **Add tags page** - Manual tags page implemented with popular tags and section links _(2025-08-02)_
- [x] **Implement night mode system** - Complete dark mode with blueprint transformation and localStorage persistence _(2025-01-19)_
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
- [x] **Implement dark mode** - User preference for dark/light themes with blueprint transformation _(2025-01-19)_
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

_Last updated: 2025-01-19_
_Status: Night mode system complete with blueprint transformation. P7 palette selected as winner. All templates updated with night mode toggle. Ready for backdrop image integration and content images._

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

## 🎨 **Brand Identity Foundation**

### **1. Visual Brand Elements**

- **Logo**: Simple, scalable design that works at small sizes
- **Color Palette**: 3-4 primary colors (your current blue is good)
- **Typography**: Consistent font hierarchy (Inter + JetBrains Mono works well)
- **Icon Style**: Unified icon language across all platforms

### **2. Favicon Strategy**

```
<code_block_to_apply_changes_from>
```

### **3. Social Media Assets**

- **Profile Pictures**: 400x400px (works for most platforms)
- **Cover Images**: Platform-specific dimensions
- **Post Templates**: Consistent layouts for different content types
- **Story/Reel Templates**: Vertical formats (9:16 ratio)

## 🛠 **Technical Implementation**

### **For Your Blog (Zola)**

```html
<!-- Add to your templates -->
<link rel="icon" type="image/x-icon" href="/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<meta property="og:image" content="https://blog.clexp.net/og-image.jpg" />
<meta property="og:title" content="{{ page.title }}" />
<meta property="og:description" content="{{ page.description }}" />
```

### **Social Media Meta Tags**

```html
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@yourhandle" />

<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:url" content="{{ page.permalink }}" />
```

## 📱 **Platform-Specific Requirements**

### **LinkedIn**

- Profile: 400x400px
- Cover: 1584x396px
- Post images: 1200x627px

### **Twitter/X**

- Profile: 400x400px
- Header: 1500x500px
- Post images: 1200x675px

### **GitHub**

- Profile: 400x400px
- Repository social preview: 1280x640px

### **YouTube**

- Channel icon: 800x800px
- Thumbnails: 1280x720px
- Channel banner: 2560x1440px

## 📝 **Content Strategy**

### **Thumbnail Templates**

- **Technical Tutorials**: Code + visual elements
- **Architecture Posts**: Network diagrams + icons
- **Troubleshooting**: Before/after states
- **Tools/Reviews**: Product screenshots

### **Consistent Elements**

- Your logo/name in corner
- Consistent color scheme
- Readable fonts at small sizes
- Clear value proposition

## 🚀 **Implementation Priority**

### **Phase 1: Core Assets**

1. **Favicon set** (all sizes)
2. **Profile pictures** (400x400px)
3. **Basic cover images** for main platforms

### **Phase 2: Content Templates**

1. **Blog post thumbnails** template
2. **Social media post** templates
3. **Video thumbnail** templates

### **Phase 3: Advanced**

1. **Animated logos** for video intros
2. **Interactive elements** for web
3. **Brand guidelines** document

## 💡 **Tools & Resources**

### **Design Tools**

- **Figma** (free tier) - Template creation
- **Canva** - Quick social media graphics
- **GIMP/Photoshop** - Advanced editing

### **Favicon Generators**

- **Favicon.io** - Generate all sizes
- **RealFaviconGenerator.net** - Comprehensive favicon sets

### **Social Media Tools**

- **Buffer/Hootsuite** - Consistent posting
- **Later** - Visual planning
- **Canva** - Template library

## 🎨 **Your Current Brand Analysis**

### **Strengths**

- ✅ Clean, professional design
- ✅ Technical expertise focus
- ✅ Consistent color scheme (blue theme)
- ✅ Good typography choices

### **Opportunities**

- 🔄 Create unified logo/icon
- 🔄 Standardize thumbnail style
- 🔄 Develop content templates
- 🔄 Optimize for each platform

Would you like me to help you implement any of these elements for your blog first? We could start with favicons and social media meta tags, then move to creating thumbnail templates for your technical content.

## 🎯 **Summary: Zola Color Palette Best Practices**

### **What Zola Expects (Standard Web Development):**

1. **SASS Variables** - For static colors and SASS functions
2. **CSS Variables** - For dynamic switching (JavaScript)
3. **Hex Colors** - Standard web color format
4. **No Special Requirements** - Just good web development practice

### **The Correct Approach:**

```scss
<code_block_to_apply_changes_from>
```

### **Why This Works:**

- **SASS Variables**: Work with SASS functions like `darken()`, `lighten()`, `mix()`
- **CSS Variables**: Enable real-time switching via JavaScript
- **Hex Colors**: Standard web format, universally supported
- **No Zola Magic**: Just standard web development practices

The palette switcher should now work perfectly! The key was separating SASS variables (for build-time processing) from CSS variables (for runtime switching).
