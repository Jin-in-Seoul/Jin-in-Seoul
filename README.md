# Jin-in-Seoul

A multilingual archive of fiction.

https://jin-in-seoul.com

## CSS maintenance

- [CSS ownership, typography, cache-version policy, and safety checklist](CSS-MAINTENANCE.md)
- Read-only CSS link/version audit: `python3 scripts/audit_css_links.py`
- **Do not modify Sweater's diary layout** or change global CSS in ways that affect it.

## SEO audit

- Read-only full-source SEO audit: `python3 scripts/audit_seo.py`
- GitHub Actions: [SEO source audit](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-audit.yml), runs on relevant changes and supports manual dispatch.
- Download the `seo-audit-report` artifact from the workflow run to review per-page findings. ERROR/WARN/INFO are diagnostic flags, not automatically confirmed production errors.
- The audit does **not** modify pages or CSS. Source-only checks cannot confirm live HTTP status, Jekyll-generated URLs, or search-engine indexing. Review findings before editing, especially Sweater.
