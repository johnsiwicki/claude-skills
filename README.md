# Treehouse Skills

A Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) distributing the `treehouse-skills` plugin.

## Install

```
/plugin marketplace add johnsiwicki/skills
/plugin install treehouse-skills@treehouse
```

## Skills

| Skill | Purpose |
| --- | --- |
| `site-builder` | Build responsive, accessible homepage and landing-page sections for ATB and Treehouse CMS templates (`borders.php`, `template.css`, `homepage.js`). |
| `ab-testing-cro` | Generate lead-gen A/B test ideas from a URL, scored with the ICE framework. |
| `tracking-pixel-audit` | Inspect a URL and report which marketing/tracking tags are present (GTM, GA4, Google Ads, and common pixels). |
| `website-qa-audit` | Repeatable QA pass: Lighthouse scores, Core Web Vitals, mobile friendliness, and severity-ranked visual defects across mobile and desktop viewports. |
| `youtube-thumbnail-creator` | Design high-CTR YouTube thumbnails incorporating a logo. |

Skills are namespaced once installed, e.g. `/treehouse-skills:tracking-pixel-audit`.

## Layout

```
.claude-plugin/marketplace.json      # marketplace catalog
plugins/treehouse-skills/
  .claude-plugin/plugin.json         # plugin manifest
  skills/<name>/SKILL.md             # one directory per skill
```

Validate changes with `claude plugin validate .` before pushing. Bump `version` in
`plugin.json` on every release — users only receive updates when that field changes.
