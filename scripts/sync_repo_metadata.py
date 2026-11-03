#!/usr/bin/env python3
"""Push catalog descriptions / topics / homepage to GitHub repos (best-effort).

Requires GH_TOKEN or GITHUB_TOKEN with repo admin on the org.
Skips repos that do not exist. Never prints tokens.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "repos.yml"
ORG = "TM-INTELLIGENCE"
API = "https://api.github.com"


def _token() -> str:
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        raise SystemExit("GH_TOKEN or GITHUB_TOKEN required")
    return tok


def api(method: str, path: str, body: dict | None = None) -> tuple[int, dict | list | None]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {_token()}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "tm-intelligence-profile-sync",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = {"message": raw}
        return e.code, payload


def sync_one(repo: dict) -> None:
    name = repo["name"]
    if not repo.get("sync_description", True):
        print(f"skip {name} (sync_description=false)")
        return
    patch: dict = {}
    if repo.get("description"):
        patch["description"] = repo["description"]
    if "homepage" in repo:
        patch["homepage"] = repo["homepage"] or ""
    code, _ = api("PATCH", f"/repos/{ORG}/{name}", patch)
    if code == 404:
        print(f"missing {name} — create the repo then re-run")
        return
    if code >= 400:
        print(f"PATCH {name} failed HTTP {code}", file=sys.stderr)
        return
    print(f"updated {name} description/homepage")

    topics = repo.get("topics") or []
    if topics:
        tcode, _ = api(
            "PUT",
            f"/repos/{ORG}/{name}/topics",
            {"names": topics},
        )
        if tcode >= 400:
            print(f"topics {name} failed HTTP {tcode}", file=sys.stderr)
        else:
            print(f"updated {name} topics: {', '.join(topics)}")


def main() -> int:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    for repo in data.get("repos") or []:
        sync_one(repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
