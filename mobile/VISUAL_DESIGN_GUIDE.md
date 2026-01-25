# Visual Design Guide

## Quick Reference: Key Design Changes

### 🎨 Color Palette

#### Primary Colors
```
OLD: #6200EE (Material Purple)
NEW: #4F46E5 (Modern Indigo)
```

#### Secondary Colors
```
OLD: #03DAC6 (Cyan)
NEW: #10B981 (Emerald Green)
```

#### Background
```
OLD: #FFFFFF (Pure White)
NEW: #F9FAFB (Subtle Off-White)
```

#### Text Hierarchy
```
Primary:   #111827 (Near Black)
Secondary: #6B7280 (Medium Gray)
Tertiary:  #9CA3AF (Light Gray)
```

### 📝 Typography Scale

| Level | Old Size | New Size | Usage |
|-------|----------|----------|-------|
| Display | N/A | 40px | Auth screen titles |
| XXXL | 32px | 32px | Large headings |
| XXL | 24px | 24px | Section titles |
| XL | N/A | 20px | Card titles |
| LG | 18px | 18px | Subtitles |
| Base | 16px | 16px | Default text |
| MD | 16px | 15px | Body text |
| SM | 14px | 13px | Labels |
| XS | 12px | 11px | Captions |

### 🔤 Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Normal | 400 | Body text |
| Medium | 500 | Emphasis |
| Semibold | 600 | Labels, metadata |
| Bold | 700 | Titles, headers |
| Extrabold | 800 | Hero text |

### 📏 Spacing System

| Level | Old | New | Usage |
|-------|-----|-----|-------|
| XXS | N/A | 2px | Micro spacing |
| XS | 4px | 4px | Minimal |
| SM | 8px | 8px | Tight |
| MD | 16px | 16px | Standard |
| LG | 24px | 24px | Generous |
| XL | 32px | 32px | Large |
| XXL | N/A | 40px | Extra large |

### 🎭 Border Radius

```
Cards:   8px → 16px
Buttons: default → 12px
Inputs:  default → 12px (via Paper)
Chips:   default → stays rounded
```

### 🌑 Shadows

#### Small
```
shadowOffset: { width: 0, height: 1 }
shadowOpacity: 0.05
shadowRadius: 2
elevation: 1
```

#### Medium
```
shadowOffset: { width: 0, height: 2 }
shadowOpacity: 0.1
shadowRadius: 4
elevation: 3
```

#### Large
```
shadowOffset: { width: 0, height: 4 }
shadowOpacity: 0.15
shadowRadius: 8
elevation: 5
```

## Component Comparisons

### StatsCard

**Before:**
- 64x64px icon container
- 28px value text
- 8px border radius
- elevation: 2
- 16px margin horizontal

**After:**
- 72x72px icon container
- 32px value text (weight: 800)
- 16px border radius
- Custom medium shadow
- 20px margin horizontal
- Uppercase title with letter spacing
- Better opacity for icon backgrounds (15%)

### InventoryCard

**Before:**
- 80x80px image
- 18px price text
- 8px border radius
- elevation: 2
- 16px margin horizontal

**After:**
- 88x88px image
- 20px price text (weight: 800)
- 16px border radius
- Custom medium shadow
- 20px margin horizontal
- Better chip styling
- Improved status indicators

### Button Styling

**Before:**
- Default border radius
- Default padding
- Standard font weight

**After:**
- 12px border radius
- 6px vertical padding
- Font weight: 600-700
- Better press states

### Tab Navigation

**Before:**
- Default height
- Default padding
- Standard font

**After:**
- 60px height
- 8px top/bottom padding
- Font size: 12px
- Font weight: 600
- Better icon sizing

## Screen-Specific Changes

### Login/Register Screens

**Title:**
- Size: 32px → 40px
- Weight: bold → 800
- Letter spacing: -0.5

**Inputs:**
- Margin: 8px → 16px between fields
- Background: explicit white
- Error text: repositioned (no negative margins)

**Padding:**
- 20px → 24px all around

### Dashboard

**Section Titles:**
- Size: 20px → 22px
- Weight: bold → 700
- Letter spacing: -0.3

**Cards:**
- Margin: 8px → 12px vertical
- Spacing: 16px → 20px horizontal

### Inventory Detail

**Image:**
- Height: 300px → 320px

**Title:**
- Size: 24px → 26px
- Weight: bold → 800
- Letter spacing: -0.5

**Price:**
- Size: 28px → 32px
- Weight: bold → 800

### Profile

**Header:**
- Background: added surface color
- Padding: 32px → 40px vertical

**Username:**
- Size: 24px → 26px
- Weight: bold → 800

## Color Usage Guide

### Primary (#4F46E5)
- Primary actions (buttons)
- Links and interactive elements
- Tab bar active state
- Headers
- Brand elements

### Secondary (#10B981)
- Success states
- Positive actions
- Growth indicators
- Checkmarks

### Error (#EF4444)
- Error messages
- Failed states
- Delete actions
- Warning indicators

### Warning (#F59E0B)
- Pending states
- Caution indicators
- Processing states

### Info (#3B82F6)
- Information boxes
- Tips and hints
- Help text

### Text Colors
- **Primary (#111827)**: Main content, titles
- **Secondary (#6B7280)**: Supporting text, labels
- **Tertiary (#9CA3AF)**: Hints, placeholders, metadata

## Opacity Usage

Common opacity values with the `withOpacity()` utility:

```typescript
// Background tints
withOpacity(Colors.primary, '08')  // 8%  - Very subtle
withOpacity(Colors.primary, '15')  // 15% - Icon backgrounds
withOpacity(Colors.primary, '20')  // 20% - Borders, dividers

// Example usage
backgroundColor: withOpacity(Colors.primary, '08')
```

## Accessibility Guidelines

### Contrast Ratios
- **Normal text**: 4.5:1 minimum (WCAG AA)
- **Large text**: 3:1 minimum (WCAG AA)
- All color combinations meet or exceed these ratios

### Touch Targets
- Minimum size: 44x44 dp
- Proper spacing between interactive elements
- Clear visual feedback on press

### Typography
- Line heights: 1.4-1.5 for body text
- Sufficient font sizes for readability
- Clear hierarchy for scanning

## Development Usage

### Importing
```typescript
import { Colors, Theme, withOpacity } from '../constants/Colors';
```

### Using Colors
```typescript
// Direct color usage
color: Colors.primary
backgroundColor: Colors.background

// With opacity
backgroundColor: withOpacity(Colors.primary, '15')
```

### Using Theme
```typescript
// Spacing
marginTop: Theme.spacing.md
padding: Theme.spacing.lg

// Typography
fontSize: Theme.fontSize.lg
fontWeight: Theme.fontWeight.bold

// Shadows
...Theme.shadows.medium
```

## Best Practices

1. **Always use theme values** instead of hardcoded numbers
2. **Use withOpacity()** for consistent opacity handling
3. **Follow the spacing scale** for consistent layouts
4. **Use semantic colors** (success, error, etc.) appropriately
5. **Maintain 44x44 minimum touch targets**
6. **Apply proper shadow levels** for depth hierarchy
7. **Use consistent border radius** (12-16px)
8. **Follow text hierarchy** (primary/secondary/tertiary)

## Common Patterns

### Card Layout
```typescript
<Card style={{
  marginVertical: 8,
  marginHorizontal: 20,
  borderRadius: 16,
  backgroundColor: Colors.surface,
  ...Theme.shadows.medium,
}}>
```

### Section Title
```typescript
<Text style={{
  fontSize: Theme.fontSize.lg,
  fontWeight: Theme.fontWeight.bold,
  color: Colors.textPrimary,
  marginBottom: Theme.spacing.md,
  letterSpacing: -0.3,
}}>
```

### Info Box
```typescript
<View style={{
  backgroundColor: withOpacity(Colors.info, '08'),
  padding: Theme.spacing.lg,
  borderRadius: 12,
  borderWidth: 1,
  borderColor: withOpacity(Colors.info, '20'),
}}>
```

---

**Last Updated**: Design Modernization PR
**Version**: 1.0.0
