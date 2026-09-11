# Screaming Frog issue catalog

Thresholds and severity used by `scripts/analyze_crawl.py`. Tune only when the user supplies different targets (for example ecommerce thin-content pages).

## Scope rules

- On-page issues (title, meta, H1, word count) apply to **indexable HTML 200** URLs unless noted.
- Status-code and redirect issues apply to every URL in the export.
- Skip `application/pdf`, images, CSS, and JS for on-page checks when `Content Type` is present.
- Do not treat `noindex` / canonicalised URLs as ranking opportunities. Flag them only when they look unintentional (homepage, high inlinks, money-page URL pattern).

## Severity

| Severity | Meaning |
| --- | --- |
| Critical | Blocks indexing, serving, or the homepage. Fix before other SEO work. |
| High | Direct ranking or crawl-budget damage on indexable pages. |
| Medium | Clear on-page or IA waste; fix at template level when clustered. |
| Low | Polish, SERP snippet truncation, or URL-hygiene nits. |

## Detection rules

| Issue ID | Severity | Signal | Typical fix |
| --- | --- | --- | --- |
| `server_error` | Critical | Status 5xx | Fix origin/hosting; add monitoring. |
| `redirect_loop` | Critical | Redirect chain report `Loop=True`, or A→B→A | Collapse to one 301 to the canonical. |
| `homepage_non_indexable` | Critical | `/` or `/index` is Non-Indexable | Remove noindex/canonical/robots block. |
| `client_error` | High | Status 4xx | 301 to replacement or 410 if gone; repair inlinks. |
| `missing_title` | High | Empty `Title 1` | Unique title in the page template. |
| `duplicate_title` | High | Same `Title 1` on 2+ indexable URLs | Unique titles; check pagination/params. |
| `unintended_noindex` | High | Non-Indexable + homepage/money URL or Unique Inlinks ≥ 20 | Confirm intent; remove noindex if it should rank. |
| `canonical_to_error` | High | Canonical target is 4xx/5xx/redirect when that data exists | Point canonical at the live 200 URL. |
| `redirect_chain` | High | 3+ hops, or 3xx → 3xx | Single 301 to final URL; update internal links. |
| `http_urls` | High | `http://` internal HTML on an https site | 301 to https; fix internal links and canonicals. |
| `missing_h1` | Medium | Empty `H1-1` | One descriptive H1 in the template. |
| `multiple_h1` | Medium | `H1-2` populated | Keep one H1; demote extras to H2. |
| `duplicate_h1` | Medium | Same `H1-1` on 2+ indexable URLs | Unique headings per template instance. |
| `missing_meta_description` | Medium | Empty `Meta Description 1` | Unique ~70–155 char descriptions. |
| `duplicate_meta_description` | Medium | Same description on 2+ indexable URLs | Unique descriptions. |
| `thin_content` | Medium | Word Count &lt; 200 (SF default) | Add unique copy, or noindex/canonical if the page should not rank. |
| `orphan_page` | Medium | Unique Inlinks = 0, indexable HTML 200 | Link from nav, sitemap, or related pages — or drop from index. |
| `title_too_long` | Low | Title &gt; 60 chars or pixel width &gt; 600 | Shorten; put primary keyword first. |
| `title_too_short` | Low | Title &lt; 30 chars or pixel width below SF floor | Expand with a differentiator. |
| `meta_too_long` | Low | Meta &gt; 155 chars or pixel width &gt; 985 | Trim to avoid SERP truncation. |
| `meta_too_short` | Low | Meta &lt; 70 chars | Expand the value proposition. |
| `h1_too_long` | Low | H1 &gt; 70 chars | Tighten the heading. |
| `title_same_as_h1` | Low | Title 1 equals H1-1 | Optional: vary wording for extra keyword coverage. |
| `deep_page` | Low | Crawl Depth &gt; 4 and Unique Inlinks &lt; 5 | Add internal links; flatten IA. |
| `slow_response` | Low | Response Time &gt; 1.0s | Hosting, TTFB, caching. |
| `long_url` | Low | Address path &gt; 115 chars | Shorter slugs where the CMS allows. |
| `underscore_url` | Low | `_` in path | Prefer hyphens on new URLs. |
| `uppercase_url` | Low | Uppercase in path | Lowercase canonicals; 301 mixed-case dupes. |
| `parameter_url_indexable` | Low | `?` in URL and Indexable | Canonical to clean URL or noindex filters/sorts. |
| `missing_image_alt` | Medium | Images export: empty alt and no null `alt=""` signal | Descriptive alt, or empty alt if decorative. |

## Clustering

Cluster every finding on **issue ID + first URL directory** (`/blog/`, `/services/`, `/`), not on individual URLs.

Keep finer path templates in the cluster detail (`/blog/{year}/{id}/…`) so the reader can see pagination or dated archives inside the directory.

If 5+ URLs in a cluster share a directory, treat it as a **template bug** (CMS field, header include, or pagination rule) and recommend one fix that repairs the set.

## Priority score

Used to rank clusters, not pages:

```
weight = critical:100, high:40, medium:12, low:3
volume = min(count, 100) + 10 * log10(count + 1)
inlink_boost = 1 + min(total_unique_inlinks, 500) / 50
indexable_boost = 1 + (indexable_urls / count)
money_boost = 2.5 homepage, 1.5 service/product/location/contact/pricing, else 1.0

score = weight * volume * inlink_boost * indexable_boost * money_boost
```

Sort clusters by score descending. Present a fix roadmap:

1. **Do now** — all Critical, plus High with homepage or inlink_boost well above 1
2. **This sprint** — remaining High, then Medium template clusters
3. **Backlog** — Low, one-off Medium, URL hygiene

## Data gaps

If the primary export is Internal HTML only, say what was not checked:

| Missing export | Gaps |
| --- | --- |
| Redirect Chains report | Loops and hop counts |
| All Inlinks | Broken-link sources, orphan confirmation |
| Images | Missing alt |
| Canonicals / Directives tabs | Conflicting canonical vs robots |
| Hreflang | Language-return issues |
| Structured data | Schema errors |
