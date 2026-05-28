# Changelog

## v2.1 — 2026-05-29

### Fixed
- **QLoRA paper incomplete**: Previous version only covered ~3 of 26 pages. Rewritten to full depth with all 7 sections, Elo ratings table, ablation studies, and KaTeX-rendered formulas.
- Bug identified: papers in batch mode may skip sections if the LLM condenses content. Added scanning step to verify nav-section alignment.

### Added
- **KaTeX math rendering** to `paper.html` template via CDN (katex 0.16.11)
  - `$$display$$` and `$inline$` math delimiters
  - Dark theme CSS overrides for KaTeX elements
  - Auto-render on page load
- `examples/qlora-efficient-finetuning.html` — full 26-page paper conversion with KaTeX formulas
- Section-missing detection script in SKILL.md workflow

### Changed
- Updated `templates/paper.html` with KaTeX CDN links and dark theme CSS
- Updated `README.md` with new QLoRA example
- Updated `SKILL.md` with Phase 4 verification step

## v2.0 — 2026-05-23

### Added
- PDF paper parsing via pymupdf (text + figure extraction)
- `paper.html` template for academic papers
- `install.py` one-click setup script
- `requirements.txt`
- 3 new examples (SoSoValue, Hyperliquid, RAG Survey)
- 16-paper batch conversion pipeline

## v1.0 — 2026-05-15

### Added
- Initial release
- GitBook/ReadTheDocs web doc parsing
- `page.html` template for web whitepapers
- Bilingual EN+CN translation
- Scroll-spy navigation, glossary sidebar, SVG diagrams
- 1 example (SoDEX)
