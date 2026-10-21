import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import art
from PIL import Image, ImageDraw
from art import INK, NAVY, GOLD, WHITE

W, H = 1080, 1800
T = {
 "en": dict(kicker="Child as your insurance nominee?", title="Nominee Checklist",
   steps=[("Check every nominee", "On every life insurance and takaful policy, including their percentage shares."),
          ("Appoint a trustee", "If any nominee is under 18, appoint a trustee you trust, aged 18 or above."),
          ("Update after life events", "Married, divorced or had a child since your last update? Review now."),
          ("Write a will", "Name a guardian for your young children and an executor for the rest of your estate."),
          ("Tell them where documents are", "So your nominee and trustee can act quickly when it matters.")],
   cta="Free nomination review: advisorx.my",
   disc="General information only, not financial or legal advice.|Source: Financial Services Act 2013, Schedule 10. Rules differ for Muslim policy owners."),
 "zh": dict(kicker="孩子是你的保险提名人？", title="提名五步检查清单",
   steps=[("检查每一位提名人", "名下每份人寿保险和伊斯兰保险，包括分配比例。"),
          ("委任信托人", "如果有提名人未满18岁，请委任一位年满18岁、你信任的信托人。"),
          ("人生大事后要更新", "上次更新后结了婚、离了婚或生了孩子？现在就检查。"),
          ("立一份遗嘱", "为孩子指定监护人，为其他遗产指定遗嘱执行人。"),
          ("告诉他们文件在哪里", "让提名人和信托人在关键时刻能迅速处理。")],
   cta="免费检查提名：advisorx.my",
   disc="仅供一般参考，不构成理财或法律建议。|资料来源：《2013年金融服务法》附表10。|穆斯林保单持有人规则不同。"),
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
        th = art.text_img(h, 40, INK, width=720, align="left")
        ts = art.text_img(s, 30, (80, 90, 110), width=720, w="Medium", align="left")
        ch = th.height + ts.height + 44
        c = art.card(W - 120, ch, WHITE, radius=28, outline=INK); cd = ImageDraw.Draw(c)
        cd.ellipse([24, ch // 2 - 34, 92, ch // 2 + 34], fill=GOLD, outline=INK, width=4)
        n = art.text_img(str(i + 1), 40, NAVY, width=60); c.alpha_composite(n, (58 - n.width // 2, ch // 2 - n.height // 2 - 2))
        c.alpha_composite(th, (120, 20)); c.alpha_composite(ts, (120, 24 + th.height))
        ck = art.icon("check", 56); c.alpha_composite(ck, (c.width - 80, ch // 2 - 28))
        c = art.shadowed(c, 6, 8, 40); bg.alpha_composite(c, (60 - (c.width - (W - 120)) // 2, y - 20)); y += ch + 18
    p = art.pill(t["cta"], 44, GOLD, NAVY, padx=44, pady=18); bg.alpha_composite(p, ((W - p.width) // 2, y + 6))
    dls = [art.text_img(x, 22, (130, 135, 150), width=960, w="Regular") for x in t["disc"].split("|")]
    ds = Image.new("RGBA", (max(x.width for x in dls), sum(x.height for x in dls)), (0, 0, 0, 0)); yy = 0
    for x in dls: ds.alpha_composite(x, ((ds.width - x.width) // 2, yy)); yy += x.height
    fy = y + 6 + p.height + 20; bg.alpha_composite(ds, ((W - ds.width) // 2, fy))
    bg = bg.crop((0, 0, W, fy + ds.height + 30))
    bg.convert("RGB").save(f"out/ep03checklist_{L}.jpg", quality=93)
    print(L, "bottom y", y)
