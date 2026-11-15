#!/usr/bin/env python3
"""Builds every Tux-Force logo file from one geometry definition.

The wordmark is converted to outlines with fontTools, so the SVGs render the same everywhere
without Inter being installed. Run with a Python that has fontTools:

    python tools/build.py && sh tools/export.sh
"""
import math
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("/usr/share/fonts/rsms-inter-fonts")

NIGHT, FOREST, LIME, EMERALD, ICE, MIST, MIST_DARK = (
    "#06140F", "#0F3B2E", "#A3E635", "#10B981", "#F4F7FB", "#8FB5A3", "#4F7564")

# Head in profile, drawn upright, then tilted and stretched into flight.
HEAD = ("M168 392C136 336 136 254 172 200C208 148 276 126 336 146C380 160 402 196 404 234"
        "L452 262L402 292C398 336 372 376 330 400C280 426 212 424 168 392Z")
CAP = ("M168 392C136 336 136 254 172 200C208 148 276 126 336 146C380 160 402 196 404 234"
       "C380 196 340 180 300 188C262 196 244 236 248 284C252 336 270 380 300 414"
       "C258 424 206 418 168 392Z")
EYE, EYE_R = (334, 230), 19
PUPIL, PUPIL_R = (340.5, 223.5), 6.1
STREAKS = []

ANGLE, SX, SY, CX, CY = -10, 1.04, 0.96, 270, 262


def fly(x, y):
    """Stretch along the direction of travel, then tilt upwards."""
    x, y = (x - CX) * SX, (y - CY) * SY
    a = math.radians(ANGLE)
    return CX + x * math.cos(a) - y * math.sin(a), CY + x * math.sin(a) + y * math.cos(a)


def rotate(x, y, cx=256, cy=262):
    a = math.radians(ANGLE)
    x, y = x - cx, y - cy
    return cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)


def transform_path(d, fn):
    out = []
    for cmd, args in re.findall(r"([MCLZ])([^MCLZ]*)", d):
        nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", args)]
        pts = [fn(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]
        out.append(cmd + " ".join(f"{x:.1f} {y:.1f}" for x, y in pts))
    return "".join(out)


def path_points(d):
    nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", d)]
    return list(zip(nums[0::2], nums[1::2]))


head_d = transform_path(HEAD, fly)
cap_d = transform_path(CAP, fly)
eye = fly(*EYE)
pupil = fly(*PUPIL)
streaks = [(rotate(*a), rotate(*b)) for a, b in STREAKS]

# Centre the drawing (head and beak) in the 512 box.
pts = path_points(head_d) + [p for s in streaks for p in s]
minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
DX, DY = 256 - (minx + maxx) / 2, 256 - (miny + maxy) / 2


def shift(d):
    return transform_path(d, lambda x, y: (x + DX, y + DY))


head_d, cap_d = shift(head_d), shift(cap_d)
eye = (eye[0] + DX, eye[1] + DY)
pupil = (pupil[0] + DX, pupil[1] + DY)
streak_d = "".join(f"M{a[0] + DX:.1f} {a[1] + DY:.1f}L{b[0] + DX:.1f} {b[1] + DY:.1f}" for a, b in streaks)


def symbol(color, pupil_color):
    return f'''  <g fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{head_d}" stroke-width="12"/>
  </g>
  <path d="{cap_d}" fill="{color}" stroke="{color}" stroke-width="12" stroke-linejoin="round"/>
  <circle cx="{eye[0]:.1f}" cy="{eye[1]:.1f}" r="{EYE_R}" fill="{color}"/>
  <circle cx="{pupil[0]:.1f}" cy="{pupil[1]:.1f}" r="{PUPIL_R}" fill="{pupil_color}"/>'''


def symbol_mono():
    # One colour: the pupil is cut out of the eye instead of painted on top.
    px, py = pupil
    ex, ey = eye
    eye_d = (f"M{ex - EYE_R:.1f} {ey:.1f}a{EYE_R} {EYE_R} 0 1 0 {2 * EYE_R} 0a{EYE_R} {EYE_R} 0 1 0 {-2 * EYE_R} 0Z"
             f"M{px - PUPIL_R:.1f} {py:.1f}a{PUPIL_R} {PUPIL_R} 0 1 0 {2 * PUPIL_R} 0a{PUPIL_R} {PUPIL_R} 0 1 0 {-2 * PUPIL_R} 0Z")
    return f'''  <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
    <path d="{head_d}" stroke-width="12"/>
  </g>
  <path d="{cap_d}" fill="currentColor" stroke="currentColor" stroke-width="12" stroke-linejoin="round"/>
  <path d="{eye_d}" fill="currentColor" fill-rule="evenodd"/>'''


BADGE_DEFS = f'''  <defs>
    <linearGradient id="badge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{FOREST}"/>
      <stop offset="1" stop-color="{NIGHT}"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="url(#badge)"/>'''


def svg(view_w, view_h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" '
            f'width="{view_w}" height="{view_h}">\n  <title>{title}</title>\n{body}\n</svg>\n')


# --- Wordmark as outlines -------------------------------------------------------------------

def text_path(font_file, text, size, x, y, tracking=0.0):
    """Returns SVG path data for text set at baseline (x, y) and the advance width."""
    font = TTFont(FONTS / font_file)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    d, cursor = [], x
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y)))
        d.append(pen.getCommands())
        cursor += glyphs[name].width * scale + tracking
    return "".join(d), cursor - tracking - x


def lockup(symbol_color, pupil_color, tux_color, force_color, tag_color):
    tux_d, tux_w = text_path("InterDisplay-BlackItalic.ttf", "TUX", 230, 520, 318, -4)
    force_d, force_w = text_path("InterDisplay-BlackItalic.ttf", "FORCE", 230, 520 + tux_w - 4, 318, -4)
    tag_d, tag_w = text_path("Inter-SemiBold.ttf", "PC GAMES ON LINUX", 50, 530, 398, 14)
    width = math.ceil(520 + tux_w + force_w + 40)
    body = f'''{symbol(symbol_color, pupil_color)}
  <path d="{tux_d}" fill="{tux_color}"/>
  <path d="{force_d}" fill="{force_color}"/>
  <path d="{tag_d}" fill="{tag_color}"/>'''
    return width, body


def write(name, content):
    (ROOT / name).write_text(content)
    print("wrote", name)


write("logo-mark.svg", svg(512, 512, "Tux-Force mark", BADGE_DEFS + "\n" + symbol(LIME, NIGHT)))
# Full-bleed square for GitHub and other services that round or crop the avatar themselves.
write("logo-mark-square.svg", svg(512, 512, "Tux-Force mark, square",
                                  BADGE_DEFS.replace('rx="112" ', '') + "\n" + symbol(LIME, NIGHT)))
write("logo-symbol.svg", svg(512, 512, "Tux-Force symbol", symbol(LIME, NIGHT)))
write("logo-symbol-dark.svg", svg(512, 512, "Tux-Force symbol for light backgrounds", symbol(FOREST, ICE)))
write("logo-mark-mono.svg", svg(512, 512, "Tux-Force symbol, single colour", symbol_mono()))

w, body = lockup(LIME, NIGHT, ICE, LIME, MIST)
write("logo-horizontal.svg", svg(w, 512, "Tux-Force logo", body))
w, body = lockup(FOREST, ICE, NIGHT, EMERALD, MIST_DARK)
write("logo-horizontal-light.svg", svg(w, 512, "Tux-Force logo for light backgrounds", body))

# Social preview: logo centred on a dark plate with a faint grid.
w, body = lockup(LIME, NIGHT, ICE, LIME, MIST)
scale = 1000 / w
sub_d, sub_w = text_path("Inter-SemiBold.ttf", "Open-source compatibility layer · community fork", 28, 0, 0)
write("social-preview.svg", svg(1280, 640, "Tux-Force social preview", f'''  <defs>
    <radialGradient id="glow" cx="0.5" cy="0.45" r="0.75">
      <stop offset="0" stop-color="{FOREST}"/>
      <stop offset="1" stop-color="#050E0A"/>
    </radialGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{LIME}" stroke-opacity="0.06"/>
    </pattern>
  </defs>
  <rect width="1280" height="640" fill="url(#glow)"/>
  <rect width="1280" height="640" fill="url(#grid)"/>
  <g transform="translate({(1280 - w * scale) / 2:.1f} {170:.1f}) scale({scale:.4f})">
{body}
  </g>
  <g transform="translate({(1280 - sub_w) / 2:.1f} 520)"><path d="{sub_d}" fill="{MIST}"/></g>'''))

# Pixel penguin: the secondary mascot for stickers, error pages and the like.
GRID = [
    "......XXXX......",
    "....XXXXXXXX....",
    "...XXXXXXXXXX...",
    "..XXX......XXX..",
    "..XX........XX..",
    "..XX.XX..XX.XX..",
    "..XX.XX..XX.XX..",
    "..XX........XX..",
    "..XX..XXXX..XX..",
    "..XXX..XX..XXX..",
    ".XXXXX....XXXXX.",
    ".XXX........XXX.",
    "XXX..........XXX",
    "XX............XX",
    "XX............XX",
    "XXX..........XXX",
    ".XXX........XXX.",
    "..XXXXXXXXXXXX..",
    ".XXXXX....XXXXX.",
]
cell = 21
ox, oy = (512 - 16 * cell) // 2, (512 - len(GRID) * cell) // 2
runs = []
for row_index, row in enumerate(GRID):
    for m in re.finditer(r"X+", row):
        runs.append(f'<rect x="{ox + m.start() * cell}" y="{oy + row_index * cell}" '
                    f'width="{(m.end() - m.start()) * cell}" height="{cell + 0.5}"/>')
write("mascot-pixel.svg", svg(512, 512, "Tux-Force pixel mascot",
                              BADGE_DEFS + f'\n  <g fill="{LIME}">' + "".join(runs) + "</g>"))

# Brand guide: the template references the SVGs by name; embed them so the page is one file.
import base64  # noqa: E402

html = (ROOT / "tools" / "brand.template.html").read_text()
html = re.sub(r'(src|href)="([a-z-]+\.svg)"',
              lambda m: f'{m.group(1)}="data:image/svg+xml;base64,'
                        + base64.b64encode((ROOT / m.group(2)).read_bytes()).decode() + '"', html)
write("brand.html", html)
