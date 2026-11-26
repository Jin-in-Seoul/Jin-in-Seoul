# CSS maintenance — Jin-in-Seoul

Last reviewed: 2026-10-14. This document describes the **current** architecture; it does not authorize restyling.

## Preservation and change-control principles

1. **All existing `sweater/` files and diary typography are protected** (bold dates, spacing above/below dates, deliberate line breaks, paragraph formatting). Global CSS changes that could indirectly affect Sweater are excluded.
2. Preserve all literary text, paragraph boundaries, headings, intentional blank lines and inline markup.
3. Single-work or language adjustments use scoped stylesheets where appropriate and do not justify changes to `assets/style.css` alone.
4. For Korean/Japanese prose, retain first-line indentation (normally `1em`), including the opening paragraph. For English/French, opening narrative paragraphs are flush left, later ordinary paragraphs retain `1em`. The policy prohibits indiscriminately remove indentation from every paragraph.
5. Preserve section-number formatting. In short stories, `<p class="section-number">N</p>` is unindented. Japanese `the-basics-of-logic` uses this markup for sections 1–5.
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

Stylesheet loading order: the global CSS is linked first; the work-specific CSS is linked afterward. Latin-specific stylesheets are not applied to Korean/Japanese pages.

## Current cache-version inventory (examples, not a complete repository-wide audit)

- Homepage: `assets/style.css?v=088`
- Short-story index: `assets/style.css?v=046`
- Children's-book index: `assets/style.css?v=049`
- Dictionary entry samples: `assets/style.css?v=051`, language-specific CSS `?v=001`
- Children's-book story samples: `assets/style.css?v=053`, Latin-specific CSS `?v=001`
- Sweater English chapter sample: `assets/style.css?v=052`

These all point to the **same** `assets/style.css` resource. **Mass replacement of versions is excluded**: a version bump forces cache refresh and should be coupled to a justified change. The audit script `scripts/audit_css_links.py` produces a complete inventory without modifying pages.

## New page / edit checklist

1. Identify work, language, and the precise HTML page(s); record all potentially affected pages.
2. Read `assets/style.css` and any existing work-specific CSS before editing.
3. Reuse the established scoped CSS rather than inserting inline style blocks.
4. For English/French Scarecrow Distance chapters 1–4, link `../../latin-first-paragraph.css?v=001` from `scarecrow-distance/<lang>/chapter-XX/index.html`; leave Korean/Japanese chapters unchanged. For English/French short stories link `../../latin-first-paragraph.css?v=001` from `short-stories/<slug>/<lang>/index.html`. For English/French children's books use the equivalent path under `childrens-books/`.
5. For dictionary entries use the matching language's `entry-common.css`. Preserve special all-view and chapter-level formatting.
6. Confirm that Korean/Japanese are not linked to Latin-only CSS; check `section-number` and `h2` structure.
7. Run `python3 scripts/audit_css_links.py` from repository root and review warnings; compare affected-page counts before and after.
8. Verify that changed HTML differs **only** in the intended stylesheet link or agreed markup, and re-fetch changed files from GitHub after commit.
9. Sweater is excluded from bulk transformations; global CSS modifications require separate explicit approval and a regression plan.

## Conflict / duplication notes

The global stylesheet intentionally has distinct selectors for `.galactic-prose`, `.short-story-prose`, `.children-prose`, `.sweater-prose`, etc. Similar declarations across those classes are not automatically redundant: they separate work-level formatting and protect specialized content. The scoped Latin rules intentionally override only `text-indent`. Similarity alone does not justify merging or deleting these rules.

## Maintenance decisions

- Keep the eight existing CSS files; no forced consolidation.
- Preserve all current cache query strings until an actual global CSS release requires cache invalidation.
- Run read-only inventory and targeted tests first; defer deleting selectors without demonstrated non-use.
- Mobile/visual verification is managed by the site owner.
