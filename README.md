# Paper Fast Scan v2

> Turn Web3 whitepapers, technical docs, and academic PDFs into bilingual static HTML pages — in minutes.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

---

## What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| Web whitepapers (GitBook, ReadTheDocs) | ✅ | ✅ |
| **Academic PDF papers** (arXiv, local PDFs) | ❌ | ✅ |
| **Figure extraction** (embedded images) | ❌ | ✅ |
| **LaTeX formula handling** | ❌ | ✅ |
| **Paper metadata header** (authors, arXiv ID) | ❌ | ✅ |
| Two HTML templates | 1 (page.html) | 2 (+ paper.html) |
| One-click install script | ❌ | ✅ `python scripts/install.py` |

## What This Does

This is a **[Hermes Agent](https://github.com/nousresearch/hermes-agent) skill** that takes any technical document and generates a **self-contained bilingual HTML page** with:

- 📖 **Bilingual content** — Original + your-language translation
- 🟡 **Term highlighting** — Key concepts in yellow
- 📑 **Scroll-spy navigation** — Sticky TOC with smooth scrolling
- 📚 **Glossary sidebar** — Every technical term explained
- 🧮 **Formula summary** — All math extracted with examples
- 🖼️ **Embedded figures** — Original images from PDFs with bilingual captions
- 🏗️ **SVG architecture diagram** — Auto-generated overview
- 🌙 **Dark theme** — GitHub-dark, responsive, no dependencies

## Quick Install

```bash
# 1. Install Python dependencies
python scripts/install.py

# 2. Copy the skill to your Hermes skills directory
#    (or let your Hermes Agent point to this directory)
cp -r paper-fast-scan ~/.hermes/skills/research/

# 3. Just ask your Hermes Agent:
"用 Paper-Fast-Scan 解析 https://sodex.com/documentation"
"读一下这篇论文 E:/2312.10997v5.pdf"
```

## Supported Inputs

| Source | Examples |
|--------|----------|
| **GitBook** | SoDEX, SoSoValue, Hyperliquid docs |
| **ReadTheDocs / Docusaurus** | Any `/docs/` site with sidebar nav |
| **arXiv PDF** | `E:/2312.10997v5.pdf` (auto-extracts title, figures, formula) |
| **Local PDF** | Any `.pdf` file with `pymupdf` access |
| **Plain Markdown** | Any `.md` file or URL |

## Examples

Open these in your browser to see the output:

| Example | Type | Source |
|---------|------|--------|
| `examples/sodex-whitepaper.html` | Web DEX whitepaper | sodex.com/documentation |
| `examples/sosovalue-whitepaper.html` | Web platform whitepaper | sosovalue.gitbook.io |
| `examples/hyperliquid-whitepaper.html` | Web L1 docs | hyperliquid.gitbook.io |
| `examples/rag-survey.html` | Academic PDF paper | arXiv 2312.10997v5 |
| `examples/qlora-efficient-finetuning.html` | Academic PDF paper (KaTeX math) | arXiv 2305.14314 |

## File Structure

```
paper-fast-scan/
├── README.md                        ← You are here
├── LICENSE                          ← MIT
├── requirements.txt                 ← pip dependencies
├── SKILL.md                         ← Full agent workflow
├── templates/
│   ├── page.html                    ← Web whitepaper template
│   └── paper.html                   ← Academic paper template (v2)
├── scripts/
│   └── install.py                   ← One-click install
└── examples/
    ├── sodex-whitepaper.html        ← DEX whitepaper example
    ├── sosovalue-whitepaper.html    ← Platform whitepaper example
    ├── hyperliquid-whitepaper.html  ← L1 docs example
    └── rag-survey.html              ← Academic paper example (v2)
```

## Template Variables

Both templates use `{{PLACEHOLDER}}` variables. The AI fills them in.

**Shared (both templates):**
`{{LANG_CODE}}` `{{NAV_ITEMS}}` `{{CONTENT}}` `{{GLOSSARY}}` `{{FORMULAS}}` `{{TABLE_DATA}}` `{{SVG_DIAGRAM}}`

**page.html (web whitepapers):**
`{{PROJECT}}` `{{SUBTITLE}}` `{{NAV_TITLE}}` `{{GLOSSARY_TITLE}}` `{{FORMULAS_TITLE}}` `{{EXAMPLE_LABEL}}` `{{DIAGRAM_TITLE}}`

**paper.html (academic papers):**
`{{PAPER_TITLE}}` `{{PAPER_AUTHORS}}` `{{PAPER_META}}` `{{PAPER_ABSTRACT_EN}}` `{{PAPER_ABSTRACT_CN}}` `{{REFERENCES}}` `{{DIAGRAM_TITLE}}`

## Language Auto-Detection

The target translation language is auto-detected from your message:

| You write in... | Output |
|-----------------|--------|
| Chinese | EN + 中文 |
| Japanese | EN + 日本語 |
| Korean | EN + 한국어 |
| English | English-only digest |

## How Translation Works

Translation is done by the **LLM itself** — not Google Translate or DeepL. The AI reads, comprehends, and rewrites in the target language using its own understanding. This means translations are semantic, idiomatic, and technically accurate for Web3/academic terminology.

## Dependencies

- **Python 3.10+** — for `pymupdf`, `pdfplumber`, `pillow`
- **Hermes Agent** — to run the skill

## License

MIT — see [LICENSE](LICENSE).
