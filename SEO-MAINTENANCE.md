# SEO maintenance and handoff — Jin-in-Seoul

Last updated: 2026-10-14. Repository: `Jin-in-Seoul/Jin-in-Seoul` (`main`). Public site: https://jin-in-seoul.com/.

## Scope and non-negotiable rules

1. **Do not change literary prose, translations, paragraph breaks, intentional whitespace, typography, CSS, or the Sweater diary layout for SEO.** Restrict corrections to verified SEO metadata, sitemap, robots, redirects, or read-only audit tools.
2. Do not treat a successful GitHub Actions job as proof that all live URLs or Google/Naver indexing are correct.
3. Do not automatically apply audit warnings. Inspect the page, its Jekyll generation, language variants, and intended index policy first.
4. Re-fetch changed GitHub files after commits; check both the Pages deployment and the relevant audit report.
5. Preserve Naver site verification and existing analytics tags.

## Site configuration and SEO conventions

- GitHub Pages / Jekyll; `_config.yml` defines `url: https://jin-in-seoul.com` and Gray Note permalink `/gray-note/:year/:month/:day/:title/`.
- `robots.txt` allows crawling and references `https://jin-in-seoul.com/sitemap.xml`.
- `sitemap.xml` is a Jekyll-templated XML source with front matter. Do not assume raw Liquid placeholders are broken in deployed output.
- Gray Note pages may be generated from `_posts/*.md` and `gray-note/**/index.md`; absence of a matching `index.html` does not prove a broken URL.
- Canonical and hreflang should reference real, indexable language variants; `x-default` normally points to English where appropriate.
- Intentional `noindex` pages include full-view pages and redirect pages. Never add such URLs to the sitemap.
- Search page metadata warnings are optional improvements, not automatically errors.

## Changes already made (2026-10-14)

| Area | Change | Verification |
|---|---|---|
| Sitemap cleanup (phase 1) | Removed stale `/short-stories/books-rule/` entries, redirect entries, and a literal Liquid entry from source sitemap | Source re-fetched; deployed sitemap should still be checked |
| Redirects (phase 1) | Six language-part meta-refresh pages set to `noindex,follow` and canonicalized to language landing pages; removed redirect-page hreflang; fixed French HTML lang | Source re-fetched |
| Redirects (phase 3) | `sweater/index.html` and `a-dictionary-of-galactic-extinction/index.html` set to `noindex,follow`, canonicalized to English destination | Source re-fetched |
| Sitemap additions (phase 3) | Added 20 Korean dictionary entries (part 03: 1; part 04: 12; part 05: 7), removed the two root redirect URLs | 233 `<loc>` entries in source |
| Source audit | Added `scripts/audit_seo.py` and `.github/workflows/seo-audit.yml`; excluded Jekyll `_includes` and `_layouts` from standalone-page checks | 240 HTML pages; 233 sitemap entries; 0 ERROR, 1 WARN, 2 INFO on run 38583032725 |
| Live audit | Added `scripts/audit_seo_live.py` and `.github/workflows/seo-live-audit.yml`; reads deployed sitemap and tests published URLs | Verified on live run 38584877114: 233 sitemap URLs, 233 fetched HTTP 200, 0 ERROR, 1 WARN (search OG), 1 INFO (search JSON-LD) |

The remaining 1 WARN and 2 INFO from the source audit concerned optional metadata on `search/index.html`. Do not change search indexing policy without deciding it deliberately.

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
- Subsequent Pages deployment for live audit documentation: run `38583823275` completed successfully. Always check the newest relevant run.

## Remaining work for the next session

1. **Completed 2026-10-14:** Live audit run [38584877114](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38584877114), report artifact `11904801736`: sitemap HTTP 200, 233/233 HTML fetched, ERROR 0, WARN 1 (`/search/` OG), INFO 1 (`/search/` JSON-LD). These two optional search-page findings require no immediate edits.
2. On the next maintenance cycle, confirm `robots.txt` and intentionally unsitemapped redirect pages separately; the 233-URL audit covers only sitemap URLs.
3. Review real-world canonical/hreflang reciprocity and language codes. Separate actual problems from generated-page and intentional exceptions.
4. Check Google Search Console and Naver Search Advisor indexing/sitemap reports **only with authorized access**. A GitHub audit cannot substitute for search-engine account data.
5. After corrections, re-run source/live audits and verify Pages deployment; record exact commit SHAs and results here.

## Change log discipline

For each future SEO change, record date, changed files, reason, GitHub commit, source audit, live audit, and Pages deployment result. Keep this document current. Do not write unverified success claims.

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
- **Performance improvement is an optional follow-up**, especially the homepage image and render-blocking resources. Do not alter prose, CSS, or typography without explicit authorization and a visual regression plan.
