# Image Processing Quick Reference

## Setup Complete! 🎉

Your blog now has professional image processing capabilities with three custom shortcodes:

### 1. Basic Image (`image`)

```markdown
{{/* image(path="images/example.jpg", alt="Description", caption="Optional caption") */}}
```

### 2. Responsive Image (`responsive_image`)

```markdown
{{/* responsive_image(path="images/example.jpg", alt="Description") */}}
```

### 3. Gallery (`gallery`)

```markdown
{{/* gallery(path="folder-name", columns=3) */}}
```

## Where to Put Images

### Global Images

```
static/images/
├── common/
├── networking/
└── system-admin/
```

### Post-Specific Images

```
content/section/
├── my-post.md
└── my-post/
    ├── image1.jpg
    └── image2.png
```

## Quick Examples

### Single Image

```markdown
{{/* image(path="images/server-diagram.png", alt="Network topology", caption="Home lab setup") */}}
```

### Responsive Image

```markdown
{{/* responsive_image(path="images/screenshot.jpg", alt="Terminal output") */}}
```

### Custom Sizing

```markdown
{{/* image(path="images/wide-diagram.png", width=1200, op="fit_width", format="webp") */}}
```

### Gallery

```markdown
{{/* gallery(path="screenshots", columns=4, thumb_width=250) */}}
```

## Image Operations

- `fit_width`: Resize to width, keep aspect ratio (default)
- `fit_height`: Resize to height, keep aspect ratio
- `fit`: Resize to fit within dimensions
- `fill`: Crop to exact dimensions
- `scale`: Scale without maintaining aspect ratio

## Formats

- `webp`: Best compression, modern browsers (default)
- `jpeg`: Good compression, universal support
- `png`: Lossless, good for diagrams/screenshots

## WebP Format Benefits

WebP provides **25-50% smaller file sizes** than JPEG with similar quality:

- **Perfect for technical photos**: Network cables, mainboards, server equipment
- **Excellent for diagrams**: Clean lines compress very well
- **Supports transparency**: Like PNG but much smaller
- **Fast loading**: Critical for professional presentation
- **Universal browser support**: 95%+ modern browsers

## Color Consistency & Site Theming

### Maintaining Visual Cohesion

For professional presentation, maintain consistent color tone across all images:

#### 1. Color Temperature

- **Warm tone (3000K-4000K)**: Cozy, approachable feel
- **Cool tone (5000K-6500K)**: Technical, professional feel
- **Neutral tone (4000K-5000K)**: Balanced, versatile

#### 2. Hue Adjustment Tools

- **Photoshop**: Image > Adjustments > Hue/Saturation
- **GIMP**: Colors > Hue-Saturation
- **Lightroom**: HSL panel for precise color control
- **Command line**: `ffmpeg -i input.jpg -vf hue=h=10:s=0.8 output.jpg`

#### 3. Batch Processing for Consistency

```bash
# ImageMagick batch hue adjustment
for img in *.jpg; do
    convert "$img" -modulate 100,120,100 -colorspace sRGB "processed_$img"
done
```

#### 4. Site Color Scheme Integration

- **Primary colors**: Match your SASS variables
- **Accent colors**: Complement your theme
- **Neutral tones**: Maintain readability

#### 5. Technical Photo Guidelines

- **Consistent lighting**: Same color temperature across shots
- **Background uniformity**: Neutral backgrounds for equipment photos
- **Post-processing**: Apply same color grading to all images
- **Depth of field**: Consistent focus style (shallow DOF for detail shots)

### Recommended Workflow

1. **Capture**: Use consistent lighting setup
2. **Grade**: Apply same color correction to all images
3. **Optimize**: Convert to WebP with appropriate quality
4. **Integrate**: Use shortcodes for consistent sizing

## Testing

1. Add some images to `static/images/`
2. Use the shortcodes in your blog posts
3. Run: `zola serve --base-url http://127.0.0.1:1111 --port 1111`
4. Check the processed images in `static/processed_images/`

## Features

✅ Automatic WebP conversion
✅ Responsive image generation
✅ Lazy loading
✅ Professional styling with hover effects
✅ Gallery grid layouts
✅ Image caching and optimization
✅ Proper alt text and captions

Ready to enhance your blog with professional image processing!
