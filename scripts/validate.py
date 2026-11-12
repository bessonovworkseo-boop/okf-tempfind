#!/usr/bin/env python3
"""Validate the Tempfind publishing profile on top of OKF v0.2.

Checks: OKF conformance (non-empty `type`, reserved index.md/log.md shapes, root okf_version),
required profile fields, record IDs, timestamps with offsets, source IDs and footnotes,
trust/status rules, relative links, marketing wording and, with --crawl, tempfind.com URLs.
Validation does not prove factual accuracy.
"""
import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".github", ".venv", "__pycache__", "dist", "docs", "scripts", "tests", "evaluations"}
REQUIRED = ["type", "title", "description", "sources", "generated", "status", "audience", "id"]
AUDIENCES = {"public", "reference", "internal-editorial"}
ACTOR = re.compile(r"^(?:human:[a-z0-9][a-z0-9._-]*|[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9._-]*)$")
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\s]+)\)")
FOOTREF = re.compile(r"\[\^([^\]\s]+)\](?!:)")
FOOTDEF = re.compile(r"^\[\^([^\]\s]+)\]:", re.M)
URL = re.compile(r"https://tempfind\.com(?:[^\s()<>`|\]]|\([^\s()]*\))*")
BANNED = re.compile(r"\b(best|leading|number one|#1|guaranteed?|fastest|lowest|premier)\b", re.I)
NEGATION = re.compile(r"\b(do not|don't|avoid|not repeat)\b", re.I)
FM = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)", re.S)


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently keeping the last one."""


def _mapping(loader, node, deep=False):
    out = {}
    for k_node, v_node in node.value:
        key = loader.construct_object(k_node, deep=deep)
        if key in out:
            raise ValueError(f"duplicate YAML key: {key}")
        out[key] = loader.construct_object(v_node, deep=deep)
    return out


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def timestamp(value):
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp needs an explicit UTC offset")
    return dt


def split(text):
    m = FM.match(text)
    if not m:
        return None, text
    meta = yaml.load(m.group(1), Loader=UniqueKeyLoader)
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a mapping")
    return meta, m.group(2)


def markdown_files(root):
    files = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if SKIP & set(rel.parts) or rel.as_posix() == "README.md":
            continue
        files.append(p)
    return files


def link_target(root, source, value):
    target = value.strip().strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    resolved = (source.parent / unquote(parsed.path)).resolve()
    if not resolved.is_relative_to(Path(root).resolve()):
        raise ValueError(f"link escapes repository: {value}")
    return resolved


def inspect(root=ROOT, now=None, crawl=None):
    root = root.resolve()
    now = now or datetime.now(timezone.utc)
    errors, warnings, records = [], [], {}
    ids = {}

    for p in markdown_files(root):
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"{rel}: empty file")
            continue
        try:
            meta, body = split(text)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        if p.name == "index.md":
            if rel == "index.md":
                if not meta or str(meta.get("okf_version")) != "0.2":
                    errors.append("index.md: root index must declare okf_version 0.2")
                elif set(meta) != {"okf_version"}:
                    errors.append("index.md: root frontmatter may only carry okf_version")
            elif meta is not None:
                errors.append(f"{rel}: only the root index.md may have frontmatter")
        elif p.name == "log.md":
            if meta is not None:
                errors.append(f"{rel}: log.md must not have frontmatter")
            dates = re.findall(r"^## (\S+)\s*$", body, flags=re.M)
            if not dates or any(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) for d in dates):
                errors.append(f"{rel}: log headings must be ## YYYY-MM-DD")
            elif dates != sorted(dates, reverse=True):
                errors.append(f"{rel}: log entries must be newest first")
        else:
            if meta is None:
                errors.append(f"{rel}: concept has no frontmatter")
                continue
            if not str(meta.get("type", "")).strip():
                errors.append(f"{rel}: `type` is required")
            for key in REQUIRED:
                if key not in meta:
                    errors.append(f"{rel}: missing `{key}`")
            expected_id = "tempfind:" + rel[:-3]
            if meta.get("id") != expected_id:
                errors.append(f"{rel}: id should be {expected_id}")
            if meta.get("id") in ids:
                errors.append(f"{rel}: duplicate id with {ids[meta['id']]}")
            ids[meta.get("id")] = rel
            audience = meta.get("audience")
            if audience not in AUDIENCES:
                errors.append(f"{rel}: audience must be one of {sorted(AUDIENCES)}")

            gen = meta.get("generated") or {}
            try:
                timestamp(gen.get("at"))
            except (ValueError, TypeError) as exc:
                errors.append(f"{rel}: generated.at: {exc}")
            if not ACTOR.match(str(gen.get("by", ""))):
                errors.append(f"{rel}: generated.by has an invalid actor")

            verified = meta.get("verified") or []
            for v in verified:
                if not ACTOR.match(str(v.get("by", ""))):
                    errors.append(f"{rel}: verified.by has an invalid actor")
                try:
                    timestamp(v.get("at"))
                except (ValueError, TypeError) as exc:
                    errors.append(f"{rel}: verified.at: {exc}")

            status = meta.get("status")
            if status == "stable":
                if not verified and audience != "reference":
                    errors.append(f"{rel}: stable record needs `verified`")
                if meta.get("review_required"):
                    errors.append(f"{rel}: stable record cannot be review_required")
                if "[NEEDS CONFIRMATION" in body:
                    errors.append(f"{rel}: stable record contains [NEEDS CONFIRMATION]")
            elif status == "draft":
                if not meta.get("review_required"):
                    errors.append(f"{rel}: draft record needs review_required: true")
            else:
                errors.append(f"{rel}: status must be stable or draft")

            if "stale_after" in meta:
                try:
                    if timestamp(meta["stale_after"]) <= now and status == "stable":
                        warnings.append(f"{rel}: stale since {meta['stale_after']}")
                except (ValueError, TypeError) as exc:
                    errors.append(f"{rel}: stale_after: {exc}")
            elif audience == "public":
                errors.append(f"{rel}: public record needs stale_after")

            src_ids = []
            for s in meta.get("sources") or []:
                if not isinstance(s, dict) or not s.get("id") or not s.get("resource"):
                    errors.append(f"{rel}: each source needs id and resource")
                    continue
                src_ids.append(s["id"])
            if len(src_ids) != len(set(src_ids)):
                errors.append(f"{rel}: duplicate source ids")
            if rel != "spec.md":
                prose = re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", body, flags=re.S))
                refs, defs = set(FOOTREF.findall(prose)), set(FOOTDEF.findall(prose))
                for r in refs - defs:
                    errors.append(f"{rel}: footnote [^{r}] has no definition")
                for r in refs - set(src_ids):
                    errors.append(f"{rel}: footnote [^{r}] is not a source id")
                if audience == "public" and not refs:
                    warnings.append(f"{rel}: no source footnotes in body")

            if audience == "public":
                for i, line in enumerate(body.splitlines(), 1):
                    if BANNED.search(line) and not NEGATION.search(line):
                        errors.append(f"{rel}: marketing wording: {line.strip()[:80]}")
            records[rel] = (meta, body)

        if rel != "spec.md":
            for value in LINK.findall(text):
                try:
                    target = link_target(root, p, value)
                except ValueError as exc:
                    errors.append(f"{rel}: {exc}")
                    continue
                if target is not None and not target.exists():
                    errors.append(f"{rel}: broken link {value}")

        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"\b2025\b", line):
                warnings.append(f"{rel}:{i}: mentions 2025 (allowed only as policy history)")

        if crawl is not None:
            for url in set(URL.findall(text)):
                u = unquote(url.rstrip(".,;:"))
                if u not in crawl and u.rstrip("/") + "/" not in crawl:
                    warnings.append(f"{rel}: not a 200 indexable URL in crawl: {u}")

    if not (root / "index.md").exists():
        errors.append("index.md: missing")
    return errors, warnings, records


def load_crawl(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return {unquote(r["Address"]) for r in csv.DictReader(fh)
                if r.get("Status Code") == "200" and r.get("Indexability") == "Indexable"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--crawl", type=Path)
    ap.add_argument("--now")
    args = ap.parse_args()
    errors, warnings, records = inspect(args.root, timestamp(args.now) if args.now else None,
                                        load_crawl(args.crawl) if args.crawl else None)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    stable = sum(1 for m, _ in records.values() if m.get("status") == "stable")
    needs = sum(b.count("[NEEDS CONFIRMATION") for _, b in records.values())
    print(f"\n{len(records)} concepts ({stable} stable, {len(records) - stable} draft), "
          f"{needs} [NEEDS CONFIRMATION] markers, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
