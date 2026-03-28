# JM Labs Corporate Document Patterns

Reference for `jmlabs-corporate-doc` skill. Contains full section blueprints, component examples, and document type templates.

---

## Metric Display Pattern

Used in Cover slide and key data slides.

```html
<!-- Hero metric grid (cover) -->
<div class="g3" style="max-width:22rem;margin:0 auto;">
  <div style="text-align:center;">
    <div class="mv">50%</div>
    <div class="ml"><span data-l="es">Margen objetivo</span><span data-l="en">Target margin</span></div>
  </div>
  <div style="text-align:center;">
    <div class="mv">10x</div>
    <div class="ml">LTV/CAC</div>
  </div>
  <div style="text-align:center;">
    <div class="mv" style="color:var(--gold);">$0</div>
    <div class="ml"><span data-l="es">Entrada</span><span data-l="en">Entry</span></div>
  </div>
</div>

<!-- Inline metric in text -->
<p>Con <strong style="color:var(--gold);font-size:1.2em;">557</strong>
   <span data-l="es">skills certificados</span>
   <span data-l="en">certified skills</span></p>
```

---

## Top Navigation Bar

```html
<nav class="jml-nav">
  <div class="jml-nav-inner">
    <!-- Logo -->
    <div class="jml-logo">
      <svg viewBox="0 0 36 36" fill="none" width="22" height="22">
        <rect width="36" height="36" rx="10" fill="#122562"/>
        <path d="M10 12h3v12h-3V12zm6 0h3v8h-3v-8zm0 10h3v2h-3v-2zm6-10h3v6h-3v-6zm0 8h3v4h-3v-4z" fill="white"/>
        <circle cx="18" cy="8" r="2" fill="#FFD700"/>
      </svg>
      <span class="jml-logo-text">JM <span class="jml-logo-accent">Labs</span></span>
    </div>
    <!-- Controls -->
    <div style="display:flex;align-items:center;gap:.5rem;">
      <span class="t" style="color:var(--gold);">
        <span data-l="es">{TIPO_DOC}</span>
        <span data-l="en">{DOC_TYPE}</span>
      </span>
      <span style="width:1px;height:12px;background:var(--divider);margin:0 .125rem;"></span>
      <button class="jml-nav-btn" onclick="toggleLang()">ES/EN</button>
      <button class="jml-nav-btn" onclick="toggleTheme()" id="theme-btn">☾</button>
      <button class="jml-nav-btn" onclick="window.print()">⎙</button>
    </div>
  </div>
</nav>
```

---

## Table of Contents Pattern

```html
<div id="toc" style="padding:2rem 0;border-bottom:1px solid var(--divider);">
  <div style="max-width:44rem;">
    <h3 style="font-size:.875rem;margin-bottom:.75rem;">
      <span data-l="es">Contenido</span><span data-l="en">Contents</span>
    </h3>
    <div class="toc g2">
      <!-- Standard section -->
      <a href="#problem">
        <span class="num">1</span>
        <span data-l="es">El Problema — Por qué ahora</span>
        <span data-l="en">The Problem — Why now</span>
      </a>
      <!-- Highlighted section (gold) -->
      <a href="#partnership">
        <span class="num" style="background:color-mix(in srgb,var(--gold) 12%,transparent);color:var(--gold);border-color:var(--gold);">8</span>
        <span data-l="es" style="color:var(--gold);font-weight:700;">Partnership &amp; Ask</span>
        <span data-l="en" style="color:var(--gold);font-weight:700;">Partnership &amp; Ask</span>
      </a>
    </div>
  </div>
</div>
```

---

## Problem Slide Pattern

```html
<div class="slide" id="problem">
  <div style="max-width:44rem;">
    <div class="t gold" style="margin-bottom:.375rem;">
      <span data-l="es">El Problema</span><span data-l="en">The Problem</span>
    </div>
    <h2 style="font-size:clamp(1.25rem,3vw,1.75rem);margin-bottom:.75rem;">
      <span data-l="es">{HEADLINE_ES} <span class="gold">{EMPHASIS_ES}</span></span>
      <span data-l="en">{HEADLINE_EN} <span class="gold">{EMPHASIS_EN}</span></span>
    </h2>
    <!-- Bridge cards for evidence -->
    <div class="bridge">
      <span class="bridge-d"><span data-l="es">Dato:</span><span data-l="en">Data:</span></span>
      {STAT} <span class="src" onclick="openModal('m-{source}')">{SOURCE}</span><br>
      <span class="bridge-i"><span data-l="es">{IMPLICATION_ES}</span><span data-l="en">{IMPLICATION_EN}</span></span><br>
      <span class="bridge-a"><span data-l="es">{ACTION_ES}</span><span data-l="en">{ACTION_EN}</span></span>
    </div>
    <span class="slide-num">{N}</span>
  </div>
</div>
```

---

## Business Model / Pricing Slide

```html
<div class="slide" id="model">
  <div style="max-width:44rem;">
    <div class="t gold" style="margin-bottom:.375rem;">
      <span data-l="es">Modelo de Negocio</span><span data-l="en">Business Model</span>
    </div>
    <h2 style="font-size:clamp(1.25rem,3vw,1.5rem);margin-bottom:.75rem;">
      <span data-l="es">Try &amp; Buy — <span class="gold">Sin riesgo de entrada</span></span>
      <span data-l="en">Try &amp; Buy — <span class="gold">Zero entry risk</span></span>
    </h2>
    <div class="g3">
      <!-- Tier card pattern -->
      <div class="c camp">
        <div class="t" style="color:var(--text-m);margin-bottom:.25rem;">Tier 1</div>
        <div class="mv" style="font-size:1.5rem;">{PRICE}</div>
        <div class="ml" style="margin-bottom:.5rem;">{BILLING}</div>
        <p class="s">{DESCRIPTION}</p>
      </div>
    </div>
    <span class="slide-num">{N}</span>
  </div>
</div>
```

---

## Team Slide Pattern

```html
<div class="slide" id="team">
  <div style="max-width:44rem;">
    <div class="t gold" style="margin-bottom:.375rem;">
      <span data-l="es">Equipo</span><span data-l="en">Team</span>
    </div>
    <div class="g2">
      <div class="c">
        <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.75rem;">
          <div style="width:40px;height:40px;border-radius:50%;background:var(--navy);border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;font-family:'Poppins',sans-serif;font-weight:800;color:var(--gold);">{INITIAL}</div>
          <div>
            <div style="font-weight:700;font-size:.875rem;color:var(--heading);">{NAME}</div>
            <div class="t" style="margin-top:2px;">{ROLE}</div>
          </div>
        </div>
        <p class="s">{BIO}</p>
      </div>
    </div>
    <span class="slide-num">{N}</span>
  </div>
</div>
```

---

## CTA / Partnership Ask Slide

```html
<div class="slide center" id="partnership">
  <div style="max-width:38rem;margin:0 auto;">
    <div class="t gold" style="margin-bottom:.5rem;">
      <span data-l="es">La Propuesta</span><span data-l="en">The Proposal</span>
    </div>
    <h2 style="font-size:clamp(1.5rem,4vw,2.5rem);margin-bottom:.75rem;">
      <span data-l="es">Construyamos juntos</span>
      <span data-l="en">Let's build together</span>
    </h2>
    <p style="font-size:.875rem;color:var(--text-s);margin-bottom:1.5rem;">
      <span data-l="es">{PROPUESTA_ES}</span>
      <span data-l="en">{PROPOSAL_EN}</span>
    </p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
      <a href="mailto:{EMAIL}" class="cta">
        <span data-l="es">Agendar reunión →</span>
        <span data-l="en">Schedule meeting →</span>
      </a>
      <button class="cta-outline" onclick="window.print()">
        <span data-l="es">Descargar PDF</span>
        <span data-l="en">Download PDF</span>
      </button>
    </div>
    <span class="slide-num">{N}</span>
  </div>
</div>
```

---

## Ghost Menu (End of Document)

```html
<!-- Always include at the bottom of every document -->
<div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid var(--divider);">
  <div class="t" style="margin-bottom:1rem;">
    <span data-l="es">¿Qué sigue?</span><span data-l="en">What's next?</span>
  </div>
  <div style="display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap;">
    <button class="cta-outline" onclick="toggleLang()">ES ↔ EN</button>
    <button class="cta-outline" onclick="window.print()">⎙ PDF</button>
    <button class="cta-outline" onclick="toggleTheme()">
      <span data-l="es">Modo claro</span><span data-l="en">Light mode</span>
    </button>
  </div>
</div>
```

---

## Complete JavaScript Block

```javascript
// Language toggle
function toggleLang() {
  const h = document.documentElement;
  h.lang = h.lang === 'es' ? 'en' : 'es';
  document.getElementById('lang-btn').textContent = h.lang === 'es' ? 'ES/EN' : 'EN/ES';
}

// Theme toggle
function toggleTheme() {
  document.body.classList.toggle('light');
  document.getElementById('theme-btn').textContent =
    document.body.classList.contains('light') ? '☀' : '☾';
}

// Modal open/close
function openModal(id) {
  document.getElementById(id).classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal(el) {
  el.classList.remove('open');
  document.body.style.overflow = '';
}
document.querySelectorAll('.modal-bg').forEach(m => {
  m.addEventListener('click', e => { if(e.target === m) closeModal(m); });
});
document.addEventListener('keydown', e => {
  if(e.key === 'Escape') document.querySelectorAll('.modal-bg.open').forEach(closeModal);
});

// Scroll reveal
const revealObserver = new IntersectionObserver(
  entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
);
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// Active sidebar link
const slideObserver = new IntersectionObserver(
  entries => entries.forEach(e => {
    const link = document.querySelector(`.jml-sidenav a[href="#${e.target.id}"] .dot`);
    if(link) link.style.background = e.isIntersecting ? 'var(--gold)' : 'var(--text-m)';
  }),
  { threshold: 0.5 }
);
document.querySelectorAll('.slide[id]').forEach(s => slideObserver.observe(s));
```
