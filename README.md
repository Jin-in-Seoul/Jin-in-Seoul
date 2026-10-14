# Jin-in-Seoul

A multilingual archive of fiction.

https://jin-in-seoul.com

## CSS maintenance

- [CSS ownership, typography, cache-version policy, and safety checklist](CSS-MAINTENANCE.md)
- Read-only CSS link/version audit: `python3 scripts/audit_css_links.py`
- **Do not modify Sweater's diary layout** or change global CSS in ways that affect it.

## SEO audit

- **[SEO maintenance and cross-session handoff](SEO-MAINTENANCE.md)** — verified changes, safety rules, audit links, and outstanding checks.

- Read-only full-source SEO audit: `python3 scripts/audit_seo.py`
- GitHub Actions: [SEO source audit](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-audit.yml), runs on relevant changes and supports manual dispatch.
- Download the `seo-audit-report` artifact from the workflow run to review per-page findings. ERROR/WARN/INFO are diagnostic flags, not automatically confirmed production errors.
- The audit does **not** modify pages or CSS. Source-only checks cannot confirm live HTTP status, Jekyll-generated URLs, or search-engine indexing. Review findings before editing, especially Sweater.

## Deployed SEO verification

- Read-only live checker: `python3 scripts/audit_seo_live.py` (requires network access).
- GitHub Actions: [SEO live audit](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-live-audit.yml), automatically triggered after successful Pages deployment or manually.
- Download `seo-live-report` artifact for HTTP, canonical, noindex, and hreflang checks on published sitemap URLs.
- Live checks are diagnostic; Search Console and Naver indexing reports require separate access. No page text, translation, CSS, or layout is changed.
