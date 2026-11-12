---
type: EditorialReference
title: Blog content overlap
description: Near-duplicate Tempfind blog posts competing for the same queries, with merge suggestions, from the 2026-11-12 crawl.
resource: https://tempfind.com/dental-insights/
tags: [seo, content, cannibalization]
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
id: tempfind:internal/seo/content-overlap
---

# Blog content overlap

Pairs of blog posts on tempfind.com cover the same topic and compete for the same queries. The bundle links only one post per topic in [blog guides](../../citations/blog-guides.md). Traffic and ranking data were not reviewed; check Search Console before merging.[^crawl]

| Topic | Posts | Suggested keeper |
|---|---|---|
| Dental receptionist salary in Canada | /blog/dental-receptionist-salary-canada/, /blog/dental-receptionist-salary-in-canada/ | /blog/dental-receptionist-salary-canada/ (longer, 2,617 words) |
| How to become a dental assistant | /blog/how-to-become-a-dental-assistant/, /blog/how-to-become-a-dental-assistant-useful-guide/ | /blog/how-to-become-a-dental-assistant/ |
| What dental hygienists do | /blog/what-do-dental-hygienists-do/, /blog/what-does-dental-hygienist-do/ | /blog/what-do-dental-hygienists-do/ |
| Dental industry overview | /blog/dental-industry-overview-trends-and-insights/, /blog/about-remote-dental-jobs-in-canada/ (same H1) | /blog/dental-industry-overview-trends-and-insights/; retitle or merge the other |
| Finding dental assistant work | /blog/how-to-find-dental-assistant-job/, /blog/how-to-find-dental-assistant-work-ottawa/ | Keep both if the Ottawa post stays local |

[^crawl]: Crawl summary, ../../docs/checks/2026-11-12-crawl-summary.json.
