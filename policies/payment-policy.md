---
type: Policy
title: Payments and payouts on Tempfind
description: How shift payments work on Tempfind - card payments through Stripe, hours approval within
  24 hours, payout in 3 to 5 business days, 3.9% handling fee.
resource: https://tempfind.com/payment-policy/
tags:
- payments
- payouts
- stripe
- handling-fee
- hours-approval
language: en-CA
sources:
- id: payment
  resource: https://tempfind.com/payment-policy/
  title: Payment Policy (Version 2.1)
- id: pricing
  resource: https://tempfind.com/dental-clinics/pricing/
  title: Dental Staffing Plans and Pricing
- id: hr
  resource: https://tempfind.com/hr-concierge/
  title: HR Concierge
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: stable
audience: public
verified:
- by: claude/source-review
  at: '2026-11-12T13:55:00Z'
approval_scope: Automated reading of the cited public pages on 2026-11-12; no human Tempfind approval implied.
stale_after: '2026-12-12T13:55:00Z'
id: tempfind:policies/payment-policy
---

# Payments and payouts on Tempfind

Clinics pay for shifts by credit card through Tempfind, processed by Stripe. Professionals submit hours after each shift, clinics approve them, and the professional is paid within 3 to 5 business days after approval. Tempfind does not store card details.[^payment][^pricing][^hr]

## How does the payment flow work?

1. The professional completes the shift and submits worked hours.
2. The clinic has 24 hours to confirm or dispute the hours. Without action, hours are auto-approved.
3. The clinic's card on file is charged for the shift total plus the 3.9% payment handling fee.
4. Payment is disbursed to the professional within 3 to 5 business days after approval.

If a professional is sent home early through no fault of their own, they are paid for the scheduled hours.

## Must all clinics pay through Tempfind?

Yes, under the current Payment Policy (Version 2.1):

- Clinics registered on or after July 1, 2025 pay by credit card through Tempfind.
- Clinics registered earlier lost the direct-payment option on October 1, 2025.
- Grandfathered Essential plan clinics could pay professionals directly until January 1, 2026.
- From January 1, 2026, all clinics use Tempfind card processing.

The HR Concierge page states that e-transfer and cheque payments to professionals are not allowed.

Some Help Center articles and the job board FAQ still describe direct payment from clinic to professional. The Payment Policy takes precedence; see [open questions](../governance/open-questions.md).

## What is the payment handling fee?

3.9% of the professional's shift total (hourly rate multiplied by hours worked). It covers card processing, payout administration and transaction oversight.

Example from the Payment Policy: 7 hours at $50 per hour is a $350 shift total, and the handling fee is $13.65.

Currency: the policy shows dollar amounts without naming the currency. State amounts as shown, without adding a currency; see [open questions](../governance/open-questions.md).

## When are clinics billed?

- Membership fees: monthly in advance on the enrolment date.
- Pay Per Shift placement fee: when a shift is completed.
- Enterprise: according to the signed agreement.

## Can payments be refunded or disputed?

- Membership fees, shift payments and handling fees are non-refundable, except as required by law.
- Billing disputes must be reported within 10 business days of the charge date. Tempfind aims to respond within 10 business days.
- Unauthorized chargebacks may lead to suspension or termination.

## Related concepts

- [Clinic plans and fees](../products/pricing.md)
- [Services for professionals](../products/for-professionals.md)
- [Cancellation rules](cancellation-policy.md)

[^payment]: Payment Policy (Version 2.1), https://tempfind.com/payment-policy/, checked 2026-11-12.
[^pricing]: Dental Staffing Plans and Pricing, https://tempfind.com/dental-clinics/pricing/, checked 2026-11-12.
[^hr]: HR Concierge, https://tempfind.com/hr-concierge/, checked 2026-11-12.
