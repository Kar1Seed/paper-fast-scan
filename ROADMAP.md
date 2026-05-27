# Paper Fast Scan — Roadmap

> See `docs/architecture-roadmap.html` for the visual architecture diagram.

## v2.0 ✅ Current

- [x] GitBook / ReadTheDocs / Docusaurus web docs parsing
- [x] PDF paper parsing (pymupdf — text + figure extraction)
- [x] LaTeX formula detection and preservation
- [x] Dual HTML templates: `page.html` (web) + `paper.html` (academic)
- [x] Bilingual (EN+CN) with auto-detect target language
- [x] Term highlighting, glossary sidebar, formula boxes
- [x] SVG architecture diagrams
- [x] Scroll-spy navigation with smooth scrolling
- [x] MIT licensed, public GitHub repo
- [x] 4 example outputs (SoDEX, SoSoValue, Hyperliquid, RAG Survey)

---

## v2.1 🚧 In Progress

- [ ] **Glossary cross-referencing & hover tooltips**
  - Hover over any highlighted term → floating card with definition
  - Click glossary sidebar item → scroll to first occurrence in main text
  - Bidirectional linking between content and sidebar

- [ ] **Multi-Agent architecture design**
  - Master Agent: task decomposition & orchestration
  - Translation Agent: EN→CN semantic translation
  - Diagram Agent: figure OCR & SVG vectorization
  - Review Agent: translation quality & terminology consistency check
  - Hermes `delegate_task` for parallel agent execution

- [ ] **One-click install script** (`scripts/install.py`)
  - Auto-install pymupdf, pdfplumber, pillow
  - Verify installation
  - Cross-platform (Windows/macOS/Linux)

- [ ] **Example library expansion** (≥5 papers)
  - DeFi protocols, zero-knowledge proofs, consensus algorithms
  - Screenshots for README

---

## v2.2 Glossary Knowledge Base

- [ ] **Persistent Glossary DB** (SQLite)
  - Cache term definitions across papers
  - Reuse explanations — avoid re-explaining "AMM" in every paper
  - Standardize translations for common Web3 terms

- [ ] **Interactive HTML features**
  - Collapsible sections (expand/collapse) — default: core sections expanded
  - Dark/Light theme toggle with preference memory

- [ ] **Glossary hover cards**
  - Rich tooltips: definition + first seen + related terms
  - Works across all highlighted terms in main content

---

## v2.3 Author & Source Ecosystem

- [ ] **Author Database**
  - Auto-fetch from arXiv API (name, institution, paper list)
  - Author co-authorship network graph (SVG)
  - Click author name → filtered paper list

- [ ] **New document sources**
  - Notion page API integration
  - Obsidian vault (`*.md` files with `[[wiki-links]]`)
  - Substack / Mirror.xyz blog posts

- [ ] **Format registry** (plugin-style)
  - Register new input formats without modifying core code
  - `registry.register('notion', NotionParser)`
  - Community-contributed parsers

---

## v2.5 Multi-Agent & Structured Output

- [ ] **Multi-Agent pipeline goes live**
  - Hermes `delegate_task` with 3 parallel sub-agents
  - Translation + Diagram + Review → Merge → Final HTML
  - Configurable agent selection per task type

- [ ] **Structured extraction**
  - PDF tables → HTML `<table>` (not just text)
  - Citation extraction → clickable links (DOI / arXiv)
  - Formula rendering with unicode/HTML entities

- [ ] **Export format expansion**
  - PDF print-ready version
  - EPUB e-book
  - JSON structured data (for programmatic use)
  - Obsidian Markdown with `[[wiki-links]]`

---

## v3.0 Knowledge Graph & Ecosystem

- [ ] **Cross-paper knowledge graph**
  - Citation chain visualization (d3.js / vis.js)
  - Topic clustering across papers
  - Research timeline view

- [ ] **Community template marketplace**
  - User-contributed HTML templates
  - Voting and ranking
  - One-click apply

- [ ] **New input modalities**
  - Video/podcast → Whisper transcription → structured summary
  - Scanned documents → OCR pipeline

- [ ] **Obsidian bidirectional link export**
  - Generated terms/authors/papers auto-linked with `[[wikilink]]`
  - Seamless integration with personal knowledge base

---

## Priority Legend

| Tag | Meaning |
|-----|---------|
| P0 | Must-have, core value |
| P1 | High impact, do soon |
| P2 | Nice to have, long tail |
