---
type: MaintenancePolicy
title: Knowledge maintenance and publication
description: Authoring rules for the Tempfind knowledge bundle - required metadata, trust signals, recheck cadence and publication path.
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: draft
review_required: true
audience: public
stale_after: '2026-12-12T13:55:00Z'
sources:
- id: spec
  resource: ../spec.md
id: tempfind:governance/maintenance
---

# Knowledge maintenance and publication

This repository is the authoring source for Tempfind knowledge in Open Knowledge Format v0.2. Every fact needs an official source. Editing a record does not prove it is current.[^spec]

## Metadata

- `type` is required by OKF. This repository's profile also requires `title`, `description`, `sources`, `generated`, `status`, `audience` and `id` on every concept.
- `id` is `tempfind:<path without .md>`.
- `sources` lists every page a record relies on, each with an `id` used in body footnotes (`[^id]`).
- `generated` names the actual writer and edit time.
- `verified` is added only after a real check of the cited sources. `claude/source-review` means an automated reading of public pages; it is not Tempfind approval. A Tempfind reviewer is recorded as a role, for example `human:tempfind-ops`, never as a personal email.
- `approval_scope` states what the verification covered.
- `status: stable` requires `verified`; `status: draft` requires `review_required: true`.
- `stale_after` is an absolute recheck deadline, not proof of truth until that date.
- `[NEEDS CONFIRMATION]` marks an unconfirmed fact. A record containing it stays draft.
- `audience` is `public`, `reference` or `internal-editorial`. Internal is a label, not access control: this GitHub repository may be public.

## Precedence of sources

Versioned policies (Terms of Use, Payment Policy, cancellation and non-circumvention policies) take precedence over the pricing page, which takes precedence over landing pages, Help Center articles and blog posts. See [official sources](../citations/official-sources.md).

## Recheck cadence

| Data | Owner to assign | Cadence |
|---|---|---|
| Prices, plans, fees | Product / Finance | On change; monthly check |
| Policies (Terms, Payment, Cancellation, Non-Circumvention) | Legal / Operations | On change; monthly change detection |
| Roles and verification steps | Operations | On change; quarterly |
| City and province pages | SEO | After any URL change or migration |
| Company-reported metrics | Marketing | Monthly, with date and definition |
| Competitor profiles | SEO | Before any comparison is published |

## Publication

1. Run `python scripts/validate.py` and the tests.
2. Run `python scripts/export_public.py --out dist/okf` to build the consumer bundle. Only `audience: public`, `status: stable`, verified and fresh records are exported; drafts and editorial files are excluded.
3. Upload `dist/okf/` to `https://tempfind.com/okf/` and apply the server rules in [docs/server](../docs/server/apache-okf.conf).
4. Add the bundle section to `/llms.txt`; see [docs/llms-txt-section.md](../docs/llms-txt-section.md).

Publishing the bundle does not make any public model fetch, cite or learn from it. Google Search states it does not use such files for ranking or AI features. The bundle is a clean, sourced copy of facts; the HTML pages on tempfind.com remain the main source for search and AI answers.

[^spec]: OKF v0.2 specification copy, ../spec.md.
