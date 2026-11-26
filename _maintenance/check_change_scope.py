#!/usr/bin/env python3
"""Read-only Git change scope checker. Python 3; local Git checkout required.

Examples (run from repository root):
  python3 _maintenance/check_change_scope.py BASE HEAD --allow index.html:css
  python3 _maintenance/check_change_scope.py BASE HEAD --allow gray-note/012/en/index.html:new --allow sitemap.xml
  python3 _maintenance/check_change_scope.py BASE --allow index.html:css
  python3 _maintenance/check_change_scope.py --self-test

Omit HEAD to inspect the working tree, including untracked files.
Rules are exact paths, not glob patterns. Default rule permits content changes
to an existing regular file only; :new permits creation, :delete deletion,
:css permits edits solely inside existing inline style blocks in HTML.
This is a manual pre-publication check, not a GitHub push blocker.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

STYLE = re.compile(rb'(<style\b[^>]*>)(.*?)(</style\s*>)', re.I | re.S)

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])

def rules_from(items):
    rules = {}
    for item in items:
        path, sep, mode = item.partition(":")
        mode = mode if sep else "modify"
        if (not path or path.startswith("/") or "\\" in path
                or any(x in ("", ".", "..") for x in path.split("/"))
                or mode not in ("modify", "new", "delete", "css")
                or path in rules):
            raise ValueError("Invalid or duplicate rule: " + item)
        rules[path] = mode
    return rules

def tree(root, ref):
    result = {}
    for record in git(root, "ls-tree", "-rz", "--full-tree", ref).split(b"\0"):
        if record:
            info, path = record.split(b"\t", 1)
            mode, kind, oid = info.split()
            result[path.decode("utf-8")] = (mode, kind, oid)
    return result

def working_tree(root):
    result = {}
    paths = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    for path in set(paths.split(b"\0")) - {b""}:
        name = path.decode("utf-8")
        p = root / name
        if p.is_symlink():
            result[name] = (b"120000", b"blob", None)
        elif p.is_file():
            mode = b"100755" if p.stat().st_mode & 0o111 else b"100644"
            result[name] = (mode, b"blob", git(root, "hash-object", "--no-filters", "--", name).strip())
        elif p.exists():
            raise ValueError("Unsupported working-tree entry: " + name)
    return result

def css_only(old, new):
    # Preserve opening/closing tags and all bytes outside existing style blocks.
    # A changed block may not add nested style tags or HTML breakout tags.
    def skeleton(data):
        matches = list(STYLE.finditer(data))
        if not matches or any(re.search(rb'<\s*/?\s*style\b', m[2], re.I) for m in matches):
            return None
        return STYLE.sub(lambda m: m[1] + m[3], data), len(matches)
    a, b = skeleton(old), skeleton(new)
    return a is not None and a == b

def check(root, base, head, rules):
    before = tree(root, base)
    after = tree(root, head) if head else working_tree(root)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    errors = []
    for p in changed:
        a, b = before.get(p), after.get(p)
        action = "new" if a is None else "delete" if b is None else "modify"
        rule = rules.get(p)
        print(f"{action:6} {p}  [allowed: {rule or 'NO'}]")
        if rule is None:
            errors.append("Unlisted path: " + p)
            continue
        if action != ("modify" if rule == "css" else rule):
            errors.append("Unexpected operation: " + p)
            continue
        if any(x and (x[0] not in (b"100644", b"100755") or x[1] != b"blob") for x in (a, b)):
            errors.append("Not a regular file: " + p)
            continue
        if a and b and a[:2] != b[:2]:
            errors.append("File mode/type changed: " + p)
            continue
        if rule == "css":
            old = git(root, "cat-file", "blob", a[2].decode())
            new = git(root, "cat-file", "blob", b[2].decode()) if head else (root / p).read_bytes()
            if not css_only(old, new):
                errors.append("Outside inline CSS changed: " + p)
    if not changed:
        errors.append("No changes to verify")
    for e in errors:
        print("ERROR:", e, file=sys.stderr)
    print(f"{'FAIL' if errors else 'PASS'}: {len(changed)} changed path(s), {len(errors)} violation(s).")
    return not errors

def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        git(root, "init", "-q")
        git(root, "config", "user.email", "test@example.invalid")
        git(root, "config", "user.name", "Scope Test")
        p = root / "index.html"
        old = "<style>p{margin:2px}</style>\n<p>Original</p>\n"
        p.write_text(old, encoding="utf-8")
        git(root, "add", ".")
        git(root, "commit", "-qm", "base")
        base = git(root, "rev-parse", "HEAD").decode().strip()
        def expect(value, message):
            if not value:
                raise RuntimeError("Self-test failed: " + message)
        p.write_text(old.replace("2px", "4px"), encoding="utf-8")
        expect(check(root, base, None, {"index.html":"css"}), "CSS only")
        (root / "extra.html").write_text("unexpected", encoding="utf-8")
        expect(not check(root, base, None, {"index.html":"css"}), "untracked file")
        (root / "extra.html").unlink()
        p.write_text(old.replace("Original", "Changed"), encoding="utf-8")
        expect(not check(root, base, None, {"index.html":"css"}), "prose changed")
        p.write_text(old.replace("2px", "4px"), encoding="utf-8")
        git(root, "add", ".")
        git(root, "commit", "-qm", "CSS edit")
        expect(check(root, base, "HEAD", {"index.html":"css"}), "commit comparison")
        p.unlink()
        expect(not check(root, base, None, {"index.html":"css"}), "deletion")
        expect(check(root, base, None, {"index.html":"delete"}), "approved deletion")
    print("SELF-TEST PASS")

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("base", nargs="?")
    parser.add_argument("head", nargs="?")
    parser.add_argument("--allow", action="append", default=[])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return 0
        if not args.base or not args.allow:
            parser.error("base and at least one --allow rule required")
        root = Path(__file__).resolve().parent.parent
        # Resolve refs before use; no user-supplied option-like refs.
        def resolve(ref):
            if ref.startswith("-"):
                raise ValueError("Invalid ref")
            return git(root, "rev-parse", "--verify", ref + "^{commit}").decode().strip()
        return 0 if check(root, resolve(args.base), resolve(args.head) if args.head else None, rules_from(args.allow)) else 1
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print("STOP:", exc, file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
