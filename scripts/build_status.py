"""Build assets/status.svg: a live status panel for the flagship repositories.

For each repo it asks the GitHub API for the latest completed CI run on the
default branch, the latest release and the last push time, then draws them as a
self-contained SVG (no scripts, no external assets).

The output deliberately contains no "generated at" timestamp, so the file only
changes when the underlying data changes and the workflow does not create empty
commits.

Usage: GITHUB_TOKEN=... python scripts/build_status.py > assets/status.svg
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Optional
from xml.sax.saxutils import escape

OWNER = "Veladicodes"
API = "https://api.github.com"

# (display name, repository, CI workflow file)
REPOS = [
    ("RT-GIDS", "Real-Time-GPU-Based-Intrusive-Detection-System", "ci.yml"),
    ("Agent Orchestration", "deterministic-agent-orchestration-mega-ai", "test.yml"),
    ("Fake Job Detector", "Realtime-Fake-Job-Predictor", "ci.yml"),
    ("Drone Fire RAG", "cloud-rag-drone-fire-detection", "ci.yml"),
]

GREEN, RED, GREY = "#3fb950", "#f85149", "#9fb3c8"


def api_get(path: str) -> Optional[Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-status-panel",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(API + path, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        print(f"warning: {path} -> HTTP {error.code}", file=sys.stderr)
        return None
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"warning: {path} -> {error}", file=sys.stderr)
        return None


def fetch_repo(repo: str, workflow_file: str) -> dict[str, Any]:
    info = api_get(f"/repos/{OWNER}/{repo}") or {}
    branch = info.get("default_branch", "main")
    runs = api_get(
        f"/repos/{OWNER}/{repo}/actions/workflows/{workflow_file}/runs"
        f"?branch={branch}&status=completed&per_page=1"
    )
    run = (runs or {}).get("workflow_runs", [])
    release = api_get(f"/repos/{OWNER}/{repo}/releases/latest") or {}

    conclusion = run[0].get("conclusion") if run else None
    pushed = (info.get("pushed_at") or "")[:10]
    return {
        "ok": bool(info),
        "conclusion": conclusion,
        "release": release.get("tag_name", "no release"),
        "pushed": pushed or "unknown",
        "language": info.get("language") or "",
    }


def status_style(conclusion: Optional[str]) -> tuple[str, str]:
    if conclusion == "success":
        return GREEN, "CI passing"
    if conclusion in {"failure", "timed_out", "startup_failure"}:
        return RED, "CI failing"
    return GREY, "CI unknown"


def render(rows: list[tuple[str, dict[str, Any]]]) -> str:
    row_height = 54
    top = 78
    height = top + row_height * len(rows) + 34
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" '
        f'width="1000" height="{height}" role="img" '
        'aria-label="Live status of the flagship projects">',
        "<style>"
        ".mono{font-family:'JetBrains Mono','SF Mono',Menlo,Consolas,monospace}"
        ".sans{font-family:'Segoe UI',Inter,Helvetica,Arial,sans-serif}"
        ".ok{animation:p 2.4s ease-in-out infinite}"
        "@keyframes p{0%,100%{opacity:1}50%{opacity:.35}}"
        "@media (prefers-reduced-motion:reduce){.ok{animation:none}}"
        "</style>",
        f'<rect width="1000" height="{height}" rx="14" fill="#0d1117" '
        'stroke="#22d3ee" stroke-opacity="0.35"/>',
        '<text x="32" y="44" class="mono" font-size="15" font-weight="700" '
        'letter-spacing="3" fill="#22d3ee">LIVE SYSTEM STATUS</text>',
        '<text x="968" y="44" class="sans" font-size="12" text-anchor="end" '
        'fill="#9fb3c8">read from the GitHub API by a scheduled workflow</text>',
        '<path d="M32 58H968" stroke="#22d3ee" stroke-opacity="0.2"/>',
    ]
    for index, (name, data) in enumerate(rows):
        y = top + index * row_height
        color, label = status_style(data["conclusion"])
        dot_class = ' class="ok"' if color == GREEN else ""
        parts.append(
            f'<circle cx="44" cy="{y + 14}" r="6" fill="{color}"{dot_class}/>'
            f'<text x="64" y="{y + 19}" class="mono" font-size="16" '
            f'font-weight="700" fill="#e6edf3">{escape(name)}</text>'
            f'<text x="340" y="{y + 19}" class="mono" font-size="14" '
            f'fill="{color}">{label}</text>'
            f'<text x="520" y="{y + 19}" class="mono" font-size="14" '
            f'fill="#e6edf3">{escape(data["release"])}</text>'
            f'<text x="660" y="{y + 19}" class="mono" font-size="14" '
            f'fill="#9fb3c8">pushed {escape(data["pushed"])}</text>'
            f'<text x="968" y="{y + 19}" class="mono" font-size="13" '
            f'text-anchor="end" fill="#9fb3c8">{escape(data["language"])}</text>'
        )
        if index < len(rows) - 1:
            parts.append(
                f'<path d="M32 {y + 36}H968" stroke="#22d3ee" stroke-opacity="0.08"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    rows = [(name, fetch_repo(repo, workflow)) for name, repo, workflow in REPOS]
    if not any(data["ok"] for _, data in rows):
        print("error: no repository data could be fetched", file=sys.stderr)
        return 1
    sys.stdout.write(render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
