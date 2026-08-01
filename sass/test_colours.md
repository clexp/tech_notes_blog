# Colour Palette

## palette 1

#D6C3C9 thistle (light pink - needs dark font)
#B49082 Beaver (medium pink / causasin skin - dark font)
#98473E Chestnut (dark brown - light font)
#A37C40 Copper (dark yellow - light font)
#07090F Rich Black (dark black - light font)

## palette 2

#82D4BB Tiffany Blue (light blue - dark font)
#82C09A Cambridge Blue (medium blue - dark font)
#82AC9F cambridge blue (dark blue - dark font)
#829298 cadet grey (dark grey - dark font)
#94778B mount batten (dark purple - dark font)

## palette 3

#D0FEF5 Mint green (light blue - dark font)
#FAB2EA Lavender pink (medium blue - dark font)
#4A051C Chocolate cosmos (dark blue - whit font)
#52FFB8 Aquamarine (dark grey - dark font)
#830A48 Marray (dark brown - whit font)

## palette 4

#B8C480 Olivene (Light green - Dark font)
#D4E79E mindaro (Light green - Dark font)
#922D50 majenta (dark brown - white font)
#501537 tyrian purple (dark black - white font)
#3C1B43 Aquamarine (light blue - dark font)

## palette 5

#FFB8D1 Lavender pink (light - dark font)
#E4B4C2 Orchid pink (light - dark font)
#E7CEE3 Cecil (light - dark font)
#E0E1E9 Ghost white (light - dark font)
#DDFDFE Light cyan (light - dark font)

## palette 6

### Review one

#606c38 dark moss green (mid green)
can pair with: #FEFAE0

#283618 pakistan green (dark green)
can pair with: #FEFAE0 and #DDA15E

#FEFAE0 cornsilk (Cream)
can pair with: #606c38 and #283618

#DDA15E earth yellow (mid/light orange)
can pair with: #283618

#BC6C25 tiger's eye (dark orange)
cannot pair. Bad choice

### Review two

Try this instead:

#ffbc42 yellow
can pair with: #8f2c55, #005b59

#ffafbd pink
can pair with: #8f2c55, #005b59

#8f2c55 magenta
can pair with: #ffafbd, #ffbc42, #73d2de

#005b59 green
can pair with: #ffafbd, #ffbc42, #73d2de

#73d2de cyan
can pair with: #8f2c55, #005b59

#

## palette 7

#32658a dark blue
can pair with: #ffafbd, #ffbc42, #73d2de

#bbe1f8 light blue
can pair with: #32658a, #a73f00

#d3e0c4 light green
can pair with: #32658a, #a73f00

#ffd4a7 light orange
can pair with: #32658a, #a73f00

#a73f00 dark orange
can pair with: #bbe1f8, #d3e0c4, #ffd4a7

## palette 8

#1c110a licorice
can pair with: #e4d6a7, #e9b44c, #91c6ca

#e4d6a7 cream
can pair with: #1c110a, #941f00

#e9b44c orange
can pair with: #1c110a, #a73f00

#941f00 maroon
can pair with: #91c6ca, #e4d6a7, #e9b44c

#91c6ca light blue
can pair with: #1c110a, #941f00

## TESTING NOTES

### ISSUES FOUND:

- **Sidebar subcategory text**: Too light, hard to read in some palettes
- **Font contrast**: Some palettes have too light fonts in certain areas
- **Palette 5**: Too pink overall
- **Emotional palettes**: Marketing-focused colors inappropriate for technical blog

### WINNING PALETTE:

- **Classic Skunk Works**: Emotionally neutral, information-focused, technically precise

### BACKGROUND STRATEGY:

- **Overall backdrop**: Manufacturing drawings/photo scans (white base) - functional 6th color
- **UI Elements**: Light colors with partial transparency to show underlying images
- **Affected areas**: Left sidebar, title, navbar, footer, post cards

### CLASSIC SKUNK WORKS ANALYSIS:

- **Philosophy**: Emotionally neutral, selectively informational, intelligent decision palette
- **Not corporate**: Avoids IBM blue and other corporate associations
- **Technical focus**: High contrast, readability, precision over decoration
- **Skunk works aesthetic**: Professional but not stuffy, serious but not corporate

### COLOR ROLES:

- **Primary (#2c3e50)**: Dark slate - headers, navigation (authoritative)
- **Secondary (#e8edf2)**: Medium gray - card backgrounds (darker than before for contrast)
- **Accent (#3498db)**: Technical blue - links, highlights (not corporate blue)
- **Background (#ffffff)**: Pure white - main background (manufacturing drawing backdrop)
- **Text (#2c3e50)**: Dark slate - main text (high contrast)
- **Text-muted (#7f8c8d)**: Medium gray - secondary text
- **Border (#bdc3c7)**: Light gray - borders

### NIGHT MODE STRATEGY:

- **Blueprint transformation**: White backdrop becomes midnight blue (#1e3a8a)
- **Avoid blue overload**: Use slate grays for UI elements instead of more blue
- **High contrast**: White text on dark backgrounds
- **Consistent hierarchy**: Same information structure, different color values

### NEXT STEPS:

1. ✅ Implement Classic Skunk Works palette
2. ✅ Create blueprint night mode
3. ✅ Ensure proper contrast ratios
4. Ready for backdrop image integration

---

## COMPREHENSIVE COLOR AUDIT 🎨

### CSS Variable System (Primary Color Management)

**Core Variables (defined in main.scss):**

```scss
:root {
  --primary-color: #2c3e50; // Headers, navigation, buttons
  --secondary-color: #e8edf2; // Card backgrounds, sidebar
  --accent-color: #3498db; // Links, highlights, tags
  --background-color: #ffffff; // Main background
  --text-color: #2c3e50; // Primary text
  --text-muted: #7f8c8d; // Secondary text
  --border-color: #bdc3c7; // Borders, dividers
}
```

**Dark Mode Overrides:**

```scss
[data-theme="dark"] {
  --background-color: #1e3a8a; // Blueprint blue background
  --text-color: #ffffff; // White text for contrast
  --text-muted: #cbd5e1; // Light gray muted text
  --border-color: #475569; // Slate gray borders
}
```

### SASS Variables (Legacy/Fallback System)

**In \_variables.scss:**

```scss
$primary-color: #98473e; // Chestnut (old palette)
$secondary-color: #b49082; // Beaver (old palette)
$accent-color: #a37c40; // Copper (old palette)
$background-color: #ffffff; // White
$text-color: #07090f; // Rich Black
$border-color: #d6c3c9; // Thistle
```

**⚠️ CONFLICT ISSUE**: SASS variables are overridden by CSS variables but still used in some calculations.

### All Color Usage Locations

#### Headers & Navigation

- `.site-header`: `var(--primary-color)` background, white text
- `.nav-brand`: `$text-color` → `var(--text-color)` on hover
- `.nav-link`: `$secondary-color` → `var(--primary-color)` on hover
- **Dark mode**: `rgba(44, 62, 80, 0.95)` semi-transparent

#### Sidebar

- `.sidebar`: `var(--primary-color)` background, white text
- `.sidebar-link`: White text, `rgba(255, 255, 255, 0.1)` hover
- `.sidebar-group-toggle`: `rgba($primary-color, 0.05)` background
- **Issue**: Still uses SASS `$primary-color` in some calculations

#### Content Areas

- `.post-card`: `var(--secondary-color)` background
- `.page-content`: `var(--text-color)` text
- Links: `var(--accent-color)` → `var(--primary-color)` on hover
- Borders: `var(--border-color)` throughout

#### Buttons & Interactive Elements

- `.btn-primary`: `var(--primary-color)` background
- `.tag`: `var(--accent-color)` background, white text
- `.search-input`: `lighten($secondary-color, 30%)` border
- **Issue**: Mix of CSS variables and SASS functions

#### Code & Special Elements

- `code`: `rgba(0, 0, 0, 0.05)` background (hardcoded)
- `pre`: `rgba(0, 0, 0, 0.05)` background (hardcoded)
- `.ai-disclaimer`: `rgba($primary-color, 0.05)` background

#### Form Elements

- `.contact-form`: `lighten($border-color, 3%)` background
- Input focus: `$primary-color` border, `rgba($primary-color, 0.1)` shadow
- `.submit-btn`: `$primary-color` background

### PROBLEMS IDENTIFIED 🚨

#### 1. **Inconsistent Color Systems**

- CSS variables used for main theming
- SASS variables still used in calculations
- Some hardcoded rgba values
- Mix of old and new color systems

#### 2. **Dark Mode Issues**

- Semi-transparent header causing text collision (✅ FIXED)
- Hardcoded `rgba(0, 0, 0, 0.05)` not adapting to dark mode
- Some SASS calculations not respecting dark mode

#### 3. **Contrast Issues**

- `.text-muted` may be too light in some palettes
- Sidebar submenu text contrast
- Code blocks need dark mode variants

#### 4. **Missing Color Definitions**

- No CSS variable for text-muted dark mode
- No proper error/success colors
- Missing hover states for some elements

### RECOMMENDED FIXES 🛠️

#### 1. **Unify Color System**

```scss
// Replace all SASS color usage with CSS variables
.sidebar-group-toggle {
  background: rgba(var(--primary-color-rgb), 0.05);
}

// Add RGB variants for transparency
:root {
  --primary-color-rgb: 44, 62, 80;
  --accent-color-rgb: 52, 152, 219;
}
```

#### 2. **Fix Dark Mode**

```scss
[data-theme="dark"] {
  --code-background: rgba(255, 255, 255, 0.1);
  --form-background: rgba(44, 62, 80, 0.3);
  --text-muted: #cbd5e1;
}
```

#### 3. **Add Missing Colors**

```scss
:root {
  --success-color: #27ae60;
  --warning-color: #f39c12;
  --error-color: #e74c3c;
  --info-color: var(--accent-color);
}
```

#### 4. **Priority Fix List**

1. ✅ **Convert SASS color calculations to CSS variables**
2. ✅ **Fix hardcoded rgba backgrounds for dark mode**
3. ✅ **Add proper contrast ratios for all text**
4. ❌ **Test all 8 palettes for accessibility** (CANCELLED - moved to single palette)
5. ✅ **Add semantic color names (success, warning, etc.)**

---

## COLOR GROUPING ANALYSIS 🎯

### Current Color Usage (173 instances found)

After converting to pure SASS, here's how our 7 core colors are being used:

#### **GROUP 1: STRUCTURAL ELEMENTS (Headers, Navigation, Buttons)**

**Uses: `$primary-color` (#2c3e50)**

- Site header background
- Navigation brand and active links
- Primary buttons (.btn-primary)
- Sidebar background
- Footer background
- Blockquote left borders
- Section headings (h2)
- Strong emphasis text
- Link hover states
- Active/focus states

**Count: ~45 instances**

#### **GROUP 2: CONTENT CONTAINERS (Cards, Backgrounds)**

**Uses: `$secondary-color` (#e8edf2)**

- Post card backgrounds
- Category/tag card backgrounds
- Contact form backgrounds
- Gallery backgrounds
- AI disclaimer secondary areas
- Muted text elements (lighten variations)
- Navigation element borders
- Search input placeholder text

**Count: ~25 instances**

#### **GROUP 3: INTERACTIVE ELEMENTS (Links, Highlights, Tags)**

**Uses: `$accent-color` (#3498db)**

- Link colors
- Tag backgrounds
- Footer link hover states
- Navigation hover accents
- Sidebar active border highlights
- Success color derivations

**Count: ~15 instances**

#### **GROUP 4: MAIN CONTENT AREAS (Page Background)**

**Uses: `$background-color` (#ffffff)**

- Body background
- Main content background
- Search results background
- Pure content areas

**Count: ~8 instances**

#### **GROUP 5: PRIMARY TEXT (Headlines, Body Text)**

**Uses: `$text-color` (#2c3e50) - SAME AS PRIMARY!**

- All heading text (h1-h6)
- Body text (p, li)
- Navigation brand text
- Post titles and content
- Form labels
- Section titles
- **All shadow/overlay rgba calculations**

**Count: ~55 instances**

#### **GROUP 6: SECONDARY TEXT (Metadata, Captions)**

**Uses: `$text-muted` (#7f8c8d)**

- Post metadata
- Breadcrumb text
- Pagination info
- Form help text
- Tag descriptions
- Sidebar secondary text

**Count: ~15 instances**

#### **GROUP 7: BORDERS & DIVIDERS (Lines, Separators)**

**Uses: `$border-color` (#bdc3c7)**

- All standard borders
- Post card borders
- Form input borders
- Pagination dividers
- Section separators
- Sidebar group borders
- Lighten variations for subtle borders

**Count: ~25 instances**

### **CONSOLIDATION OPPORTUNITIES** 🔄

#### **Major Overlap Issue:**

**`$primary-color` and `$text-color` are IDENTICAL (#2c3e50)**

- This creates 100 instances using the same color
- Headers and text share the same color
- All shadows/overlays use this color for rgba calculations

#### **Recommended 5-Color Consolidation:**

**1. SURFACE** (`$primary-color` + `$text-color` merged)

- Headers, navigation, primary text, shadows
- The dominant "dark" color for structure and readability

**2. CONTAINER** (`$secondary-color`)

- All background containers, cards, form backgrounds
- The light background for content areas

**3. ACCENT** (`$accent-color`)

- Interactive elements, links, highlights, active states
- The "pop" color for user interaction

**4. CANVAS** (`$background-color`)

- Main page background, pure content areas
- The base layer (likely always white)

**5. SUBTLE** (`$border-color` + `$text-muted` merged)

- Borders, dividers, secondary text, metadata
- The quiet color for organization and hierarchy

### **QUESTIONS FOR REVIEW:**

1. **Should headers and body text be the same color?** (Currently both #2c3e50)
2. **Can we merge `$border-color` and `$text-muted`?** (Very similar usage patterns)
3. **Is `$background-color` always white?** (Could be a constant, not variable)
4. **Should we have separate light/dark variants?** (Day/night modes)

This analysis shows we can realistically get down to **4-5 core colors** instead of 7, with much cleaner semantic meaning.
