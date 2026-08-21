---
name: website-qa-audit
description: Run a repeatable website QA pass combining automated Lighthouse checks with manual visual review across mobile and desktop viewports. Reports Performance/Accessibility/Best-Practices/SEO scores, Core Web Vitals, mobile friendliness, and severity-ranked visual defects (broken or distorted images, overlapping text, bad spacing, horizontal scroll, broken CTAs/forms). Use when asked to QA, audit, or review a site or page before or after launch, to check page speed or Lighthouse scores, to verify mobile responsiveness, or to find visual and layout bugs across pages.
---

# Website QA Audit

## Purpose

Use this skill to perform a repeatable website QA pass that combines automated Lighthouse checks with manual visual review across mobile and desktop viewports.

## Required inputs

- Website URL or list of page URLs to test.
- Scope:
    - Single page
    - All key pages from sitemap/navigation
    - Specific supplied URLs
- Any known priority pages, conversion pages, or templates.
- Whether the user wants a quick pass or deep audit.

## Workflow

1. **Define the page set**
    - If the user provides one URL, inspect the site navigation and/or sitemap to identify key pages.
    - Prioritize homepage, service/product pages, landing pages, blog/article templates, contact/signup/checkout pages, and any pages the user names.
    - Keep the tested page list explicit in the final report.
2. **Group pages by template, then sample**
    - CMS sites repeat a handful of templates across many URLs. Audit *templates*, not pages: most defects are template-level and repeat identically on every page using it.
    - Infer templates from URL structure and page markup, e.g. `/roof-repair/*` and `/roof-replacement/*` sharing one service template.
    - Pick one representative URL per template, plus every page the user named and every conversion page (forms, checkout, contact) regardless of template.
    - Target set size: **3-5 URLs for a quick pass, one per template plus all conversion pages for a deep audit.**
    - State the template->URL mapping in the report so the reader knows what coverage they actually got.
3. **Run Lighthouse checks**
    - Run Lighthouse/PageSpeed-style checks for each priority URL when tooling is available.
    - Capture scores and notable failures for:
        - Performance
        - Accessibility
        - Best Practices
        - SEO
    - Record Core Web Vitals or lab metrics when available:
        - LCP
        - CLS
        - INP/TBT
        - FCP
        - Speed Index
    - **Run both mobile and desktop for every page.** The gap between them is the diagnosis: a site can score 98 desktop and 47 mobile, and a mobile-only run hides that the desktop path is healthy.
    - When LCP is poor, always report the **LCP phase breakdown** (TTFB / load delay / load time / render delay). "LCP 11.6s" is not actionable; "74% render delay" points straight at main-thread contention.
4. **Check mobile friendliness**
    - Use Google's mobile-friendly test when available: https://search.google.com/test/mobile-friendly
    - If the tool is unavailable, manually inspect mobile viewport behavior and report that the Google test was not run.
    - Check for:
        - Text too small
        - Content wider than screen
        - Tap targets too close
        - Viewport misconfiguration
        - Layout shifts or overlapping content
5. **Perform manual visual review**
    - Review each tested page on mobile viewport.
    - Review each tested page on desktop in Chrome.
    - Look for:
        - Broken or missing images
        - Distorted, stretched, blurry, or incorrectly cropped images
        - Wonky formatting
        - Overlapping text or components
        - Bad spacing, alignment, or wrapping
        - Sticky header/footer issues
        - Broken navigation, buttons, forms, embeds, or CTAs
        - Horizontal scrolling
        - Popups, cookie banners, or chat widgets blocking content
        - Console-visible obvious asset failures if available
6. **Capture evidence**
    - For each issue, capture:
        - Page URL
        - Device/browser
        - Severity
        - What is wrong
        - Where it appears
        - Suggested fix
    - Include screenshots when tools support them.
    - Do not over-report tiny aesthetic preferences unless they affect credibility, usability, or conversion.

## Severity scale

- **Critical**: Blocks conversion, navigation, reading, form submission, or indexing.
- **High**: Clearly damages trust, usability, accessibility, or SEO.
- **Medium**: Noticeable visual/UX issue but not blocking.
- **Low**: Minor polish issue.

## Output format

Return a concise QA report with these sections:

1. **Executive summary**
    - Overall status: Pass / Pass with fixes / Needs attention
    - Biggest risks
    - Recommended next actions
2. **Pages tested**
    - Table with URL, template/page type, mobile checked, Chrome checked, Lighthouse run.
3. **Lighthouse summary**
    - Table with page, device, scores, major findings.
4. **Visual review findings**
    - Table with severity, page, device/browser, issue, evidence, recommended fix.
5. **Mobile friendliness**
    - Summarize Google mobile-friendly result or manual mobile findings.
6. **Fix priority checklist**
    - Ordered list of fixes from highest leverage to lowest.

## Reporting rules

- Be direct and practical.
- Separate verified findings from assumptions.
- If a tool/browser is unavailable, say exactly what was not checked.
- Prefer actionable fixes over vague notes like "improve design."
- Avoid claiming all pages were checked unless the tested URL list is complete.
- If the request says "all pages," explain how pages were discovered and list any exclusions.
- **Close the loop on the declared page set.** Before writing the report, re-check the list from step 2 and confirm every URL was actually tested. Any page declared but not tested must be named explicitly as not tested, with the reason.

## Tooling notes

Concrete tools that satisfy the steps above:

- **Lighthouse** (step 2): the `lighthouse` CLI, run headless with JSON output, e.g.
  `lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=<file> --preset=desktop`
  Omit `--preset=desktop` for the mobile run. Parse `categories.*.score` and
  `audits['largest-contentful-paint'|'cumulative-layout-shift'|'total-blocking-time'|'first-contentful-paint'|'speed-index'].displayValue`.
  Run both mobile and desktop when the user asks for a deep audit; mobile only for a quick pass.
- **Page discovery** (step 1): try `/sitemap.xml` and `/robots.txt` first, then fall back to parsing nav links from the homepage HTML. Strip non-page entries (`.xml`, `.kml`, feeds) before counting.
- **Batching multiple pages** (steps 3-6): Lighthouse is the slow part — roughly 30-60s per URL per form factor. Run the whole set as one backgrounded loop rather than one call per page, then parse all the JSON at once:

  ```bash
  for u in "${URLS[@]}"; do
    slug=$(echo "$u" | sed 's|https\?://||; s|[/.]|_|g')
    lighthouse "$u" --quiet --chrome-flags="--headless" --output=json --output-path="./lh-$slug-m.json"
    lighthouse "$u" --quiet --chrome-flags="--headless" --preset=desktop --output=json --output-path="./lh-$slug-d.json"
  done
  ```

  While that runs, do the visual review in the browser — the two are independent, so never sit idle waiting on Lighthouse.
- **Per-page DOM checks** (step 5): run the same JS probe on every page so findings are comparable — horizontal scroll, broken images (`complete && naturalWidth === 0`), missing `alt`, unlabeled form inputs, and fixed/sticky elements with their `z-index`. Collect into one table rather than narrating page by page.
- **Deduplicate template-level findings**: a missing `alt` in shared furniture (header, footer, nav) will repeat on every page. Report it once, note which template it lives in, and say how many URLs inherit it — do not list it five times.
- **Visual review** (step 4): the browser tools — `resize_window` (`mobile` 375x812 / `desktop` 1280x800), `computer` with `screenshot`, `read_console_messages` for asset failures, and `read_page` for structure. Reload after switching viewport so load-time device gates re-run.
- **Horizontal scroll** is best detected directly rather than by eye:
  `document.documentElement.scrollWidth > document.documentElement.clientWidth`.
- **Google's mobile-friendly test** requires an interactive session and often blocks automation. Expect to fall back to manual viewport inspection and say so.
