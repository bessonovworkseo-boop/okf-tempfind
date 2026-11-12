# Publishing the Tempfind knowledge bundle

GitHub holds the source, history and review of the bundle. Publishing means copying a filtered export to tempfind.com. Having a repository, an OKF bundle or an llms.txt file does not by itself make any AI system crawl, cite or learn from Tempfind.

## Proposed URLs

These addresses are a plan; nothing is deployed by this repository.

| Material | Proposed location | Purpose |
|---|---|---|
| OKF export | `https://tempfind.com/okf/` (entry `index.md`) | Agents that read OKF or Markdown |
| Manifest | `https://tempfind.com/okf/manifest.json` | Included and excluded records, export time |
| Pointer | Section in `https://tempfind.com/llms.txt` | Navigation to the bundle; see [llms-txt-section.md](llms-txt-section.md) |
| JSON-LD | Page templates on tempfind.com | Organization, WebSite, Service, FAQPage; see [schema](schema/) |
| Editorial research | GitHub only (`internal/seo/`, `competitors/`) | Content team; excluded from export |

## Build

Python 3.11 or newer:

```bash
python -m pip install -r requirements.txt
python scripts/build.py            # rebuild indexes and FAQPage JSON-LD
python scripts/validate.py         # profile and OKF checks
python -m unittest discover -s tests -v
python scripts/export_public.py --out dist/okf
```

Only records with `audience: public`, `status: stable`, a `verified` entry and a future `stale_after` are exported. Links to records that are not exported are rewritten to the record's official `resource` URL or to plain text.

## Deploy

1. Upload the contents of `dist/okf/` to the web root as `/okf/`.
2. Apply [Apache](server/apache-okf.conf) or [Nginx](server/nginx-okf.conf) rules: `text/markdown; charset=utf-8`, `X-Robots-Tag: noindex`, no directory listing.
3. Confirm `/okf/` is not disallowed in robots.txt and is not in the XML sitemap.
4. Check `https://tempfind.com/okf/index.md` returns 200 with the right content type.
5. Add the llms.txt section.

## Recheck

Records expire at `stale_after` and drop out of the next export. Re-read the sources, update the record and its `verified` date, and export again. After the site migration, run `scripts/build.py --crawl <new export>` and `scripts/validate.py --crawl <new export>` to find changed URLs.
