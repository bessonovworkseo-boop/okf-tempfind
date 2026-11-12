# Tempfind Open Knowledge Format bundle

Knowledge about Tempfind Inc. and the Tempfind dental staffing platform in Canada, following [Open Knowledge Format v0.2](spec.md). Start with the [English reference](markets/en.md) or the [bundle index](index.md).

## Scope and trust

This repository holds reviewed public records, drafts awaiting confirmation and editorial research. Being in the repository does not make a claim verified. Current policies on tempfind.com take precedence.

`verified.by: claude/source-review` records an automated reading of the cited public pages on the stated date. It is not Tempfind approval. Record a real Tempfind review separately, with a role-based actor such as `human:tempfind-ops`. See [maintenance](governance/maintenance.md) and [open questions](governance/open-questions.md).

`competitors/` and `internal/seo/` are labelled `internal-editorial` and are excluded from the public export. The label is not access control: if this repository is public, so are those files.

## Structure

| Folder | Contents |
|---|---|
| `brand/` | Company facts, wording rules, reported metrics |
| `products/` | Services for clinics and professionals, HR Concierge, pricing |
| `concepts/` | Roles, verification, platform vs agency, glossary |
| `guides/` | How Tempfind works, step by step |
| `destinations/` | Cities, provinces, Ottawa |
| `policies/` | Terms, payment, cancellation and non-circumvention summaries |
| `faq/` | Ten topic FAQs |
| `citations/` | Official sources, Help Center and blog lists |
| `markets.md`, `markets/` | Language and market inventory, English reference |
| `internal-links/` | Entity relationship map |
| `competitors/` | Neutral competitor profiles (editorial) |
| `internal/seo/` | Site issues, city slugs, content overlap (editorial) |
| `governance/` | Maintenance rules, data model, open questions, evaluation protocol |
| `evaluations/` | AI answer test cases and result template |
| `docs/` | Publication plan, site follow-up, server rules, JSON-LD, review notes, crawl summary |
| `scripts/`, `tests/` | Build, validation, export and tests |

## Validate

```bash
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

With a Screaming Frog `internal_html.csv` export, `python scripts/build.py --crawl internal_html.csv` refreshes the Help Center and blog lists, and `python scripts/validate.py --crawl internal_html.csv` flags any tempfind.com URL that is no longer a 200 indexable page. Validation does not prove factual accuracy.

## Export for https://tempfind.com/okf/

```bash
python scripts/export_public.py --out dist/okf
```

Only public, stable, verified and fresh records are exported. The export is a conformant OKF bundle with its own `index.md`, `log.md` and `manifest.json`. Records past `stale_after` drop out until they are rechecked. Deployment steps: [docs/publication.md](docs/publication.md).

## Website follow-up

Repository changes do not change tempfind.com, its llms.txt, robots rules or Schema.org. See [site follow-up](docs/site-follow-up.md). No AI crawling, citation or recommendation is promised by publishing the bundle.

## Licensing

The bundled [specification](spec.md) is from GoogleCloudPlatform/open-knowledge-format under the Apache-2.0 license; see [docs/OKF-LICENSE.txt](docs/OKF-LICENSE.txt). No license for Tempfind content is implied.
