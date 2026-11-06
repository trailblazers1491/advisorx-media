#!/usr/bin/env python3
"""Build the Week 2 ("Stuck in job") Monday + Friday carousels (6 slides each,
1080x1350) in the same visual system as recruitment/week1.

Usage: python3 build_carousels.py
Reads photos from ./photos_src/*.jpg (downloaded free stock photos).
Writes recruitment/week2/wk2_mon_0N.jpg and wk2_fri_0N.jpg.
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLKIT = os.path.join(HERE, "..", "..", "toolkit")
sys.path.insert(0, TOOLKIT)
import art
import aina as AinaMod

W, H = 1080, 1350
DARK = (7, 16, 11)
GREEN = (4, 218, 69)
GREEN_HOVER = (2, 121, 38)
ORANGE = (244, 158, 11)
MINT = (227, 249, 236)
HEADING_DARK = (0, 24, 8)
WHITE = (255, 255, 255)
INK = art.INK

PHOTO_DIR = os.path.join(HERE, "photos_src")
OUT_DIR = HERE


def load_bg(name, w=W, h=H):
    im = Image.open(os.path.join(PHOTO_DIR, name)).convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((int(sw * scale) + 1, int(sh * scale) + 1), Image.LANCZOS)
    sw, sh = im.size
    x0, y0 = (sw - w) // 2, (sh - h) // 2
    im = im.crop((x0, y0, x0 + w, y0 + h))
    return im.convert("RGBA")


def grad(w, h, stops, horizontal=False):
    """stops: list of (pos0..1, (r,g,b,a))"""
    im = Image.new("RGBA", (w, h))
    px = im.load()
    n = h if not horizontal else w
    ramp = []
    for i in range(n):
        t = i / max(1, n - 1)
        for j in range(len(stops) - 1):
            p0, c0 = stops[j]; p1, c1 = stops[j + 1]
            if p0 <= t <= p1 or j == len(stops) - 2:
                tt = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                tt = max(0, min(1, tt))
                col = tuple(int(c0[k] + (c1[k] - c0[k]) * tt) for k in range(4))
                ramp.append(col)
                break
    if horizontal:
        for x in range(w):
            for y in range(0, h, h):
                pass
        row = Image.new("RGBA", (w, 1))
        row.putdata(ramp)
        im = row.resize((w, h))
    else:
        col_im = Image.new("RGBA", (1, h))
        col_im.putdata(ramp)
        im = col_im.resize((w, h))
    return im


def rings_bg(w, h, base):
    im = Image.new("RGBA", (w, h), base + (255,))
    overlay = grad(w, h, [(0, (255, 255, 255, 0)), (1, (0, 0, 0, 70))])
    im.alpha_composite(overlay)
    d = ImageDraw.Draw(im, "RGBA")
    cx, cy = w * 0.62, h * 0.30
    for r in (420, 300, 190):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 28), width=26)
    return im


def text_lines(lines, size, width, w="Black", lh=1.2, align="left"):
    """lines: [(text, color), ...] -> composed RGBA image, left aligned block."""
    imgs = [art.text_img(t, size, c, width=width, w=w, align="left") for t, c in lines]
    W_ = max(i.width for i in imgs)
    gap = int(size * (lh - 1))
    H_ = sum(i.height for i in imgs) + gap * (len(imgs) - 1)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    y = 0
    for i in imgs:
        out.alpha_composite(i, (0, y))
        y += i.height + gap
    return out


def multiline(text, size, color, width, w="Black", lh=1.2):
    """art.text_img does NOT treat '\\n' as a forced line break (wrap() folds it
    into whitespace), so any text with explicit newlines must go through here
    instead, which splits on '\\n' itself and stacks each line with text_lines."""
    return text_lines([(t, color) for t in text.split("\n")], size, width, w=w, lh=lh)


def outline_pill(text, size=32, color=ORANGE, padx=34, pady=16):
    t = art.text_img(text, size, color, width=800, w="Bold")
    w_, h_ = t.width + padx * 2, t.height + pady * 2
    im = art.canvas(w_, h_)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([art.OUT, art.OUT, w_ * art.SS - art.OUT, h_ * art.SS - art.OUT], (h_ * art.SS) // 2,
                        outline=color, width=art.OUT)
    im = art.done(im)
    im.alpha_composite(t, (padx, pady))
    return im


def filled_pill(text, size=34, fill=GREEN, color=HEADING_DARK, padx=40, pady=22, arrow=False):
    label = text + ("  →" if arrow else "")
    t = art.text_img(label, size, color, width=900, w="Bold")
    w_, h_ = t.width + padx * 2, t.height + pady * 2
    im = art.card(w_, h_, fill, radius=h_ // 2)
    im.alpha_composite(t, (padx, pady - 2))
    return art.shadowed(im, 8, 14, 90)


def whatsapp_pill(text="WhatsApp us", size=36):
    chat = art.icon("chat", size=64)
    t = art.text_img(text, size, WHITE, width=900, w="Bold")
    padx, pady, gap = 34, 20, 18
    w_ = chat.width + gap + t.width + padx * 2
    h_ = max(chat.height, t.height) + pady * 2
    im = art.card(w_, h_, (8, 18, 10), radius=h_ // 2)
    im.alpha_composite(chat, (padx, (h_ - chat.height) // 2))
    im.alpha_composite(t, (padx + chat.width + gap, (h_ - t.height) // 2))
    return art.shadowed(im, 8, 14, 90)


def number_chip(n, size=86, fill=GREEN):
    im = art.card(size, size, fill, radius=24)
    t = art.text_img(str(n), 44, HEADING_DARK, width=size, w="Black")
    im.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2 - 2))
    return art.shadowed(im, 6, 16, 90)


def insight_card(w_, number, title, sub, dark_fill=(8, 16, 11, 215), chip_fill=GREEN, number_light=False):
    pad = 44
    title_im = art.text_img(title, 46, WHITE, width=w_ - pad * 2 - 20, w="Black", align="left")
    sub_im = art.text_img(sub, 30, (170, 210, 190), width=w_ - pad * 2 - 20, w="Medium" if False else "Bold", align="left") if sub else None
    chip = number_chip(number, fill=chip_fill)
    h_ = pad * 2 + chip.height + 24 + title_im.height + (14 + sub_im.height if sub_im else 0)
    im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w_, h_], 34, fill=dark_fill)
    im.alpha_composite(chip, (pad, pad))
    y = pad + chip.height + 24
    im.alpha_composite(title_im, (pad, y))
    y += title_im.height + 14
    if sub_im:
        im.alpha_composite(sub_im, (pad, y))
    return art.shadowed(im, 10, 18, 70)


def benefit_row(w_, number, title, sub, style="white"):
    pad_x, pad_y = 30, 22
    chip_slot = 96   # fixed horizontal slot for the (shadow-padded) chip image
    tx = pad_x + chip_slot
    chip = number_chip(number, size=66, fill=GREEN if style != "dark" else ORANGE)
    title_im = art.text_img(title, 32, HEADING_DARK if style != "dark" else WHITE, width=w_ - tx - pad_x, w="Black", align="left")
    sub_im = art.text_img(sub, 24, (70, 80, 76) if style != "dark" else (190, 220, 205), width=w_ - tx - pad_x, w="Bold", align="left")
    h_ = pad_y * 2 + max(66, title_im.height + 8 + sub_im.height)
    im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fill = WHITE if style == "white" else HEADING_DARK
    d.rounded_rectangle([0, 0, w_, h_], 28, fill=fill)
    im.alpha_composite(chip, (pad_x - (chip.width - 66) // 2, (h_ - chip.height) // 2))
    ty = (h_ - (title_im.height + 8 + sub_im.height)) // 2
    im.alpha_composite(title_im, (tx, ty))
    im.alpha_composite(sub_im, (tx, ty + title_im.height + 8))
    return art.shadowed(im, 6, 12, 60) if style == "dark" else im


def header(im, idx, total):
    logo = art.logo_badge()
    im.alpha_composite(logo, (56, 50))
    counter = art.pill(f"{idx} / {total}", size=32, fill=(10, 20, 14), color=WHITE, outline=None)
    im.alpha_composite(counter, (W - counter.width - 56, 50))


def footer_source(im, text, light=False):
    t = art.text_img(text, 21, (210, 225, 218) if light else (160, 190, 172), width=w_max(), w="Bold", align="left")
    im.alpha_composite(t, (56, H - t.height - 48))


def w_max():
    return W - 112


def save(im, name):
    im.convert("RGB").save(os.path.join(OUT_DIR, name), quality=92)
    print("wrote", name)


# ---------------------------------------------------------------- MONDAY ----

def mon_slide1():
    bg = load_bg("stressed_laptop.jpg")
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 10, 7, 235)), (0.42, (5, 10, 7, 160)), (0.62, (5, 10, 7, 90)), (1, (5, 10, 7, 235))]))
    header(im, 1, 6)
    tag = outline_pill("CAREER CHECK", color=ORANGE)
    im.alpha_composite(tag, (56, 300))
    head = text_lines([
        ("Still at the same", WHITE),
        ("desk. Still waiting", WHITE),
        ("for the", WHITE),
        ("‘right time.’", GREEN),
    ], 70, 640, w="Black")
    im.alpha_composite(head, (56, 380))
    sub = multiline("Malaysia's median salary grew 7.3% this year.\nDid yours move at all?", 32, MINT, 620, w="Bold")
    im.alpha_composite(sub, (56, 380 + head.height + 36))
    pill = filled_pill("Swipe", arrow=True)
    im.alpha_composite(pill, (56, H - pill.height - 60))
    char = AinaMod.aina_with_prop_text("worried", "THIS MONTH'S\nRAISE", "RM0", scale=1.05)
    im.alpha_composite(char, (W - char.width - 10, H - char.height - 40))
    save(im, "wk2_mon_01.jpg")


def mon_slide2():
    bg = load_bg("typing_keyboard.jpg")
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 12, 8, 210)), (0.5, (5, 12, 8, 120)), (1, (5, 16, 9, 235))]))
    header(im, 2, 6)
    tagcard = Image.new("RGBA", (300, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(tagcard)
    d.rounded_rectangle([0, 10, 280, 150], 18, fill=(246, 240, 228), outline=None)
    tag_year = art.text_img("2023", 26, (80, 80, 88), width=250, w="Bold")
    tag_amt = art.text_img("RM2,602", 46, (40, 40, 46), width=250, w="Black")
    tagcard.alpha_composite(tag_year, (24, 30))
    tagcard.alpha_composite(tag_amt, (24, 68))
    d.line([(16, 140), (266, 36)], fill=(205, 60, 50), width=6)
    im.alpha_composite(art.shadowed(tagcard, 6, 10, 70), (72, 300))

    stat = Image.new("RGBA", (420, 230), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stat)
    sd.rounded_rectangle([0, 0, 400, 210], 26, fill=(7, 16, 11, 235), outline=GREEN, width=5)
    y2024 = art.text_img("2024", 28, GREEN, width=360, w="Black")
    amt = Image.new("RGBA", (380, 110), (0, 0, 0, 0))
    ad = ImageDraw.Draw(amt)
    rm = art.text_img("RM", 44, WHITE, width=120, w="Black")
    big = art.text_img("2,793", 86, WHITE, width=320, w="Black")
    amt.alpha_composite(rm, (0, 36))
    amt.alpha_composite(big, (rm.width + 6, 0))
    stat.alpha_composite(y2024, (34, 30))
    stat.alpha_composite(amt, (30, 80))
    im.alpha_composite(art.shadowed(stat, 8, 16, 90), (296, 490))

    badge = Image.new("RGBA", (190, 190), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.ellipse([0, 0, 170, 170], fill=ORANGE, outline=INK, width=art.OUT)
    pct = art.text_img("+7.3%", 36, HEADING_DARK, width=160, w="Black")
    badge.alpha_composite(pct, ((170 - pct.width) // 2, (170 - pct.height) // 2))
    im.alpha_composite(art.shadowed(badge, 6, 14, 80), (690, 450))

    label = art.text_img("NATIONAL MEDIAN SALARY · DOSM", 28, GREEN, width=w_max(), w="Black")
    im.alpha_composite(label, (56, 860))
    head = text_lines([("Salaries moved.", WHITE), ("Did your pay packet", WHITE), ("move with it?", GREEN)], 56, w_max(), w="Black")
    im.alpha_composite(head, (56, 908))
    footer_source(im, "Photo: free stock · Wages: DOSM, Salaries & Wages Survey 2024")
    save(im, "wk2_mon_02.jpg")


def mon_slide3():
    bg = load_bg("worried_computer.jpg")
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 10, 7, 225)), (0.48, (5, 10, 7, 130)), (1, (5, 10, 7, 235))]))
    header(im, 3, 6)

    def bar(label, v23, v24, y):
        bw = 700
        row = Image.new("RGBA", (bw, 150), (0, 0, 0, 0))
        rd = ImageDraw.Draw(row)
        lab = art.text_img(label, 28, WHITE, width=bw - 20, w="Bold")
        row.alpha_composite(lab, (0, 0))
        base_y = 54
        track = 360
        w23 = int(track * (v23 / 8))
        w24 = int(track * (v24 / 8))
        rd.rounded_rectangle([0, base_y, w23, base_y + 22], 10, fill=(100, 108, 104))
        rd.rounded_rectangle([0, base_y + 32, w24, base_y + 32 + 22], 10, fill=GREEN)
        t23 = art.text_img(f"2023: {v23}%", 22, (215, 220, 216), width=260, w="Bold")
        t24 = art.text_img(f"2024: {v24}%", 22, GREEN, width=260, w="Black")
        row.alpha_composite(t23, (track + 20, base_y - 2))
        row.alpha_composite(t24, (track + 20, base_y + 28))
        im.alpha_composite(row, (56, y))

    panel = Image.new("RGBA", (W - 112, 420), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([0, 0, W - 112, 400], 32, fill=(7, 16, 11, 225))
    im.alpha_composite(panel, (56, 330))

    bar("Skilled workers' pay rise", 7.5, 6.5, 360)
    bar("Semi-skilled workers' pay rise", 6.0, 5.2, 540)

    label = art.text_img("THE RAISE IS SHRINKING · DOSM 2024", 26, ORANGE, width=w_max(), w="Black")
    im.alpha_composite(label, (56, 790))
    head = text_lines([("Even the yearly", WHITE), ("increment is getting", WHITE), ("smaller.", ORANGE)], 60, w_max(), w="Black")
    im.alpha_composite(head, (56, 836))
    footer_source(im, "Source: DOSM, Salaries & Wages Survey Report 2024")
    save(im, "wk2_mon_03.jpg")


def mon_slide4():
    bg = load_bg("tired_desk.jpg")
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 10, 7, 60)), (0.3, (5, 10, 7, 180)), (1, (5, 10, 7, 235))]))
    header(im, 4, 6)
    label = art.text_img("THE GOLDEN HANDCUFFS", 26, GREEN, width=w_max(), w="Black")
    im.alpha_composite(label, (56, 280))
    c1 = insight_card(W - 112, 1, "You've got seniority,", "But the raise still doesn't match it.")
    im.alpha_composite(c1, (56, 340))
    c2 = insight_card(W - 112, 2, "‘Just one more year’", "...is what you told yourself last year too.")
    im.alpha_composite(c2, (56, 340 + c1.height + 28))
    save(im, "wk2_mon_04.jpg")


def mon_slide5():
    im = Image.new("RGBA", (W, H))
    bgphoto = load_bg("confident_woman.jpg")
    bgphoto.putalpha(90)
    base = grad(W, H, [(0, (176, 214, 192, 255)), (1, (227, 249, 236, 255))])
    im.alpha_composite(base)
    im.alpha_composite(bgphoto)
    im.alpha_composite(grad(W, H, [(0, (176, 214, 192, 60)), (0.55, (210, 236, 220, 40)), (1, (227, 249, 236, 215))]))
    header(im, 5, 6)
    label = art.text_img("GOOD NEWS", 30, (8, 110, 46), width=w_max(), w="Black")
    im.alpha_composite(label, (56, 290))
    head = multiline("Your experience is worth\nmore outside the cubicle too.", 54, HEADING_DARK, 820, w="Black")
    im.alpha_composite(head, (56, 336))
    sub = multiline("Build a part-time or full-time career in financial\nplanning, starting from where you are:", 28, (30, 60, 42), 820, w="Bold")
    im.alpha_composite(sub, (56, 336 + head.height + 24))
    y = 336 + head.height + 24 + sub.height + 30
    rows = [
        (1, "Keep your current job", "Start part-time, on evenings and weekends."),
        (2, "Earn on effort, not tenure", "Your income isn't capped by years of service."),
        (3, "A supported start", "Training, a mentor & financial support for serious joiners."),
    ]
    for i, (n, t, s) in enumerate(rows):
        style = "dark" if i == len(rows) - 1 else "white"
        row = benefit_row(640, n, t, s, style=style)
        im.alpha_composite(row, (56, y))
        y += row.height + 20
    char = AinaMod.aina("happy", scale=1.05)
    im.alpha_composite(char, (W - char.width + 20, H - char.height - 10))
    save(im, "wk2_mon_05.jpg")


def cta_slide(idx, total, out_name, headline, sub):
    im = rings_bg(W, H, (4, 142, 48))
    header(im, idx, total)
    head = multiline(headline, 62, HEADING_DARK, 760, w="Black")
    im.alpha_composite(head, (56, 420))
    sub_im = multiline(sub, 32, (4, 50, 20), 740, w="Bold")
    im.alpha_composite(sub_im, (56, 420 + head.height + 26))
    wa = whatsapp_pill()
    im.alpha_composite(wa, (56, 420 + head.height + 26 + sub_im.height + 40))
    note = art.text_img("Link in caption · Save & share with a friend", 24, (4, 70, 28), width=700, w="Bold")
    im.alpha_composite(note, (56, 420 + head.height + 26 + sub_im.height + 40 + wa.height + 24))
    char = AinaMod.aina_idea(scale=1.0)
    im.alpha_composite(char, (W - char.width + 10, H - char.height - 10))
    save(im, out_name)


def mon_slide6():
    cta_slide(6, 6, "wk2_mon_06.jpg", "Ready to stop\nwaiting for the\n‘right time’?",
              "Join our FREE weekly online career talk.\n45 minutes. No commitment.")


# ---------------------------------------------------------------- FRIDAY ----

def fri_slide1():
    bg = load_bg("stressed_charts.jpg")
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 10, 7, 235)), (0.42, (5, 10, 7, 150)), (0.62, (5, 10, 7, 90)), (1, (5, 10, 7, 235))]))
    header(im, 1, 6)
    tag = outline_pill("SELF-CHECK", color=GREEN)
    im.alpha_composite(tag, (56, 300))
    head = text_lines([("5 signs you're", WHITE), ("stuck, not just", WHITE), ("busy.", GREEN)], 70, w_max() - 160, w="Black")
    im.alpha_composite(head, (56, 380))
    sub = art.text_img("(And what to do about it.)", 34, ORANGE, width=620, w="Bold")
    im.alpha_composite(sub, (56, 380 + head.height + 30))
    pill = filled_pill("Count how many fit you", arrow=True)
    im.alpha_composite(pill, (56, H - pill.height - 60))
    char = AinaMod.aina("shocked", scale=1.05)
    im.alpha_composite(char, (W - char.width - 10, H - char.height - 40))
    save(im, "wk2_fri_01.jpg")


def fri_signs_slide(idx, bg_name, items, total=6):
    bg = load_bg(bg_name)
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 10, 7, 40)), (0.32, (5, 10, 7, 170)), (1, (5, 10, 7, 235))]))
    header(im, idx, total)
    y = 300
    for n, t, s, chip in items:
        c = insight_card(W - 112, n, t, s, chip_fill=chip)
        im.alpha_composite(c, (56, y))
        y += c.height + 28
    footer_source(im, "Photo: free stock photo")
    save(im, f"wk2_fri_0{idx}.jpg")


def fri_slide4():
    bg = load_bg("tired_desk.jpg")
    im = Image.new("RGBA", (W, H))
    im.alpha_composite(bg)
    im.alpha_composite(grad(W, H, [(0, (5, 10, 7, 40)), (0.34, (5, 10, 7, 190)), (1, (5, 10, 7, 235))]))
    header(im, 4, 6)
    c = insight_card(W - 112, 5, "You're staying for ‘stability’", "The paycheck is steady. Your peace of mind isn't.", chip_fill=ORANGE)
    im.alpha_composite(c, (56, 440))
    tick = art.text_img("Ticked 2 or more? Keep swiping.", 36, WHITE, width=w_max(), w="Bold")
    im.alpha_composite(tick, (56, 440 + c.height + 60))
    save(im, "wk2_fri_04.jpg")


def fri_slide5():
    im = Image.new("RGBA", (W, H))
    bgphoto = load_bg("confident_woman.jpg")
    bgphoto.putalpha(90)
    base = grad(W, H, [(0, (176, 214, 192, 255)), (1, (227, 249, 236, 255))])
    im.alpha_composite(base)
    im.alpha_composite(bgphoto)
    im.alpha_composite(grad(W, H, [(0, (176, 214, 192, 60)), (0.55, (210, 236, 220, 40)), (1, (227, 249, 236, 215))]))
    header(im, 5, 6)
    label = art.text_img("GOOD NEWS", 30, (8, 110, 46), width=w_max(), w="Black")
    im.alpha_composite(label, (56, 290))
    head = multiline("You don't have to quit\nto find out.", 54, HEADING_DARK, 820, w="Black")
    im.alpha_composite(head, (56, 336))
    sub = art.text_img("Try a part-time career in financial planning:", 28, (30, 60, 42), width=900, w="Bold", align="left")
    im.alpha_composite(sub, (56, 336 + head.height + 24))
    y = 336 + head.height + 24 + sub.height + 30
    rows = [
        (1, "Flexible hours", "Evenings and weekends."),
        (2, "Keep your income", "Start part-time — no need to resign first."),
        (3, "A supported start", "Training, mentor & financial support for serious joiners."),
    ]
    for i, (n, t, s) in enumerate(rows):
        style = "dark" if i == len(rows) - 1 else "white"
        row = benefit_row(640, n, t, s, style=style)
        im.alpha_composite(row, (56, y))
        y += row.height + 20
    char = AinaMod.aina("happy", scale=1.05)
    im.alpha_composite(char, (W - char.width + 20, H - char.height - 10))
    save(im, "wk2_fri_05.jpg")


def fri_slide6():
    cta_slide(6, 6, "wk2_fri_06.jpg", "See if this\ncareer fits you.",
              "Join our FREE weekly online career talk.\n45 minutes. No commitment.")


if __name__ == "__main__":
    mon_slide1(); mon_slide2(); mon_slide3(); mon_slide4(); mon_slide5(); mon_slide6()
    fri_slide1()
    fri_signs_slide(2, "clock_plant.jpg", [
        (1, "You've stopped expecting", "next year to be different from this one.", GREEN),
        (2, "You've outgrown the role,", "but not the title. Same tasks as 3 years ago.", GREEN),
    ])
    fri_signs_slide(3, "phone_night.jpg", [
        (3, "Payday barely covers", "the rising cost of living — this year's raise too.", GREEN),
        (4, "You dread Monday", "more than you enjoy Friday.", GREEN),
    ])
    fri_slide4()
    fri_slide5()
    fri_slide6()
