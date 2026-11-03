#!/usr/bin/env python3
"""Generate profile/README.md from catalog/repos.yml + template.

Markers <!-- BEGIN:PROJECTS --> … <!-- END:PROJECTS --> are replaced.
Hand-edits outside markers in the generated file are discarded on regen —
edit the template or the catalog instead.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "repos.yml"
TEMPLATE = ROOT / "profile" / "README.template.md"
OUTPUT = ROOT / "profile" / "README.md"
ORG = "TM-INTELLIGENCE"


def render_projects(repos: list[dict]) -> str:
    lines: list[str] = [
        "| Projet | Dépôt | Description |",
        "|--------|-------|-------------|",
    ]
    for r in repos:
        name = r["name"]
        title = r.get("title") or name
        blurb = (r.get("blurb") or "").replace("|", "\\|")
        url = f"https://github.com/{ORG}/{name}"
        home = r.get("homepage")
        title_cell = f"**[{title}]({url})**"
        if home:
            title_cell += f"<br/><sub>[site]({home})</sub>"
        lines.append(f"| {title_cell} | [`{name}`]({url}) | {blurb} |")
    return "\n".join(lines)


def generate() -> str:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    org = data["org"]
    projects = render_projects(data.get("repos") or [])
    text = TEMPLATE.read_text(encoding="utf-8")
    text = (
        text.replace("{{TAGLINE}}", org["tagline"])
        .replace("{{WEBSITE}}", org["website"])
        .replace("{{GITHUB}}", org["github"])
        .replace("{{PROJECTS}}", projects)
    )
    return text.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if profile/README.md is stale (CI / pre-commit).",
    )
    args = parser.parse_args()
    rendered = generate()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print("profile/README.md is stale — run scripts/generate_profile_readme.py", file=sys.stderr)
            return 1
        print("profile/README.md is up to date")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
