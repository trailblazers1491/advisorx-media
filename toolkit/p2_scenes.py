# ---------- scenes (Part 2) ----------
def row_card(icon_name, title, sub, w=900, fill=WHITE, icon_color=None):
    ic = art.icon(icon_name, 130, color=icon_color)
    t1 = art.text_img(title, 50, INK, width=w - 230, align="left")
    t2 = art.text_img(sub, 40, (90, 100, 120), width=w - 230, w="Bold", align="left")
    h = max(ic.height, t1.height + t2.height + 10) + 60
    c = art.card(w, h, fill, radius=40, outline=INK)
    c.alpha_composite(ic, (35, (h - ic.height) // 2))
    y = (h - t1.height - t2.height - 10) // 2
    c.alpha_composite(t1, (190, y)); c.alpha_composite(t2, (190, y + t1.height + 10))
    return art.shadowed(c, 10, 14, 50)

def step_row(n, text, w=900, done=False):
    t = art.text_img(text, 46, INK, width=w - 260, w="Bold", align="left")
    h = max(96, t.height + 40)
    c = art.card(w, h, WHITE, radius=30, outline=INK); d = ImageDraw.Draw(c)
    d.ellipse([28, h // 2 - 32, 92, h // 2 + 32], fill=GOLD, outline=INK, width=4)
    nt = art.text_img(str(n), 40, NAVY, width=60); c.alpha_composite(nt, (60 - nt.width // 2, h // 2 - nt.height // 2))
    c.alpha_composite(t, (120, (h - t.height) // 2))
    return art.shadowed(c, 6, 8, 40)

S = []
# 0 hook
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[1], 11), pill=L["pills"][0], els=[
    E(big_card([(L["hook"], 76, INK, "Black")]), 540, 360, at(0, 0, 0), "pop"),
    E(rot(chip(L["switch"], (190, 240, 200), size=56, w=320), -6), 230, 640, at(0, 0, .5), "slide_l"),
    E(rot(chip(L["keep"], (200, 225, 255), size=56, w=320), 6), 850, 640, at(0, 0, .6), "slide_r"),
    CH("alex", "happy", 540, 640, at(0, 0, .2), 1.15),
    E(art.icon("question", 110), 200, 860, at(0, 0, .8), "pop"),
    E(art.icon("question", 90), 880, 880, at(0, 0, .9), "pop"),
    E(rot(art.pill(L["depends"], 84, RED, WHITE, padx=56, pady=24), -5), 540, 1180, at(0, 1, 0), "pop", pulse=at(0, 1, .5)),
]))
# 1 may suit
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[2], 12), pill=L["pills"][1], els=[
    CH("dad", "happy", 300, 340, at(1, 0, 0), 0.9, phase=.5),
    E(art.icon("check", 120), 470, 360, at(1, 0, .2), "pop"),
    E(row_card("shield", L["c1_t"], L["c1"]), 540, 820, at(1, 0, .1), "slide_b"),
    CH("mum", "happy", 780, 340, at(1, 1, 0), 0.9, phase=1.6),
    E(art.icon("check", 120), 950, 360, at(1, 1, .2), "pop"),
    E(row_card("doc", L["c2_t"], L["c2"]), 540, 1060, at(1, 1, .1), "slide_b"),
]))
# 2 think twice
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[4], 13), pill=L["pills"][2], els=[
    CH("mum", "worried", 300, 360, at(2, 0, 0), 1.0, phase=.9),
    E(art.icon("heart", 170), 760, 380, at(2, 0, .15), "pop"),
    E(art.icon("hospital", 170), 790, 570, at(2, 0, .3), "pop"),
    E(chip(L["w1"], (255, 230, 220), size=48, w=880), 540, 880, at(2, 0, .2), "slide_b", pulse=at(2, 0, .7)),
    E(art.icon("padlock", 110), 105, 1135, at(2, 1, 0), "pop"),
    E(chip(L["w2"], WHITE, size=44, w=760), 610, 1130, at(2, 1, .1), "slide_r"),
]))
# 3 smart move
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[3], 14), pill=L["pills"][3], els=[
    CH("alex", "happy", 300, 380, at(3, 0, 0), 1.05, phase=.3),
    E(big_card([(L["floor"], 62, NAVY, "Black"), (L["floor_sub"], 42, (90, 100, 120), "Bold")], w=560), 760, 440, at(3, 0, .2), "pop", pulse=at(3, 0, .7)),
    E(art.icon("shield", 140), 900, 740, at(3, 0, .4), "pop", color=(130, 200, 150)),
    E(art.icon("phone", 170), 190, 1000, at(3, 1, 0), "slide_l"),
    E(chip(L["ask"], (255, 240, 200), size=46, w=740), 640, 1020, at(3, 1, .1), "slide_r"),
]))
# 4 checklist (ticks as each step is spoken)
els4 = [E(art.icon("doc", 130), 160, 330, at(4, 0, 0), "pop")]
for i, txt in enumerate(L["steps"]):
    y = 470 + i * 160
    els4.append(E(step_row(i + 1, txt), 520, y, at(4, i + 1, 0), "slide_r"))
    els4.append(E(art.icon("check", 90), 930, y + 18, at(4, i + 1, .6), "pop"))
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[0], 15, floor=False), pill=L["pills"][4], els=els4))
# 5 CTA (dark)
S.append(dict(bg=art.stars_bg(W, H, (22, 38, 62), NAVY), pill=None, dark=True, els=[
    E(art.logo_badge(True), 540, 230, 0.1, "pop"),
    E(art.text_img(L["q"], 80, WHITE, width=1000), 540, 380, at(5, 0, 0), "pop"),
    E(art.icon("question", 110), 160, 520, at(5, 0, .3), "pop"),
    E(art.icon("question", 80), 930, 560, at(5, 0, .4), "pop"),
    CH("alex", "happy", 540, 520, at(5, 0, .2), 1.05),
    E(art.pill(L["cta"], 64, GOLD, NAVY, padx=56, pady=24, outline=INK), 540, 1020, at(5, 1, 0), "pop", pulse=at(5, 1, .7)),
    E(art.pill(L["follow"], 52, WHITE, NAVY, padx=46, pady=18), 540, 1190, at(5, 2, 0), "pop"),
    E(art.text_img(L["disclaimer"], 24, (170, 180, 200), width=880, w="Regular"), 540, 1580, at(5, 2, .2), "fade"),
]))
