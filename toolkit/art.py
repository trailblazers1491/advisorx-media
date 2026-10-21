import os
"""Flat 2D cartoon art kit: characters, icons, cards, pills. Drawn at 2x then downscaled for smooth edges."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SS = 2                                   # supersample factor
INK = (35, 38, 52)                       # outline colour
OUT = 4 * SS                             # ~4px outlines
NAVY = (14, 27, 44); GOLD = (229, 170, 64); CREAM = (255, 249, 238)
RED = (232, 76, 61); GREEN = (76, 175, 110); WHITE = (255, 255, 255)
SKIN = (248, 214, 186); CHEEK = (246, 160, 160)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-{}.ttc"

_f = {}
def font(size, w="Black"):
    k = (size, w)
    if k not in _f: _f[k] = ImageFont.truetype(FONT.format(w), size, index=2)
    return _f[k]

def canvas(w, h): return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
def done(im): return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)

def wrap(text, f, width):
    import re
    toks = re.findall(r"[A-Za-z0-9,.\-–'’%$/()+:=\"“”>≠~]+\s*|\s+|.", text)
    lines, line = [], ""
    for t in toks:
        if f.getlength((line + t).rstrip()) <= width or not line or t[0] in "，。？！：；、）」”?!,.:;": line += t
        else: lines.append(line.rstrip()); line = t.lstrip()
    lines.append(line.rstrip()); return [l for l in lines if l]

def text_img(text, size, color=INK, width=900, w="Black", align="center", lh=1.22):
    f = font(size * SS, w); lines = wrap(text, f, width * SS); step = int(size * SS * lh)
    cw = int(max([width * SS] + [f.getlength(l) + 4 for l in lines]))
    im = Image.new("RGBA", (cw, step * len(lines) + int(size * SS * .35)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = {"center": (cw - f.getlength(ln)) / 2, "left": 0}[align]
        d.text((x, i * step), ln, font=f, fill=color)
    bb = im.getbbox() or (0, 0, 2, 2)
    return done(im.crop((0 if align == "left" else bb[0], 0, bb[2] if align == "center" else im.width, im.height)))

def shadowed(im, off=10, blur=14, alpha=60):
    pad = blur * 2 + off
    base = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (20, 30, 50, 0)); sh.putalpha(im.getchannel("A").point(lambda v: v * alpha // 255))
    base.alpha_composite(sh, (pad, pad + off)); base = base.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(im, (pad, pad)); return base

def card(w, h, fill=WHITE, radius=40, outline=None):
    im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle([OUT // 2, OUT // 2, w * SS - OUT // 2, h * SS - OUT // 2], radius * SS, fill=fill,
                        outline=outline, width=OUT if outline else 0)
    return done(im)

def compose(base, items):
    """items: list of (img, x_center, y_top)"""
    for img, x, y in items: base.alpha_composite(img, (int(x - img.width / 2), int(y)))
    return base

def pill(text, size=54, fill=WHITE, color=INK, padx=48, pady=20, outline=INK):
    t = text_img(text, size, color, width=980)
    w, h = t.width + padx * 2, t.height + pady * 2
    im = card(w, h, fill, radius=h // 2, outline=outline)
    im.alpha_composite(t, (padx, pady + 2)); return shadowed(im, 8, 10, 50)

# ---------------- characters ----------------
STYLES = {
    "dad":     dict(shirt=(96, 156, 232), hair=(45, 40, 48), hairstyle="short"),
    "mum":     dict(shirt=(240, 128, 150), hair=(60, 40, 40), hairstyle="bob"),
    "advisor": dict(shirt=WHITE, hair=(30, 30, 40), hairstyle="side", suit=NAVY, tie=GOLD, glasses=True),
    "alex":    dict(shirt=WHITE, hair=(30, 30, 40), hairstyle="side", suit=(28, 28, 32), tie=(18, 18, 22), glasses=True),
    "kid":     dict(shirt=(255, 196, 70), hair=(50, 36, 36), hairstyle="bob"),
    "uncle":   dict(shirt=(120, 190, 140), hair=(170, 170, 175), hairstyle="bald", glasses=True),
}

def character(kind="dad", mood="happy", blink=False, scale=1.0):
    if kind == "alex": return alex(mood, blink, scale)
    st = STYLES[kind]; W, H = int(360 * scale), int(520 * scale)
    im = canvas(W, H); d = ImageDraw.Draw(im); S = SS * scale
    cx = W * SS / 2
    # body
    top, bot = 300 * S, 515 * S
    body = [(cx - 120 * S, bot), (cx - 105 * S, top + 30 * S), (cx - 60 * S, top), (cx + 60 * S, top), (cx + 105 * S, top + 30 * S), (cx + 120 * S, bot)]
    d.polygon(body, fill=st.get("suit", st["shirt"]), outline=INK, width=OUT)
    if "suit" in st:
        d.polygon([(cx - 42 * S, top + 2 * S), (cx + 42 * S, top + 2 * S), (cx, top + 120 * S)], fill=WHITE, outline=INK, width=OUT)
        d.polygon([(cx - 13 * S, top + 18 * S), (cx + 13 * S, top + 18 * S), (cx + 18 * S, top + 105 * S), (cx, top + 130 * S), (cx - 18 * S, top + 105 * S)], fill=st["tie"], outline=INK, width=OUT // 2)
    # neck + head
    d.rectangle([cx - 28 * S, top - 30 * S, cx + 28 * S, top + 8 * S], fill=SKIN)
    hr = 130 * S; hy = 170 * S
    if st["hairstyle"] == "bob":
        d.rounded_rectangle([cx - hr - 18 * S, hy - hr - 12 * S, cx + hr + 18 * S, hy + 105 * S], 110 * S, fill=st["hair"], outline=INK, width=OUT)
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=SKIN, outline=INK, width=OUT)
    # ears
    for sx in (-1, 1):
        ex = cx + sx * (hr - 4 * S)
        d.ellipse([ex - 22 * S, hy - 5 * S, ex + 22 * S, hy + 40 * S], fill=SKIN, outline=INK, width=OUT)
    d.ellipse([cx - hr + 8 * S, hy - hr + 8 * S, cx + hr - 8 * S, hy + hr - 8 * S], fill=SKIN)
    # hair
    hs = st["hairstyle"]
    if hs in ("short", "side", "bob"):
        d.chord([cx - hr - 4 * S, hy - hr - 10 * S, cx + hr + 4 * S, hy + hr * 0.55], 180, 360, fill=st["hair"], outline=INK, width=OUT)
        if hs == "side":
            d.polygon([(cx - hr + 10 * S, hy - 40 * S), (cx + 30 * S, hy - hr - 6 * S), (cx + hr, hy - 30 * S), (cx + hr - 6 * S, hy - 10 * S), (cx + 20 * S, hy - 70 * S)], fill=st["hair"])
        else:
            fy = (hy - hr - 10 * S + hy + hr * 0.55) / 2   # flat edge of the hair chord
            for i in range(-3, 4):
                x = cx + i * 34 * S
                if abs(x - cx) < hr - 20 * S:
                    d.pieslice([x - 22 * S, fy - 22 * S, x + 22 * S, fy + 22 * S], 0, 180, fill=st["hair"])
    elif hs == "bald":
        for sx in (-1, 1):
            d.chord([cx + sx * hr - 40 * S, hy - 60 * S, cx + sx * hr + 40 * S, hy + 30 * S], 0, 360, fill=st["hair"], outline=INK, width=OUT // 2)
    # eyes
    ey = hy + 18 * S; ex = 50 * S
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.arc([x - 20 * S, ey - 10 * S, x + 20 * S, ey + 16 * S], 200, 340, fill=INK, width=OUT)
        else:
            r = (22 if mood == "surprised" else 17) * S
            d.ellipse([x - r, ey - r, x + r, ey + r], fill=INK)
            d.ellipse([x - r * .15, ey - r * .65, x + r * .45, ey - r * .05], fill=WHITE)
    if st.get("glasses"):
        for sx in (-1, 1):
            x = cx + sx * ex
            d.ellipse([x - 38 * S, ey - 34 * S, x + 38 * S, ey + 34 * S], outline=INK, width=OUT)
        d.line([cx - 12 * S, ey - 4 * S, cx + 12 * S, ey - 4 * S], fill=INK, width=OUT)
    # brows for mood
    if mood == "worried":
        for sx in (-1, 1):
            x = cx + sx * ex
            d.line([x - 22 * S, ey - 46 * S - sx * 6 * S, x + 22 * S, ey - 46 * S + sx * 6 * S], fill=INK, width=OUT)
    if mood == "surprised":
        for sx in (-1, 1):
            x = cx + sx * ex
            d.arc([x - 24 * S, ey - 70 * S, x + 24 * S, ey - 30 * S], 200, 340, fill=INK, width=OUT)
    # cheeks
    cy = hy + 62 * S
    for sx in (-1, 1):
        x = cx + sx * 82 * S
        d.ellipse([x - 24 * S, cy - 13 * S, x + 24 * S, cy + 13 * S], fill=CHEEK)
    # mouth
    my = hy + 72 * S
    if mood == "happy":
        d.arc([cx - 34 * S, my - 30 * S, cx + 34 * S, my + 18 * S], 20, 160, fill=INK, width=OUT)
    elif mood == "surprised":
        d.ellipse([cx - 18 * S, my - 12 * S, cx + 18 * S, my + 28 * S], fill=(140, 50, 60), outline=INK, width=OUT)
    else:
        d.arc([cx - 26 * S, my + 4 * S, cx + 26 * S, my + 34 * S], 200, 340, fill=INK, width=OUT)
    # arms
    for sx in (-1, 1):
        x0 = cx + sx * 104 * S
        d.line([x0, top + 50 * S, x0 + sx * 22 * S, top + 170 * S], fill=st.get("suit", st["shirt"]), width=44 * int(S))
        d.ellipse([x0 + sx * 22 * S - 26 * S, top + 150 * S, x0 + sx * 22 * S + 26 * S, top + 202 * S], fill=SKIN, outline=INK, width=OUT)
    return done(im)

# ---------------- icons ----------------
def icon(name, size=220, color=None, label=None):
    im = canvas(size, size); d = ImageDraw.Draw(im); s = size * SS; o = OUT
    def P(*pts): return [(x * s, y * s) for x, y in pts]
    if name == "shield":
        c = color or (110, 170, 240)
        d.polygon(P((.5, .05), (.9, .2), (.86, .55), (.5, .95), (.14, .55), (.1, .2)), fill=c, outline=INK, width=o)
        d.line(P((.32, .5), (.46, .64), (.7, .36)), fill=WHITE, width=int(s * .08), joint="curve")
    elif name == "hospital":
        d.rectangle(P((.12, .3), (.88, .92)), fill=WHITE, outline=INK, width=o)
        d.rectangle(P((.3, .1), (.7, .3)), fill=WHITE, outline=INK, width=o)
        d.rectangle(P((.44, .14), (.56, .26)), fill=RED); d.rectangle(P((.4, .18), (.6, .22)), fill=RED)
        for x in (.22, .42, .62):
            for y in (.4, .58):
                d.rectangle(P((x, y), (x + .14, y + .1)), fill=(170, 210, 245), outline=INK, width=o // 2)
        d.rectangle(P((.42, .74), (.58, .92)), fill=(240, 190, 120), outline=INK, width=o // 2)
    elif name == "moneybag":
        d.ellipse(P((.12, .3), (.88, .95)), fill=(240, 200, 100), outline=INK, width=o)
        d.polygon(P((.34, .32), (.66, .32), (.72, .12), (.28, .12)), fill=(240, 200, 100), outline=INK, width=o)
        d.line(P((.33, .32), (.67, .32)), fill=INK, width=o)
        f = font(int(s * .2)); d.text((s * .5, s * .64), "RM", font=f, fill=INK, anchor="mm")
    elif name == "phone":
        d.rounded_rectangle(P((.22, .04), (.78, .96)), int(s * .08), fill=(60, 64, 80), outline=INK, width=o)
        d.rounded_rectangle(P((.27, .12), (.73, .86)), int(s * .04), fill=(236, 246, 240))
        d.rounded_rectangle(P((.31, .22), (.69, .4)), int(s * .04), fill=(150, 225, 160))
        d.rounded_rectangle(P((.31, .46), (.6, .6)), int(s * .04), fill=WHITE)
    elif name == "doc":
        d.polygon(P((.2, .06), (.66, .06), (.82, .22), (.82, .94), (.2, .94)), fill=WHITE, outline=INK, width=o)
        for y in (.32, .46, .6, .74): d.line(P((.32, y), (.7, y)), fill=(190, 195, 210), width=int(s * .035))
    elif name == "padlock":
        d.arc(P((.28, .06), (.72, .56)), 180, 360, fill=INK, width=int(s * .09))
        d.rounded_rectangle(P((.18, .4), (.82, .92)), int(s * .08), fill=(240, 190, 80), outline=INK, width=o)
        d.ellipse(P((.44, .56), (.56, .68)), fill=INK); d.rectangle(P((.48, .62), (.52, .8)), fill=INK)
    elif name == "heart":
        d.ellipse(P((.1, .18), (.52, .6)), fill=RED, outline=INK, width=o); d.ellipse(P((.48, .18), (.9, .6)), fill=RED, outline=INK, width=o)
        d.polygon(P((.13, .46), (.87, .46), (.5, .9)), fill=RED, outline=INK, width=o)
        d.ellipse(P((.14, .22), (.5, .58)), fill=RED); d.ellipse(P((.5, .22), (.86, .58)), fill=RED)
        d.polygon(P((.18, .46), (.82, .46), (.5, .84)), fill=RED)
        d.line(P((.2, .5), (.36, .5), (.42, .38), (.5, .62), (.56, .46), (.8, .46)), fill=WHITE, width=int(s * .04))
    elif name == "xmark":
        d.ellipse(P((.06, .06), (.94, .94)), fill=RED, outline=INK, width=o)
        d.line(P((.32, .32), (.68, .68)), fill=WHITE, width=int(s * .12)); d.line(P((.68, .32), (.32, .68)), fill=WHITE, width=int(s * .12))
    elif name == "check":
        d.ellipse(P((.06, .06), (.94, .94)), fill=GREEN, outline=INK, width=o)
        d.line(P((.28, .52), (.44, .68), (.73, .36)), fill=WHITE, width=int(s * .11), joint="curve")
    elif name == "question":
        d.ellipse(P((.08, .08), (.92, .92)), fill=GOLD, outline=INK, width=o)
        d.text((s * .5, s * .48), "?", font=font(int(s * .62)), fill=WHITE, anchor="mm")
    elif name == "uparrow":
        d.polygon(P((.5, .04), (.92, .5), (.66, .5), (.66, .95), (.34, .95), (.34, .5), (.08, .5)), fill=RED, outline=INK, width=o)
    elif name == "sparkle":
        c = color or GOLD
        d.polygon(P((.5, 0), (.6, .4), (1, .5), (.6, .6), (.5, 1), (.4, .6), (0, .5), (.4, .4)), fill=c, outline=INK, width=o // 2)
    elif name == "scissors":
        d.ellipse(P((.08, .58), (.42, .92)), outline=INK, width=int(s * .07)); d.ellipse(P((.58, .58), (.92, .92)), outline=INK, width=int(s * .07))
        d.polygon(P((.36, .62), (.8, .06), (.86, .1), (.46, .66)), fill=(200, 205, 215), outline=INK, width=o // 2)
        d.polygon(P((.64, .62), (.2, .06), (.14, .1), (.54, .66)), fill=(200, 205, 215), outline=INK, width=o // 2)
    elif name == "chat":
        d.rounded_rectangle(P((.04, .1), (.96, .76)), int(s * .14), fill=(150, 225, 160), outline=INK, width=o)
        d.polygon(P((.2, .7), (.36, .74), (.14, .94)), fill=(150, 225, 160), outline=INK, width=o)
        d.polygon(P((.2, .68), (.36, .7), (.18, .86)), fill=(150, 225, 160))
    return done(im)

def stars_bg(W, H, top, bottom, n=60, seed=3):
    import random
    rnd = random.Random(seed)
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,))
    for _ in range(n):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.choice([2, 2, 3, 4])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 200, rnd.randint(120, 230)))
    return im

def pastel_bg(W, H, color, seed=1, floor=True):
    import random
    rnd = random.Random(seed)
    im = Image.new("RGBA", (W, H), color + (255,)); d = ImageDraw.Draw(im, "RGBA")
    for _ in range(9):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(60, 220)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 55))
    for _ in range(3):  # clouds
        x, y = rnd.randint(80, W - 200), rnd.randint(380, 700)
        for dx, dy, r in ((0, 0, 40), (45, -18, 52), (95, 0, 40)):
            d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(255, 255, 255, 120))
    if floor:
        fy = int(H * .70)
        d.rectangle([0, fy, W, H], fill=tuple(max(0, c - 18) for c in color) + (255,))
        d.line([0, fy, W, fy], fill=INK + (90,), width=4)
    return im

def logo_badge_old(big=False):
    size = 64 if big else 30
    f = font(size * SS, "Black")
    tw = f.getlength("ADVISOR") + f.getlength("X")
    w, h = int(tw / SS) + (56 if big else 30), int(size * 1.7)
    im = card(w, h, NAVY if big else WHITE, radius=h // 3, outline=INK if not big else GOLD)
    c = canvas(w, h); d = ImageDraw.Draw(c)
    x = (w * SS - tw) / 2; y = h * SS / 2
    d.text((x, y), "ADVISOR", font=f, fill=(WHITE if big else NAVY), anchor="lm")
    d.text((x + f.getlength("ADVISOR"), y), "X", font=f, fill=GOLD, anchor="lm")
    im.alpha_composite(done(c)); return im


# ---------------- Alex Song mascot (from his profile photo) ----------------
A_SKIN = (240, 200, 165); A_HAIR = (28, 28, 34); A_FADE = (96, 92, 98); SUIT = (30, 30, 36); SUIT_LINE = (110, 110, 122)
def alex(mood="happy", blink=False, scale=1.0, arms_crossed=False):
    W, H = int(360 * scale), int(520 * scale)
    im = canvas(W, H); d = ImageDraw.Draw(im); S = SS * scale; cx = W * SS / 2
    top, bot = 300 * S, 515 * S
    # suit body
    body = [(cx - 128 * S, bot), (cx - 115 * S, top + 30 * S), (cx - 62 * S, top), (cx + 62 * S, top), (cx + 115 * S, top + 30 * S), (cx + 128 * S, bot)]
    d.polygon(body, fill=SUIT, outline=INK, width=OUT)
    # white shirt V + collar
    d.polygon([(cx - 44 * S, top + 2 * S), (cx + 44 * S, top + 2 * S), (cx, top + 135 * S)], fill=WHITE, outline=INK, width=OUT)
    d.polygon([(cx - 44 * S, top + 2 * S), (cx - 8 * S, top + 26 * S), (cx - 30 * S, top + 44 * S)], fill=WHITE, outline=INK, width=OUT // 2)
    d.polygon([(cx + 44 * S, top + 2 * S), (cx + 8 * S, top + 26 * S), (cx + 30 * S, top + 44 * S)], fill=WHITE, outline=INK, width=OUT // 2)
    # black tie (grey outline so it reads on black)
    d.polygon([(cx - 11 * S, top + 22 * S), (cx + 11 * S, top + 22 * S), (cx + 7 * S, top + 36 * S), (cx - 7 * S, top + 36 * S)], fill=(14, 14, 18), outline=SUIT_LINE, width=OUT // 2)
    d.polygon([(cx - 7 * S, top + 36 * S), (cx + 7 * S, top + 36 * S), (cx + 15 * S, top + 125 * S), (cx, top + 150 * S), (cx - 15 * S, top + 125 * S)], fill=(14, 14, 18), outline=SUIT_LINE, width=OUT // 2)
    # lapels
    for sx in (-1, 1):
        d.line([(cx + sx * 44 * S, top + 2 * S), (cx + sx * 22 * S, top + 150 * S)], fill=SUIT_LINE, width=OUT // 2)
    # white pocket square (viewer's right)
    d.polygon([(cx + 62 * S, top + 92 * S), (cx + 100 * S, top + 84 * S), (cx + 98 * S, top + 96 * S), (cx + 64 * S, top + 102 * S)], fill=WHITE, outline=INK, width=OUT // 2)
    if arms_crossed:
        ay = top + 128 * S
        d.rounded_rectangle([cx - 132 * S, ay, cx + 132 * S, ay + 62 * S], 30 * S, fill=SUIT, outline=INK, width=OUT)
        d.line([(cx - 20 * S, ay + 6 * S), (cx + 30 * S, ay + 56 * S)], fill=SUIT_LINE, width=OUT // 2)
        # hands tucked: one hand on the left arm, white cuff on the right
        d.rounded_rectangle([cx - 150 * S, ay + 6 * S, cx - 92 * S, ay + 58 * S], 24 * S, fill=A_SKIN, outline=INK, width=OUT)
        d.rounded_rectangle([cx + 70 * S, ay + 4 * S, cx + 92 * S, ay + 58 * S], 8 * S, fill=WHITE, outline=INK, width=OUT // 2)
        d.rounded_rectangle([cx + 92 * S, ay + 8 * S, cx + 128 * S, ay + 54 * S], 20 * S, fill=A_SKIN, outline=INK, width=OUT)
    else:
        # relaxed arms at the sides: sleeve seam, white cuff, hand
        for sx in (-1, 1):
            x0 = cx + sx * 112 * S
            d.line([(x0, top + 50 * S), (x0 + sx * 12 * S, top + 148 * S)], fill=SUIT_LINE, width=OUT // 2)
            hx0 = x0 + sx * 8 * S
            d.rounded_rectangle([hx0 - 22 * S, top + 146 * S, hx0 + 22 * S, top + 162 * S], 6 * S, fill=WHITE, outline=INK, width=OUT // 2)
            d.ellipse([hx0 - 26 * S, top + 156 * S, hx0 + 26 * S, top + 206 * S], fill=A_SKIN, outline=INK, width=OUT)
    # neck
    d.rectangle([cx - 30 * S, top - 34 * S, cx + 30 * S, top + 6 * S], fill=A_SKIN)
    # head (slightly wide oval)
    hx, hyr, hy = 122 * S, 132 * S, 198 * S
    for sx in (-1, 1):  # ears
        ex = cx + sx * (hx - 2 * S)
        d.ellipse([ex - 24 * S, hy - 8 * S, ex + 24 * S, hy + 44 * S], fill=A_SKIN, outline=INK, width=OUT)
    d.ellipse([cx - hx, hy - hyr, cx + hx, hy + hyr], fill=A_SKIN, outline=INK, width=OUT)
    # faded short sides: thin segments of the head, above the ears
    d.chord([cx - hx, hy - hyr, cx + hx, hy + hyr], 188, 238, fill=(70, 68, 76))
    d.chord([cx - hx, hy - hyr, cx + hx, hy + hyr], 302, 352, fill=(70, 68, 76))
    d.ellipse([cx - hx, hy - hyr, cx + hx, hy + hyr], outline=INK, width=OUT)
    # slicked-back pompadour with a high, rounded hairline
    hair = [(cx - 108 * S, hy - 66 * S), (cx - 118 * S, hy - 100 * S), (cx - 108 * S, hy - 136 * S), (cx - 76 * S, hy - 166 * S),
            (cx - 30 * S, hy - 184 * S), (cx + 26 * S, hy - 188 * S), (cx + 76 * S, hy - 172 * S), (cx + 110 * S, hy - 140 * S),
            (cx + 122 * S, hy - 102 * S), (cx + 110 * S, hy - 66 * S), (cx + 90 * S, hy - 96 * S), (cx + 50 * S, hy - 112 * S),
            (cx, hy - 116 * S), (cx - 50 * S, hy - 112 * S), (cx - 88 * S, hy - 100 * S)]
    d.polygon(hair, fill=A_HAIR, outline=INK, width=OUT)
    d.line([(cx - 68 * S, hy - 106 * S), (cx - 86 * S, hy - 156 * S)], fill=(100, 100, 112), width=OUT // 2)   # side part
    for off in (-36, 6, 48):   # comb lines swept back
        d.arc([cx + off * S - 64 * S, hy - 178 * S, cx + off * S + 64 * S, hy - 86 * S], 210, 290, fill=(78, 78, 92), width=OUT // 2)
    # brows
    ey = hy + 14 * S; ex = 50 * S
    for sx in (-1, 1):
        x = cx + sx * ex; tilt = 7 * S if mood == "worried" else 0
        lift = -14 * S if mood == "surprised" else 0
        d.line([(x - 26 * S, ey - 34 * S + lift - sx * tilt), (x + 26 * S, ey - 38 * S + lift + sx * tilt)], fill=A_HAIR, width=int(OUT * 1.6))
    # eyes: smiling crescents when happy (like his photo)
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.line([(x - 18 * S, ey), (x + 18 * S, ey)], fill=INK, width=OUT)
        elif mood == "happy":
            d.arc([x - 22 * S, ey - 14 * S, x + 22 * S, ey + 18 * S], 200, 340, fill=INK, width=int(OUT * 1.4))
        else:
            r = (19 if mood == "surprised" else 15) * S
            d.ellipse([x - r, ey - r, x + r, ey + r], fill=INK)
            d.ellipse([x - r * .1, ey - r * .65, x + r * .5, ey - r * .05], fill=WHITE)
    # nose
    d.arc([cx - 16 * S, hy + 30 * S, cx + 16 * S, hy + 56 * S], 20, 160, fill=INK, width=OUT // 2 + 1)
    # cheeks
    for sx in (-1, 1):
        x = cx + sx * 84 * S
        d.ellipse([x - 22 * S, hy + 58 * S, x + 22 * S, hy + 78 * S], fill=(240, 160, 150))
    # mouth
    my = hy + 74 * S
    if mood == "happy":   # big open smile with teeth
        d.chord([cx - 44 * S, my - 26 * S, cx + 44 * S, my + 40 * S], 0, 180, fill=(150, 50, 60), outline=INK, width=OUT)
        d.chord([cx - 40 * S, my - 4 * S, cx + 40 * S, my + 18 * S], 0, 180, fill=WHITE)
        d.line([(cx - 43 * S, my + 7 * S), (cx + 43 * S, my + 7 * S)], fill=INK, width=OUT)
    elif mood == "surprised":
        d.ellipse([cx - 17 * S, my - 6 * S, cx + 17 * S, my + 32 * S], fill=(150, 50, 60), outline=INK, width=OUT)
    else:
        d.arc([cx - 26 * S, my + 6 * S, cx + 26 * S, my + 34 * S], 200, 340, fill=INK, width=OUT)
    return done(im)

_LOGO = {}
def real_logo(height=60, color=None):
    """The AdvisorX wordmark from Alex's logo file, background removed."""
    k = (height, color)
    if k not in _LOGO:
        import numpy as np
        src = Image.open(LOGO_PATH).convert("RGB"); a = np.asarray(src).astype(np.float32)
        bgc = a[2, 2]; dist = np.sqrt(((a - bgc) ** 2).sum(-1))
        alpha = np.clip((dist - 30) * 3, 0, 255).astype(np.uint8)
        rgb = np.zeros_like(a, dtype=np.uint8); rgb[:] = color or (11, 37, 69)
        im = Image.fromarray(np.dstack([rgb, alpha]), "RGBA"); im = im.crop(im.getbbox())
        _LOGO[k] = im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
    return _LOGO[k]
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "advisorx_logo.png")


def logo_badge(big=False):
    """Real AdvisorX logo: small white badge (top-right) or large navy card (end screen)."""
    if big:
        lg = real_logo(64, WHITE); w, h = lg.width + 70, lg.height + 44
        im = card(w, h, NAVY, radius=h // 3, outline=GOLD)
    else:
        lg = real_logo(30); w, h = lg.width + 34, lg.height + 22
        im = card(w, h, WHITE, radius=h // 3, outline=INK)
    im.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2)); return im
