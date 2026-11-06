#!/usr/bin/env python3
"""Parse a .handoff file. Exit 0 only if the handoff is valid."""

import re
import sys
from pathlib import Path


BANNERS = {"# handoff v1": 1, "# handoff v2": 2}
SECTIONS = ("FILES", "PASTE", "RULES")


def parse(text: str) -> dict:
    lines = text.splitlines()
    banner = lines[0].strip() if lines else ""
    if banner not in BANNERS:
        raise ValueError("line 1 must be # handoff v1 or # handoff v2")
    version = BANNERS[banner]

    if len(lines) < 2 or lines[1].strip() != "---":
        raise ValueError("missing opening --- fence")

    end = None
    for i in range(2, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("missing closing --- fence")

    meta = {}
    for raw in lines[2:end]:
        if not raw.strip() or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip()
    for key in ("mission", "continue_from", "stop_rule"):
        if not meta.get(key):
            raise ValueError(f"missing {key}")

    # Optional pin fields. Older v1 files without them stay valid.
    repo = meta.get("repo", "")
    commit = meta.get("commit", "")
    if repo and not re.fullmatch(r"https?://\S+", repo):
        raise ValueError(f"repo must be an http(s) URL: {repo}")
    if commit and not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        raise ValueError(f"commit must be a 7-40 char lowercase hex git SHA: {commit}")
    if version >= 2:
        for key in ("repo", "commit"):
            if not meta.get(key):
                raise ValueError(f"v2 requires {key}")
    if commit and not repo:
        raise ValueError("commit requires repo")

    sections = {"FILES": [], "PASTE": [], "RULES": []}
    current = None
    for raw in lines[end + 1 :]:
        if raw in ("FILES", "PASTE", "RULES"):
            current = raw
            continue
        if current is None:
            continue
        sections[current].append(raw)

    files = [p.strip() for p in sections["FILES"] if p.strip()]
    paste = "\n".join(sections["PASTE"]).strip("\n")
    rules = {}
    for raw in sections["RULES"]:
        if not raw.strip():
            continue
        if ": " not in raw:
            raise ValueError(f"rule must split on ': ': {raw}")
        key, value = raw.split(": ", 1)
        rules[key] = value

    if not files:
        raise ValueError("empty FILES list")
    if not paste.strip():
        raise ValueError("empty PASTE section")

    return {
        "version": version,
        "mission": meta["mission"],
        "continue_from": meta["continue_from"],
        "stop_rule": meta["stop_rule"],
        "repo": repo,
        "commit": commit,
        "files": files,
        "paste": paste,
        "rules": rules,
    }


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "sample.handoff")
    doc = parse(path.read_text())
    print(f"version: {doc['version']}")
    print(f"mission: {doc['mission']}")
    print(f"continue_from: {doc['continue_from']}")
    print(f"stop_rule: {doc['stop_rule']}")
    print(f"repo: {doc['repo'] or '(not set)'}")
    print(f"commit: {doc['commit'] or '(not pinned)'}")
    print(f"files: {len(doc['files'])}")
    for name in doc["files"]:
        print(f"  {name}")
    print(f"paste_chars: {len(doc['paste'])}")
    print(f"rules: {len(doc['rules'])}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
