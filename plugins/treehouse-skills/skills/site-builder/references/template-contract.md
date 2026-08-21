# ATB Template Contract

Use this reference when editing the bundled ATB and Treehouse CMS template family. Inspect the actual target files first because deployed variants may differ.

## Contents

- File responsibilities and homepage placement
- CMS placeholders and CSS contract
- JavaScript contract and bundled baseline

## File Responsibilities

| File | Responsibility | Default action |
| --- | --- | --- |
| `borders.php` | Homepage HTML/PHP and CMS placeholders | Insert or update component markup inside the homepage branch |
| `template.css` | Shared and component presentation | Append or update a marker-delimited, scoped component block |
| `homepage.js` | Homepage-only interaction | Append or update a marker-delimited module only when needed |

## Homepage Placement

The bundled baseline ends the header and opens an empty homepage branch in this order:

```php
<!-- === end: 1. ATB Header === -->
<?php if ($thePage == "index") { ?>

    <!-- Insert homepage components here. -->

<?php
}
else
{
?>
<div id="page-wrap">
```

Insert homepage components after the opening `<?php if ($thePage == "index") { ?>` line and before the PHP block that closes that branch. Do not insert immediately after the header comment because that location is outside the homepage guard.

Treat the following as separate anchors:

- `<!-- === end: 1. ATB Header === -->` confirms the header boundary.
- `<?php if ($thePage == "index") { ?>` opens the homepage-only branch.
- `<div id="page-wrap">` belongs to the non-homepage `else` branch in the bundled baseline.

If these anchors are missing, reordered, duplicated, or split across different control-flow branches, inspect the surrounding PHP and derive a safe insertion point before editing.

## CMS Placeholders

Preserve the exact placeholder forms used by this template:

| Value | Placeholder |
| --- | --- |
| Display phone number | `[phone]` |
| Company name | `[[company]]` |
| Service territory | `[territory]` |
| Navigation | `[[top_nav]]` |
| Main CMS content | `[[content]]` |
| Social footer | `[[social_footer]]` |

Use `<?php echo $phonenumber; ?>` for a telephone link value and `[phone]` for its displayed text:

```php
<a href="tel:<?php echo $phonenumber; ?>">[phone]</a>
```

Do not change double-bracket placeholders to single brackets or the reverse.

## CSS Contract

The bundled baseline defines these reusable variables:

```css
--brand-default
--brand-dark
--brand-light
--brand-accent
--white
```

Some variables are declared more than once in the baseline. Use `var(...)` rather than copying a resolved hex value, and do not introduce another `:root` block.

Use the component root as the selector namespace:

```css
.sb-service-grid { ... }
.sb-service-grid__item { ... }
.sb-service-grid__title { ... }
```

Use the target file's existing query style. The bundled desktop header query is:

```css
@media (width >= 1024px) { ... }
```

## JavaScript Contract

Prefer no JavaScript for static sections. When interaction is required:

- Query from the `.sb-<slug>` root.
- Exit without error when the root is absent.
- Use event listeners instead of inline handlers.
- Preserve keyboard and screen-reader behavior.
- Avoid dependencies unless the target project already loads them and the request requires them.
- Use a scoped IIFE or `DOMContentLoaded` listener when initialization timing requires it.

## Bundled Baseline

Use `../assets/atb-template/` as a clean baseline for comparison or as starter material only when requested. Treat the user's project files as authoritative during normal edits.
