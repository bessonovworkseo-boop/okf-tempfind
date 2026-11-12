---
type: Reference
title: Tempfind knowledge relationships
description: Map of relationships between Tempfind company, products, roles, policies, fees and locations, as links between records.
resource: https://tempfind.com/
tags: [entity-map, relationships]
language: en-CA
sources:
- id: home
  resource: https://tempfind.com/
  title: Homepage
- id: pricing
  resource: https://tempfind.com/dental-clinics/pricing/
  title: Dental Staffing Plans and Pricing
- id: terms
  resource: https://tempfind.com/terms-of-use/
  title: Terms of Use (Version 4, updated 2026-08-11)
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: stable
audience: public
verified:
- by: claude/source-review
  at: '2026-11-12T13:55:00Z'
approval_scope: Relationships taken from the cited public pages on 2026-11-12; no human Tempfind approval implied.
stale_after: '2026-12-12T13:55:00Z'
id: tempfind:internal-links/entity-map
---

# Tempfind knowledge relationships

This map shows how Tempfind entities relate. It describes relationships, not anchor-text targets for site pages.[^home][^pricing][^terms]

| Subject | Relationship | Target |
|---|---|---|
| Tempfind Inc. | Operates | [Tempfind platform](../brand/company.md) |
| Tempfind Inc. | Is not the employer of | [Dental professionals](../products/for-professionals.md) |
| Dental clinic | Books shifts through | [Services for clinics](../products/for-clinics.md) |
| Dental clinic | Pays for shifts under | [Payment policy](../policies/payment-policy.md) |
| Dental clinic | Chooses a plan from | [Pricing](../products/pricing.md) |
| Business and Enterprise plans | Include | [HR Concierge](../products/hr-concierge.md) |
| Dental professional | Must pass | [Professional verification](../concepts/professional-verification.md) |
| Dental professional | Is bound by | [Cancellation policy](../policies/cancellation-policy.md) |
| Clinic and professional | Are bound by | [Non-circumvention policy](../policies/non-circumvention-policy.md) |
| Registered dental hygienist | Is a role on | [Tempfind](../concepts/registered-dental-hygienist.md) |
| Dental assistant | Is a role on | [Tempfind](../concepts/dental-assistant.md) |
| Ottawa | Has a city page within | [Cities](../destinations/cities.md) |
| Direct hire | Runs through | [HR Concierge](../products/hr-concierge.md) and the Direct Recruitment Policy |

[^home]: Homepage, https://tempfind.com/, checked 2026-11-12.
[^pricing]: Dental Staffing Plans and Pricing, https://tempfind.com/dental-clinics/pricing/, checked 2026-11-12.
[^terms]: Terms of Use (Version 4, updated 2026-08-11), https://tempfind.com/terms-of-use/, checked 2026-11-12.
