import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import art
from PIL import Image, ImageDraw
from art import INK, NAVY, GOLD, WHITE, RED

def stroke_text(txt, size, fill, stroke=(20, 20, 30), sw=14, width=1000):
    f = art.font(size, "Black"); lines = art.wrap(txt, f, width)
    step = int(size * 1.12); w = int(max(f.getlength(l) for l in lines)) + sw * 4
    im = Image.new("RGBA", (w, step * len(lines) + sw * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (w - f.getlength(l)) / 2; y = sw * 2 + i * step
        d.text((x + 8, y + 10), l, font=f, fill=(0, 0, 0, 150), stroke_width=sw, stroke_fill=(0, 0, 0, 150))
        d.text((x, y), l, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return im

for L, t2, ban in [("en", "Cancel your card?", "The catch most people miss"), ("zh", "要取消医药卡？", "大多数人忽略这一点")]:
    bg = art.stars_bg(1080, 1920, (40, 20, 40), (14, 27, 44), n=40); d = ImageDraw.Draw(bg, "RGBA")
    for r, a in ((700, 40), (520, 55), (360, 70)): d.ellipse([540 - r, 1000 - r, 540 + r, 1000 + r], fill=(232, 76, 61, a))
    a1 = stroke_text("RM65", 300, GOLD); bg.alpha_composite(a1, ((1080 - a1.width) // 2, 150))
    a2 = stroke_text(t2, 120 if L == "en" else 130, WHITE, width=960); bg.alpha_composite(a2, ((1080 - a2.width) // 2, 500))
    ch = art.character("alex", "surprised", scale=1.7); bg.alpha_composite(ch, (540 - ch.width // 2, 790))
    for n, x, y, s in (("hospital", 70, 900, 230), ("xmark", 810, 880, 170), ("moneybag", 830, 1150, 180), ("question", 90, 1230, 130)):
        bg.alpha_composite(art.icon(n, s), (x, y))
    b = art.pill(ban, 60, RED, WHITE, padx=50, pady=22, outline=INK).rotate(-3, resample=Image.BICUBIC, expand=True)
    bg.alpha_composite(b, ((1080 - b.width) // 2, 1640))
    lg = art.logo_badge(True); bg.alpha_composite(lg, ((1080 - lg.width) // 2, 1800))
    bg.convert("RGB").save(f"out/cover_{L}.jpg", quality=92)

a = Image.open("out/cover_en.jpg").resize((405, 720)); b = Image.open("out/cover_zh.jpg").resize((405, 720))
s = Image.new("RGB", (810, 720)); s.paste(a, (0, 0)); s.paste(b, (405, 0)); s.save("out/covers.jpg")
