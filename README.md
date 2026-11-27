# Jin-in-Seoul

A multilingual archive of fiction.

https://jin-in-seoul.com

## Site operation and maintenance

- [ABC — Site operation and maintenance regulations](ABC.md)

## Premodern Korean fiction translation

- [Translation and editing principles for premodern Korean fiction](PREMODERN-KOREAN-FICTION-TRANSLATION-GUIDE.md) — English and Korean; thirteen principles, practical translation standards, and shared English terminology.

- [Work-specific translation guide — The Tale of Jeon Unchi](JEON-UNCHI-TRANSLATION-GUIDE.md)
- [Work-specific translation guide — The Tale of Master Rabbit](MASTER-RABBIT-TRANSLATION-GUIDE.md)

## Publication log maintenance

- [Publication Log policy](PUBLICATION-LOG-POLICY.md) — English work titles, fixed language order (English, Japanese, French, Korean), actual publication dates, historical preservation, and verification procedures.

## Asset maintenance

- [Images, audio, PDF/EPUB storage and publication policy](ASSET-MAINTENANCE.md) — preservation of existing paths and originals, web photograph optimization, aggregate image-size review, and the November 2, 2026 digital-edition suspension.

## CSS maintenance

- [CSS ownership, typography, cache-version policy, and safety checklist](CSS-MAINTENANCE.md)
- Read-only CSS link/version audit: `python3 scripts/audit_css_links.py`
- **The diary layout of Sweater is protected**, including against changes to global CSS.

## SEO audit

- **[SEO maintenance policy](SEO-MAINTENANCE.md)** — verified changes, safety rules, audit links, and outstanding checks.

- Read-only full-source SEO audit: `python3 scripts/audit_seo.py`
- GitHub Actions: [SEO source audit](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-audit.yml), runs on relevant changes and supports manual dispatch.
- Per-page findings are available in the `seo-audit-report` artifact. ERROR/WARN/INFO are diagnostic flags, not automatically confirmed production errors.
- The audit does **not** modify pages or CSS. Source-only checks cannot confirm live HTTP status, Jekyll-generated URLs, or search-engine indexing. Changes based on findings require prior review, especially for Sweater.

## Deployed SEO verification

- Read-only live checker: `python3 scripts/audit_seo_live.py` (requires network access).
- GitHub Actions: [SEO live audit](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-live-audit.yml), automatically triggered after successful Pages deployment or manually.
- The `seo-live-report` artifact contains HTTP, canonical, noindex, and hreflang checks on published sitemap URLs.
- Live checks are diagnostic; Search Console and Naver indexing reports require separate access. No page text, translation, CSS, or layout is changed.
