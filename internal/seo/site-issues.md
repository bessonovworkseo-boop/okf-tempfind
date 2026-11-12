---
type: EditorialReference
title: tempfind.com issues that affect AI answers
description: Inconsistencies and unsupported claims on tempfind.com found while building the bundle on 2026-11-12, with priority and fix.
resource: https://tempfind.com/
tags: [seo, geo, site-issues]
language: en-CA
sources:
- id: crawl
  resource: ../../docs/checks/2026-11-12-crawl-summary.json
- id: review
  resource: ../../docs/review-2026-11-12.md
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: draft
review_required: true
audience: internal-editorial
stale_after: '2026-12-12T13:55:00Z'
id: tempfind:internal/seo/site-issues
---

# tempfind.com issues that affect AI answers

AI assistants answer about Tempfind mainly from the HTML pages on tempfind.com, not from this bundle. Where pages contradict each other, assistants may repeat the wrong version. The issues below were found in the 2026-11-12 crawl and page reads.[^crawl][^review]

| Priority | Issue | Pages | Fix | Team |
|---|---|---|---|---|
| High | Five different clinic counts (10,715; 10,340; 2,177; 2,000+; 1,100+), all undated | /, /dental-clinics/, /about-us/, city pages, meta descriptions | One dated, defined figure, reused everywhere | Marketing |
| High | Help Center and job board FAQ describe direct payment to professionals; Payment Policy requires platform card payments from 2026-01-01 | /help-center/for-clinics/how-and-when-do-we-pay-to-a-professional/, /help-center/for-clinics/paying-directly-to-the-professional/, /find-a-job/ | Rewrite or 301 to the payment article | Support / Content |
| High | Fee article describes the $99 Essential plan as current; closed to new clinics on 2025-06-30 | /help-center/for-clinics/what-is-tempfind-placement-fee/ | Rewrite for Pay Per Shift, Business, Enterprise | Support |
| High | Role pages say the platform is temporary only; HR Concierge and Ottawa page offer direct hire; Help Center allows permanent postings | /professionals/*/all-cities/, /hr-concierge/, Help Center | One consistent statement | Product / Content |
| High | Comparison page shows outdated figures: TempStars $72 and "$80+", Tempfind $99 and $149, no sources | /tempfind-vs-tempstars/ | Update to dated, sourced figures; remove unsupported claims | Marketing |
| Medium | Two phone numbers | /, /about-us/, city pages | One primary number in footer and schema | Marketing |
| Medium | Unsupported superlatives in H1 and meta: "Premier", "Fastest", "Lowest", "New Leader" | /, /dental-clinics/, /dental-clinics/pricing/, /tempfind-vs-tempstars/, Help Center fee article | Replace with checkable statements | Content |
| Medium | Payout timing differs: 2 to 3 days vs 3 to 5 business days | /dental-professionals/, /payment-policy/ | Use the policy figure | Content |
| Medium | Policy meta descriptions show `%date%` or raw policy text | /booking-policy/, /payment-policy/, /professionals-compensation-policy/ | Real effective dates and written descriptions | Developer |
| Medium | RN listed as coming soon on one page and bookable on role pages | /dental-clinics/, /professionals/sedation-general-nurse-(rn)/all-cities/ | Align | Product |
| Medium | City slug duplicates and mismatches; see [city slugs](city-slugs.md) | /professionals/, /find-a-job/ | Canonical city list, 301 duplicates | SEO / Developer |
| Medium | Near-duplicate blog posts; see [content overlap](content-overlap.md) | /blog/ | Merge and 301 | SEO |
| Low | No Organization, Service or FAQPage JSON-LD reviewed for consistency with visible text | Templates | Use docs/schema as a reference | Developer |

[^crawl]: Crawl summary, ../../docs/checks/2026-11-12-crawl-summary.json.
[^review]: Source review, ../../docs/review-2026-11-12.md.
