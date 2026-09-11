---
name: screaming-frog-analyzer
description: Analyze a Screaming Frog crawl export (CSV/Excel) to identify technical and on-page SEO problems, cluster them by template/directory, and prioritize fixes. Use when given an Internal HTML export, crawl CSV, redirect-chain report, inlinks export, or when asked to audit Screaming Frog results, find crawl issues, or rank SEO fixes.
---

# Screaming Frog Analyzer

Turn a Screaming Frog crawl export into a clustered, prioritized fix list. Do not scroll the CSV by eye and do not paste the file into the model context.

## Required inputs

- One or more Screaming Frog exports. Best starting file: **Internal** tab, filtered to **HTML**, exported as CSV.
- Optional extras that fill gaps:
    - `Reports > Redirects > Redirect Chains`
    - `Bulk Export > All Inlinks`
    - Images tab export
- Site context if known: CMS (including Treehouse/ATB), primary conversion URLs, locales.

If the user has not attached a file, ask for the Internal HTML CSV and tell them how to export it:

1. Finish the crawl.
2. Internal tab → Filter: HTML.
3. Export (CSV). Include Title, Meta Description, H1, Canonical, Indexability, Word Count, Unique Inlinks, Crawl Depth, Response Time when those columns are enabled.

## Workflow

1. **Locate the exports**
    - Prefer files named like `internal_html.csv`, `internal_all.csv`, or anything with `Address` + `Status Code` headers.
    - Accept a folder of CSVs. Google Sheets links should be downloaded as CSV before analysis.
    - Convert `.xlsx` to CSV if needed. Do not invent columns that are not in the file.
2. **Run the bundled analyzer**
    - Script: [scripts/analyze_crawl.py](scripts/analyze_crawl.py)
    - Catalog: [references/issue-catalog.md](references/issue-catalog.md)
    - Command:

      ```bash
      python3 scripts/analyze_crawl.py /path/to/export.csv --out /tmp/sf-report.md
      ```

      Pass every related CSV in one call, or pass a directory:

      ```bash
      python3 scripts/analyze_crawl.py /path/to/exports/ --json --out /tmp/sf-report.json
      ```
    - Read the Markdown (or JSON) output. That is the source of truth for counts and clusters.
3. **Interpret with site context**
    - Read the issue catalog before renaming or re-severing anything.
    - Treat a cluster as a **template bug** when 5+ URLs share a directory or `{id}`/`{year}` pattern.
    - Homepage, `/contact`, `/services/`, `/locations/`, and other money URLs outrank blog/tag/search URLs of the same issue.
    - Confirm likely unintended `noindex` against the user's intent before telling them to index a page.
    - Ecommerce category/product pages can be legitimately thin. Say so instead of demanding 500 words.
4. **Write the human report**
    - Use the output format below.
    - Keep example URL lists short (the script already caps them). Offer a full URL dump only if asked.
    - Every recommended fix should say *what to change* and *where* (template vs one-off URL).

## Output format

### Screaming Frog analysis for `[domain or filename]`

1. **Executive summary**
    - Overall status: Healthy / Needs work / Urgent
    - Top 3 risks
    - What to do first this week
2. **Crawl snapshot**
    - Files used, HTML URL count, indexable 200s, status-code mix
    - Data gaps (which optional exports were missing)
3. **Fix roadmap**
    - Do now / This sprint / Backlog, copied from the analyzer then edited for business context
4. **Prioritized clusters**
    - Table: rank, severity, issue, URL template, count, why it matters, recommended fix
5. **Cluster details**
    - For the top 8–12 clusters: sample URLs, likely root cause, concrete fix, owner hint (content, CMS template, redirects, hosting)
6. **Out of scope / ignored**
    - Non-HTML assets skipped, intentional noindex, thin utility pages, and anything the export could not prove

## Reporting rules

- Be direct. "42 service pages share one title tag" is better than "title tags could be improved."
- Separate **verified** (in the export) from **inferred** (template/CMS guess).
- Do not claim the whole site was crawled unless the user said the crawl completed and limits were not hit.
- Prefer one template-level fix over a URL-by-URL content rewrite when the cluster pattern says the template is wrong.
- Never mark a page "must be indexed" just because it is non-indexable. Thank-you, search, cart, and faceted-filter URLs are often correct as noindex.
- If the analyzer cannot map columns, show the headers you saw and ask for an Internal HTML export rather than guessing.

## Tooling notes

- The script uses Python 3 stdlib only (`csv`, `json`, `urllib.parse`). No pip install.
- Run it from any cwd; pass the script by its path next to this `SKILL.md`:

  ```bash
  python3 /path/to/screaming-frog-analyzer/scripts/analyze_crawl.py /path/to/export.csv --out /tmp/sf-report.md
  ```
- Screaming Frog CSVs are comma-separated even when `Content Type` is `text/html; charset=utf-8`. The script does not sniff `;` as a delimiter. Treat a `.tsv` header as tab-separated only. UTF-8 BOMs are handled via `utf-8-sig`.
- Default thresholds match Screaming Frog filters: title 30–60 chars, meta 70–155, H1 70, thin content &lt; 200 words, title pixel width 600, meta pixel width 985.
- Unique Inlinks = 0 is only an orphan signal when that column exists. Without it, do not call pages orphans.
- Redirect loops and hop counts need the Redirect Chains report. A single 301 in the Internal tab is not a chain.
- For huge crawls (tens of thousands of rows) still run the script; do not sample the CSV by reading it into chat.
