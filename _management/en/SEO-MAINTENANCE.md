# SEO maintenance policy — Jin-in-Seoul

Last updated: 2026-11-27. Repository: `Jin-in-Seoul/Jin-in-Seoul` (`main`). Public site: https://jin-in-seoul.com/.

## Scope and non-negotiable rules

1. **Literary prose, translations, paragraph breaks, intentional whitespace, typography, CSS and the Sweater diary layout are protected during SEO maintenance.** Corrections are restricted to verified SEO metadata, sitemap, robots, redirects or read-only audit tools.
2. A successful GitHub Actions job does not establish validity of all live URLs or Google/Naver indexing.
3. Audit warnings do not automatically authorize changes. Review of the page, its Jekyll generation, language variants and intended index policy precedes corrections.
4. Verification includes post-commit retrieval of changed GitHub files, Pages deployment and the relevant audit report.
5. Naver site verification and existing analytics tags are preserved.

## Site configuration and SEO conventions

- GitHub Pages / Jekyll; `_config.yml` defines `url: https://jin-in-seoul.com` and Gray Note numbered HTML pages (`/gray-note/001/{lang}/`, `/gray-note/002/`).
- `robots.txt` allows crawling and references `https://jin-in-seoul.com/sitemap.xml`.
- `sitemap.xml` is a Jekyll-templated XML source with front matter. Raw Liquid placeholders alone do not establish an error in deployed output.
- Gray Note uses standalone HTML under numbered folders: `gray-note/001/{lang}/index.html` and `gray-note/002/index.html`. There are no Gray Note posts in `_posts`.
- Canonical and hreflang should reference real, indexable language variants; `x-default` normally points to English where appropriate.
- Intentional `noindex` pages include full-view pages and redirect pages. Such URLs are excluded from the sitemap.
- Search page metadata warnings are optional improvements, not automatically errors.

## Technical change history (2026-10-14)

| Area | Change | Verification |
|---|---|---|
| Sitemap cleanup (phase 1) | Removed stale `/short-stories/books-rule/` entries, redirect entries, and a literal Liquid entry from source sitemap | Source re-fetched; deployed sitemap should still be checked |
| Redirects (phase 1) | Six language-part meta-refresh pages set to `noindex,follow` and canonicalized to language landing pages; removed redirect-page hreflang; fixed French HTML lang | Source re-fetched |
| Redirects (phase 3) | `sweater/index.html` and `a-dictionary-of-galactic-extinction/index.html` set to `noindex,follow`, canonicalized to English destination | Source re-fetched |
| Sitemap additions (phase 3) | Added 20 Korean dictionary entries (part 03: 1; part 04: 12; part 05: 7), removed the two root redirect URLs | 233 `<loc>` entries in source |
| Source audit | Added `scripts/audit_seo.py` and `.github/workflows/seo-audit.yml`; excluded Jekyll `_includes` and `_layouts` from standalone-page checks | 240 HTML pages; 233 sitemap entries; 0 ERROR, 1 WARN, 2 INFO on run 38583032725 |
| Live audit | Added `scripts/audit_seo_live.py` and `.github/workflows/seo-live-audit.yml`; reads deployed sitemap and tests published URLs | Verified on live run 38584877114: 233 sitemap URLs, 233 fetched HTTP 200, 0 ERROR, 1 WARN (search OG), 1 INFO (search JSON-LD) |

The remaining 1 WARN and 2 INFO from the source audit concerned optional metadata on `search/index.html`. Changes to search indexing policy require a deliberate decision.

## Automated checks and reports

### Source SEO audit
- Run: `python3 scripts/audit_seo.py` from repository root.
- Workflow: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-audit.yml
- Report artifact: `seo-audit-report` containing `seo-audit-report.md`.
- Known successful source run: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38583032725
- Checks raw repository HTML, not fully rendered Jekyll output; source warnings may be false positives.

### Published-site SEO audit
- Run: `python3 scripts/audit_seo_live.py` from a network-enabled environment.
- Workflow: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-live-audit.yml
- Report artifact: `seo-live-report` containing `seo-live-report.md`.
- Triggered by audit script/workflow pushes, after successful Pages deployment, or by manual dispatch. Initial push-triggered verification succeeded on run 38584877114.
- Checks the live sitemap, URL responses, metadata, and hreflang reciprocity among sitemap URLs.
- The live checker is read-only. It does not establish actual Google/Naver indexing, nor does it prove that unsitemapped URLs work.

### Deployment
- GitHub Pages workflow: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions
- Successful Pages deployment for the phase-3 SEO changes: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38583033007
- Subsequent Pages deployment for live audit documentation: run `38583823275` completed successfully. Verification is based on the newest relevant run.

## Periodic maintenance and verification

1. **Completed 2026-10-14:** Live audit run [38584877114](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38584877114), report artifact `11904801736`: sitemap HTTP 200, 233/233 HTML fetched, ERROR 0, WARN 1 (`/search/` OG), INFO 1 (`/search/` JSON-LD). These two optional search-page findings require no immediate edits.
2. Periodic verification covers `robots.txt` and intentionally unsitemapped redirect pages separately. The 233-URL figures above refer to the 14 October 2026 audit, not the current sitemap size. On 27 November 2026, the latest `sitemap.xml` source contains 315 `<loc>` entries; this source count is not a fresh live-URL audit.
3. Verification covers deployed canonical/hreflang reciprocity and language codes, distinguishing actual problems from generated-page and intentional exceptions.
4. Google Search Console and Naver Search Advisor indexing/sitemap reports are reviewed **only with authorized access**. A GitHub audit cannot substitute for search-engine account data.
5. Corrections are followed by source/live audits and Pages deployment verification, with exact commit SHAs and results recorded.

## Change log discipline

- Each SEO change record includes the date, changed files, reason, GitHub commit, source audit, live audit and Pages deployment result. This document is maintained as a current reference; unverified success claims are excluded.

Related documentation: [README.md](README.md) · [CSS-MAINTENANCE.md](CSS-MAINTENANCE.md).

## Site quality verification (2026-10-14)

Read-only site quality workflow: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38585658888
- `scripts/audit_site_quality.py` + `.github/workflows/site-quality-audit.yml`
- Published sitemap pages fetched: **233/233**; distinct internal link targets **254**, assets **35**.
- **ERROR 0, WARN 0, INFO 5**. Three heading-level skips (children's books, music, short stories), one search button accessible-name review, and one homepage figure PNG approximately 1.22 MB. No broken internal targets or missing assets found.
- This is static HTML/HTTP inspection, not a full interactive accessibility or device test.

Mobile Lighthouse workflow: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38585718512
- `.github/workflows/browser-quality-audit.yml` uses headless Chrome and Lighthouse on three representative published pages.
- Homepage: performance **68**, accessibility **100**, best practices **100**; FCP 3.8s, LCP 4.6s, CLS 0.
- Sweater English landing page: performance **91**, accessibility **100**, best practices **100**; FCP/LCP 2.1s, CLS 0.
- Dictionary Korean part-05 entry-07: performance **59**, accessibility **100**, best practices **100**; FCP 6.0s, LCP 7.0s, CLS 0.
- Scores are a one-run mobile simulation, not real-user Core Web Vitals or proof of flawless visual layout across phones.
- **Performance improvement is an optional follow-up**, especially the homepage image and render-blocking resources. Changes to prose, CSS or typography require explicit authorization and a visual regression plan.

## Structured-data attribution normalization (2026-11-26)

- **Approved public identity:** Jin-in-Seoul is a pen name for published creative work. Schema.org JSON-LD attribution of the site's original works and eligible translation/publishing credits uses `{"@type":"Person","name":"Jin-in-Seoul","url":"https://jin-in-seoul.com/"}`. This is a public pen name, **not a disclosure of a legal name** and not a claim of a registered organization. A change from `Person` to `Organization` requires new authorization.

- Original works (novels, entries, short stories, children's books, Gray Note essays, haiku, music): the existing `author` or other applicable credit retains the same public pen-name identity. The `translator` property is not added indiscriminately to every language edition.
- Anonymous classical source `The Tale of Jeon Unchi` (`tales-from-premodern-korea/jeon-unchi/ko/index.html` and `en/index.html`): retains `"author":"Anonymous"` and `translator` as `Person / Jin-in-Seoul`, including the modern Korean edition's existing credit. The description of the edition's modern-language rendering should remain in its published explanatory text.
- Content `@type` classifications are preserved, including `Book`, `Article`, `CreativeWork`, `MusicRecording`, `CollectionPage`, and `WebSite`; attribution normalization alone does not justify changes to prose, translations, layout, canonical URLs, hreflang, sitemap or analytics.

**Work and verification history:**

1. An earlier one-time normalization to unclassified attribution created commit [db303d77e](https://github.com/Jin-in-Seoul/Jin-in-Seoul/commit/db303d77e5a56252f1b5b792f0d9c270b6cf6ed6); it was **superseded** by the approved `Person` attribution policy.
2. The final one-time workflow `restore-pen-name-person-once.yml` succeeded ([run 45641099753](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/45641099753)). Its log reports **306 modified HTML files**, **303 author credits**, **2 translator credits**, **1 publisher credit**, and **0 parse failures**. The resulting content commit is [7c57cad976](https://github.com/Jin-in-Seoul/Jin-in-Seoul/commit/7c57cad97685db425f3a605922b3b6aa44be1dec).
3. GitHub Pages completed successfully for this content commit ([run 45641135130](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/45641135130)). Representative source files were re-read: homepage, dictionary landing/entry, Sweater, short stories, children's books, Gray Note, haiku, music and the two Jeon Unchi editions.
4. The Gray Note Liquid layout `_layouts/gray-note-post.html` was updated along with standalone pages. A source audit's JSON parsing of a Liquid template is not equivalent to parsing deployed HTML; site-wide JSON-LD audits require separate validation of rendered output.
5. **Completed:** The one-time workflow was removed in [commit 90aff30c](https://github.com/Jin-in-Seoul/Jin-in-Seoul/commit/90aff30c7d33c26537655c7692774988aae3c131). GitHub Pages deployment for that commit succeeded. The temporary workflow is no longer present on `main`.

- **Audit scope:** The workflow verified that changes were confined to JSON-LD scripts and reported no JSON parse failures in its covered files. This does not itself establish comprehensive live HTML validation or actual Google/Naver indexing. Those claims require deployed-site SEO audits and authorized Search Console access, as applicable. Anonymous original-author attribution and the public pen name remain protected.
