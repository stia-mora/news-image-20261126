#!/usr/bin/env python3
"""Draw entry.png for news-image-20261126 from scratch with PIL.

Newspaper front page summarising verified world news of Thursday
26 November 2026. All artwork is vector shapes + system fonts.
No photos, no copied images, no AI generation.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (166, 30, 34)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
RULE = (26, 26, 26)
LIGHT = (233, 228, 216)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

M = 36  # margin


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines = []
    for para in s.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if text_w(draw, trial, f) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(x, y, lines, f, fill=INK, leading=None):
    if leading is None:
        leading = int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def hrule(y, x0=M, x1=W - M, width=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)
    return y + width


# ---------- masthead ----------
y = 24
f_mast = font(SERIF_B, 74)
mast = "THE WORLD TODAY"
d.text(((W - text_w(d, mast, f_mast)) / 2, y), mast, font=f_mast, fill=INK)
y += 86

f_date = font(SANS_B, 33)
date = "THURSDAY  \u2022  26 NOVEMBER 2026"
d.text(((W - text_w(d, date, f_date)) / 2, y), date, font=f_date, fill=RED)
y += 42

f_sub = font(SANS, 20)
sub = "SIX STORIES FROM AROUND THE GLOBE  \u2014  IN ONE PAGE"
d.text(((W - text_w(d, sub, f_sub)) / 2, y), sub, font=f_sub, fill=GREY)
y += 28

y = hrule(y, width=4)
y = hrule(y + 4, width=1)
y += 14

# ---------- lead story: tariffs ----------
f_kick = font(SANS_B, 20)
d.text((M, y), "TRADE  \u2022  WASHINGTON", font=f_kick, fill=RED)
y += 28

f_head = font(SERIF_B, 44)
lead_head = ["Trump fires new tariff salvo", "at 14 trading partners"]
y = draw_lines(M, y, lead_head, f_head, leading=50)
y += 8

# small declining-bars chart at right of lead body; caption inside the box
chart_x0, chart_y0 = W - M - 150, y
chart_x1, chart_y1 = W - M, y + 68
d.rectangle([chart_x0, chart_y0, chart_x1, chart_y1], outline=GREY, width=2)
bars = [30, 25, 20, 13]
bw = 22
for i, bh in enumerate(bars):
    x0 = chart_x0 + 14 + i * 34
    d.rectangle([x0, chart_y0 + 40 - bh, x0 + bw, chart_y0 + 40], fill=RED)
f_cap = font(SANS_B, 14)
cap = "NASDAQ -3%"
d.text((chart_x0 + (150 - text_w(d, cap, f_cap)) / 2, chart_y0 + 46),
       cap, font=f_cap, fill=GREY)

f_body = font(SANS, 23)
lead_body = ("China faces the highest rate, 20%, on top of duties "
             "from Trump's first term. The Nasdaq fell more than 3% "
             "as markets recoiled from the new levies.")
lines = wrap(d, lead_body, f_body, W - 2 * M - 170)
y = draw_lines(M, y, lines, f_body, leading=30)
y += 12
y = hrule(y, width=2)
y += 14

# ---------- row 2: two columns ----------
col_w = (W - 2 * M - 24) // 2
col2_x = M + col_w + 24

f_h2 = font(SERIF_B, 33)


def story(x, w, y0, kicker, headline, body, icon=None):
    f_k = font(SANS_B, 19)
    d.text((x, y0), kicker, font=f_k, fill=RED)
    yy = y0 + 26
    hl = wrap(d, headline, f_h2, w)
    yy = draw_lines(x, yy, hl, f_h2, leading=36)
    yy += 4
    f_b = font(SANS, 22)
    bl = wrap(d, body, f_b, w)
    yy = draw_lines(x, yy, bl, f_b, leading=27)
    return yy


y2 = story(
    M, col_w, y, "TECH  \u2022  WASHINGTON",
    "Vance: Nvidia chief Huang is \u201cunder no investigation\u201d",
    "Vice President JD Vance defended the reinstated CEO, saying "
    "he needs no pardon. Huang faces Congress next week.")
y2b = story(
    col2_x, col_w, y, "CONFLICT  \u2022  RED SEA",
    "Houthis threaten Saudi ports as coalition hits Hodeidah",
    "The Saudi-led coalition struck Yemen's port of Hodeidah. A day "
    "earlier a Houthi drone hit Riyadh's tallest tower, wounding 11.")
y = max(y2, y2b) + 14
y = hrule(y, width=2)
y += 14

# ---------- row 3: three columns ----------
col3_w = (W - 2 * M - 2 * 20) // 3
x2 = M + col3_w + 20
x3 = x2 + col3_w + 20
f_h3 = font(SERIF_B, 29)


def story3(x, w, y0, kicker, headline, body):
    f_k = font(SANS_B, 18)
    d.text((x, y0), kicker, font=f_k, fill=RED)
    yy = y0 + 25
    hl = wrap(d, headline, f_h3, w)
    yy = draw_lines(x, yy, hl, f_h3, leading=32)
    yy += 4
    f_b = font(SANS, 21)
    bl = wrap(d, body, f_b, w)
    yy = draw_lines(x, yy, bl, f_b, leading=27)
    return yy


ya = story3(
    M, col3_w, y, "DIPLOMACY  \u2022  PYONGYANG",
    "North Korea expels Swiss envoy",
    "Pyongyang gave the head of Switzerland's office 48 hours to "
    "leave, in a row over sanctions on a children's camp.")
yb = story3(
    x2, col3_w, y, "LATIN AMERICA  \u2022  CARTAGENA",
    "All hostages freed in Colombia siege",
    "Troops stormed a supermarket after a 17-hour siege; police "
    "later said 76 people were held. One gunman was killed.")
yc = story3(
    x3, col3_w, y, "USA  \u2022  THANKSGIVING",
    "Record crowds brave stormy Thanksgiving",
    "AAA expects 81.5m travellers; security lines topped an hour "
    "at Miami and JFK as a storm bears down on the East Coast.")
y = max(ya, yb, yc) + 14
y = hrule(y, width=2)
y += 14

# ---------- also in brief ----------
f_brief_h = font(SANS_B, 19)
d.text((M, y), "ALSO IN BRIEF", font=f_brief_h, fill=RED)
y += 24
f_brief = font(SANS, 20)
briefs = [
    "China launched Shenzhou 24, carrying the first Pakistani astronaut to its space station.",
    "A US jury convicted Huawei of conspiring to steal trade secrets and bank fraud.",
    "Democrats clinched a House majority of at least 259 seats, their largest since 1990.",
]
for b in briefs:
    d.text((M, y), "\u2022", font=f_brief, fill=RED)
    bl = wrap(d, b, f_brief, W - 2 * M - 24)
    y = draw_lines(M + 24, y, bl, f_brief, leading=25)
y += 2

y = hrule(y, width=4)
y += 8
f_foot = font(SANS, 17)
foot = ("Sources: Reuters, Associated Press, AFP, CNN, Al Jazeera  \u2014  "
        "wire reports of 26 Nov 2026 (Asia) / 25 Nov (US & Europe).")
d.text((M, y), foot, font=f_foot, fill=GREY)
y += 24
foot2 = "THE WORLD TODAY  \u2022  26 NOVEMBER 2026"
d.text(((W - text_w(d, foot2, f_foot)) / 2, y), foot2, font=f_foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
