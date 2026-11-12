#!/usr/bin/env python3
"""Export the public consumer bundle for https://tempfind.com/okf/.

Includes only records with audience: public, status: stable, a `verified` entry,
no review_required and a future stale_after. Links to records that are not exported
are rewritten to their official `resource` URL, or to plain text.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import ROOT, inspect, link_target, timestamp  # noqa: E402

LINK = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")


def eligible(meta, now):
    return (meta.get("audience") == "public" and meta.get("status") == "stable"
            and bool(meta.get("verified")) and not meta.get("review_required")
            and bool(meta.get("stale_after")) and timestamp(meta["stale_after"]) > now)


def export(root, out, now=None):
    root, out = root.resolve(), out.resolve()
    now = now or datetime.now(timezone.utc)
    errors, _, records = inspect(root, now)
    if errors:
        raise ValueError("source validation failed: " + "; ".join(errors))
    if out == root or root.is_relative_to(out):
        raise ValueError("unsafe export destination")
    if out.exists() and any(out.iterdir()):
        raise ValueError("destination must be absent or empty")
    selected = {rel: rec for rel, rec in records.items() if eligible(rec[0], now)}
    if not selected:
        raise ValueError("no fresh verified public records to export")

    out.mkdir(parents=True)
    for rel, (meta, body) in selected.items():
        source = root / rel

        def rewrite(m, source=source):
            label, value = m.group(1), m.group(2)
            target = link_target(root, source, value)
            if target is None:
                return m.group(0)
            dest = target.relative_to(root).as_posix()
            if dest in selected:
                return m.group(0)
            resource = records.get(dest, ({}, ""))[0].get("resource")
            return f"[{label}]({resource})" if resource else label

        body = LINK.sub(rewrite, body)
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=100).strip()
                          + "\n---\n\n" + body.strip() + "\n", encoding="utf-8")

    groups = {}
    for rel, (meta, _) in sorted(selected.items()):
        groups.setdefault(rel.split("/")[0] if "/" in rel else "", []).append((rel, meta))
    lines = ['---', 'okf_version: "0.2"', '---', '', '# Tempfind knowledge bundle', '',
             'Source-reviewed facts about Tempfind Inc. and the Tempfind dental staffing platform in Canada. '
             'Current policies on tempfind.com take precedence. Each record lists its sources, review date and recheck date.', '']
    if "markets/en.md" in selected:
        lines += ['Start with the [English reference](markets/en.md).', '']
    for group, items in groups.items():
        lines.append(f"## {group.replace('-', ' ').capitalize() if group else 'General'}")
        lines.append("")
        lines += [f"* [{m['title']}]({rel}) - {m.get('description', '').strip()}" for rel, m in items]
        lines.append("")
    (out / "index.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "log.md").write_text((root / "log.md").read_text(encoding="utf-8"), encoding="utf-8")

    manifest = {"generated_at": now.isoformat(), "okf_version": "0.2",
                "included": sorted(selected), "excluded": sorted(set(records) - set(selected))}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    errors, _, _ = inspect(out, now)
    if errors:
        raise ValueError("export validation failed: " + "; ".join(errors))
    return len(selected)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--now")
    args = ap.parse_args()
    try:
        n = export(args.root, args.out, timestamp(args.now) if args.now else None)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Exported {n} records to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
