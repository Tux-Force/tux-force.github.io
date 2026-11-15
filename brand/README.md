# Tux-Force brand assets

Logo and basic corporate design for the Tux-Force community fork. Open `brand.html` for the full guide.

The mark is a round penguin head in profile, tilted slightly upwards as if taking off. The penguin is an original drawing and is not derived from Larry Ewing's Tux.

| File | Use |
| --- | --- |
| `logo-mark.svg` | Mark on its badge: avatar, favicon, app icon |
| `logo-mark-square.svg` | Full-bleed square for GitHub and services that round avatars themselves (`png/avatar-square-*.png`) |
| `logo-symbol.svg` | Symbol without badge, for dark backgrounds |
| `logo-symbol-dark.svg` | Symbol for light backgrounds |
| `logo-mark-mono.svg` | Single colour (`currentColor`) |
| `logo-horizontal.svg` | Lockup for dark backgrounds |
| `logo-horizontal-light.svg` | Lockup for light backgrounds |
| `social-preview.svg` | GitHub social preview |
| `mascot-pixel.svg` | Secondary pixel mascot (stickers, error pages) |
| `png/` | Raster exports |

## Colours

| Name | Hex | Use |
| --- | --- | --- |
| Night | `#06140F` | Backgrounds |
| Forest | `#0F3B2E` | Backgrounds, symbol on light |
| Lime | `#A3E635` | Brand colour on dark |
| Emerald | `#10B981` | Accent on light |
| Ice | `#F4F7FB` | Text on dark |
| Mist | `#8FB5A3` | Secondary text |

## Typography

Inter Display Black Italic for the wordmark and headlines, Inter for text, JetBrains Mono for code. All under the SIL Open Font License. The logo files contain the wordmark as outlines, so no font needs to be installed.

## Rebuilding

All logo files come from `tools/build.py`, which needs fontTools and the Inter fonts. `tools/export.sh` rasterises them with ImageMagick.

```bash
python tools/build.py
sh tools/export.sh
```
