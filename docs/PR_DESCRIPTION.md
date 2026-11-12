# Add /okf/ AI knowledge bundle (OKF v0.2) and llms.txt reference

## 1. Summary

- Built an Open Knowledge Format v0.2 bundle for tempfind.com: 24 concept files, 8 index files, 1 log file.
- Sources: Screaming Frog crawl of 2026-11-12 (954 URLs, 918 indexable) and live pages read on 2026-11-12: homepage, clinics, pricing, professionals, About Us, HR Concierge, Terms of Use, Payment Policy, cancellation policies, Non-Circumvention Policy, Ottawa page, RDH and dental assistant hire pages, job board, Help Center articles on verification and fees.
- All concepts are `status: draft`, `stale_after: 2027-02-12`, no `verified` field. Facts not confirmed on live pages are marked `[NEEDS CONFIRMATION]` (23 markers in concepts).
- Validator: 0 errors. Warnings: 5 short role concepts, 3 lines with 2025 policy dates (historical, kept on purpose).
- Every tempfind.com URL in the bundle exists in the crawl as 200 indexable.

### Changes from the original brief (to comply with OKF v0.2)

| Brief | Done instead | Reason |
|---|---|---|
| `okf/README.md` | `README.md` at repo root | Any `.md` in the bundle other than `index.md` and `log.md` is a concept and must have `type` |
| `okf/okf.json` manifest | Root `index.md` with `okf_version: "0.2"` | OKF declares the version only in the root index; a JSON manifest is not part of the spec |
| `okf/changelog.md` | `okf/log.md` with `## YYYY-MM-DD` headings | Reserved filename defined by the spec |
| Frontmatter `canonical_url`, `summary`, `last_verified`, `source_urls` | `resource`, `description`, `generated`, `sources`, `status`, `stale_after` | OKF v0.2 field names |
| `okf/schema/*.jsonld` | `integration/schema/*.jsonld` | Schema.org is read from HTML pages; kept out of the bundle |
| `learn.tempfind.com` as Help Center | `tempfind.com/help-center/` | The crawl and live site show the Help Center under `/help-center/` |
| One file per city | `locations/service-area.md` plus `locations/ottawa.md` | Only Ottawa was read in full; 13 other city pages need review before separate files |

### Not done in this PR

- `/llms.txt` edit: the live file and the WordPress repo are not in this repository. The block to append is in `integration/llms-txt-section.md`.
- Server headers: no server config exists in this repository. Apache and Nginx rules are in `integration/server/`.
- `robots.txt` check: not in this repository. Confirm `/okf/` is not disallowed.
- `ai-catalog.json` (Agentic Resource Discovery): not created; optional, separate spec.

## 2. Files

| File | Canonical URL | Fact it anchors | User question it answers | Schema type for the HTML page |
|---|---|---|---|---|
| company/tempfind.md | /about-us/ | Tempfind Inc., Ontario corporation, Canada scope, not an employer | What is Tempfind and who runs it? | Organization |
| platform/how-it-works.md | / | Two booking routes, professional flow, hours approval | How does Tempfind work? | HowTo |
| platform/for-clinics.md | /dental-clinics/ | Clinic tools, roles, responsibilities | How can my clinic find temp dental staff? | Service |
| platform/for-professionals.md | /dental-professionals/ | Free for professionals, eligibility, rate control | How do I get dental temp shifts? | Service |
| platform/verification.md | /help-center/.../professional-verification-process/ | Manual document review before access | Are Tempfind professionals verified? | Article |
| platform/payments.md | /payment-policy/ | Card payments via Stripe, 24-hour approval, 3 to 5 business day payout, 3.9% fee | How and when are temps paid? | Article |
| platform/hr-concierge.md | /hr-concierge/ | Assisted matching, 30-day candidate commitment, direct hire | Can Tempfind help hire long-term staff? | Service |
| pricing/clinic-plans.md | /dental-clinics/pricing/ | $49 per shift, $149 per month, Enterprise custom | How much does Tempfind cost? | Service + Offer |
| policies/cancellation.md | /cancelation-policy/ | 48-hour notice, no-show rules, $500 deposit | What if a temp cancels? | Article |
| policies/non-circumvention.md | /non-circumvention-policy/ | 12-month rule, fees, legitimate paths | Can we hire a temp directly? | Article |
| policies/terms-of-use.md | /terms-of-use/ | Eligibility, governing law, role of Tempfind | Who can use Tempfind? | Article |
| roles/*.md (7) | /professionals/<role>/all-cities/ | Role booking, profile data, sample rates | How do I hire a temp hygienist or assistant? | Service + BreadcrumbList |
| locations/service-area.md | / | 14 city pages, Canada scope | Where does Tempfind operate? | ItemList |
| locations/ottawa.md | /dental-staffing-agency-ottawa/ | Ottawa roles, booking steps | Is there dental staffing in Ottawa? | Service (areaServed City) |
| faq.md | /help-center/ | 19 short answers | Common questions | FAQPage |
| glossary.md | /blog/basic-dental-terminology/ | Neutral term definitions | What is an RDH, HARP, locum? | DefinedTermSet |
| resources/help-center.md | /help-center/ | 62 Help Center links | Where is the help article for X? | CollectionPage |
| resources/guides.md | /dental-insights/ | 21 curated blog guides | Where can I read about salaries and careers? | ItemList |

## 3. [NEEDS CONFIRMATION]

| File | Line | Question for Tempfind |
|---|---|---|
| company/tempfind.md | 68 | Founding year |
| company/tempfind.md | 69 | Primary phone: 1-877-455-3513 (homepage) or 416-839-6682 (About Us, Ottawa) |
| company/tempfind.md | 70 | One verified figure for clinics and professionals: pages show 10,715 clinics, 10,340 clinics and professionals, 2,177 clinics, 2,000+ clinics and 1,100+ clinics |
| platform/for-clinics.md | 32 | Is RN booking live, or coming soon? |
| platform/for-clinics.md | 44 | Can clinics post permanent jobs on the job board? Role pages say temporary only |
| platform/how-it-works.md | 69 | Same: align permanent-hiring wording across role pages and HR Concierge |
| platform/for-professionals.md | 70 | Payout timing: 2 to 3 days (landing page) vs 3 to 5 business days (Payment Policy) |
| platform/payments.md | 50 | Retire Help Center and job board text that describes direct clinic-to-professional payment |
| platform/payments.md | 58 | Currency of all prices (CAD assumed in JSON-LD) |
| platform/verification.md | 45 | Does every professional have a one-on-one interview? |
| platform/verification.md | 53 | Verification turnaround time |
| platform/hr-concierge.md | 51 | Direct-hire agency fee amount |
| pricing/clinic-plans.md | 39 | Currency |
| pricing/clinic-plans.md | 69 | Free trial terms; do job board hires carry the $49 fee? |
| policies/cancellation.md | 59 | Clinic cancellation notice period and compensation amounts |
| policies/cancellation.md | 63 | Steps when a professional does not arrive |
| policies/non-circumvention.md | 46 | Direct Recruitment Policy agency fee amount |
| roles/dental-receptionist.md | 42 | Typical receptionist rate range |
| roles/dentist-dds.md | 40 | Provincial licensing bodies to name |
| roles/sedation-general-nurse-rn.md | 28 | RN booking status |
| locations/service-area.md | 64 | US availability (Terms say Canada; New York, New Jersey and Texas pages exist) |
| locations/service-area.md | 68 | Quebec, Saskatchewan, Nova Scotia coverage |
| locations/ottawa.md | 50 | French-language service in Ottawa |

## 4. URLs to re-verify after migration

All `resource` and `sources` URLs in the bundle, plus the 62 Help Center and 21 blog URLs in `okf/resources/`. After migration, run:

```
python3 scripts/build_okf.py --crawl <new internal_html.csv>
python3 scripts/validate_okf.py --crawl <new internal_html.csv>
```

The validator lists every tempfind.com URL that is not a 200 indexable page in the new crawl.

## 5. Server and robots changes

| Item | Status |
|---|---|
| Serve `/okf/*.md` as `text/markdown; charset=utf-8` | Proposed: `integration/server/` |
| `X-Robots-Tag: noindex` on `/okf/` | Proposed: Markdown copies duplicate HTML pages |
| No `Disallow: /okf/` in robots.txt | To check |
| `/okf/` excluded from XML sitemap | To check |
| `/llms.txt` Knowledge bundle section | Proposed: `integration/llms-txt-section.md` |
| JSON-LD in page templates | Proposed: `integration/schema/` |

## 6. Site issues found while building the bundle

These affect AI answers about Tempfind more than the bundle does. Fixing them on the HTML pages is the priority.

| Priority | Issue | Where | Fix |
|---|---|---|---|
| High | Five different clinic counts across pages | Homepage, /dental-clinics/, /about-us/, city pages, meta descriptions | One dated, sourced figure everywhere |
| High | Help Center and job board describe direct payment to professionals; Payment Policy requires platform card payments from 2026-01-01 | /help-center/for-clinics/how-and-when-do-we-pay-to-a-professional/, /paying-directly-to-the-professional/, /find-a-job/ FAQ | Update or redirect |
| High | Help Center fee article describes the $99 Essential plan as current; it closed on 2025-06-30 | /help-center/for-clinics/what-is-tempfind-placement-fee/ | Rewrite for Pay Per Shift, Business, Enterprise |
| High | Permanent hiring: role pages say temporary only, HR Concierge and Ottawa page offer direct hire | /professionals/*/all-cities/, /hr-concierge/ | Align wording |
| Medium | Two phone numbers | Homepage, About Us, Ottawa | One primary number |
| Medium | Unsupported superlatives in H1 and meta ("Premier", "Fastest", "Lowest", "New Leader") | /, /dental-clinics/, /dental-clinics/pricing/, /tempfind-vs-tempstars/, Help Center fee article | Replace with checkable statements |
| Medium | Policy pages with `%date%` placeholder or raw policy text as meta description | /booking-policy/, /payment-policy/, /professionals-compensation-policy/ | Real effective dates and written descriptions |
| Medium | 275 city slugs in role and job URLs, 90 in the US, with duplicates and typos (`mississauaga_on`, `orleans_on` and `orléans_on`, `burnaby_on`, `montreal_qc` and `montréal_qc`) | /professionals/, /find-a-job/ | Canonical city list, 301 duplicates |
| Medium | Near-duplicate blog posts competing for the same query | receptionist salary (2 posts), how to become a dental assistant (2), what hygienists do (2), industry overview (2) | Merge and 301 |
| Low | Payout timing differs (2 to 3 days vs 3 to 5 business days) | /dental-professionals/ vs /payment-policy/ | Use the policy figure |

## 7. Maintenance

- Update `stale_after`, `sources` and `log.md` on every content or URL change.
- Add `verified` with a role-based actor (`human:tempfind-ops`) only after review; then set `status: stable`.
- Review quarterly. Next review due 2027-02-12.
- OKF governance is moving from GoogleCloudPlatform to a vendor-neutral repository with a planned v0.3. Recheck field names when v0.3 is published.
