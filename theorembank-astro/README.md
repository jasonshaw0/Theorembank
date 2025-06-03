# Theorembank Astro Prototype

This directory contains a minimal Astro implementation of the Theorembank formula reference site.

## Prerequisites

* Node.js >= 18
* pnpm / npm / yarn (examples below use **npm**)

## Getting Started

**PowerShell/Windows:**
```powershell
cd theorembank-astro
npm install       # first-time only
npm run dev       # opens http://localhost:4321
```

**Bash/Unix:**
```bash
cd theorembank-astro && npm install && npm run dev
```

## Production Build

```bash
npm run build   # outputs static site to `dist/`
```

You can then deploy the contents of `dist/` to GitHub Pages, Netlify, Cloudflare Pages, etc.

## Structure Overview

```
theorembank-astro/
  astro.config.mjs      – Astro config
  package.json          – dependencies & scripts
  public/
    style.css           – basic layout styles
  src/
    layouts/
      BaseLayout.astro  – global HTML skeleton with sidebar nav
    pages/
      index.astro       – home page
      editor.astro      – live MathLive editor
```

The sidebar navigation currently uses plain HTML. In Phase 2, it will be generated from the formula content collection and include instant filtering.

The **Live Math Editor** page embeds [MathLive](https://github.com/arnog/mathlive) via CDN as a web component. It lets users type math and copy the LaTeX with a single click. 