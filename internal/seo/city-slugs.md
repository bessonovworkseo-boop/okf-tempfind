---
type: EditorialReference
title: City slug audit for role and job pages
description: Duplicate, malformed and out-of-market city slugs in /professionals/ and /find-a-job/ URLs from the 2026-11-12 crawl.
resource: https://tempfind.com/professionals/
tags: [seo, technical, url-structure]
language: en-CA
sources:
- id: crawl
  resource: ../../docs/checks/2026-11-12-crawl-summary.json
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: draft
review_required: true
audience: internal-editorial
stale_after: '2026-12-12T13:55:00Z'
id: tempfind:internal/seo/city-slugs
---

# City slug audit for role and job pages

The 2026-11-12 crawl found 741 indexable role-by-city and job-by-city pages across 276 city slugs. Of these, 147 pages use 92 US slugs. Median unique inlinks per page is 5. Several slugs duplicate one place under two spellings or attach a city to the wrong province.[^crawl]

## Duplicates and mismatches

| Place | Slugs found | Pages | Issue | Suggested canonical |
|---|---|---|---|---|
| Orléans, ON | `orleans_on`, `orléans_on` | 5 | Accent variant | `orleans_on` |
| Montréal, QC | `montreal_qc`, `montréal_qc` | 2 | Accent variant | `montreal_qc` |
| Mississauga, ON | `mississauga`, `mississauaga_on` | 1 malformed | Typo in slug | `mississauga` |
| Burnaby | `burnaby_bc`, `burnaby_on` | 17 | `burnaby_on` H1 reads "Burnaby, Wainfleet, Ontario" | Review; likely remove `burnaby_on` |
| Saanich, BC | `saanich`, `saanich_bc` | 2 | Missing province suffix | `saanich_bc` |
| Flushing, NY | `flushing`, `flushing_ny` | 3 | Missing state suffix | `flushing_ny` |
| Far Rockaway, NY | `far-rockaway`, `far-rockaway_ny` | 3 | Missing state suffix | `far-rockaway_ny` |
| Lake Placid, NY | `lake` | 1 | Truncated slug | `lake-placid_ny` |
| Richmond, BC | `/professionals/all-specialists/richmond_bc/` | 1 | Title shown in search: "Dental Staffing in Richmond Hill, ON" | Fix title |

`richmond-hill` (Ontario) and `richmond-hill_ny`, `belleville_on` and `belleville_nj`, `wilmot_on` and `wilmot_ns` are different places and are not duplicates.

## Out-of-market pages

US slugs include New York, New Jersey, Texas, California, Illinois, North Carolina, Connecticut and Alabama localities (for example `nymph_al`, `stamford_ct`). The Terms of Use apply to individuals residing in Canada. Decide whether US pages stay indexable; if not, noindex or remove them.

## Recommendation

1. Build one canonical city list with province or state suffix for every slug.
2. 301 duplicates to the canonical slug and update internal links.
3. Keep city pages only where professionals or clinics are active, or merge thin pages into a province page.
4. Re-run the crawl and `scripts/build.py --crawl` after the change.

[^crawl]: Crawl summary, ../../docs/checks/2026-11-12-crawl-summary.json.
