# CSS maintenance — Jin-in-Seoul

Architecture checked: 2026-11-27 (eight CSS files). Historical cache-version examples below were recorded on 2026-10-14; this document does not authorize restyling.

## Preservation and change-control principles

1. **All existing `sweater/` files and diary typography are protected** (bold dates, spacing above/below dates, deliberate line breaks, paragraph formatting). Global CSS changes that could indirectly affect Sweater are excluded.
2. All literary text, paragraph boundaries, headings, intentional blank lines and inline markup are preserved.
3. Single-work or language adjustments use scoped stylesheets where appropriate and do not justify changes to `assets/style.css` alone.
4. Korean/Japanese prose retains first-line indentation (normally `1em`), including the opening paragraph. For English/French, opening narrative paragraphs are flush left, later ordinary paragraphs retain `1em`. Indiscriminate removal of paragraph indentation is excluded.
5. Section-number formatting is preserved. In short stories, `<p class="section-number">N</p>` is unindented. Japanese `the-basics-of-logic` uses this markup for sections 1–5.
6. Repository-wide CSS cache-key changes require a verified reason and full affected-page audit. Different `?v=` values are cache keys, not different source CSS files.
7. Stylesheet changes require prior inspection of selectors and HTML and post-commit retrieval of every changed file.

## Stylesheet ownership (8 CSS files)

| File | Purpose | Change impact |
| --- | --- | --- |
| `assets/style.css` | Site-wide typography, navigation, headings, body, and work-specific baseline rules | **Global; high risk**, including Sweater |
| `a-dictionary-of-galactic-extinction/ko/entry-common.css` | Korean dictionary chapter layout | Korean dictionary chapters |
| `a-dictionary-of-galactic-extinction/en/entry-common.css` | English dictionary chapter layout and opening paragraphs | English dictionary chapters |
| `a-dictionary-of-galactic-extinction/fr/entry-common.css` | French dictionary chapter layout and opening paragraphs | French dictionary chapters |
| `a-dictionary-of-galactic-extinction/ja/entry-common.css` | Japanese dictionary chapter layout; preserve first-line indent | Japanese dictionary chapters |
| `short-stories/latin-first-paragraph.css` | English/French short-story opening paragraph and first paragraph after section number | Only linked English/French story pages |
| `childrens-books/latin-first-paragraph.css` | English/French children's-book opening paragraph and first paragraph after `h2` | Only linked English/French children's-book pages |
| `scarecrow-distance/latin-first-paragraph.css` | English/French Scarecrow Distance opening paragraph for each chapter | Only linked English/French chapters 1–4 |

- Stylesheet loading order: the global CSS is linked first; the work-specific CSS is linked afterward. Latin-specific stylesheets are not applied to Korean/Japanese pages.

## Historical cache-version examples (2026-10-14; not a current inventory)

- Homepage: `assets/style.css?v=088`
- Short-story index: `assets/style.css?v=046`
- Children's-book index: `assets/style.css?v=049`
- Dictionary entry samples: `assets/style.css?v=051`, language-specific CSS `?v=001`
- Children's-book story samples: `assets/style.css?v=053`, Latin-specific CSS `?v=001`
- Sweater English chapter sample: `assets/style.css?v=052`

- These all point to the **same** `assets/style.css` resource. **Mass replacement of versions is excluded**: a version bump forces cache refresh and should be coupled to a justified change. The audit script `scripts/audit_css_links.py` produces a complete inventory without modifying pages.

## New page / edit checklist

1. The work, language, precise HTML pages and potentially affected pages are identified and recorded.
2. Prior review of `assets/style.css` and existing work-specific CSS is required.
3. Established scoped CSS takes precedence over new inline style blocks.
4. English/French Scarecrow Distance chapters 1–4 link `../../latin-first-paragraph.css?v=001` from `scarecrow-distance/<lang>/chapter-XX/index.html`; Korean/Japanese chapters remain unchanged. English/French short stories link `../../latin-first-paragraph.css?v=001` from `short-stories/<slug>/<lang>/index.html`. English/French children's books use the equivalent path under `childrens-books/`.
5. Dictionary entries use the matching language's `entry-common.css`. Special all-view and chapter-level formatting is preserved.
6. Verification covers the absence of Latin-only CSS links on Korean/Japanese pages and the `section-number` and `h2` structure.
7. Verification includes execution of `python3 scripts/audit_css_links.py` from the repository root, review of warnings and comparison of affected-page counts before and after.
8. Verification establishes that changed HTML differs **only** in the intended stylesheet link or agreed markup; changed files are retrieved from GitHub after commit.
9. Sweater is excluded from bulk transformations; global CSS modifications require separate explicit approval and a regression plan.

## Conflict / duplication notes

- The global stylesheet intentionally has distinct selectors for `.galactic-prose`, `.short-story-prose`, `.children-prose`, `.sweater-prose`, etc. Similar declarations across those classes are not automatically redundant: they separate work-level formatting and protect specialized content. The scoped Latin rules intentionally override only `text-indent`. Similarity alone does not justify merging or deleting these rules.

## Maintenance decisions

- The eight existing CSS files are retained without forced consolidation.
- Current cache query strings are retained until a global CSS release requires cache invalidation.
- Read-only inventory and targeted tests precede changes; deletion of selectors requires demonstrated non-use.
- Mobile/visual verification is managed by the site owner.
