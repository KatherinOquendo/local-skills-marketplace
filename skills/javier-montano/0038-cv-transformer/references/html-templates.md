# HTML Resume Templates

## WOW HTML Template Structure

The WOW HTML resume is a single-file, self-contained web page. All CSS and JS must be inline.

### Template Blueprint

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{FULL_NAME}} — Resume</title>
  <style>
    /* ═══════════ CSS CUSTOM PROPERTIES ═══════════ */
    :root {
      --primary: {{PRIMARY_COLOR}};
      --secondary: {{SECONDARY_COLOR}};
      --accent: {{ACCENT_COLOR}};
      --bg: {{BG_COLOR}};
      --text: #1a1a2e;
      --text-light: #6b7280;
      --card-bg: #ffffff;
      --shadow: 0 4px 20px rgba(0,0,0,0.08);
      --radius: 12px;
      --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    [data-theme="dark"] {
      --bg: #0f172a;
      --text: #f1f5f9;
      --text-light: #94a3b8;
      --card-bg: #1e293b;
      --shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* ═══════════ RESET & BASE ═══════════ */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      transition: var(--transition);
    }

    /* ═══════════ HERO SECTION ═══════════ */
    .hero {
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      padding: 80px 40px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .hero::after {
      content: '';
      position: absolute;
      bottom: -50px;
      left: 0;
      right: 0;
      height: 100px;
      background: var(--bg);
      transform: skewY(-3deg);
    }
    .hero h1 {
      font-size: 3rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 0.5rem;
    }
    .hero .subtitle {
      font-size: 1.3rem;
      opacity: 0.9;
      font-weight: 300;
    }
    .hero .tagline {
      margin-top: 1rem;
      font-size: 1rem;
      opacity: 0.75;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }
    .contact-bar {
      display: flex;
      justify-content: center;
      gap: 24px;
      margin-top: 24px;
      flex-wrap: wrap;
    }
    .contact-bar a {
      color: white;
      text-decoration: none;
      opacity: 0.85;
      font-size: 0.9rem;
      transition: var(--transition);
    }
    .contact-bar a:hover { opacity: 1; }

    /* ═══════════ NAVIGATION ═══════════ */
    .nav {
      position: sticky;
      top: 0;
      background: var(--card-bg);
      z-index: 100;
      padding: 12px 40px;
      display: flex;
      justify-content: center;
      gap: 32px;
      box-shadow: var(--shadow);
    }
    .nav a {
      color: var(--text);
      text-decoration: none;
      font-weight: 500;
      font-size: 0.9rem;
      transition: var(--transition);
      border-bottom: 2px solid transparent;
      padding-bottom: 4px;
    }
    .nav a:hover, .nav a.active {
      color: var(--primary);
      border-bottom-color: var(--accent);
    }

    /* ═══════════ CONTENT SECTIONS ═══════════ */
    .container { max-width: 900px; margin: 0 auto; padding: 40px 24px; }
    section { margin-bottom: 60px; }
    .section-title {
      font-size: 1.6rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .section-title::after {
      content: '';
      flex: 1;
      height: 2px;
      background: linear-gradient(to right, var(--accent), transparent);
    }

    /* ═══════════ EXPERIENCE CARDS ═══════════ */
    .exp-card {
      background: var(--card-bg);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
      border-left: 4px solid var(--accent);
      transition: var(--transition);
      opacity: 0;
      transform: translateY(20px);
    }
    .exp-card.visible {
      opacity: 1;
      transform: translateY(0);
    }
    .exp-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .exp-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }
    .exp-title { font-size: 1.1rem; font-weight: 700; }
    .exp-company { color: var(--primary); font-weight: 600; }
    .exp-date { color: var(--text-light); font-size: 0.85rem; }
    .exp-card ul { padding-left: 20px; }
    .exp-card li {
      margin-bottom: 8px;
      color: var(--text);
      line-height: 1.5;
    }
    .metric {
      background: linear-gradient(to right, var(--accent), var(--primary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-weight: 700;
    }

    /* ═══════════ SKILLS ═══════════ */
    .skills-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 16px;
    }
    .skill-category h3 {
      font-size: 0.9rem;
      text-transform: uppercase;
      color: var(--text-light);
      margin-bottom: 12px;
      letter-spacing: 0.05em;
    }
    .skill-bar {
      margin-bottom: 10px;
    }
    .skill-bar .label {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      margin-bottom: 4px;
    }
    .skill-bar .bar {
      height: 6px;
      background: #e5e7eb;
      border-radius: 3px;
      overflow: hidden;
    }
    .skill-bar .fill {
      height: 100%;
      background: linear-gradient(to right, var(--primary), var(--accent));
      border-radius: 3px;
      width: 0%;
      transition: width 1.5s ease;
    }

    /* ═══════════ EDUCATION ═══════════ */
    .edu-item {
      display: flex;
      gap: 16px;
      margin-bottom: 20px;
      align-items: flex-start;
    }
    .edu-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--accent);
      margin-top: 6px;
      flex-shrink: 0;
    }

    /* ═══════════ THEME TOGGLE ═══════════ */
    .theme-toggle {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--primary);
      color: white;
      border: none;
      cursor: pointer;
      font-size: 1.2rem;
      box-shadow: var(--shadow);
      z-index: 200;
      transition: var(--transition);
    }
    .theme-toggle:hover { transform: scale(1.1); }

    /* ═══════════ PRINT STYLES ═══════════ */
    @media print {
      .nav, .theme-toggle { display: none !important; }
      .hero { padding: 30px; }
      .hero h1 { font-size: 2rem; }
      .exp-card { box-shadow: none; border: 1px solid #ddd; break-inside: avoid; }
      .exp-card { opacity: 1 !important; transform: none !important; }
      body { font-size: 10pt; }
    }

    /* ═══════════ RESPONSIVE ═══════════ */
    @media (max-width: 640px) {
      .hero { padding: 50px 20px; }
      .hero h1 { font-size: 2rem; }
      .nav { gap: 16px; padding: 10px 16px; overflow-x: auto; }
      .container { padding: 24px 16px; }
      .exp-header { flex-direction: column; }
      .skills-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <!-- HERO -->
  <div class="hero">
    <h1>{{FULL_NAME}}</h1>
    <p class="subtitle">{{PROFESSIONAL_TITLE}}</p>
    <p class="tagline">{{TAGLINE}}</p>
    <div class="contact-bar">
      <a href="mailto:{{EMAIL}}">{{EMAIL}}</a>
      <a href="tel:{{PHONE}}">{{PHONE}}</a>
      <a>{{LOCATION}}</a>
      <a href="{{LINKEDIN_URL}}" target="_blank">LinkedIn</a>
    </div>
  </div>

  <!-- NAV -->
  <nav class="nav">
    <a href="#about">About</a>
    <a href="#experience">Experience</a>
    <a href="#skills">Skills</a>
    <a href="#education">Education</a>
  </nav>

  <div class="container">
    <!-- ABOUT -->
    <section id="about">
      <h2 class="section-title">About</h2>
      <p>{{PROFESSIONAL_SUMMARY}}</p>
    </section>

    <!-- EXPERIENCE -->
    <section id="experience">
      <h2 class="section-title">Experience</h2>
      {{EXPERIENCE_CARDS}}
      <!--
      For each role, generate:
      <div class="exp-card">
        <div class="exp-header">
          <div>
            <div class="exp-title">{{JOB_TITLE}}</div>
            <div class="exp-company">{{COMPANY_NAME}}</div>
          </div>
          <div class="exp-date">{{DATE_RANGE}}</div>
        </div>
        <ul>
          <li>{{ACHIEVEMENT_WITH_METRICS}}</li>
        </ul>
      </div>
      -->
    </section>

    <!-- SKILLS -->
    <section id="skills">
      <h2 class="section-title">Skills</h2>
      <div class="skills-grid">
        {{SKILLS_CATEGORIES}}
        <!--
        For each category:
        <div class="skill-category">
          <h3>{{CATEGORY_NAME}}</h3>
          <div class="skill-bar">
            <div class="label"><span>{{SKILL}}</span><span>{{LEVEL}}%</span></div>
            <div class="bar"><div class="fill" data-width="{{LEVEL}}"></div></div>
          </div>
        </div>
        -->
      </div>
    </section>

    <!-- EDUCATION -->
    <section id="education">
      <h2 class="section-title">Education</h2>
      {{EDUCATION_ITEMS}}
    </section>

    <!-- CERTIFICATIONS -->
    <section id="certifications">
      <h2 class="section-title">Certifications</h2>
      {{CERTIFICATIONS_LIST}}
    </section>
  </div>

  <!-- THEME TOGGLE -->
  <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
    <span id="theme-icon">🌙</span>
  </button>

  <script>
    // Theme toggle
    function toggleTheme() {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'light' ? 'dark' : 'light';
      html.setAttribute('data-theme', next);
      document.getElementById('theme-icon').textContent = next === 'light' ? '🌙' : '☀️';
    }

    // Scroll animations
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.exp-card').forEach(card => observer.observe(card));

    // Skill bar animations
    const skillObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.querySelectorAll('.fill').forEach(fill => {
            fill.style.width = fill.dataset.width + '%';
          });
        }
      });
    }, { threshold: 0.3 });

    document.querySelectorAll('.skill-category').forEach(cat => skillObserver.observe(cat));

    // Active nav on scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav a');
    window.addEventListener('scroll', () => {
      let current = '';
      sections.forEach(section => {
        const top = section.offsetTop - 100;
        if (scrollY >= top) current = section.getAttribute('id');
      });
      navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === '#' + current);
      });
    });
  </script>
</body>
</html>
```

## ATS HTML Template

The ATS HTML is semantic, clean, and parseable with zero visual frills.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{FULL_NAME}} — Resume</title>
  <style>
    body {
      font-family: Calibri, Arial, sans-serif;
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      color: #333;
      line-height: 1.5;
      font-size: 11pt;
    }
    h1 { font-size: 18pt; margin-bottom: 4px; color: #000; }
    .contact { font-size: 10pt; color: #555; margin-bottom: 20px; }
    h2 {
      font-size: 12pt;
      text-transform: uppercase;
      border-bottom: 1px solid #333;
      padding-bottom: 4px;
      margin-top: 20px;
      margin-bottom: 12px;
      color: #000;
    }
    h3 { font-size: 11pt; margin-bottom: 2px; }
    .date { font-size: 10pt; color: #666; margin-bottom: 8px; }
    ul { padding-left: 20px; margin-bottom: 16px; }
    li { margin-bottom: 6px; }
    .skills-list { columns: 2; }
    @media print {
      body { margin: 0; padding: 0; }
    }
  </style>
</head>
<body>
  <article itemscope itemtype="https://schema.org/Person">
    <h1 itemprop="name">{{FULL_NAME}}</h1>
    <p class="contact">
      <span itemprop="email">{{EMAIL}}</span> |
      <span itemprop="telephone">{{PHONE}}</span> |
      <span itemprop="address">{{LOCATION}}</span> |
      <a itemprop="url" href="{{LINKEDIN_URL}}">LinkedIn</a>
    </p>

    <h2>Professional Summary</h2>
    <p itemprop="description">{{SUMMARY}}</p>

    <h2>Professional Experience</h2>
    {{EXPERIENCE_ENTRIES}}

    <h2>Education</h2>
    {{EDUCATION_ENTRIES}}

    <h2>Skills</h2>
    <div class="skills-list">{{SKILLS_LIST}}</div>

    <h2>Certifications</h2>
    {{CERTIFICATIONS}}
  </article>
</body>
</html>
```

## Generation Instructions

When generating HTML resumes:

1. **WOW version**: Use the WOW template as a starting point. Replace all `{{templateS}}` with actual data. Customize colors based on industry (see design-specs.md). Add real content for all sections. Make sure all animations work. Test responsiveness mentally.

2. **ATS version**: Use the ATS template. Pure semantic HTML. Schema.org markup. No visual flourishes. Ensure all text is directly readable by ATS parsers.

3. **Both versions**: Write valid HTML5. Include proper `<meta>` tags. Ensure print styles work. All links should be functional.
