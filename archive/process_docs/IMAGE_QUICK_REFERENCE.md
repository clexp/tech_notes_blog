# Image System Quick Reference

## 📏 Image Specifications

| Type               | Dimensions       | File Size | Format    | Purpose              |
| ------------------ | ---------------- | --------- | --------- | -------------------- |
| **Thumbnails**     | 400×300px (4:3)  | 15-30KB   | WebP/JPEG | Post cards, listings |
| **Hero Images**    | 1200×600px (2:1) | 50-100KB  | WebP/JPEG | Post headers         |
| **Content Images** | 800×600px (4:3)  | 30-80KB   | WebP/PNG  | Inline content       |
| **Page Headers**   | 1200×400px (3:1) | 40-70KB   | WebP/JPEG | Page banners         |

## 🗂 Directory Structure

```
static/images/
├── defaults/           # Default fallback images
├── pages/             # Page header images
├── networking/        # Networking section images
├── system-admin/      # System admin section images
├── security/          # Security section images
└── home-lab/          # Home lab section images
```

## 🎨 Shortcode Usage

### Basic Image Processing

```markdown
{{/* image(path="images/example.jpg", alt="Description", caption="Caption") */}}
```

### Post-Specific Images

```markdown
{{/* post_image(path="images/networking/hero.jpg", type="hero", alt="Network diagram") */}}
{{/* post_image(path="images/networking/thumb.jpg", type="thumbnail", alt="Preview") */}}
{{/* post_image(path="images/networking/content.png", type="content", alt="Screenshot") */}}
```

### Responsive Images

```markdown
{{/* responsive_image(path="images/example.jpg", alt="Description") */}}
```

### Galleries

```markdown
{{/* gallery(path="screenshots", columns=3, thumb_width=300) */}}
```

## 🎯 Image Sources

- **Unsplash**: https://unsplash.com/ (free, high-quality)
- **Pexels**: https://www.pexels.com/ (free stock photos)
- **Pixabay**: https://pixabay.com/ (free images/vectors)

## 🚀 Getting Started

1. **Create default images** (8 total: 4 sections × 2 types)
2. **Add page headers** (about, contact, main)
3. **Start with top posts** (add hero + thumbnail)
4. **Bulk add content images** to technical posts

## 💡 Pro Tips

- Keep images under 100KB
- Use WebP for better compression
- Always include alt text
- Use consistent styling across sections
- Optimize before uploading

---

_All shortcodes include automatic WebP conversion, lazy loading, and responsive sizing._
