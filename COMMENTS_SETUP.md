# Comments System Setup Guide

## Overview

This blog uses **Giscus** for comments, which integrates GitHub Discussions into your blog posts. This provides a modern, privacy-friendly commenting system that doesn't require user registration.

## Setup Steps

### 1. Create GitHub Repository for Comments

1. Create a new public repository on GitHub (e.g., `blog-comments`)
2. Enable GitHub Discussions in the repository settings
3. Create a discussion category (e.g., "Announcements")

### 2. Install Giscus App

1. Go to [giscus.app](https://giscus.app)
2. Select your repository
3. Choose the discussion category
4. Copy the generated script

### 3. Update Template Configuration

In `templates/page.html`, update the Giscus configuration:

```html
<script
  src="https://giscus.app/client.js"
  data-repo="YOUR_USERNAME/YOUR_REPO_NAME"
  data-repo-id="YOUR_REPO_ID"
  data-category="YOUR_CATEGORY_NAME"
  data-category-id="YOUR_CATEGORY_ID"
  data-mapping="pathname"
  data-strict="0"
  data-reactions-enabled="1"
  data-emit-metadata="0"
  data-input-position="bottom"
  data-theme="preferred_color_scheme"
  data-lang="en"
  crossorigin="anonymous"
  async
></script>
```

### 4. Contact Form Setup (Optional)

For the contact form, you can use:

- **Formspree**: Free tier available, easy setup
- **Netlify Forms**: If hosting on Netlify
- **Custom backend**: For more control

Update the form action in `templates/shortcodes/contact_form.html`:

```html
<form
  class="contact-form"
  action="https://formspree.io/f/YOUR_FORM_ID"
  method="POST"
></form>
```

## Features

### Comments System

- ✅ Privacy-friendly (no user tracking)
- ✅ GitHub integration
- ✅ Dark/light mode support
- ✅ Markdown support
- ✅ Reactions and replies
- ✅ Spam protection

### Contact Form

- ✅ Professional styling
- ✅ Form validation
- ✅ Topic categorization
- ✅ Responsive design
- ✅ Dark mode support

## Customization

### Disable Comments on Specific Pages

Add to the page front matter:

```yaml
[extra]
show_comments = false
```

### Customize Contact Form

Edit `templates/shortcodes/contact_form.html` to:

- Add/remove form fields
- Change styling
- Integrate with different services

## Security Considerations

1. **Giscus**: Uses GitHub's authentication, very secure
2. **Contact Form**: Consider rate limiting and spam protection
3. **Privacy**: No user tracking or cookies required

## Troubleshooting

### Comments Not Loading

- Check repository permissions
- Verify Giscus app installation
- Check browser console for errors

### Contact Form Issues

- Verify form service configuration
- Check form action URL
- Test form submission

## Alternative Comment Systems

If you prefer different options:

1. **Disqus**: Traditional but requires registration
2. **Utterances**: GitHub issues-based (similar to Giscus)
3. **Custom**: Build your own with a backend

## Maintenance

- Monitor GitHub Discussions for spam
- Review contact form submissions regularly
- Update Giscus configuration as needed
- Backup discussion data periodically
