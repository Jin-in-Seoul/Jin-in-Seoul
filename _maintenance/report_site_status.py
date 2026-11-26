#!/usr/bin/env python3
"""Read-only summary of existing GitHub Actions checks for Jin-in-Seoul.

Run with Python 3.10+: python3 _maintenance/report_site_status.py
Optional GH_TOKEN or GITHUB_TOKEN environment variable for API rate limits.
No workflow dispatch, repository edits, artifact downloads or deployment.
A successful job does not establish zero SEO errors or live visual correctness.
"""
import datetime as dt
import json
import os
import subprocess
import urllib.request
import urllib.error
import urllib.parse

REPO = "Jin-in-Seoul/Jin-in-Seoul"
API = "https://api.github.com/repos/" + REPO
CHECKS = {
    "Pages deployment": "pages build and deployment",
    "SEO source": "SEO source audit",
    "SEO live": "SEO live audit",
    "Links and site quality": "Site quality audit",
    "Mobile browser quality": "Browser quality audit",
}
WORKFLOWS = {
    "SEO source": "seo-audit.yml",
    "SEO live": "seo-live-audit.yml",
    "Links and site quality": "site-quality-audit.yml",
    "Mobile browser quality": "browser-quality-audit.yml",
}

def get(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Jin-in-Seoul-maintenance"}
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request(API + path, headers=headers), timeout=20) as response:
        return json.load(response)

def safe_get(path):
    try:
        return get(path), None
    except (OSError, ValueError) as exc:
        return None, str(exc)

def latest(runs, name):
    matches = [r for r in runs if r.get("name") == name and r.get("head_branch") == "main"]
    return max(matches, key=lambda r: (r.get("created_at", ""), r.get("id", 0)), default=None)

def row(label, run, head):
    if not run:
        return f"| {label} | UNKNOWN | — | — | — |"
    status = run.get("status", "unknown")
    conclusion = run.get("conclusion") or status
    sha = run.get("head_sha", "")
    relation = "current SHA" if sha and sha == head else "different SHA; review scope"
    if not head:
        relation = "main SHA unknown"
    if label in ("SEO live", "Links and site quality", "Mobile browser quality"):
        relation += "; live snapshot not proven by run SHA"
    url = run.get("html_url", "")
    link = f"[run {run['id']}]({url})" if url and run.get("id") else "—"
    return f"| {label} | {conclusion} | {run.get('created_at', '—')} | {sha[:12] or '—'} ({relation}) | {link} |"

def main():
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    branch, err = safe_get("/branches/main")
    head = ((branch or {}).get("commit") or {}).get("sha")
    print("# Jin-in-Seoul maintenance status")
    print(f"\nCollected (UTC): {now}\nMain SHA: {head or 'UNKNOWN'}")
    if err:
        print("Main lookup failed:", err)
    general, err = safe_get("/actions/runs?branch=main&per_page=100")
    runs = (general or {}).get("workflow_runs", [])
    if err:
        print("General run lookup failed:", err)
    print("\n| Check | Job conclusion | Started (UTC) | Run commit | Evidence |")
    print("|---|---|---|---|---|")
    notes = []
    for label, name in CHECKS.items():
        run = latest(runs, name)
        if label in WORKFLOWS:
            data, error = safe_get("/actions/workflows/" + WORKFLOWS[label] + "/runs?branch=main&per_page=1")
            if error:
                notes.append(label + ": workflow-specific lookup failed; recent general listing used if available. " + error)
            else:
                candidate = latest(data.get("workflow_runs", []), name)
                if candidate and (not run or candidate.get("created_at", "") >= run.get("created_at", "")):
                    run = candidate
        print(row(label, run, head))
        if not run:
            notes.append(label + ": no matching main run retrieved; not evidence of success or failure.")
    print("\n## Additional checks")
    print("- Sitemap and hreflang: inspect SEO report artifacts linked from the runs.")
    print("- CSS links: run existing read-only command python3 scripts/audit_css_links.py locally.")
    print("- Change scope: use _maintenance/check_change_scope.py with explicit base and allowed paths.")
    print("- Numeric error counts and Lighthouse scores: UNKNOWN until report artifacts are inspected.")
    print("- Google/Naver indexing and visual rendering: not established by job status.")
    final, error = safe_get("/branches/main")
    final_head = ((final or {}).get("commit") or {}).get("sha")
    if not final_head or final_head != head:
        notes.append("Main changed or could not be rechecked; rerun before relying on this snapshot.")
    for note in notes:
        print("- " + note)
    print("\nRead-only collection; no files or workflows changed.")

if __name__ == "__main__":
    main()
