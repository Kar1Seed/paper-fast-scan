---
name: paper-fast-scan
description: Parse a Web3/crypto whitepaper or technical documentation into a bilingual (EN+CN) static HTML page with key terms highlighted, glossary sidebar, and architecture diagram. Use when the user wants to "quickly understand" a whitepaper or docs.
---

# Paper Fast Scan

Turn a whitepaper / technical documentation URL into a self-contained, bilingual static HTML page for rapid comprehension.

## Trigger Conditions

Use this skill when the user:
- Shares a whitepaper / documentation URL and asks to "understand it quickly"
- Says "帮我解析这个白皮书" / "快速看懂这个文档"
- Mentions "Paper-Fast-Scan" or asks to save this workflow
- Wants a bilingual (EN+CN) digest with diagrams

## Language / Translation Rule

**The target translation language is the language the user is speaking.**

- User speaks Chinese → output EN + 中文对照 (current default)
- User speaks Japanese → output EN + 日本語
- User speaks Korean → output EN + 한국어
- User speaks English → skip translation, just explain in English with glossary

Always keep the **original English as the source column** and translate into whatever language the user used to invoke this skill. The sidebar glossary terms should also be explained in the user's language.

**Exception:** If the whitepaper itself is not in English (e.g., a Chinese whitepaper), swap: use the whitepaper's original language as the source, English as the translation.

## Workflow

### Phase 1: Fetch Content

1. Use `execute_code` with Python `urllib` (through the local proxy if in mainland China: `http://127.0.0.1:7890`) to scrape the documentation pages.
2. For **GitBook** sites: the index page only shows TOC. Find the actual page URLs by pattern (e.g., `/about-sodex/how-sodex-works`). Fetch each key page individually.
3. Strip `<script>`, `<style>`, `<nav>`, `<header>`, `<footer>` tags. Convert remaining HTML to plain text with `re.sub(r'<[^>]+>', '\n', text)`.
4. Focus on: project motivation, architecture, core mechanics, tokenomics, roadmap.
5. Skip: API reference pages, rate limits, legal terms, onboarding steps unless the user specifically asks for them.

### Phase 2: Understand & Plan

Before writing HTML, internally map out:
- What problem does this project solve?
- How does it work (architecture)?
- What are the key Web3 concepts involved (e.g., AMM, order book, liquidation, cross-chain bridge)?
- What formulas / calculations are worth showing?
- What would a good architecture diagram look like?

### Phase 3: Write the HTML

Deliver a single self-contained `.html` file. Do NOT use markdown — the user opens this in a browser.

**Required sections:**
1. **Header** — Project name + subtitle
2. **Left nav** — Sticky table of contents with `scrollIntoView` smooth scrolling + scroll-spy active highlighting
3. **Main column** — Bilingual content: English block (dark background, "EN" label) → Chinese block (green left border, "中文" label). Key terms wrapped in `<span class="hl">` (yellow highlight).
4. **Right sidebar** — Glossary (term + definition), formula summary (monospace code blocks), tier/leverage tables, flow summaries
5. **Bottom SVG diagram** — Architecture overview showing layers: users → core product → infrastructure → external connections → key flows (liquidation, cross-chain, etc.)

**Design requirements:**
- Dark theme (GitHub-dark style: `--bg: #0d1117`, `--surface: #161b22`, `--text: #c9d1d9`)
- Yellow highlight for key terms: `--highlight: #f0c040`
- All CSS inline, no external dependencies
- Responsive: 3-column layout on wide screens, stacked on mobile
- SVG diagram: hand-crafted, no external libraries, using `<rect>`, `<text>`, `<line>`, `<linearGradient>`, `<marker>` for arrows

**Content guidelines:**
- Each major concept gets 1 EN block + 1 CN block
- Formulas go in `<div class="formula-box">` with monospace font
- Worked examples go in `<div class="example-box">` with green styling
- Keep Chinese natural — don't transliterate, rephrase in idiomatic Chinese
- Highlight core Web3 terminology: AMM, CLOB, DEX, CEX, liquidation, margin, collateral, mark price, appchain, MPC, TEE, etc.

**Glossary sidebar entries:**
- Term (yellow, bold) + one-sentence plain explanation
- Include ALL highlighted terms from the main text
- Group formulas under "核心公式汇总"
- Add relevant data tables (leverage tiers, fee structures, etc.)

### Phase 4: Iterate

After delivering the HTML, ask the user:
- Is the content accurate?
- Any sections need more detail?
- Diagram clear enough?
- Then offer to add navigation (if not already present) or enhance the diagram.

## HTML Template Reference

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PROJECT — 中英对照解读</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #c9d1d9; --text-dim: #8b949e;
  --highlight: #f0c040; --highlight-bg: rgba(240,192,64,0.15);
  --accent: #58a6ff; --accent-dim: rgba(88,166,255,0.12);
  --red: #f85149; --green: #3fb950; --purple: #a371f7; --orange: #d2991d;
}
/* Three-column layout: .nav (220px) | .main (flex) | .sidebar (380px) */
/* .en-block for English, .cn-block for Chinese, .hl for highlights */
/* .formula-box, .example-box, .glossary-item for sidebar */
</style>
</head>
<body>
<div class="header"><h1>🔬 PROJECT — 中英对照深度解读</h1></div>
<div class="container">
  <nav class="nav"><!-- Sticky TOC with IDs --></nav>
  <div class="main"><!-- Bilingual content --></div>
  <div class="sidebar"><!-- Glossary + formulas --></div>
</div>
<div class="diagram-section" id="diagram">
  <h2>🏗️ Architecture Overview</h2>
  <svg class="diagram" viewBox="0 0 1060 820">...</svg>
</div>
<script>/* Scroll spy + smooth scroll */</script>
</body>
</html>
```

## Pitfalls

- **GitBook sites** return SPA shell HTML. The primary page only has TOC — MUST fetch individual sub-pages.
- **Proxy required** for most Google/GitBook sites from mainland China. Use `http://127.0.0.1:7890` if available. Test without proxy first, fall back to proxy on SSL/connect errors.
- **Don't guess** formulas. Only include what's explicitly in the whitepaper. If a formula is unclear (LaTeX garbled by HTML scraping), flag it rather than fabricating.
- **SVG diagrams**: keep `viewBox` dimensions proportional. Use layers: top=users, middle=core product, bottom=infrastructure/external. Color-code: blue for users, purple for core product, green for chain infra, orange for bridges/vaults, grey for external chains.
- **File size**: Keep under 60KB. Don't inline fonts or images.
- **Desktop path** on the user's Windows machine is `C:\Users\Administrator\Desktop\`.

## Example Output

For SoDEX whitepaper (`https://sodex.com/documentation`), the output was:
- 7 major sections covering: motivation, architecture, ValueChain, Mirror Protocol, trading mechanics (fees, margin, leverage tiers, liquidations, mark price), SLP vault, SoPoints
- 17 glossary terms + 8 core formulas + leverage tier tables + liquidation flow diagram
- 5-layer SVG diagram: Users → SoDEX Core → ValueChain → Mirror Protocol → External chains + liquidation flow
- 803 lines, 47KB, self-contained HTML
