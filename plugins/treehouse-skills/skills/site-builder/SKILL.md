---
name: site-builder
description: Build or modify responsive, accessible homepage and landing-page sections for ATB and Treehouse CMS templates. Use when asked to create or update heroes, trust badges, service grids, reviews, calls to action, or related HTML/PHP, CSS, and JavaScript in borders.php, template.css, and homepage.js.
---

# ATB Site Builder

Create cohesive CMS components while preserving the template's PHP branches, CMS placeholders, design tokens, and existing behavior.

## Workflow

1. Locate `borders.php`, `template.css`, and `homepage.js` in the user's target project.
2. Read [references/template-contract.md](references/template-contract.md) before editing an ATB or Treehouse CMS template.
3. Inspect the target files instead of assuming they match the bundled baseline. Use `assets/atb-template/` only when the user asks to start from the bundled template or when comparison helps resolve an anchor.
4. Derive a short lowercase component slug such as `hero`, `service-grid`, or `reviews`.
5. Search all three target files for existing `sb:<slug>` markers and `.sb-<slug>` selectors. Update an existing component instead of inserting a duplicate.
6. Implement only the HTML/PHP, CSS, and JavaScript required by the request.
7. Validate syntax, placement, accessibility, responsive behavior, and the final diff.

## Edit Behavior

- Edit target files directly when they are present in the workspace and the user asks to build, add, implement, or modify a component.
- Return labeled payload blocks only when the user explicitly requests snippets or when target files are unavailable.
- Preserve unrelated user changes and existing formatting where practical.
- Do not modify the bundled files under `assets/atb-template/` unless the user explicitly asks to update the baseline.

## Component Boundaries

Wrap each component in stable markers so later requests can find and update it:

```html
<!-- === sb:service-grid:start === -->
<section class="sb-service-grid" aria-labelledby="sb-service-grid-title">
  ...
</section>
<!-- === sb:service-grid:end === -->
```

Use matching CSS and JavaScript markers:

```css
/* === sb:service-grid:start === */
/* === sb:service-grid:end === */
```

```js
// === sb:service-grid:start ===
// === sb:service-grid:end ===
```

## Implementation Standards

- Scope component selectors beneath one `.sb-<slug>` root. Avoid global element selectors, broad utility names, and new `:root` declarations.
- Reuse the target stylesheet's active brand variables, especially `--brand-default`, `--brand-dark`, `--brand-light`, and `--brand-accent`.
- Follow the target file's media-query syntax. The bundled baseline uses `@media (width >= 1024px)` for desktop behavior.
- Use mobile-first layout, fluid sizing where useful, and the fewest breakpoints needed.
- Use semantic landmarks and heading order. Provide accessible names, meaningful image alternatives, visible focus states, keyboard operation, and sufficient contrast.
- Respect `prefers-reduced-motion` for nonessential animation.
- Use CMS placeholders exactly as documented. Do not invent alternate bracket forms.
- Add JavaScript only when CSS and native HTML cannot provide the behavior. Scope it to the component, tolerate a missing component root, and avoid global variables.
- Keep user-facing copy specific to the request. Do not invent unverifiable awards, ratings, testimonials, guarantees, or performance claims.

## Validation

Before completing the task:

1. Confirm the PHP markup remains inside the intended `$thePage == "index"` branch.
2. Confirm exactly one start marker and one end marker exist per edited file.
3. Run `php -l borders.php` when PHP is available.
4. Run `node --check homepage.js` when JavaScript changed and Node.js is available.
5. Search for unscoped selectors, duplicate IDs, placeholder spelling errors, and accidental duplicate components.
6. Review the diff and report the files changed and checks run.

If a required anchor is missing or the PHP branch structure differs materially from the contract, stop before inserting and explain the mismatch.
