#!/usr/bin/env python3
"""Inject / refresh the Oktoneo presentation header in a product README.md.

Idempotent: replaces content between BEGIN/END:OKTONEO-HEADER markers.
On first run, inserts the header at the top and drops a leading H1 that
duplicates the product title (keeps the rest of the README intact).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "repos.yml"
HEADER_TMPL = ROOT / "profile" / "PRODUCT_README.header.md"

BEGIN = "<!-- BEGIN:OKTONEO-HEADER -->"
END = "<!-- END:OKTONEO-HEADER -->"
MARKER_RE = re.compile(
    re.escape(BEGIN) + r".*?" + re.escape(END),
    re.DOTALL,
)


def load_repo(name: str) -> dict:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    org = data["org"]
    for r in data.get("repos") or []:
        if r["name"] == name:
            return {"org": org, "repo": r}
    raise SystemExit(f"repo {name!r} not in catalog/repos.yml")


def render_header(org: dict, repo: dict) -> str:
    title = repo.get("title") or repo["name"]
    blurb = repo.get("blurb") or repo.get("description") or ""
    links: list[str] = [
        f"[Organisation]({org['github']})",
        f"[{org['product']}]({org['website']})",
    ]
    if repo.get("homepage"):
        links.append(f"[Site produit]({repo['homepage']})")
    links.append(f"[Dépôt](https://github.com/TM-INTELLIGENCE/{repo['name']})")
    text = HEADER_TMPL.read_text(encoding="utf-8")
    return (
        text.replace("{{TITLE}}", title)
        .replace("{{BLURB}}", blurb)
        .replace("{{LINKS}}", " · ".join(links))
        .rstrip()
        + "\n"
    )


def strip_leading_h1(body: str, title: str) -> str:
    """Remove first markdown H1 if it looks like the product title / old brand."""
    lines = body.lstrip("\n").splitlines()
    if not lines:
        return body
    m = re.match(r"^#\s+(.+)$", lines[0])
    if not m:
        return body
    h1 = m.group(1).strip()
    aliases = {
        title.lower(),
        title.lower().replace("oktoneo ", ""),
        "blitzpal (retailigy)",
        "oktoneo-karrio",
        "oktoneo karrio",
    }
    if h1.lower() in aliases or title.lower() in h1.lower():
        rest = "\n".join(lines[1:]).lstrip("\n")
        return rest
    return body


def apply(readme: Path, repo_name: str, check: bool = False) -> bool:
    meta = load_repo(repo_name)
    header = render_header(meta["org"], meta["repo"])
    original = readme.read_text(encoding="utf-8") if readme.exists() else ""

    if MARKER_RE.search(original):
        new = MARKER_RE.sub(header.rstrip(), original)
        # ensure trailing newline after END block separation
        if not new.endswith("\n"):
            new += "\n"
    else:
        title = meta["repo"].get("title") or repo_name
        body = strip_leading_h1(original, title)
        new = header + "\n" + body.lstrip("\n")
        if not new.endswith("\n"):
            new += "\n"

    if new == original:
        print(f"OK unchanged {readme}")
        return False
    if check:
        print(f"STALE {readme}", file=sys.stderr)
        return True
    readme.write_text(new, encoding="utf-8")
    print(f"Wrote {readme}")
    return True


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True, help="Catalog repo name")
    p.add_argument("--readme", type=Path, required=True, help="Path to README.md")
    p.add_argument("--check", action="store_true", help="Exit 1 if would change")
    args = p.parse_args()
    changed = apply(args.readme, args.repo, check=args.check)
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
