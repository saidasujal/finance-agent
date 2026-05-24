# NexFi AI Finance Manager — Design System & Visual Specification

This document provides a comprehensive, pixel-perfect specification of the visual design system, UI layout, GUI components, micro-interactions, CSS properties, and animation dynamics of the NexFi AI Finance Manager. It serves as the single source of truth for UI redesigns and implementations using design platforms such as **Google Stitch**.

---

## 1. Visual Theme & Philosophy

NexFi utilizes a high-end, futuristic **Cyber-Noir** aesthetic. It blends deep dark slate and charcoal surfaces with neon cyan (Cyber Blue) and rich violet accents. The design achieves tactile and atmospheric depth through a combination of:
*   **Frosted Glassmorphism**: Translucent interfaces that overlay organic shapes.
*   **Ambient Auroras**: Large, slow-moving radial background blobs that soften the dark atmosphere.
*   **Noise Grain**: An organic, paper-like fine grain texture that breaks up digital flat surfaces.
*   **High-Tech Micro-Interactions**: Hover states characterized by mouse-following sheen reflections, smooth scaling, glow-enhanced elevations, and fluid physics-based transitions.

---

## 2. Global Design Tokens (CSS Variables)

The core theme values are registered as CSS custom properties under the `:root` scope:

```css
:root {
  /* Core Base Colors (Deep Charcoal Grid) */
  --bg-primary: #06080d;
  --bg-primary-rgb: 6, 8, 13;
  --bg-secondary: #0d1117;
  --bg-tertiary: #161b22;

  /* Primary Accent: Electric Cyber Blue */
  --accent-primary: #00e5ff;
  --accent-primary-rgb: 0, 229, 255;
  --accent-hover: #67f0ff;
  --accent-hover-rgb: 103, 240, 255;
  --accent-active: #00b3cc;
  --accent-active-rgb: 0, 179, 204;
  --accent-glow: rgba(0, 229, 255, 0.3);
  --accent-glow-subtle: rgba(0, 229, 255, 0.08);

  /* Secondary Accent: Neon Violet */
  --accent-secondary: #7c3aed;
  --accent-secondary-rgb: 124, 58, 237;

  /* Static Data State Indicators */
  --data-green: #10b981;      /* Safe / Earn / Positive State */
  --data-cyan: #06b6d4;       /* Balanced / Transport / Neutral */
  --data-purple: #8b5cf6;     /* Savings / Entertainment */
  --data-rose: #ef4444;       /* Overspending / Critical Limit */

  /* Text Typography Hierarchy */
  --text-primary: #e2e8f0;    /* High contrast titles and body */
  --text-secondary: #8b9cb7;  /* Secondary details / labels */
  --text-muted: #3e4c63;      /* Placeholder text / disabled / axis lines */

  /* Frosted Glass Properties */
  --glass-bg: rgba(13, 17, 23, 0.6);
  --glass-bg-hover: rgba(22, 27, 34, 0.8);
  --glass-border: rgba(255, 255, 255, 0.04);
  --glass-border-hover: rgba(0, 229, 255, 0.5);

  /* Shadows, Elevations, and Borders */
  --shadow-flat: 0 4px 24px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.04);
  --shadow-raised: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 30px rgba(0, 229, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  --shadow-inset: inset 0 1px 0 rgba(255, 255, 255, 0.08);
  --shadow-inset-hover: inset 0 1px 0 rgba(255, 255, 255, 0.16);

  /* Animation Easings & Timings (Luxury Feel) */
  --ease-luxury: cubic-bezier(0.22, 1, 0.36, 1);
  --transition-slow: 0.6s var(--ease-luxury);
  --transition-normal: 0.35s var(--ease-luxury);
  --transition-fast: 0.18s var(--ease-luxury);
}
```

---

## 3. Typography Spec

Typography utilizes three custom Google Font families, chosen to support high legibility, clean readability, and structural tabular data layouts:

| Font Name | Scope of Use | CSS Declaration | Weight Tokens | Characteristics |
| :--- | :--- | :--- | :--- | :--- |
| **Inter** | Global body copy, descriptions, buttons, chat text | `font-family: 'Inter', sans-serif;` | 300 (Light), 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold) | Balanced geometric shapes, modern sans-serif readability. |
| **Plus Jakarta Sans** | Section Headings (`h1`, `h2`, `h3`, `h4`, `h5`, `h6`) | `font-family: 'Plus Jakarta Sans', sans-serif;` | 600 (Semi-Bold), 700 (Bold), 800 (Extra-Bold) | Open apertures, premium editorial headings. |
| **Geist Mono** | Numeric values, budgets, CLI inputs, steps, statistics | `font-family: 'Geist Mono', monospace;` | 400 (Regular), 600 (Semi-Bold), 800 (Extra-Bold) | High-tech console look. Uses `font-variant-numeric: tabular-nums` to prevent shifting digits. |

---

## 4. Background & Surface Environment

The background layout relies on fixed ambient decorations that sit behind content (at `z-index: 0`):

### 4.1 Ambient Aurora Background
Four radial-gradient blur blobs float independently behind content to generate shifting backlighting:
*   **Blob 1 (Cyber Blue)**: `width: 600px; height: 600px; background: radial-gradient(circle, rgba(0, 229, 255, 0.5) 0%, transparent 70%); top: -15%; left: -10%;`
*   **Blob 2 (Violet)**: `width: 500px; height: 500px; background: radial-gradient(circle, rgba(124, 58, 237, 0.4) 0%, transparent 70%); bottom: -15%; right: -8%;`
*   **Blob 3 (Teal/Cyan)**: `width: 450px; height: 450px; background: radial-gradient(circle, rgba(6, 182, 212, 0.35) 0%, transparent 70%); top: 40%; left: 35%;`
*   **Blob 4 (Subtle Violet)**: `width: 350px; height: 350px; background: radial-gradient(circle, rgba(124, 58, 237, 0.25) 0%, transparent 70%); top: 15%; right: 20%;`

#### Blob Physics (CSS Keyframe Animations)
*   **Blob 1 (`aurora1`)**: Moves from origin `(0, 0)` to `translate(100px, 80px) scale(1.15)` over 20s.
*   **Blob 2 (`aurora2`)**: Moves from origin `(0, 0)` to `translate(-80px, -60px) scale(0.9)` over 26s.
*   **Blob 3 (`aurora3`)**: Moves from origin `(0, 0)` to `translate(60px, -90px) scale(1.1)` over 22s.
*   **Blob 4 (`aurora4`)**: Moves from origin `(0, 0)` to `translate(-50px, 70px) scale(0.95)` over 28s.
*   *Note: All run on `infinite alternate ease-in-out` loops.*

### 4.2 Noise Grain Overlay
To avoid flat gradient banding, a full-screen fixed texture is rendered over all elements:
*   **Method**: `body::after` pseudo-element with `z-index: 9000` and `pointer-events: none` (completely non-interactive).
*   **Filter**: Inline SVG Fractal Noise overlay set to `3.5%` opacity.
*   **Filter Code**:
    ```css
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-size: 256px 256px;
    background-repeat: repeat;
    opacity: 0.035;
    ```

---

## 5. Navigational Layout: Sidebar & Nav Pill

Navigation is locked to the viewport using a premium, floating, left-aligned sidebar:

*   **Structure**: Positioned `fixed` at `left: 14px`, `top: 50%`, translating vertical center `transform: translateY(-50%)`.
*   **Dimensions**: Width is set to `64px`. Rounded border-radius of `24px`. Frosted glass body with a `backdrop-filter: blur(28px) saturate(200%)`.
*   **Glow Indicator Pill (`#nav-pill`)**:
    *   A single visual accent pill is positioned absolutely inside the sidebar.
    *   **Style**: Width is `48px`, Height is `48px`, Border-radius `16px`, background `rgba(0, 229, 255, 0.12)`, border `1.5px solid rgba(0, 229, 255, 0.4)`.
    *   **Animation**: When a user scrolls to or clicks a navigation item, the pill dynamically updates its `top` position using a smooth transition: `transition: top 0.4s cubic-bezier(0.16, 1, 0.3, 1)`.
*   **Nav Items (`.nav-item`)**:
    *   Contain small emojis (`.nav-icon`) at `17px` and text descriptions (`.nav-label`) at `8px` uppercase.
    *   **Hover/Active Transition**: Hover shifts the item `translateX(4px)` and transitions text color to `--accent-hover`.

---

## 6. GUI Component Catalog

### 6.1 Glassmorphism Card (`.glass`)
The foundational card component used across all sections to wrap content.

*   **HTML Structure**:
    ```html
    <div class="glass">
      <!-- Child content inside -->
    </div>
    ```
*   **Base Styling**:
    *   **Background**: `var(--glass-bg)` (frosted charcoal)
    *   **Borders**: `1px solid var(--glass-border)` (soft white tint)
    *   **Backdrop Filter**: `blur(24px) saturate(200%) brightness(100%)` (macOS-style refraction)
    *   **Border Angle Registration**: Uses CSS `@property --border-angle` for custom gradients.
*   **Holographic Sheen Effect**:
    *   A radial gradient sheen tracks the user's cursor across the card using the `mousemove` event.
    *   **CSS Pseudo-element**: `.glass::after` with `position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity 0.3s;`
    *   **Background Style**:
        ```css
        background: radial-gradient(
          circle at var(--sheen-x, 50%) var(--sheen-y, 50%),
          rgba(255, 255, 255, 0.08) 0%,
          rgba(0, 229, 255, 0.06) 30%,
          transparent 60%
        );
        ```
    *   **State change**: Opacity triggers to `1` when hovering (`.glass:hover::after`).
*   **Hover Lift Dynamics**:
    *   On mouse-over, cards smoothly elevate and expand:
        ```css
        transform: translateY(-8px) scale(1.015);
        border-color: var(--glass-border-hover);
        background: var(--glass-bg-hover);
        box-shadow: var(--shadow-raised);
        ```

### 6.2 Interactive Buttons

#### Primary Button (`.btn-primary`)
Used for main calls to action (e.g., Launching NexFi, Sending Messages).
*   **Appearance**: Pill shape (`border-radius: 999px`), gradient fill `linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-active) 100%)`.
*   **Details**: Top border inset highlight `border-top: 1px solid rgba(255, 255, 255, 0.25)`. Text is bold and white.
*   **Transitions**: Hover triggers a slight lift (`translateY(-3px) scale(1.03)`) and an expanded cyber-glow shadow (`box-shadow: 0 8px 30px rgba(99,102,241,0.6)`). Active clicks compress the button (`translateY(-1px) scale(0.98)`).

#### Secondary Button (`.btn-secondary`)
Used for supporting actions (e.g., "See How It Works").
*   **Appearance**: Semi-transparent frosted capsule (`background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-top: 1px solid rgba(255,255,255,0.18)`).
*   **Hover State**: Transforms to a Cyber Blue tinted edge (`border-color: rgba(99,102,241,0.4)`), a subtle blue glow, and lifts `translateY(-2px)`.

#### CSV Download Pill (`.btn-csv`)
Compact utility button to trigger exports.
*   **Appearance**: Cyber Blue border with light blue glowing background (`border: 1px solid rgba(99, 102, 241, 0.4); background: var(--accent-glow-subtle); color: var(--accent-hover)`).
*   **Hover State**: Full Cyber Blue glow with white text.

### 6.3 Savings Goal Capsules (`.goal-capsule`)
Displays savings goals on the Hero banner.
*   **Structure**: A clear vertical tube container (`width: 32px; height: 72px; border-radius: 99px; border: 1.5px solid rgba(255,255,255,0.15)`).
*   **Fill State (`.goal-liquid`)**: Liquid gradient (`linear-gradient(180deg, #00e5ff 0%, #00b3cc 100%)`) fills the container from the bottom up based on completion percentage. Includes a glowing shadow.
*   **Text Overlay**: A bold Geist Mono percentage indicator sits centered in the tube, styled with a high-contrast text drop shadow.

### 6.4 Live Transaction Ticker Tape (`.ticker-wrap`)
Displays recent expenses in a continuous loop.
*   **Visual Layout**: An overflow-hidden full-width section with edge-fades.
*   **Edge Fades (Pseudo-elements)**:
    *   Both left and right boundaries fade out over `80px` using gradients.
    *   `::before`: `left: 0; background: linear-gradient(90deg, var(--bg-primary), transparent);`
    *   `::after`: `right: 0; background: linear-gradient(270deg, var(--bg-primary), transparent);`
*   **Scrolling Motion**: Content slides horizontally using `@keyframes ticker-scroll` (`0% { transform: translateX(0); } 100% { transform: translateX(-50%); }` over `32s`).
*   **Interactivity**: Hovering over the ticker halts the animation (`animation-play-state: paused`).

### 6.5 Sticky Scroll Walkthrough Layout (`#how-it-works`)
A split-screen sticky section explaining product steps.
*   **Left Column (`.sticky-left`)**:
    *   Houses a detailed mobile hardware mockup (`.device-mockup`). The device features rounded edges (`36px`), a physical notch, and a dark screen layout (`#020617`).
    *   Inside the mockup, three mock step screens (Input, AI Parsing, Insights) automatically fade in/out and scale depending on which step is active.
    *   *Step 1* shows a dynamic typing simulation typing out "Spent 2400 for new running shoes today".
    *   *Step 2* shows a code categorization spinner extraction.
    *   *Step 3* displays a progress bar filling up next to a mock assistant bubble.
*   **Right Column (`.sticky-right`)**:
    *   Contains three separate step cards.
    *   As the user scrolls, the active step card's border illuminates with a Cyber Blue border (`rgba(99,102,241,0.6)`), while inactive cards fade to `rgba(255,255,255,0.12)`.

---

## 7. Interactive Dashboards & AI Widgets

### 7.1 What-If Purchase Simulator
Allows users to preview purchase impacts before logging them.

*   **Structure**: Compact glass card (`.sim-card`) containing input inputs, category select, and a visual range slider.
*   **Accent Range Slider (`.sim-slider`)**:
    *   Track height is `6px` in matte dark grey.
    *   **Thumb**: Bold Cyber Blue circle (`width: 16px; height: 16px; box-shadow: 0 0 8px var(--accent-primary)`).
    *   **Thumb Hover**: Scales up (`scale(1.2)`) and adds a dual white/cyan glow.
*   **Projected Status Badges (`.sim-badge`)**:
    *   `SAFE`: Emerald green background with glow (`rgba(16, 185, 129, 0.12)`).
    *   `WARNING`: Warning orange background with glow (`rgba(245, 158, 11, 0.12)`).
    *   `CRITICAL`: Crimson red background with glow (`rgba(239, 68, 68, 0.12)`).
*   **Budget Ring Overlay (SVG Integration)**:
    *   An SVG circle overlay sits behind the monthly goal indicator.
    *   When a user drags the simulator slider, the underlying indicator (`#budgetRingSimFill`) sweeps forward dynamically to show projected usage, changing color from Cyber Blue to warning red as it fills.

### 7.2 GitHub-Style Spending Heatmap
Renders a grid mapping spending intensity over 90 days.

*   **Grid Specs**: 7 rows (Sunday to Saturday), columns populate dynamically to form a grid. Grid cells are spaced by `4px`.
*   **Heatmap Cells (`.heatmap-cell`)**:
    *   Size: `11px` by `11px` square, `2px` border-radius.
    *   **Hover state**: Scales up slightly (`scale(1.2)`), raising its z-index.
    *   **Color Scale Mapping**:
        *   Level 0 (Zero spend): `#1e293b` (slate charcoal)
        *   Level 1 (₹1 - ₹500): `#0e3f5c` (dark cyan)
        *   Level 2 (₹501 - ₹1500): `#0c628f` (medium cyan)
        *   Level 3 (₹1501 - ₹3000): `#0099cc` (deep blue-cyan)
        *   Level 4 (₹3000+): `#00e5ff` (neon Cyber Blue glow)
*   **Heatmap Tooltips (`.heatmap-tooltip`)**:
    *   Hovering over any cell reveals a tooltip indicating date and transaction volume.
    *   **Tooltip style**: Matte black background with a Cyber Blue border, positioned `8px` above the cell with a custom pointing chevron (`::after` bottom border).

### 7.3 CLI Terminal Overlay
A developers' high-tech console overlay.

*   **Toggle Button (`#cli-toggle-btn`)**: A floating circular trigger at the bottom-right corner (`>_`). Features a Cyber Blue border and active text centering. Hovering lifts the trigger and turns it solid Cyber Blue.
*   **Console Drawer (`#cli-overlay`)**:
    *   Slides in from the right edge (`width: 400px; height: 100vh; right: -420px;`).
    *   Slides open by setting `right: 0`.
    *   Uses a matte translucent black body (`rgba(9, 10, 15, 0.95)`) with a left border of `2px solid var(--accent-primary)`.
*   **Command Line Autocomplete Drawer (`#cli-autocomplete`)**:
    *   As the user types a slash `/`, a matching suggested list drawer opens above the command input field.
    *   **Style**: Cyber Blue borders, dark slate background. Items display the command structure in neon blue next to a grey descriptor. Selecting a line fills in the prompt.

### 7.4 Detailed Activity Log
A list mapping expense transactions.
*   **Items (`.activity-log-item`)**: Flexible rows with soft borders that slightly brighten on hover.
*   **Category Badges (`.activity-log-badge`)**:
    *   Each category uses a unique semi-transparent color tint:
        *   `Food`: Orange tint (`rgba(249, 115, 22, 0.12)`)
        *   `Transport`: Cyan tint (`rgba(6, 182, 212, 0.12)`)
        *   `Entertainment`: Purple tint (`rgba(168, 85, 247, 0.12)`)
        *   `Shopping`: Pink tint (`rgba(236, 72, 153, 0.12)`)
        *   `Health`: Red tint (`rgba(239, 68, 68, 0.12)`)
        *   `Education`: Blue tint (`rgba(59, 130, 246, 0.12)`)
        *   `Other`: Slate grey tint (`rgba(148, 163, 184, 0.12)`)

---

## 8. Layout Structures & Responsive Grids

All core sections follow standard grids that scale gracefully across viewport sizes:

### 8.1 3-Column Features Grid (`.features-grid`)
*   **Desktop**: `display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;`
*   **Mobile / Tablet (<= 768px)**: Collapses to `grid-template-columns: 1fr;`

### 8.2 Charts Dashboard Grid (`.charts-grid`)
*   **Desktop**: 6-column grid structure.
    *   Row 1 contains two cards (`.chart-card-double`), each taking up `span 3` (50% width).
    *   Row 2 contains three cards (`.chart-card-triple`), each taking up `span 2` (33% width).
*   **Mobile / Tablet (<= 900px)**: All charts scale to `span 6` (100% width) for comfortable reading.

---

## 9. Animation & Transition Specifications

All animations are designed to render smoothly at 60fps by targeting GPU-accelerated CSS properties (`transform`, `opacity`, `filter`).

### 9.1 Hero Text Masked Word Reveal
Hero titles slide up from behind an invisible threshold:
*   **Wrapper**: `.word-reveal-wrap { display: inline-block; overflow: hidden; }`
*   **Trigger**: On page load, `.word-reveal` applies `@keyframes wordSlideUp`:
    ```css
    @keyframes wordSlideUp {
      from { transform: translateY(110%) rotate(3deg); }
      to { transform: translateY(0) rotate(0deg); }
    }
    ```
*   **Timing**: Duration `0.7s`, cubic-bezier easing `var(--ease-luxury)`.
*   **Staggering**: Controlled using inline delay custom variables: `--d` delay mapping (`delay: calc(var(--d) * 0.07s)`).

### 9.2 Scroll-Triggered Fade-Ups (`.fu`)
Cards and sections fade and scale into view as the user scrolls:
*   **Initial Hidden State**: `opacity: 0; transform: translateY(28px) scale(0.97); filter: blur(4px);`
*   **Triggered Active State (`.fu.in`)**: Transitions to normal state: `opacity: 1; transform: translateY(0) scale(1); filter: blur(0);`.
*   **Timing**: Transition duration is `0.7s` using luxury easing. Stagger classes (`.d1` through `.d6`) apply delay offsets in increments of `0.06s`.

### 9.3 Scroll Progress Bar (`#scroll-progress`)
*   A fixed indicator sits at the very top of the page.
*   **Styling**: Height `3px`, z-index `9999`, Cyber Blue to Violet gradient (`linear-gradient(90deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-primary) 100%)`).
*   **Glow**: Cyber Blue drop-glow (`box-shadow: 0 0 12px rgba(0, 229, 255, 0.4)`).
*   **Animation**: Width updates dynamically (`0%` to `100%`) based on current page scroll height.

---

## 10. Chart.js Styling Configurations

Charts rendered in the Analytics panel are styled using the following aesthetic overrides:
*   **Gridlines**: Set to `rgba(255, 255, 255, 0.05)` (extremely faint lines to preserve visual cleanliness).
*   **Ticks & Labels**: Soft text color `rgba(241, 245, 249, 0.5)`.
*   **Doughnut Chart Palette**: Uses neon segments (`#00e5ff`, `#06B6D4`, `#10B981`, `#F59E0B`, `#EF4444`, `#8B5CF6`).
*   **Budget Comparison**: Features a semi-transparent Cyber Blue bar for the target budget next to a solid Emerald Green bar for actual spending.

---

## 11. Accessibility (A11y) & Performance Optimization

To ensure smooth performance and accessibility compliance, the following guidelines are implemented:
*   **Reduced Motion Override**:
    When a user has motion-reduction enabled at the OS level, slow background animations are halted immediately:
    ```css
    @media (prefers-reduced-motion: reduce) {
      .aurora-blob {
        animation: none !important;
      }
      .ticker-content {
        animation: none !important;
      }
    }
    ```
*   **Performance Optimization**:
    All slow-moving backgrounds use CSS translation and `will-change: transform`. This offloads layout calculation to the GPU, preventing browser repaints during scroll.
