#!/usr/bin/env python3
"""Build generated parts of the Tempfind OKF v0.2 bundle.

Generates:
  okf/resources/help-center.md   (from a Screaming Frog internal_html.csv export)
  okf/resources/guides.md        (curated blog guides, titles from the crawl)
  okf/**/index.md                (directory listings; root carries okf_version)
  integration/schema/faqpage.jsonld (FAQPage built from okf/faq.md, identical text)

Usage:
  python3 scripts/build_okf.py --crawl path/to/internal_html.csv
  python3 scripts/build_okf.py            # indexes and FAQPage only
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "okf"
SITE = "https://tempfind.com"
TODAY = dt.date(2026, 11, 12)
GENERATED = '{ by: "claude/opus-5-5", at: "2026-11-12T00:00:00Z" }'
STALE_AFTER = "2027-02-12"
BANNED = re.compile(r"\b(best|leading|number one|#1|guaranteed?|fastest|lowest)\b", re.I)

# Blog guides to expose to agents. One URL per topic; near-duplicates are left out
# (see docs/PR_DESCRIPTION.md for the cannibalization list).
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


def frontmatter(fm: dict, sources: list) -> str:
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append(f"generated: {GENERATED}")
    lines.append("sources:")
    for s in sources:
        lines.append(f"  - resource: {s['resource']}")
        lines.append(f"    id: {s['id']}")
        lines.append(f"    title: {s['title']}")
        lines.append("    author: Tempfind Inc.")
    lines.append("status: draft")
    lines.append(f"stale_after: {STALE_AFTER}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def load_crawl(path):
    rows = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("Status Code") != "200" or r.get("Indexability") != "Indexable":
                continue
            p = re.sub(r"^https?://[^/]+", "", r["Address"])
            rows[p] = r.get("H1-1") or r.get("Title 1") or p
    return rows


def build_help_center(crawl):
    groups = {"for-clinics": [], "for-professionals": []}
    for p, h1 in sorted(crawl.items()):
        m = re.match(r"^/help-center/(for-clinics|for-professionals)/[^/]+/$", p)
        if m and not BANNED.search(h1):
            groups[m.group(1)].append((h1.strip(), SITE + p))
    fm = {
        "type": "Collection",
        "title": "Tempfind Help Center articles",
        "description": "List of Tempfind Help Center articles for dental clinics and dental professionals, with links to the live pages.",
        "resource": f"{SITE}/help-center/",
        "tags": "[help-center, support, clinics, professionals]",
        "language": "en-CA",
    }
    src = [
        {"resource": f"{SITE}/help-center/for-clinics/", "id": "help-clinics", "title": "Help Topics For Dental Clinics"},
        {"resource": f"{SITE}/help-center/for-professionals/", "id": "help-pros", "title": "Help Topics For Dental Professionals"},
    ]
    body = [
        "# Tempfind Help Center articles",
        "",
        f"The Tempfind Help Center lives at {SITE}/help-center/ and has {len(groups['for-clinics'])} articles for clinics "
        f"and {len(groups['for-professionals'])} articles for professionals listed below. Titles are copied from the live pages. "
        "Some older articles describe direct payment from clinic to professional; the current rules are in "
        "[Payments and payouts](../platform/payments.md).",
        "",
        "## Articles for dental clinics",
        "",
    ]
    body += [f"- [{t}]({u})" for t, u in groups["for-clinics"]]
    body += ["", "## Articles for dental professionals", ""]
    body += [f"- [{t}]({u})" for t, u in groups["for-professionals"]]
    body += ["", "## Related concepts", "", "- [Frequently asked questions](../faq.md)", "- [How Tempfind works](../platform/how-it-works.md)", ""]
    (BUNDLE / "resources" / "help-center.md").write_text(frontmatter(fm, src) + "\n" + "\n".join(body), encoding="utf-8")


def build_guides(crawl):
    fm = {
        "type": "Collection",
        "title": "Tempfind career and staffing guides",
        "description": "Curated Tempfind blog guides on dental hygienist, assistant and receptionist careers in Canada and on temporary staffing for clinics.",
        "resource": f"{SITE}/dental-insights/",
        "tags": "[guides, blog, careers, salary, staffing]",
        "language": "en-CA",
    }
    src = [{"resource": f"{SITE}/dental-insights/", "id": "insights", "title": "Dental Insights"}]
    body = [
        "# Tempfind career and staffing guides",
        "",
        "A curated selection of articles from the Tempfind blog. Salary figures in these articles are estimates published by "
        "Tempfind; they are not platform rates. Each professional sets their own hourly rate.",
        "",
    ]
    missing = []
    for section, paths in GUIDES.items():
        body += [f"## {section}", ""]
        for p in paths:
            if crawl is not None and p not in crawl:
                missing.append(p)
                continue
            title = crawl[p].strip() if crawl else p
            if BANNED.search(title):
                # keep the link, drop the marketing tail of the page title
                title = title.split(":")[0].strip()
            body.append(f"- [{title}]({SITE}{p})")
        body.append("")
    body += ["## Related concepts", "", "- [Roles](../roles/index.md)", "- [Glossary](../glossary.md)", ""]
    (BUNDLE / "resources" / "guides.md").write_text(frontmatter(fm, src) + "\n" + "\n".join(body), encoding="utf-8")
    return missing


FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def read_fm(path):
    m = FM_RE.match(path.read_text(encoding="utf-8"))
    out = {}
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"^(title|description|type):\s*(.+)$", line)
            if mm:
                out[mm.group(1)] = mm.group(2).strip().strip('"')
    return out


SECTION_NAMES = {
    "company": "Company",
    "platform": "Platform and services",
    "pricing": "Pricing",
    "policies": "Policies",
    "roles": "Roles",
    "locations": "Locations",
    "resources": "Resources",
}
ORDER = ["company", "platform", "pricing", "roles", "locations", "policies", "resources"]


def build_indexes():
    # Sub-directory indexes: no frontmatter (SPEC: only the bundle root may carry okf_version).
    for d in ORDER:
        folder = BUNDLE / d
        concepts = sorted(p for p in folder.glob("*.md") if p.name not in ("index.md", "log.md"))
        lines = [f"# {SECTION_NAMES[d]}", ""]
        for p in concepts:
            fm = read_fm(p)
            lines.append(f"* [{fm.get('title', p.stem)}](./{p.name}) - {fm.get('description', '')}")
        (folder / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    top = sorted(p for p in BUNDLE.glob("*.md") if p.name not in ("index.md", "log.md"))
    lines = [
        "---",
        'okf_version: "0.2"',
        "---",
        "",
        "# Tempfind knowledge bundle",
        "",
        "Source-of-truth facts about Tempfind Inc. and the Tempfind dental staffing platform in Canada, "
        "written as an Open Knowledge Format (OKF) v0.2 bundle for AI agents and people. "
        f"Every concept links to the live page it summarizes on {SITE}. "
        "The live pages and published policies prevail if anything here differs. "
        "Concepts are drafts until verified by Tempfind; see `status` and `stale_after` in each file. "
        "Update history: [log.md](./log.md).",
        "",
        "## Start here",
        "",
    ]
    for p in top:
        fm = read_fm(p)
        lines.append(f"* [{fm.get('title', p.stem)}](./{p.name}) - {fm.get('description', '')}")
    for d in ORDER:
        lines += ["", f"## {SECTION_NAMES[d]}", ""]
        for p in sorted(x for x in (BUNDLE / d).glob("*.md") if x.name not in ("index.md", "log.md")):
            fm = read_fm(p)
            lines.append(f"* [{fm.get('title', p.stem)}](./{d}/{p.name}) - {fm.get('description', '')}")
    (BUNDLE / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def md_to_text(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def build_faqpage():
    text = FM_RE.sub("", (BUNDLE / "faq.md").read_text(encoding="utf-8"))
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    qa = []
    for i in range(1, len(parts), 2):
        q, a = parts[i].strip(), parts[i + 1].strip()
        if q.lower().startswith("related concepts"):
            continue
        qa.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": md_to_text(a)},
        })
    doc = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{SITE}/#faq",
        "inLanguage": "en-CA",
        "dateModified": TODAY.isoformat(),
        "mainEntity": qa,
    }
    out = ROOT / "integration" / "schema" / "faqpage.jsonld"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(qa)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crawl", help="Screaming Frog internal_html.csv export")
    args = ap.parse_args()
    if args.crawl:
        crawl = load_crawl(args.crawl)
        build_help_center(crawl)
        missing = build_guides(crawl)
        if missing:
            print("Guides not found in crawl (skipped):", *missing, sep="\n  ")
    build_indexes()
    n = build_faqpage()
    print(f"Indexes rebuilt; FAQPage has {n} questions.")


if __name__ == "__main__":
    main()
