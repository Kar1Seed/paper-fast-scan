---
name: paper-fast-scan
description: Parse a Web3/crypto whitepaper, technical documentation, or academic PDF into a bilingual (EN+CN) static HTML page with key terms highlighted, glossary sidebar, embedded figures, and architecture diagram. Use when the user wants to "quickly understand" a whitepaper, docs, or paper.
---

# Paper Fast Scan

Turn a whitepaper / technical documentation URL into a self-contained, bilingual static HTML page for rapid comprehension.

## Trigger Conditions

Use this skill when the user:
- Shares a whitepaper / documentation URL and asks to "understand it quickly"
- Provides a PDF file path (academic paper, arXiv paper) and wants it parsed
- Says "帮我解析这个白皮书" / "快速看懂这个文档" / "读一下这篇论文"
- Mentions "Paper-Fast-Scan" or asks to save this workflow
- Wants a bilingual (EN+CN) digest with diagrams

## Source Type Detection

**Web documentation** (URLs containing `gitbook.io`, `docs.`, `/documentation`):
→ Use Phase 1A (Web Fetch) workflow.

**Academic PDFs** (local `.pdf` files, arXiv links):
→ Use Phase 1B (PDF Parse) workflow. PDF papers get saved to `E:\中英对照论文\` with Chinese+English filename (e.g., `RAG综述-大语言模型的检索增强生成-RAG_Survey_LLM.html`).

## Language / Translation Rule

**The target translation language is the language the user is speaking.**

- User speaks Chinese → output EN + 中文对照 (current default)
- User speaks Japanese → output EN + 日本語
- User speaks Korean → output EN + 한국어
- User speaks English → skip translation, just explain in English with glossary

Always keep the **original English as the source column** and translate into whatever language the user used to invoke this skill. The sidebar glossary terms should also be explained in the user's language.

**Exception:** If the whitepaper itself is not in English (e.g., a Chinese whitepaper), swap: use the whitepaper's original language as the source, English as the translation.

## How Translation Works (Important)

Translation is done by the **LLM itself** — NOT by calling an external plugin or API (no Google Translate, no DeepL). The agent reads and comprehends the whitepaper, then rewrites it in the target language using its own understanding. This means:

- Translations are **semantic, not literal** — idioms and concepts are rephrased naturally
- Technical terms stay accurate because the LLM understands Web3 context
- Compound nouns (e.g., "threefold dilemma") get idiomatic treatment, not character-by-character mapping
- If a user asks "what plugin does the translation", explain it's LLM-native, not a separate tool

## Workflow

### Phase 1: Fetch Content

1. Use `execute_code` with Python `urllib` (through the local proxy if in mainland China: `http://127.0.0.1:7890`) to scrape the documentation pages.
2. For **GitBook** sites: the index page only shows TOC. To find the full URL tree, extract all `href` attributes matching the base path from the main page HTML: `re.findall(r'href="(/<base-path>/[^"]+)"', content)`. GitBook typically nests sub-pages under their parent section slug (e.g., `/3.-the-solution/3.1-data-makes-it-insightful`), NOT as flat siblings. If href extraction fails, search for `__NEXT_DATA__` JSON block which contains the full page tree.
3. Strip `<script>`, `<style>`, `<nav>`, `<header>`, `<footer>` tags. Convert remaining HTML to plain text with `re.sub(r'<[^>]+>', '\n', text)`.
4. Focus on: project motivation, architecture, core mechanics, tokenomics, roadmap.
5. Skip: API reference pages, rate limits, legal terms, onboarding steps unless the user specifically asks for them.

### Phase 1B: Parse PDF (Academic Papers)

For local PDF files (typically arXiv papers):

1. **Extract text & metadata** using `pymupdf` (imported as `fitz`):
   ```python
   import fitz
   pdf = fitz.open(r'path/to/paper.pdf')
   # Read first pages for title/abstract
   text = pdf[0].get_text()
   # Extract all images
   for page in pdf:
       for img in page.get_images(full=True):
           base = pdf.extract_image(img[0])
           # save base['image'] as PNG/JPEG
   ```

2. **⚠️ Critical**: `execute_code` sandbox does NOT have `pymupdf`. Must use `terminal` with the full Windows Python path:
   ```
   /c/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe -c "..."
   ```

3. **Install tools if missing** (one-time): `pip install pymupdf pdfplumber pillow`

4. **Extract figures**: PDF images are embedded per-page. Save them to `{paper_dir}/{arxiv_id}_assets/fig_p{NN}.{ext}`. Reference them in HTML as relative paths: `<img src="2312.10997v5_assets/fig_p01.png">`.

5. **LaTeX formula handling**: Academic PDFs often contain LaTeX formulas (e.g., `\frac{a}{b}`, `\mathcal{L}`). The raw text extraction won't render them. Either:
   - Keep the LaTeX source as-is in `<div class="formula-box">` for readers who know LaTeX
   - Describe the formula in natural language in the Chinese translation
   - Do NOT attempt to fabricate formula renderings

6. **Paper structure**: Academic papers have a standard structure (Abstract → Introduction → Methodology → Experiments → Conclusion). Map this to the HTML section hierarchy. Include the paper metadata in a header bar (title, authors, institution, arXiv ID, page count, figure count).

7. **Naming**: Save output as `{中文名}-{英文名}.html` in `E:\中英对照论文\`. example: `RAG综述-大语言模型的检索增强生成-RAG_Survey_LLM.html`

8. **Figure placement**: Embed figures in `<div class="figure-box">` with their original captions (translated). Place them between the relevant EN/CN blocks where they appear in the paper's flow.

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

### Phase 5: Package & Publish (if user wants to open-source)

When the user wants to publish the skill to GitHub:

1. **Add README.md** — Project intro, quick start, screenshot, supported platforms, template variables table, license note. See `references/packaging-checklist.md` for the full template.
2. **Add LICENSE** — MIT by default (user: Kar1Seed).
3. **Add screenshots** — User will provide. Copy to `examples/` directory. Update README image references.
4. **GitHub push**:
   ```bash
   cd <skill-dir>
   git init && git checkout -b main
   gh repo create <user>/<repo> --public --description "..."
   git remote add origin git@github.com:<user>/<repo>.git
   git add -A && git commit -m "Initial release: <Skill Name>"
   git push -u origin main
   ```
   ⚠️ **Pitfall**: `gh repo create --push` fails without existing commits. Always create the repo first, then commit, then push separately.
5. Verify the repo is public and README renders correctly at `https://github.com/<user>/<repo>`.

### Phase 6: Post-Delivery Skill Update

## HTML Template Reference

The full i18n-ready template is at `templates/page.html`. It uses `{{PLACEHOLDER}}` variables:

| Placeholder | Replaced with |
|-------------|---------------|
| `{{LANG_CODE}}` | Target language code (`zh`, `ja`, `ko`, `en`) |
| `{{PROJECT}}` | Project name |
| `{{SUBTITLE}}` | One-line description |
| `{{NAV_TITLE}}` | Navigation heading |
| `{{NAV_ITEMS}}` | `<a href="#sec1">...</a>` links |
| `{{CONTENT}}` | Main bilingual content |
| `{{GLOSSARY_TITLE}}` | Sidebar glossary heading |
| `{{GLOSSARY}}` | Glossary entries |
| `{{FORMULAS_TITLE}}` | Formula summary heading |
| `{{FORMULAS}}` | Formula blocks |
| `{{TABLE_DATA}}` | Optional data tables |
| `{{EXAMPLE_LABEL}}` | Label for worked examples |
| `{{DIAGRAM_TITLE}}` | Architecture diagram heading |
| `{{SVG_DIAGRAM}}` | SVG markup |

**I18N mechanism:** The template uses CSS custom properties (`--ui-source-label`, `--ui-target-label`) controlled by `data-lang` on `<html>`. The template ships with `zh`, `ja`, `ko`, and `en` language packs. The AI sets `data-lang` and fills placeholders in the matching language.

## Pitfalls

- **GitBook sites** return SPA shell HTML. The primary page only has TOC. To discover all page URLs: fetch the main page and extract with `re.findall(r'href="(/base-path/[^"]+)"', content)`. This yields the complete nested URL tree — GitBook sub-pages live under their parent slug (e.g., `/5.-parent/5.1-child`), NOT flat.
- **GitBook TOC bloat**: every sub-page embeds the full TOC as inline text. Your `skip_keywords` filter must be aggressive — exclude all section titles from every fetched page, not just the main one. The actual content always follows after the TOC entries.
- **Proxy required** for most Google/GitBook sites from mainland China. Use `http://127.0.0.1:7890` if available. Test without proxy first, fall back to proxy on SSL/connect errors.
- **Don't guess** formulas. Only include what's explicitly in the whitepaper. If a formula is unclear (LaTeX garbled by HTML scraping), flag it rather than fabricating.
- **SVG diagrams**: keep `viewBox` dimensions proportional. Use layers: top=users, middle=core product, bottom=infrastructure/external. Color-code: blue for users, purple for core product, green for chain infra, orange for bridges/vaults, grey for external chains.
- **File size**: Keep under 60KB. Don't inline fonts or images.
- **Desktop path** on the user's Windows machine is `C:\Users\Administrator\Desktop\`.
- **Paper storage path**: the user stores academic papers at `E:\中英对照论文\`. Output filenames MUST follow the pattern `{中文名}-{英文名}.html`. Extract the paper title from the PDF and create a concise Chinese+English name.
- **PDF tools**: `pymupdf`, `pdfplumber`, `pillow` are installed on the user's Windows Python (`/c/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe`). Do NOT try to import them in `execute_code` — use `terminal` with the full Python path.
- **PDF image extraction**: `pymupdf` extracts images per-page. The `extract_image(xref)` method returns a dict with `image` (bytes) and `ext` (format). Save to an `_assets/` subdirectory next to the HTML and reference with relative paths.
- **`gh repo create --push`** fails if the repo has zero commits. Always: (1) `gh repo create` without `--push`, (2) `git add -A && git commit`, (3) `git push -u origin main`. Do not combine into one command.

## Example Output

For SoDEX whitepaper (`https://sodex.com/documentation`), the output was:
- 7 major sections covering: motivation, architecture, ValueChain, Mirror Protocol, trading mechanics (fees, margin, leverage tiers, liquidations, mark price), SLP vault, SoPoints
- 17 glossary terms + 8 core formulas + leverage tier tables + liquidation flow diagram
- 5-layer SVG diagram: Users → SoDEX Core → ValueChain → Mirror Protocol → External chains + liquidation flow
- 803 lines, 47KB, self-contained HTML

For SoSoValue whitepaper (`https://sosovalue-white-paper.gitbook.io/sosovalue-whitepaper`), the output was:
- 6 major sections covering: 4-pillar overview, 3 market pain points, solution layers (Data/AI/Protocol/Infrastructure), market opportunity, SSI index protocol (4 products + 6 participants + methodology), SOSO tokenomics (distribution table + Lock-and-Release cross-chain)
- 16 glossary terms + 4 core formulas + 4-pillar quick-reference table + token allocation chart
- 5-layer SVG diagram: Users → Application Layer (Terminal/SSI/SoDEX/AI) → ValueChain → Cross-Chain → External + SOSO token flow bar
- 384 lines, 46KB, self-contained HTML

For Hyperliquid docs (`https://hyperliquid.gitbook.io/hyperliquid-docs`), the output was:
- 6 major sections covering: overview (L1 + order book DEX + HYPE buyback), technical architecture (HyperBFT / HyperCore 6 modules / HyperEVM Alpha), trading mechanics (CLOB / portfolio margin / multi-stage liquidation / funding), HYPE tokenomics (utility + $1B+/yr buyback + Builder Codes), ecosystem & governance (HIP 1-4 / validators / points & referrals), team & philosophy (Harvard/MIT · Citadel/HRT · self-funded · no VCs · no insiders)
- 15 glossary terms + 5 core formulas + HyperCore modules table + HIP proposals table + "Why Hyperliquid stands out" checklist
- 5-layer SVG diagram: Users → HyperCore+HyperEVM dual-engine → HyperBFT consensus → HYPE buyback flow → Validators/Governance/Builder Codes → External + bottom highlight bar
- Self-contained HTML with scroll-spy nav

For RAG Survey paper (`E:\2312.10997v5.pdf` — arXiv academic paper), the output was:
- 8 sections covering: Abstract, Introduction, RAG Overview (3 paradigms), Retrieval optimization, Generation techniques, Augmentation processes (3 stages), Evaluation (26 tasks, 50 datasets), Challenges & Future
- 13 glossary terms + RAG core flow formula + paradigm comparison table + paper metadata box
- 6 embedded original figures with bilingual captions
- 5-layer SVG diagram: Indexing → Retrieval → Generation → Augmentation (3 modes) → Paradigm evolution → Evaluation
- Self-contained HTML in `E:\中英对照论文\` with `_assets/` subdirectory for extracted images
