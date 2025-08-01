# Favicon & Profile Photo Workflow

## 🎯 **Project Overview**

Create consistent branding across all sites with professional profile photo and favicon design representing dual expertise (engineering + medical).

## 🎨 **Brand Identity Foundation**

### **Font Hierarchy (Use Across All Sites)**

- **Primary**: Inter (clean, professional, highly readable)
- **Code/Mono**: JetBrains Mono (perfect for technical content)
- **Hierarchy**:
  - H1: Inter Bold 700
  - H2: Inter SemiBold 600
  - Body: Inter Regular 400
  - Code: JetBrains Mono 400

### **Unified Icon Language**

- **Style**: Outline vs filled, rounded vs sharp corners
- **Weight**: Consistent line thickness
- **Color**: Same palette across platforms
- **Examples**:
  - GitHub: Same icon style in READMEs
  - Blog: Same icons in navigation
  - Social posts: Consistent icon treatment

## 📱 **Favicon Requirements**

**Multiple sizes needed:**

```
favicon.ico (32x32) - Browser tabs
apple-touch-icon.png (180x180) - iOS
android-chrome-192x192.png - Android
favicon-16x16.png - Small displays
favicon-32x32.png - Standard displays
```

## 🏥 **Profile Photo Strategy**

### **Concept: Caliper + Stethoscope**

**Brilliant representation of dual expertise**

### **Professional Recommendations**

**Clothing:**

- ✅ Navy jacket + pinstripe shirt = Perfect professional look
- ✅ Colors: Navy, white, subtle pinstripes work well
- ✅ Avoid: Bright colors that compete with your tools

**Glasses Decision:**

- ✅ **ON** - Professional, distinctive, fits engineer persona
- ✅ Thin rims are current and professional
- ✅ Ensure good lighting to avoid glare

**Pose & Expression:**

- **Expression**: Neutral to slight smile (approachable but professional)
- **Gaze**: Direct eye contact (confident, trustworthy)
- **Angle**: Slight 3/4 turn (more dynamic than straight-on)

**Background:**

- **Clean, neutral**: Light gray, white, or subtle gradient
- **Avoid**: Busy backgrounds, bright colors
- **Consider**: Soft bokeh effect for depth

### **Anonymity Decision**

**Skip the anonymity approach**

- ✅ Professional credibility > anonymity
- ✅ Trust factor: People trust faces they can see
- ✅ Industry standard: Most tech professionals show their face
- ❌ Gimmicky: Eye-covering idea might seem unprofessional

## 🔧 **Favicon Design Options**

### **Option 1: Crossed (X-formation)**

```
   /stethoscope\
  /            \
 /              \
|                |
 \              /
  \            /
   \caliper  /
```

**Pros**: Dynamic, shows interaction
**Cons**: Might be too busy at 16x16px

### **Option 2: Parallel (Side-by-side)**

```
[stethoscope] [caliper]
```

**Pros**: Clean, readable at small sizes
**Cons**: Less dynamic

### **Option 3: Interacting**

```
stethoscope bell touching caliper jaws
```

**Pros**: Shows connection between disciplines
**Cons**: Might be too complex

## 🎨 **Color Strategy**

### **Python Color Picker Workflow:**

```python
from PIL import Image
import numpy as np

# Load your photo
img = Image.open('suit_photo.jpg')
# Convert to array
pixels = np.array(img)
# Sample colors from jacket/shirt areas
# Extract dominant colors
```

### **Color Palette from Your Suit:**

- **Primary**: Navy from jacket
- **Secondary**: White/light from shirt
- **Accent**: Subtle pinstripe color
- **Background**: Light neutral

### **Implementation:**

1. **Extract colors** from your photo
2. **Apply to favicon** (navy + white/light)
3. **Use in blog** CSS variables
4. **Consistent across** all platforms

## 📋 **Workflow Priority**

### **Phase 1: Core Identity (This Week)**

1. **Design favicon** (caliper + stethoscope graphic)
2. **Take profile photo** (professional setup)
3. **Create basic social templates**

### **Phase 2: Implementation (Next Week)**

1. **Add favicon to blog**
2. **Update social profiles**
3. **Create thumbnail templates**

### **Phase 3: Optimization (Following Week)**

1. **A/B test different profile photos**
2. **Refine brand guidelines**
3. **Create content templates**

## 🎯 **My Recommendations**

### **Favicon Design:**

- **Style**: Parallel, simple
- **Colors**: Navy + white from your suit
- **Size**: Optimized for 16x16px readability

### **Profile Photo:**

- **Glasses**: ON
- **Pose**: 3/4 turn, direct gaze, slight smile
- **Tools**: Caliper in one hand, stethoscope in other
- **Background**: Clean, neutral

### **Color Workflow:**

1. **Take photo** of your suit
2. **Extract colors** with Python
3. **Create favicon** with those colors
4. **Update blog** CSS with color palette
5. **Apply consistently** across all sites

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

## 🎨 **Current Brand Analysis**

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

---

_Last updated: 2025-01-19_
_Status: Planning phase - ready for implementation_
