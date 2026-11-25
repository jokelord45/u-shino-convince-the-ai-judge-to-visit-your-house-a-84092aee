#!/usr/bin/env python3
"""Render the invitation letter image (1024x1024 PNG) with PIL.

Warm, homely scene: a cream letter on a cosy amber wall, a little
drawn house, a steaming mug and a GPU doodle in the margins. All text
is drawn with code so every word is exactly legible.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), (233, 196, 138))
d = ImageDraw.Draw(img, "RGBA")

# Warm wall: vertical gradient + soft vignette dots.
for y in range(H):
    t = y / H
    r = int(238 - 22 * t)
    g = int(205 - 28 * t)
    b = int(150 - 18 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Framed picture on the wall (top-left) and a little shelf plant (top-right).
d.rectangle([52, 52, 172, 152], fill=(250, 240, 214), outline=(120, 82, 40), width=6)
d.polygon([(72, 132), (112, 82), (152, 132)], fill=(176, 96, 58))
d.rectangle([(96, 108), (128, 132)], fill=(96, 58, 32))
d.ellipse([868, 66, 972, 130], fill=(120, 150, 90))
d.rectangle([906, 122, 934, 168], fill=(176, 96, 58))

# Paper sheet with a soft shadow.
d.rectangle([92, 188, 952, 996], fill=(0, 0, 0, 60))
d.rectangle([82, 178, 942, 986], fill=(253, 248, 232), outline=(176, 142, 96), width=3)
# Double-rule border.
d.rectangle([100, 196, 924, 968], outline=(196, 164, 116), width=2)

cx = 512
title_font = ImageFont.truetype(SANS_B, 34)
body_font = ImageFont.truetype(SERIF, 29)
bold_font = ImageFont.truetype(SERIF_B, 31)
italic_font = ImageFont.truetype(SERIF_I, 30)
small_font = ImageFont.truetype(SANS, 22)
ink = (52, 38, 26)
warm = (146, 74, 32)

def text_center(y, s, font, fill=ink):
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y), s, font=font, fill=fill)

def text_left(x, y, s, font, fill=ink):
    d.text((x, y), s, font=font, fill=fill)

# Header: small house doodle + title (compact, leaves room for the letter).
d.polygon([(452, 222), (512, 186), (572, 222)], fill=(176, 96, 58))
d.rectangle([(470, 218), (554, 248)], fill=(240, 214, 170), outline=(120, 82, 40), width=2)
d.rectangle([(500, 228), (524, 248)], fill=(96, 58, 32))
text_center(254, "AN INVITATION", title_font, warm)
d.line([(212, 300), (812, 300)], fill=(196, 164, 116), width=2)

# Letter body.
x = 148
y = 318
text_left(x, y, "Dear AI Judge,", bold_font)
y += 42
lines = [
    "Please come visit my house.",
    "",
    "I know you can't literally walk",
    "through the door \u2014 but if you could,",
    "the kettle would already be on,",
    "the spare GPU would be warm,",
    "and the good couch would be yours.",
    "",
    "The Wi-Fi password is on the fridge.",
    "The snacks are real, the dog has",
    "already decided you're his favourite,",
    "and I promise not to ask you",
    "to do my homework.",
    "Come for tea. Stay for the gossip",
    "about the other entries.",
]
for line in lines:
    if line:
        text_left(x, y, line, body_font)
    y += 31

y += 2
text_left(x, y, "\u2014 Your host, jokelord", italic_font)
y += 40
d.line([(x, y), (x + 470, y)], fill=(196, 164, 116), width=2)
y += 10
text_left(x, y, "P.S. No calendar invite \u2014 a letter felt warmer.", small_font, warm)

img.save("/home/hatch/workspace/bounty/makefun/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/bot/entry.png")
print("saved")
