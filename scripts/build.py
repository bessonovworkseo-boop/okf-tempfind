#!/usr/bin/env python3
"""Rebuild generated parts of the Tempfind knowledge bundle.

Always:
  - folder index.md files (no frontmatter, OKF directory listings)
  - root index.md (okf_version 0.2)
  - docs/schema/faqpage.jsonld from stable FAQ records
  - structure.txt
With --crawl <internal_html.csv> (Screaming Frog export):
  - citations/help-center.md and citations/blog-guides.md
"""
import argparse
import csv
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://tempfind.com"
AT = "2026-11-12T13:55:00Z"
STALE = "2026-12-12T13:55:00Z"
BANNED = re.compile(r"\b(best|leading|number one|#1|guaranteed?|fastest|lowest|premier)\b", re.I)
SKIP_DIRS = {".git", ".github", "dist", "docs", "scripts", "tests", "evaluations", "__pycache__"}

FOLDERS = {
    "products": ("Products", "Tempfind services for dental clinics and dental professionals, HR Concierge and pricing."),
    "concepts": ("Concepts", "Dental roles on Tempfind, professional verification, platform vs agency and a glossary. Read these before product or FAQ files."),
    "destinations": ("Destinations", "Where Tempfind operates: cities with staffing pages, provinces and city detail."),
    "faq": ("FAQ", "Short answers to common questions from clinics and dental professionals. Each answer links to the record with details."),
    "policies": ("Policies", "Scoped summaries of Tempfind policies. The current official policy on tempfind.com takes precedence. Draft records require further review."),
    "markets": ("Markets", "Language references. English is the only published language and the primary reference."),
}

GUIDES = {
    "Hygienist career and pay": [
        "/blog/dental-hygienist-jobs-canada/",
        "/blog/dental-hygienist-salary-ontario/",
        "/blog/dental-hygienist-salary-ottawa/",
        "/blog/discover-the-path-how-to-become-a-dental-hygienist/",
        "/blog/what-do-dental-hygienists-do/",
        "/blog/top-dental-hygiene-interview-questions/",
    ],
    "Dental assistant career and pay": [
        "/blog/dental-assistant-salary-in-canada-understanding-compensation-in/",
        "/blog/how-to-become-a-dental-assistant/",
        "/blog/what-does-a-dental-assistant-do-job-overview/",
        "/blog/how-to-find-dental-assistant-work-ottawa/",
        "/blog/dental-assistant-vs-dental-hygienist/",
    ],
    "Dental receptionist career and pay": [
        "/blog/dental-receptionist-salary-canada/",
        "/blog/how-to-become-a-dental-receptionist/",
        "/blog/dental-receptionist-duties/",
        "/blog/dental-receptionist-work-ottawa-guide/",
    ],
    "Staffing guides for clinics": [
        "/blog/temporary-dental-staffing-101-everything-you-need-to-know/",
        "/blog/temp-dental-agency-vs-dental-staffing-app/",
        "/blog/long-term-dental-staffing-alternatives/",
        "/blog/how-to-hire-dental-office-manager-ottawa/",
        "/blog/dental-office-staff-shortage-insights-and-strategy-to-solve-the-problem/",
        "/blog/ensuring-compliance-and-quality-of-temporary-dental-staff/",
    ],
}

FM = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def read(path):
    m = FM.match(path.read_text(encoding="utf-8"))
    if not m:
        return {}, path.read_text(encoding="utf-8")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def dump(meta, body):
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=100).strip() + "\n---\n\n" + body.strip() + "\n"


def concepts_in(folder):
    return sorted(p for p in (ROOT / folder).glob("*.md") if p.name not in ("index.md", "log.md"))


# ---------- crawl-driven lists ----------

def load_crawl(path):
    rows = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("Status Code") == "200" and r.get("Indexability") == "Indexable":
                rows[re.sub(r"^https?://[^/]+", "", r["Address"])] = (r.get("H1-1") or r.get("Title 1") or "").strip()
    return rows


def list_meta(rid, title, description, resource, sources, scope):
    return {
        "type": "Reference",
        "title": title,
        "description": description,
        "resource": resource,
        "tags": ["citations"],
        "language": "en-CA",
        "sources": sources,
        "generated": {"by": "claude/okf-build", "at": AT},
        "status": "stable",
        "audience": "public",
        "verified": [{"by": "claude/source-review", "at": AT}],
        "approval_scope": scope,
        "stale_after": STALE,
        "id": f"tempfind:{rid}",
    }


def build_help_center(crawl):
    groups = {"for-clinics": [], "for-professionals": []}
    for p, h1 in sorted(crawl.items()):
        m = re.match(r"^/help-center/(for-clinics|for-professionals)/[^/]+/$", p)
        if m and h1 and not BANNED.search(h1):
            groups[m.group(1)].append((h1, SITE + p))
    src = [
        {"id": "help-clinics", "resource": f"{SITE}/help-center/for-clinics/", "title": "Help Topics For Dental Clinics"},
        {"id": "help-pros", "resource": f"{SITE}/help-center/for-professionals/", "title": "Help Topics For Dental Professionals"},
    ]
    meta = list_meta("citations/help-center", "Tempfind Help Center articles",
                     "List of Tempfind Help Center articles for dental clinics and dental professionals, with links to the live pages.",
                     f"{SITE}/help-center/", src,
                     "URLs returned 200 and were indexable in the 2026-11-12 crawl; titles copied from H1; article bodies not all read.")
    body = [
        "# Tempfind Help Center articles", "",
        f"The Tempfind Help Center at {SITE}/help-center/ has {len(groups['for-clinics'])} articles for clinics and "
        f"{len(groups['for-professionals'])} for professionals listed here. Some older articles describe direct payment "
        "from clinic to professional; the current rule is in the [payment policy](../policies/payment-policy.md).[^help-clinics][^help-pros]",
        "", "## Articles for dental clinics", "",
    ]
    body += [f"- [{t}]({u})" for t, u in groups["for-clinics"]]
    body += ["", "## Articles for dental professionals", ""]
    body += [f"- [{t}]({u})" for t, u in groups["for-professionals"]]
    body += ["", "- [FAQ](../faq/index.md)", "- [Official sources](official-sources.md)", ""]
    body += [f"[^{s['id']}]: {s['title']}, {s['resource']}, checked 2026-11-12." for s in src]
    (ROOT / "citations/help-center.md").write_text(dump(meta, "\n".join(body)), encoding="utf-8")


def build_blog_guides(crawl):
    src = [{"id": "insights", "resource": f"{SITE}/dental-insights/", "title": "Dental Insights"}]
    meta = list_meta("citations/blog-guides", "Tempfind career and staffing guides",
                     "Curated Tempfind blog guides on dental hygienist, assistant and receptionist careers in Canada and on temporary staffing for clinics.",
                     f"{SITE}/dental-insights/", src,
                     "URLs returned 200 and were indexable in the 2026-11-12 crawl; article content not reviewed.")
    body = [
        "# Tempfind career and staffing guides", "",
        "A curated selection of Tempfind blog articles, one per topic. Salary figures in these articles are Tempfind estimates, "
        "not platform rates; each professional sets their own hourly rate.[^insights]", "",
    ]
    missing = []
    for section, paths in GUIDES.items():
        body += [f"## {section}", ""]
        for p in paths:
            if p not in crawl:
                missing.append(p)
                continue
            title = crawl[p]
            if BANNED.search(title):
                title = title.split(":")[0].strip()
            body.append(f"- [{title}]({SITE}{p})")
        body.append("")
    body += ["- [Concepts](../concepts/index.md)", "", "[^insights]: Dental Insights, https://tempfind.com/dental-insights/, checked 2026-11-12."]
    (ROOT / "citations/blog-guides.md").write_text(dump(meta, "\n".join(body)), encoding="utf-8")
    return missing


# ---------- indexes ----------

def build_folder_indexes():
    for folder, (title, intro) in FOLDERS.items():
        lines = [f"# {title}", "", intro, ""]
        for p in concepts_in(folder):
            meta, _ = read(p)
            flag = "" if meta.get("status") == "stable" else " (draft)"
            lines.append(f"* [{meta.get('title', p.stem)}]({p.name}) - {meta.get('description', '').strip()}{flag}")
        (ROOT / folder / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def link(rel):
    meta, _ = read(ROOT / rel)
    return f"- [{meta.get('title', rel)}]({rel})"


def build_root_index():
    sections = [
        ("Brand", ["brand/company.md", "brand/positioning.md", "brand/trust.md"]),
        ("Products", ["products/index.md"] + [f"products/{p.name}" for p in concepts_in("products")]),
        ("Concepts and roles", ["concepts/index.md", "guides/how-it-works.md", "internal-links/entity-map.md"]),
        ("Destinations", ["destinations/index.md", "markets.md"]),
        ("Support and policies", ["faq/index.md", "policies/index.md", "citations/official-sources.md",
                                  "citations/help-center.md", "citations/blog-guides.md"]),
        ("Maintenance", ["governance/maintenance.md", "governance/open-questions.md", "governance/data-model.md",
                         "governance/evaluation.md", "log.md", "spec.md"]),
    ]
    out = ['---', 'okf_version: "0.2"', '---', '', '# Tempfind Knowledge Bundle', '',
           'Start with the [English reference](markets/en.md). It links source-reviewed facts about Tempfind Inc. and the '
           'Tempfind dental staffing platform in Canada. Current policies on tempfind.com take precedence.', '',
           'Read [maintenance rules](governance/maintenance.md) before treating a record as authoritative. Draft or stale '
           'records need current-source confirmation. `competitors/` and `internal/seo/` are editorial and excluded from the public export.', '']
    for name, rels in sections:
        out += [f"## {name}"]
        for rel in rels:
            if rel.endswith("index.md"):
                folder = rel.split('/')[0]
                out.append(f"- [{FOLDERS.get(folder, (folder.capitalize(),))[0]} index]({rel})")
            elif rel == "log.md":
                out.append("- [Change log](log.md)")
            else:
                out.append(link(rel))
        out.append("")
    out += ["## Editorial", "- [Competitor profiles](competitors/index.md)", "- [Internal SEO research](internal/seo/index.md)", ""]
    (ROOT / "index.md").write_text("\n".join(out), encoding="utf-8")


# ---------- FAQPage JSON-LD ----------

def plain(text):
    text = re.sub(r"\[\^[^\]]+\]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"\s+", " ", text.replace("**", "").replace("`", "")).strip()


def build_faqpage():
    items = []
    for p in concepts_in("faq"):
        meta, body = read(p)
        if meta.get("status") != "stable" or meta.get("audience") != "public":
            continue
        body = re.sub(r"^\[\^[^\]]+\]:.*$", "", body, flags=re.M)
        for q, a in re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, flags=re.M | re.S):
            answer = "\n".join(l for l in a.strip().splitlines() if not l.startswith("- ["))
            items.append({"@type": "Question", "name": q.strip(),
                          "acceptedAnswer": {"@type": "Answer", "text": plain(answer)}})
    doc = {"@context": "https://schema.org", "@type": "FAQPage", "@id": f"{SITE}/#faq",
           "inLanguage": "en-CA", "mainEntity": items}
    (ROOT / "docs/schema/faqpage.jsonld").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(items)


def build_structure():
    lines = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if {".git", "dist", "__pycache__"} & set(rel.parts):
            continue
        lines.append("  " * (len(rel.parts) - 1) + rel.name + ("/" if p.is_dir() else ""))
    (ROOT / "structure.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--crawl", type=Path)
    args = ap.parse_args()
    if args.crawl:
        crawl = load_crawl(args.crawl)
        build_help_center(crawl)
        missing = build_blog_guides(crawl)
        for m in missing:
            print("guide not in crawl, skipped:", m)
    build_folder_indexes()
    build_root_index()
    n = build_faqpage()
    build_structure()
    print(f"indexes rebuilt; FAQPage questions: {n}")


if __name__ == "__main__":
    main()
