# Tempfind OKF knowledge bundle

Open Knowledge Format (OKF) v0.2 bundle for tempfind.com: source-of-truth facts about Tempfind Inc. and its dental staffing platform in Canada, written as linked Markdown with YAML frontmatter for AI agents.

Target URL: `https://tempfind.com/okf/` (entry point `https://tempfind.com/okf/index.md`).

## Repository layout

| Path | Purpose | Deployed to site |
|---|---|---|
| `okf/` | The OKF bundle. Only this folder is copied to the web root. | Yes, as `/okf/` |
| `okf/index.md` | Root index with `okf_version: "0.2"` | Yes |
| `okf/log.md` | Update history, newest first | Yes |
| `integration/llms-txt-section.md` | Block to append to `/llms.txt` | Manually |
| `integration/server/` | Apache and Nginx rules for serving `/okf/` | Server config |
| `integration/schema/` | JSON-LD reference for WordPress page templates (Organization, WebSite, Service, FAQPage) | Into HTML pages, not into `/okf/` |
| `scripts/build_okf.py` | Rebuilds index files, Help Center and guides lists, FAQPage JSON-LD | No |
| `scripts/validate_okf.py` | OKF conformance and house-rule checks | No |
| `docs/PR_DESCRIPTION.md` | Review notes, open questions, site issues found | No |

The repository README and docs live outside `okf/` on purpose: in OKF every `.md` file inside the bundle other than `index.md` and `log.md` is a concept.

## Bundle rules

- Every concept has `type`, `title`, `description`, `resource` (the live page it summarizes), `sources`, `generated`, `status` and `stale_after`.
- `verified` is added only after a named Tempfind reviewer checks the facts, for example `verified: [{ by: "human:tempfind-ops", at: "2027-01-15T00:00:00Z" }]`. Use a role, not a personal email.
- Concepts start as `status: draft`. Set `status: stable` after verification.
- Unconfirmed facts are written as `[NEEDS CONFIRMATION]`.
- No marketing superlatives, no unverified statistics, no competitor names.
- Dates use 2026 as the current year. Past dates appear only as policy history.

## Update workflow

1. Edit or add concept files in `okf/`.
2. Run `python3 scripts/build_okf.py --crawl internal_html.csv` (or without `--crawl` to rebuild indexes and FAQPage only).
3. Run `python3 scripts/validate_okf.py --crawl internal_html.csv` and fix errors.
4. Add a dated entry at the top of `okf/log.md`.
5. Upload `okf/` to the site web root.

Review quarterly, and immediately after any change to pricing, policies, roles or city pages. Each concept's `stale_after` date marks when it must be rechecked.

## Deployment checklist

- `https://tempfind.com/okf/index.md` returns 200 with `Content-Type: text/markdown; charset=utf-8`.
- `/okf/` is not blocked in `robots.txt`.
- `X-Robots-Tag: noindex` is sent for `/okf/` files.
- `/okf/` is not in the XML sitemap.
- `/llms.txt` contains the Knowledge bundle section.
