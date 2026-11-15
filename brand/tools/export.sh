#!/bin/sh
# Rasterises the SVGs built by tools/build.py. Needs ImageMagick with librsvg.
set -e
cd "$(dirname "$0")/.."
mkdir -p png
magick -background none logo-mark.svg -resize 1024x1024 png/avatar-1024.png
magick -background none logo-mark.svg -resize 512x512 png/avatar-512.png
magick logo-mark-square.svg -resize 1024x1024 png/avatar-square-1024.png
magick logo-mark-square.svg -resize 512x512 png/avatar-square-512.png
magick -background none logo-mark.svg -resize 180x180 png/apple-touch-icon-180.png
magick -background none logo-mark.svg -resize 64x64 png/favicon-64.png
magick -background none logo-mark.svg -resize 32x32 png/favicon-32.png
magick -background none logo-mark.svg -resize 16x16 png/favicon-16.png
magick png/favicon-16.png png/favicon-32.png png/favicon-64.png favicon.ico
magick -background none logo-symbol.svg -resize 512x512 png/symbol-512.png
magick -background none logo-horizontal.svg -resize 1600x png/logo-horizontal-dark-bg.png
magick -background none logo-horizontal-light.svg -resize 1600x png/logo-horizontal-light-bg.png
magick social-preview.svg png/social-preview-1280x640.png
magick -background none mascot-pixel.svg -resize 512x512 png/mascot-pixel-512.png
