import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import art
from PIL import Image, ImageDraw
from art import INK, NAVY, GOLD, WHITE

W, H = 1080, 1800
T = {
 "en": dict(kicker="Before you switch to MediAsas", title="Medical Card Checklist",
   steps=[("List all family medical policies", "Include employer cover. Note each limit, deductible and premium."),
          ("Note new health conditions", "Anything diagnosed since you bought your card. A new plan may not cover it."),
          ("Ask your insurer first", "A higher deductible or co-payment may lower your premium."),
          ("Compare side by side", "When MediAsas launches (Jan 2027): limits, deductibles, panel hospitals, exclusions."),
          ("Don't cancel too early", "Keep your old cover until the new one is approved and the waiting period is covered.")],
   cta="Free medical cover review: advisorx.my",
   disc="General information only, not financial advice. Source: Bank Negara Malaysia, as reported."),
 "zh": dict(kicker="转去 MediAsas 之前", title="医药卡五步检查清单",
   steps=[("列出全家医药保单", "包括雇主团体保险，记下限额、自付额和保费。"),
          ("记下新确诊的病症", "买医药卡之后才确诊的病，新计划可能不保。"),
          ("先问保险公司", "提高自付额或共同付费，可能降低保费。"),
          ("逐项比较", "2027 年 1 月推出后，比较限额、自付额、指定医院和不受保项目。"),
          ("别太早取消", "新保单获批、等待期也过了，才取消旧保单。")],
   cta="免费医药保障检视：advisorx.my",
   disc="仅供一般参考，不构成理财建议。资料来源：国家银行（据报道）。"),
}
for L, t in T.items():
    bg = Image.new("RGBA", (W, H), (255, 249, 238, 255)); d = ImageDraw.Draw(bg)
    d.rectangle([0, 0, W, 330], fill=NAVY)
    for x, y, r in ((960, 60, 4), (880, 140, 3), (1020, 220, 3), (60, 280, 3), (140, 40, 2)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 200))
    lg = art.real_logo(44, WHITE); bg.alpha_composite(lg, (60, 50))
    k = art.text_img(t["kicker"], 36, GOLD, width=700, w="Bold", align="left"); bg.alpha_composite(k, (60, 130))
    ti = art.text_img(t["title"], 58 if L == "en" else 70, WHITE, width=720, align="left"); bg.alpha_composite(ti, (60, 180))
    m = art.character("alex", "happy", scale=0.72); bg.alpha_composite(m, (W - m.width - 30, 330 - m.height + 36))
    y = 370
    for i, (h, s) in enumerate(t["steps"]):
        th = art.text_img(h, 40, INK, width=760, align="left")
        ts = art.text_img(s, 30, (80, 90, 110), width=760, w="Medium", align="left")
        ch = th.height + ts.height + 44
        c = art.card(W - 120, ch, WHITE, radius=28, outline=INK); cd = ImageDraw.Draw(c)
        cd.ellipse([24, ch // 2 - 34, 92, ch // 2 + 34], fill=GOLD, outline=INK, width=4)
        n = art.text_img(str(i + 1), 40, NAVY, width=60); c.alpha_composite(n, (58 - n.width // 2, ch // 2 - n.height // 2 - 2))
        c.alpha_composite(th, (120, 20)); c.alpha_composite(ts, (120, 24 + th.height))
        ck = art.icon("check", 56); c.alpha_composite(ck, (c.width - 80, ch // 2 - 28))
        c = art.shadowed(c, 6, 8, 40); bg.alpha_composite(c, (60 - (c.width - (W - 120)) // 2, y - 20)); y += ch + 18
    p = art.pill(t["cta"], 44, GOLD, NAVY, padx=44, pady=18); bg.alpha_composite(p, ((W - p.width) // 2, y + 6))
    ds = art.text_img(t["disc"], 22, (130, 135, 150), width=960, w="Regular")
    fy = y + 6 + p.height + 20; bg.alpha_composite(ds, ((W - ds.width) // 2, fy))
    bg = bg.crop((0, 0, W, fy + ds.height + 30))
    bg.convert("RGB").save(f"out/checklist_{L}.jpg", quality=93)
    print(L, "bottom y", y)
