"""Aina mascot: flat 2D cartoon character kit extension for AdvisorX recruitment content.

Aina, 29 — tudung-wearing office worker. Drawn with the same supersample /
PIL-primitive approach as `alex()` in art.py, so it can be composited with
the rest of the art kit (cards, pills, icons, logo badge).

Moods: "worried", "shocked", "happy", "idea".
Props (drawn attached to the raised/front hand): "phone_balance", "receipt",
"sparkle_only", "lightbulb".

NOTE ON SCOPE: toolkit/art.py as committed to this repo only implements a
male "alex" mascot (see STYLES / alex() in art.py) — there is no "aina"
character defined anywhere in the toolkit or its git history. The Week 1
recruitment carousels nonetheless show a female, tudung-wearing mascot named
Aina (mustard tudung, white blouse, green AdvisorX lanyard; moods shocked /
worried / happy / idea), matching what the client described. That mascot's
source was evidently never committed. This module recreates her from the
Week 1 JPEGs (same palette, proportions and props) using art.py's existing
drawing primitives, so Week 2 (and future weeks) can keep using her
consistently and the code is now actually in the repo.
"""
import math
from PIL import Image, ImageDraw
import art
from art import canvas, done, shadowed, SS, INK, WHITE, GREEN, RED

# ---------------- palette (sampled from Week 1 renders) ----------------
A_SKIN = (247, 207, 173)
A_CHEEK = (246, 150, 140)
TUDUNG = (229, 170, 64)        # outer tudung — same GOLD as art.py
TUDUNG_IN = (196, 139, 41)     # inner cap (darker gold)
TUDUNG_LINE = (150, 104, 28)
BLOUSE = (255, 255, 255)
LANYARD = (10, 20, 14)         # badge card ink
BADGE_GREEN = GREEN if 'GREEN' in dir(art) else (76, 175, 110)


def _lightbulb(d, cx, cy, s):
    """Small lightbulb glyph (glass + base) at (cx, cy), scaled by s."""
    r = 30 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 210, 90), outline=INK, width=int(4 * s))
    d.rectangle([cx - 10 * s, cy + r - 6 * s, cx + 10 * s, cy + r + 14 * s], fill=(170, 170, 178), outline=INK, width=int(3 * s))
    for i in range(3):
        y = cy + r + 2 * s + i * 5 * s
        d.line([cx - 10 * s, y, cx + 10 * s, y], fill=INK, width=int(2 * s))
    # filament (two simple diagonal strokes, not a zigzag that reads as a letter)
    d.line([cx - 9 * s, cy - 8 * s, cx + 9 * s, cy + 8 * s], fill=INK, width=int(2.5 * s))
    d.line([cx - 9 * s, cy + 8 * s, cx + 9 * s, cy - 8 * s], fill=INK, width=int(2.5 * s))
    # rays
    for ang in (-40, 20, 70, 140, 200, 250):
        a = math.radians(ang)
        x0, y0 = cx + math.cos(a) * (r + 10 * s), cy + math.sin(a) * (r + 10 * s)
        x1, y1 = cx + math.cos(a) * (r + 26 * s), cy + math.sin(a) * (r + 26 * s)
        d.line([x0, y0, x1, y1], fill=(250, 210, 90), width=int(5 * s))


def _sparkle(d, cx, cy, r, color=(90, 230, 130)):
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i
        rad = r if i % 2 == 0 else r * 0.35
        pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
    d.polygon(pts, fill=color)


def aina(mood="happy", prop=None, scale=1.0, blink=False):
    """Returns a transparent PNG (PIL Image) of Aina, standing, ~360x600 at scale=1.

    mood: "worried" | "shocked" | "happy" | "idea"
    prop: None | "phone_balance" (amount shown via prop_text) | "receipt" (amount via prop_text) | "lightbulb" | "sparkle_only"
    """
    W, H = int(380 * scale), int(620 * scale)
    im = canvas(W, H)
    d = ImageDraw.Draw(im)
    S = SS * scale
    cx = W * SS / 2

    shoulder_y = 330 * S
    bot = H * SS - 4 * S

    # ---- body: white blouse ----
    body = [(cx - 112 * S, bot), (cx - 118 * S, shoulder_y + 40 * S), (cx - 70 * S, shoulder_y),
            (cx + 70 * S, shoulder_y), (cx + 118 * S, shoulder_y + 40 * S), (cx + 112 * S, bot)]
    d.polygon(body, fill=BLOUSE, outline=INK, width=art.OUT)
    # collar v
    d.polygon([(cx - 36 * S, shoulder_y + 4 * S), (cx + 36 * S, shoulder_y + 4 * S), (cx, shoulder_y + 70 * S)],
               fill=(236, 240, 238), outline=INK, width=art.OUT // 2)

    # ---- arms ----
    raised = mood in ("idea", "happy")
    for sx in (-1, 1):
        x0 = cx + sx * 100 * S
        if raised and sx == 1:
            # right arm raised up beside the head
            d.line([(x0, shoulder_y + 30 * S), (x0 + 46 * S, shoulder_y - 90 * S)], fill=BLOUSE, width=int(40 * S))
            hx, hy = x0 + 50 * S, shoulder_y - 128 * S
            d.ellipse([hx - 24 * S, hy - 24 * S, hx + 24 * S, hy + 24 * S], fill=A_SKIN, outline=INK, width=art.OUT)
            # one finger / peace-ish up
            d.rounded_rectangle([hx - 8 * S, hy - 48 * S, hx + 8 * S, hy - 10 * S], 8 * S, fill=A_SKIN, outline=INK, width=art.OUT // 2)
        else:
            d.line([(x0, shoulder_y + 30 * S), (x0 + sx * 16 * S, shoulder_y + 150 * S)], fill=BLOUSE, width=int(40 * S))
            hx, hy = x0 + sx * 16 * S, shoulder_y + 176 * S
            if mood == "worried" and sx == -1:
                hy -= 30 * S  # hand up near chin
            d.ellipse([hx - 24 * S, hy - 24 * S, hx + 24 * S, hy + 24 * S], fill=A_SKIN, outline=INK, width=art.OUT)

    # ---- green AdvisorX lanyard ----
    for sx in (-1, 1):
        d.line([(cx + sx * 30 * S, shoulder_y + 2 * S), (cx + sx * 10 * S, shoulder_y + 170 * S)],
               fill=(60, 200, 110), width=int(10 * S))
    d.rounded_rectangle([cx - 24 * S, shoulder_y + 160 * S, cx + 24 * S, shoulder_y + 230 * S], 10 * S,
                        fill=(60, 200, 110), outline=INK, width=art.OUT // 2)
    d.rounded_rectangle([cx - 17 * S, shoulder_y + 167 * S, cx + 17 * S, shoulder_y + 223 * S], 6 * S, fill=WHITE)

    # ---- neck ----
    d.rectangle([cx - 24 * S, shoulder_y - 28 * S, cx + 24 * S, shoulder_y + 6 * S], fill=A_SKIN)

    # ---- head + tudung ----
    hy = shoulder_y - 160 * S           # head centre y
    hr = 108 * S                        # face radius

    # outer tudung: a draped robe shape from the crown down past both shoulders
    outer = [
        (cx, hy - hr - 48 * S),
        (cx - hr - 10 * S, hy - hr + 30 * S),
        (cx - hr - 40 * S, hy + 30 * S),
        (cx - 96 * S, shoulder_y + 230 * S),
        (cx - 48 * S, shoulder_y + 210 * S),
        (cx, shoulder_y + 190 * S),
        (cx + 48 * S, shoulder_y + 210 * S),
        (cx + 96 * S, shoulder_y + 230 * S),
        (cx + hr + 40 * S, hy + 30 * S),
        (cx + hr + 10 * S, hy - hr + 30 * S),
    ]
    d.polygon(outer, fill=TUDUNG, outline=INK, width=art.OUT)

    # face skin oval
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=A_SKIN, outline=INK, width=art.OUT)

    # inner cap framing the face (darker gold): forehead band + under-chin wrap
    d.chord([cx - hr - 2 * S, hy - hr - 2 * S, cx + hr + 2 * S, hy + hr + 2 * S], 195, 345,
            fill=TUDUNG_IN, outline=INK, width=art.OUT)
    # re-expose the face (skin) under the forehead band, keep a thin gold edge showing
    d.ellipse([cx - hr + 16 * S, hy - hr + 34 * S, cx + hr - 16 * S, hy + hr - 6 * S], fill=A_SKIN)
    # under-chin wrap piece
    d.chord([cx - 58 * S, hy + 36 * S, cx + 58 * S, hy + 132 * S], 0, 180, fill=TUDUNG_IN, outline=INK, width=art.OUT // 2)
    d.chord([cx - 46 * S, hy + 40 * S, cx + 46 * S, hy + 110 * S], 0, 180, fill=A_SKIN)

    # brows / eyes
    ey = hy + 2 * S
    ex = 42 * S
    for sx in (-1, 1):
        x = cx + sx * ex
        tilt = 10 * S if mood == "worried" else 0
        lift = -10 * S if mood == "shocked" else 0
        d.line([(x - 20 * S, ey - 36 * S + lift - sx * tilt), (x + 20 * S, ey - 40 * S + lift + sx * tilt)],
               fill=(70, 50, 24), width=int(art.OUT * 1.3))
        if blink:
            d.line([(x - 16 * S, ey), (x + 16 * S, ey)], fill=INK, width=art.OUT)
        elif mood == "happy":
            d.arc([x - 20 * S, ey - 12 * S, x + 20 * S, ey + 16 * S], 200, 340, fill=INK, width=int(art.OUT * 1.4))
        else:
            r = (20 if mood == "shocked" else 15) * S
            d.ellipse([x - r, ey - r, x + r, ey + r], fill=INK)
            d.ellipse([x - r * .15, ey - r * .65, x + r * .45, ey - r * .05], fill=WHITE)

    # cheeks
    for sx in (-1, 1):
        x = cx + sx * 66 * S
        d.ellipse([x - 18 * S, ey + 46 * S, x + 18 * S, ey + 64 * S], fill=A_CHEEK)

    # mouth
    my = ey + 62 * S
    if mood == "happy":
        d.chord([cx - 32 * S, my - 18 * S, cx + 32 * S, my + 24 * S], 0, 180, fill=(150, 50, 60), outline=INK, width=art.OUT)
        d.chord([cx - 28 * S, my - 2 * S, cx + 28 * S, my + 12 * S], 0, 180, fill=WHITE)
    elif mood == "shocked":
        d.ellipse([cx - 15 * S, my - 6 * S, cx + 15 * S, my + 26 * S], fill=(150, 50, 60), outline=INK, width=art.OUT)
    elif mood == "worried":
        d.arc([cx - 20 * S, my + 2 * S, cx + 20 * S, my + 22 * S], 200, 340, fill=INK, width=art.OUT)
    else:  # idea / neutral-positive
        d.line([cx - 16 * S, my + 8 * S, cx - 4 * S, my + 14 * S, cx + 16 * S, my + 4 * S], fill=INK, width=art.OUT, joint="curve")

    # sweat drop for worried
    if mood == "worried":
        x, y = cx + hr - 14 * S, hy - hr + 70 * S
        d.polygon([(x, y - 16 * S), (x - 10 * S, y + 6 * S), (x, y + 14 * S), (x + 10 * S, y + 6 * S)],
                  fill=(120, 200, 235), outline=INK, width=art.OUT // 2)

    im = done(im)

    # ---- props (added on the *downscaled* image so text/icons stay crisp) ----
    if prop == "sparkle_only" or mood == "happy":
        for (dx, dy, r, col) in ((-62, -18, 11, (90, 230, 130)), (40, -34, 15, (90, 230, 130))):
            pr = int(r * scale)
            pim = Image.new("RGBA", (pr * 6, pr * 6), (0, 0, 0, 0))
            pd = ImageDraw.Draw(pim)
            _sparkle(pd, pr * 3, pr * 3, pr)
            im.alpha_composite(pim, (int(cx / SS + dx * scale - pr * 3), int((hy - hr) / SS + dy * scale - pr * 3)))

    return im


def aina_with_prop_text(mood, prop_label, prop_value, value_color=(205, 40, 40), scale=1.0):
    """Aina plus a small white card prop (used for 'shocked'/'worried' slides),
    e.g. prop_label='BALANCE', prop_value='RM23'."""
    base = aina(mood, scale=scale)
    cw, ch = int(150 * scale), int(94 * scale)
    card = art.card(cw, ch, WHITE, radius=int(14 * scale), outline=INK)
    cd = ImageDraw.Draw(card)
    lab = art.text_img(prop_label, int(13 * scale), (60, 60, 68), width=cw - 20, w="Bold")
    val = art.text_img(prop_value, int(22 * scale), value_color, width=cw - 20, w="Black")
    card.alpha_composite(lab, ((cw - lab.width) // 2, int(14 * scale)))
    card.alpha_composite(val, ((cw - val.width) // 2, int(38 * scale)))
    card = shadowed(card, 6, 8, 60)
    out = Image.new("RGBA", (base.width + 40, base.height), (0, 0, 0, 0))
    out.alpha_composite(base, (0, 0))
    # place card near the raised/forward hand
    px = int(base.width * 0.60)
    py = int(base.height * 0.52) if mood == "shocked" else int(base.height * 0.56)
    out.alpha_composite(card, (px, py))
    return out


def aina_idea(scale=1.0):
    base = aina("idea", scale=scale)
    out = Image.new("RGBA", (base.width + 30, base.height + 30), (0, 0, 0, 0))
    out.alpha_composite(base, (0, 10))
    lb = Image.new("RGBA", (int(140 * scale), int(140 * scale)), (0, 0, 0, 0))
    lbd = ImageDraw.Draw(lb)
    _lightbulb(lbd, int(70 * scale), int(70 * scale), scale)
    out.alpha_composite(lb, (int(base.width * 0.66), 0))
    for (dx, dy, r) in ((8, 60, 9), (-6, 110, 12)):
        pr = int(r * scale)
        pim = Image.new("RGBA", (pr * 6, pr * 6), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pim)
        _sparkle(pd, pr * 3, pr * 3, pr, (120, 230, 150))
        out.alpha_composite(pim, (int(base.width * 0.20 + dx * scale), int(dy * scale)))
    return out
