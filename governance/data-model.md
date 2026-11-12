---
type: PublishingProfile
title: Tempfind knowledge data model and ownership
description: Entities, required fields, authoritative sources and owners for Tempfind knowledge records.
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: draft
review_required: true
audience: reference
sources:
- id: spec
  resource: ../spec.md
- id: products
  resource: ../products/index.md
id: tempfind:governance/data-model
---

# Tempfind knowledge data model and ownership

This is a Tempfind authoring profile on top of OKF v0.2, not a separate standard. Record IDs use `tempfind:<path without .md>`. Links between records express relationships; `sources` express evidence.[^spec][^products]

## Folders

| Folder | Holds | Audience |
|---|---|---|
| `brand/` | Company identity, wording rules, reported metrics | public |
| `products/` | Clinic and professional services, HR Concierge, pricing | public |
| `concepts/` | Roles, verification, platform vs agency, glossary | public |
| `guides/` | Step-by-step processes | public |
| `destinations/` | Cities and provinces | public |
| `policies/` | Scoped summaries of Tempfind policies | public |
| `faq/` | Short answers that link to the records above | public |
| `citations/` | Official source directory, Help Center and blog lists | public |
| `markets.md`, `markets/` | Language and market references | public |
| `internal-links/` | Relationship map between records | public |
| `competitors/` | Neutral competitor profiles | internal-editorial |
| `internal/seo/` | Site issues and editorial research | internal-editorial |
| `governance/` | Rules, open questions, evaluation | public or reference |
| `evaluations/` | Test prompts and expected answers | not exported |
| `docs/` | Publication notes, server rules, JSON-LD, reviews | not exported |

## Entities

| Entity | Required fields | Authoritative source | Owner to assign | Refresh |
|---|---|---|---|---|
| Company | Legal name, jurisdiction, address in Terms, official URLs | Terms of Use, About Us | Legal / Marketing | On change |
| Product or service | Name, audience, what it includes, plan availability | Product pages, pricing page | Product | On change |
| Plan | Name, price, currency, billing unit, term, inclusions | Pricing page, Payment Policy | Product / Finance | On change; monthly |
| Fee | Name, amount or rate, who pays, when charged | Payment Policy, pricing page | Finance | On change |
| Role | Title, booking routes, verification items, page URLs | Role pages | Operations / SEO | Quarterly |
| Destination | City or province, page URL, status of coverage | City pages, Terms | SEO / Operations | After URL changes |
| Policy | Name, version, effective date, key rules, URL | Policy page | Legal | Immediately on change |
| Metric | Value, definition, date, page | Page showing it | Marketing | Monthly |

Unknown is not false. A field without evidence is omitted or marked `[NEEDS CONFIRMATION]`; it is never filled with a guess.

[^spec]: OKF v0.2 specification copy, ../spec.md.
[^products]: Product index, ../products/index.md.
