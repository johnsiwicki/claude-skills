---
name: tracking-pixel-audit
description: Inspect a public webpage URL and report which marketing/tracking tags are present, with special attention to Google Tag Manager containers (GTM-), Google tag/Ads/Analytics IDs (G-, AW-, UA-), and other common pixels (Meta, LinkedIn, TikTok, Pinterest, Bing UET, Hotjar, Clarity, Segment, HubSpot, Adobe). Use when asked whether a site has GTM, a Google tag, or a tracking pixel installed, to verify a specific expected container/measurement ID, or to audit a page's analytics and ad-tech stack.
---

# Tracking Pixel Audit

## Purpose

Use this skill to inspect a public webpage URL and report which marketing/tracking tags are present, with special attention to:

- Google Tag Manager containers (`GTM-XXXX`)
- Google tag / Google Ads / Google Analytics IDs (`G-XXXX`, `AW-XXXX`, `UA-XXXX`)
- Other common tracking pixels and analytics scripts

## Required input

- A public URL to inspect.
- Optional: a specific expected ID, such as `GTM-ABC1234`, `G-XXXXXXXXXX`, or `AW-123456789`.

## Workflow

1. Load the URL with the web page loader.
    - Start with fast mode.
    - If the extracted page text is too thin or does not include scripts/source hints, retry with full mode.
2. Search the loaded source/text for Google tags:
    - `GTM-`
    - `googletagmanager.com/gtm.js`
    - `googletagmanager.com/ns.html`
    - `gtag(`
    - `gtag/js?id=`
    - `G-`
    - `AW-`
    - `UA-`
    - `DC-`
3. Look for other common pixels and analytics tools:
    - Meta/Facebook Pixel: `connect.facebook.net`, `fbq(`, `facebook.com/tr`
    - LinkedIn Insight Tag: `snap.licdn.com`, `linkedin.com/px`
    - TikTok Pixel: `analytics.tiktok.com`, `ttq.`
    - Pinterest Tag: `ct.pinterest.com`, `pintrk`
    - Microsoft/Bing UET: `bat.bing.com`, `uetq`
    - Twitter/X Pixel: `static.ads-twitter.com`, `twq(`
    - Hotjar: `hotjar.com`, `hj(`
    - Microsoft Clarity: `clarity.ms`
    - Segment: `segment.com`, `analytics.load`
    - HubSpot tracking: `js.hs-scripts.com`, `hubspot`
    - Adobe Analytics/Launch: `assets.adobedtm.com`, `s_code`, `AppMeasurement`
4. Distinguish between strong and weak evidence:
    - **Confirmed**: actual tag script, container ID, noscript iframe, or pixel endpoint found in page source/extracted content.
    - **Likely**: vendor domain or function found, but no clear account/container ID.
    - **Not found**: no matching evidence in the loaded page content.
    - **Inconclusive**: page blocks source extraction, scripts are injected after interaction, or the loader cannot see rendered JavaScript.
5. If an expected Google ID was provided, explicitly say whether that exact ID was found.

## Output format

Return a concise audit:

### Tracking pixel audit for `[domain]`

| Platform | Status | IDs found | Evidence |
| --- | --- | --- | --- |
| Google Tag Manager | Confirmed / Likely / Not found / Inconclusive | `GTM-XXXX` | Short source clue |
| Google Analytics / Google tag | Confirmed / Likely / Not found / Inconclusive | `G-XXXX`, `UA-XXXX` | Short source clue |
| Google Ads | Confirmed / Likely / Not found / Inconclusive | `AW-XXXX` | Short source clue |
| Meta Pixel | Confirmed / Likely / Not found / Inconclusive | Pixel ID if visible | Short source clue |
| Other pixels | Confirmed / Likely / Not found / Inconclusive | IDs if visible | Short source clue |

### Summary

- **Google tags present:** Yes / No / Inconclusive
- **GTM present:** Yes / No / Inconclusive
- **Expected ID found:** Yes / No / Not provided
- **Main caveat:** One short caveat if applicable

### Recommended next checks

Include 2–4 practical next steps only when useful, such as:

- Verify in Google Tag Assistant.
- Check the site's rendered DOM in a browser if scripts are injected client-side.
- Confirm the tag fires on conversion pages, not just the homepage.
- Check consent mode/CMP behavior if tags appear blocked until consent.

## Notes and caveats

- Static page loading may miss tags injected after JavaScript execution, user consent, login, geolocation, or interaction.
- Do not claim a tag is absent with absolute certainty unless the page source was fully accessible and no relevant patterns were found.
- Prefer precise IDs and evidence snippets over generic statements.
