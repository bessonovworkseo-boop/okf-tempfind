#!/usr/bin/env python3
"""Validate the Tempfind OKF bundle against OKF v0.2 conformance and house rules.

Conformance (OKF SPEC v0.2):
  - every non-reserved .md has parseable YAML frontmatter with a non-empty `type`
  - reserved index.md has no frontmatter, except the bundle-root index.md (okf_version only)
  - reserved log.md has no frontmatter and uses `## YYYY-MM-DD` headings, newest first
House rules:
  - recommended keys present: title, description, resource, generated, sources, status, stale_after
  - relative links resolve inside the bundle
  - tempfind.com links exist in the crawl export (when --crawl is given)
  - no marketing superlatives; no "2025" used as the current year (flagged for review)
  - JSON-LD files parse

Usage: python3 scripts/validate_okf.py [--crawl internal_html.csv]
Exit code 1 on any error.
"""
import argparse
import csv
import json
import pathlib
import re
import sys
import urllib.parse

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "okf"
RESERVED = {"index.md", "log.md"}
RECOMMENDED = ["title", "description", "resource", "generated", "sources", "status", "stale_after"]
BANNED = re.compile(r"\b(best|leading|number one|#1|guaranteed?|fastest|lowest|premier)\b", re.I)
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
URL_RE = re.compile(r"https://tempfind\.com(?:[^\s()>`|]|\([^\s()]*\))*")

errors, warnings = [], []


def err(f, msg):
    errors.append(f"ERROR {f.relative_to(ROOT)}: {msg}")


def warn(f, msg):
    warnings.append(f"WARN  {f.relative_to(ROOT)}: {msg}")


def load_crawl(path):
    urls = set()
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("Status Code") == "200" and r.get("Indexability") == "Indexable":
                urls.add(urllib.parse.unquote(r["Address"]))
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crawl")
    args = ap.parse_args()
    crawl = load_crawl(args.crawl) if args.crawl else None

    files = sorted(BUNDLE.rglob("*.md"))
    for f in files:
        text = f.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        body = FM_RE.sub("", text, count=1)

        if f.name == "index.md":
            if f.parent == BUNDLE:
                if not m:
                    warn(f, "root index.md has no okf_version frontmatter")
                else:
                    fm = yaml.safe_load(m.group(1)) or {}
                    if set(fm) - {"okf_version"}:
                        err(f, "root index.md frontmatter may only carry okf_version")
                    if str(fm.get("okf_version")) != "0.2":
                        warn(f, f"okf_version is {fm.get('okf_version')!r}, expected '0.2'")
            elif m:
                err(f, "non-root index.md must not contain frontmatter")
        elif f.name == "log.md":
            if m:
                err(f, "log.md must not contain frontmatter")
            dates = re.findall(r"^## (\S+)$", body, flags=re.M)
            if not dates:
                err(f, "log.md has no date headings")
            for d in dates:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
                    err(f, f"log heading {d!r} is not ISO 8601")
            if dates != sorted(dates, reverse=True):
                err(f, "log.md entries must be newest first")
        else:
            if not m:
                err(f, "concept has no frontmatter")
                continue
            try:
                fm = yaml.safe_load(m.group(1)) or {}
            except yaml.YAMLError as e:
                err(f, f"frontmatter is not valid YAML: {e}")
                continue
            if not str(fm.get("type", "")).strip():
                err(f, "frontmatter `type` is required and must be non-empty")
            for k in RECOMMENDED:
                if k not in fm:
                    warn(f, f"recommended key `{k}` missing")
            if "verified" in fm:
                warn(f, "`verified` present: confirm a real review took place")
            if len(str(fm.get("description", ""))) > 200:
                warn(f, "description longer than 200 characters")
            words = len(re.findall(r"\w+", body))
            if words < 250:
                warn(f, f"short concept ({words} words)")

        # links
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = (f.parent / target.split("#")[0]).resolve()
            if not path.exists():
                err(f, f"broken relative link: {target}")
            elif BUNDLE.resolve() not in path.parents and path != BUNDLE.resolve():
                err(f, f"link leaves the bundle: {target}")

        if crawl is not None:
            for url in set(URL_RE.findall(text)):
                u = urllib.parse.unquote(url.rstrip(".,;:"))
                if u.endswith("<role>/<city>/") or "<" in u:
                    continue
                if u not in crawl and u.rstrip("/") + "/" not in crawl:
                    warn(f, f"URL not in crawl as 200 indexable: {u}")

        for i, line in enumerate(text.splitlines(), 1):
            if BANNED.search(line):
                err(f, f"line {i}: marketing wording: {line.strip()[:90]}")
            if "2025" in line:
                warn(f, f"line {i}: contains 2025 (historical dates only): {line.strip()[:90]}")

    for j in sorted((ROOT / "integration").rglob("*.jsonld")):
        try:
            json.loads(j.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(j, f"invalid JSON: {e}")

    needs = sum(p.read_text(encoding="utf-8").count("[NEEDS CONFIRMATION") for p in files)
    for line in warnings + errors:
        print(line)
    concepts = [p for p in files if p.name not in RESERVED]
    print(f"\n{len(files)} files ({len(concepts)} concepts), {len(errors)} errors, "
          f"{len(warnings)} warnings, {needs} [NEEDS CONFIRMATION] markers")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
