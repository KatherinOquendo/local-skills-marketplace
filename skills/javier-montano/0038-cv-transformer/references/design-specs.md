# CV Design Specifications

## WOW Version — Visual Design System

### Color Palettes by Industry

Choose the palette that best matches the candidate's industry. If uncertain, use "Professional Modern."

| Industry | Primary | Secondary | Accent | Background |
|----------|---------|-----------|--------|------------|
| **Tech / Startup** | `2563EB` (electric blue) | `1E293B` (slate dark) | `06B6D4` (cyan) | `F8FAFC` |
| **Finance / Banking** | `1E3A5F` (navy) | `D4AF37` (gold) | `FFFFFF` (white) | `F5F5F5` |
| **Healthcare** | `0D9488` (teal) | `134E4A` (dark teal) | `F0FDF4` (mint) | `FFFFFF` |
| **Creative / Design** | `7C3AED` (purple) | `EC4899` (pink) | `FBBF24` (amber) | `FAFAFA` |
| **Engineering** | `DC2626` (red) | `1F2937` (charcoal) | `F59E0B` (orange) | `F9FAFB` |
| **Education** | `059669` (emerald) | `1E40AF` (blue) | `FBBF24` (gold) | `FFFFF0` |
| **Marketing / Sales** | `F97316` (orange) | `1E293B` (dark) | `8B5CF6` (violet) | `FFF7ED` |
| **Legal** | `44403C` (stone) | `78716C` (warm gray) | `B45309` (amber) | `FAFAF9` |
| **Professional Modern** | `0F172A` (near black) | `3B82F6` (blue) | `10B981` (green) | `F8FAFC` |

### Typography Pairing

| Style | Header Font | Body Font | Size Header | Size Body |
|-------|-------------|-----------|-------------|-----------|
| **Executive** | Georgia | Calibri | 28-36pt | 10-11pt |
| **Modern** | Arial Black | Arial | 24-32pt | 10-11pt |
| **Creative** | Trebuchet MS | Calibri Light | 26-34pt | 10-11pt |
| **Classic** | Cambria | Garamond | 26-32pt | 10.5-11pt |
| **Minimal** | Calibri | Calibri Light | 24-30pt | 10-11pt |

### WOW DOCX Layout Spec

```
┌─────────────────────────────────────────────┐
│  ┌──────────┬────────────────────────────┐  │
│  │          │                            │  │
│  │  SIDEBAR │  MAIN CONTENT AREA         │  │
│  │  (30%)   │  (70%)                     │  │
│  │          │                            │  │
│  │ ┌──────┐ │  FULL NAME          36pt   │  │
│  │ │PHOTO │ │  Professional Title  14pt   │  │
│  │ │ area │ │  ─────────────────────────  │  │
│  │ └──────┘ │                            │  │
│  │          │  PROFESSIONAL SUMMARY       │  │
│  │ CONTACT  │  [2-3 lines, compelling]    │  │
│  │ ──────── │                            │  │
│  │ 📧 Email │  EXPERIENCE                │  │
│  │ 📱 Phone │  ┌─────────────────────┐   │  │
│  │ 📍 City  │  │ Company — Title     │   │  │
│  │ 🔗 Link  │  │ Date Range          │   │  │
│  │          │  │ • Achievement 1     │   │  │
│  │ SKILLS   │  │ • Achievement 2     │   │  │
│  │ ──────── │  │ • Achievement 3     │   │  │
│  │ ████░ 90%│  └─────────────────────┘   │  │
│  │ ███░░ 75%│                            │  │
│  │ ████░ 85%│  EDUCATION                 │  │
│  │          │  ┌─────────────────────┐   │  │
│  │ LANGS    │  │ Degree — Institution│   │  │
│  │ ──────── │  │ Date | Honors       │   │  │
│  │ EN ████░ │  └─────────────────────┘   │  │
│  │ ES █████ │                            │  │
│  │          │  CERTIFICATIONS            │  │
│  │ CERTS    │  • Cert 1 — Issuer (Year) │  │
│  │ ──────── │  • Cert 2 — Issuer (Year) │  │
│  │ • Cert 1 │                            │  │
│  │ • Cert 2 │                            │  │
│  └──────────┴────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

**Sidebar specifications:**
- Width: 30% of page (approximately 2.5 inches / 3600 DXA)
- Background: Primary color from palette
- Text color: White or light contrast
- Section dividers: thin line in accent color
- Skill bars: filled rectangles with percentage

**Main area specifications:**
- Width: 70% of page (approximately 5.5 inches / 7920 DXA)
- Background: White or very light neutral
- Section headers: Primary color, 14pt bold
- Company names: Bold, with accent color
- Dates: Right-aligned, muted gray

### WOW HTML Layout Spec

Single-page web resume with these sections:
1. **Hero Section** — Full-width, gradient background, name + title + tagline
2. **About** — Professional summary with subtle animation on scroll
3. **Experience** — Cards with company logo template, expandable details
4. **Skills** — Animated progress bars or tag cloud
5. **Education** — Timeline visual
6. **Contact** — Clean footer with social links

**Technical requirements:**
- All CSS inline or in `<style>` block (single file)
- Responsive: works on mobile, tablet, desktop
- Print-friendly: `@media print` styles that produce clean output
- No external dependencies
- Dark/light theme CSS custom properties
- Smooth scroll navigation
- Subtle animations (fade-in on scroll, skill bar fills)

### WOW PPTX Layout Spec

| Slide | Content | Layout |
|-------|---------|--------|
| 1 — Hero | Name, Title, Tagline, Photo template | Dark bg, large text, accent border |
| 2 — Summary | Professional summary + key metrics | Two-column: text + stat callouts |
| 3 — Experience | Timeline of roles | Visual timeline with icons |
| 4-N — Role Detail | One slide per major role | Company + achievements + metrics |
| N+1 — Skills | Technical + soft skills | Icon grid or category columns |
| N+2 — Education | Degrees, certifications | Clean cards layout |
| N+3 — Contact | Contact info + QR code template | Centered, clean |

---

## ATS Version — Technical Specs

### ATS DOCX Layout

```
[Full Name]                              16pt Bold Calibri
[Email] | [Phone] | [City, Country] | [LinkedIn URL]    10pt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY                     12pt Bold Calibri
[2-3 sentence summary with keywords]     10.5pt Calibri

PROFESSIONAL EXPERIENCE                  12pt Bold Calibri

[Job Title] | [Company Name]             11pt Bold
[City, Country] | [MM/YYYY – MM/YYYY]    10pt, Gray

• [Power Verb] + [Achievement] + [Metric]    10.5pt
• [Power Verb] + [Achievement] + [Metric]
• [Power Verb] + [Achievement] + [Metric]

EDUCATION                                12pt Bold Calibri

[Degree] | [Institution]                 11pt Bold
[City, Country] | [YYYY]                 10pt, Gray

SKILLS                                   12pt Bold Calibri

[Skill 1] • [Skill 2] • [Skill 3] • [Skill 4]  10.5pt

CERTIFICATIONS                           12pt Bold Calibri

[Certification] — [Issuer], [Year]       10.5pt
```

**ATS formatting rules:**
- Page margins: 1 inch (1440 DXA) all sides
- Single column only
- No tables, no text boxes, no shapes
- No images or graphics
- Standard bullet character: • (U+2022)
- Section dividers: simple line or space only
- Date format: MM/YYYY or YYYY consistently
- File: .docx (NOT .pdf — docx parses better in ATS)

### ATS HTML Layout

```html
<!-- Semantic, clean, no JavaScript -->
<article itemscope itemtype="https://schema.org/Person">
  <header>
    <h1 itemprop="name">Full Name</h1>
    <p>Email | Phone | Location | LinkedIn</p>
  </header>
  <section>
    <h2>Professional Summary</h2>
    <p>...</p>
  </section>
  <section>
    <h2>Professional Experience</h2>
    <div itemscope itemtype="https://schema.org/OrganizationRole">
      <h3>Job Title — Company</h3>
      <p>Dates</p>
      <ul><li>Achievement...</li></ul>
    </div>
  </section>
  <!-- etc. -->
</article>
```

### ATS PPTX Layout

Clean, text-focused slides:
- White background
- Standard fonts (Calibri)
- No animations or transitions
- One section per slide
- Bullet points with full achievement text
