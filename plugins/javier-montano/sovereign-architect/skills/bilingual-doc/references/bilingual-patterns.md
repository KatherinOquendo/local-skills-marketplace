# Bilingual Document Patterns

Reference for `bilingual-doc` skill. Full examples for complex scenarios.

---

## Complete Bilingual Slide

```html
<div class="slide" id="problem">
  <div style="max-width:44rem;">
    <div class="t gold" style="margin-bottom:.375rem;">
      <span data-l="es">El Problema</span>
      <span data-l="en">The Problem</span>
    </div>
    <h2 style="font-size:clamp(1.25rem,3vw,1.75rem);margin-bottom:.75rem;">
      <span data-l="es">La mayoría adopta IA como herramienta.<br>
        Los que ganan la usan como <span class="gold">palanca.</span></span>
      <span data-l="en">Most adopt AI as a tool.<br>
        Those who win use it as a <span class="gold">lever.</span></span>
    </h2>
    <div class="bridge">
      <span class="bridge-d">
        <span data-l="es">Dato:</span>
        <span data-l="en">Data:</span>
      </span>
      1,100M <span data-l="es">empleos transformados</span><span data-l="en">jobs transformed</span>
      <span class="src">WEF Davos 2026</span><br>
      <span class="bridge-i">
        <span data-l="es">Gap masivo de método, no de herramientas.</span>
        <span data-l="en">Massive method gap, not tool gap.</span>
      </span><br>
      <span class="bridge-a">
        <span data-l="es">Quien construya el método primero, captura el mercado.</span>
        <span data-l="en">Whoever builds the method first captures the market.</span>
      </span>
    </div>
    <span class="slide-num">3</span>
  </div>
</div>
```

---

## Bilingual Table

```html
<table>
  <thead>
    <tr>
      <th><span data-l="es">Métrica</span><span data-l="en">Metric</span></th>
      <th><span data-l="es">Valor</span><span data-l="en">Value</span></th>
      <th><span data-l="es">Fuente</span><span data-l="en">Source</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong><span data-l="es">Skills canónicos</span><span data-l="en">Canonical skills</span></strong></td>
      <td>557</td>
      <td><span class="src">JM Labs Registry</span></td>
    </tr>
    <tr>
      <td><strong><span data-l="es">Agentes activos</span><span data-l="en">Active agents</span></strong></td>
      <td>215</td>
      <td><span class="src">Plugin manifests</span></td>
    </tr>
  </tbody>
</table>
```

---

## Bilingual Modal

```html
<div class="modal-bg" id="m-concept" onclick="if(event.target===this)closeModal(this)">
  <div class="modal">
    <button class="modal-x" onclick="closeModal(this.closest('.modal-bg'))">&times;</button>
    <div class="modal-label" style="background:color-mix(in srgb,var(--gold) 12%,transparent);color:var(--gold);">
      <span data-l="es">Concepto</span>
      <span data-l="en">Concept</span>
    </div>
    <h3>
      <span data-l="es">Soberanía Digital</span>
      <span data-l="en">Digital Sovereignty</span>
    </h3>
    <p>
      <span data-l="es">Capacidad de operar con IA sin depender del consultor. Métrica: &gt;80% autonomía post-programa.</span>
      <span data-l="en">Ability to operate with AI without consultant dependency. Metric: &gt;80% autonomy post-program.</span>
    </p>
  </div>
</div>
```

---

## Bilingual List Items

```html
<ul style="font-size:.75rem;color:var(--text-s);line-height:1.8;padding-left:1.25rem;">
  <li>
    <strong style="color:var(--heading);">
      <span data-l="es">Método antes que tecnología</span>
      <span data-l="en">Method before technology</span>
    </strong>
    — <span data-l="es">Limpiar procesos primero, amplificar después.</span>
       <span data-l="en">Clean processes first, amplify after.</span>
  </li>
  <li>
    <strong style="color:var(--heading);">
      <span data-l="es">Caos + IA = Caos²</span>
      <span data-l="en">Chaos + AI = Chaos²</span>
    </strong>
    — <span data-l="es">Sin método, la IA amplifica el problema.</span>
       <span data-l="en">Without method, AI amplifies the problem.</span>
  </li>
</ul>
```

---

## Language Persistence (localStorage)

```javascript
// Mantener idioma entre sesiones
function toggleLang() {
  const h = document.documentElement;
  const newLang = h.lang === 'es' ? 'en' : 'es';
  h.lang = newLang;
  localStorage.setItem('jml-lang', newLang);
  document.getElementById('lang-btn').textContent = newLang === 'es' ? 'ES/EN' : 'EN/ES';
}

// Restaurar al cargar
(function() {
  const saved = localStorage.getItem('jml-lang');
  if(saved) document.documentElement.lang = saved;
})();
```

---

## Bilingual SEO Meta Tags

```html
<head>
  <!-- Primary language -->
  <meta property="og:locale" content="es_ES">
  <meta property="og:locale:alternate" content="en_US">

  <!-- Alternate links -->
  <link rel="alternate" hreflang="es" href="{CANONICAL_URL}">
  <link rel="alternate" hreflang="en" href="{CANONICAL_URL}?lang=en">
  <link rel="alternate" hreflang="x-default" href="{CANONICAL_URL}">

  <!-- Title and description (JS-updated) -->
  <title id="doc-title">JM Labs — Prospecto de Partnership</title>
  <meta name="description" id="doc-desc" content="El método para escalar con IA sin depender del consultor.">
</head>
<script>
  const META = {
    es: { title: 'JM Labs — Prospecto de Partnership', desc: 'El método para escalar con IA sin depender del consultor.' },
    en: { title: 'JM Labs — Partnership Prospectus', desc: 'The method to scale with AI without consultant dependency.' }
  };
  function toggleLang() {
    const h = document.documentElement;
    h.lang = h.lang === 'es' ? 'en' : 'es';
    document.getElementById('doc-title').textContent = META[h.lang].title;
    document.getElementById('doc-desc').content = META[h.lang].desc;
    document.title = META[h.lang].title;
  }
</script>
```

---

## Validation Script (Development)

```javascript
// Run in browser console to find unbilingual text nodes
function findUnbilingualText() {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    { acceptNode: n => n.textContent.trim().length > 3 ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT }
  );
  const issues = [];
  let node;
  while((node = walker.nextNode())) {
    const parent = node.parentElement;
    if(!parent.dataset.l && !parent.dataset.lb &&
       !['SCRIPT','STYLE','CODE','PRE'].includes(parent.tagName) &&
       !parent.closest('[data-l],[data-lb]')) {
      issues.push({ text: node.textContent.trim().slice(0,50), el: parent });
    }
  }
  console.table(issues);
  return issues;
}
findUnbilingualText();
```
