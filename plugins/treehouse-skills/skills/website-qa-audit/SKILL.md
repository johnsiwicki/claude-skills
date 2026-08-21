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
2. **Run Lighthouse checks**
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
    - Note whether results are mobile, desktop, or both.
3. **Check mobile friendliness**
    - Use Google's mobile-friendly test when available: https://search.google.com/test/mobile-friendly
    - If the tool is unavailable, manually inspect mobile viewport behavior and report that the Google test was not run.
    - Check for:
        - Text too small
        - Content wider than screen
        - Tap targets too close
        - Viewport misconfiguration
        - Layout shifts or overlapping content
4. **Perform manual visual review**
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
5. **Capture evidence**
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

## Tooling notes

Concrete tools that satisfy the steps above:

- **Lighthouse** (step 2): the `lighthouse` CLI, run headless with JSON output, e.g.
  `lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=<file> --preset=desktop`
  Omit `--preset=desktop` for the mobile run. Parse `categories.*.score` and
  `audits['largest-contentful-paint'|'cumulative-layout-shift'|'total-blocking-time'|'first-contentful-paint'|'speed-index'].displayValue`.
  Run both mobile and desktop when the user asks for a deep audit; mobile only for a quick pass.
- **Page discovery** (step 1): try `/sitemap.xml` and `/robots.txt` first, then fall back to parsing nav links from the homepage HTML.
- **Visual review** (step 4): the browser tools — `resize_window` (`mobile` 375x812 / `desktop` 1280x800), `computer` with `screenshot`, `read_console_messages` for asset failures, and `read_page` for structure. Reload after switching viewport so load-time device gates re-run.
- **Horizontal scroll** is best detected directly rather than by eye:
  `document.documentElement.scrollWidth > document.documentElement.clientWidth`.
- **Google's mobile-friendly test** requires an interactive session and often blocks automation. Expect to fall back to manual viewport inspection and say so.
