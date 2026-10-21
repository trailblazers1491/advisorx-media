# ---------- scenes (Ep03: child nominee) ----------
def row_card(icon_name, title, sub, w=900, fill=WHITE, icon_color=None):
    ic = art.icon(icon_name, 130, color=icon_color)
    t1 = art.text_img(title, 52, INK, width=w - 230, align="left")
    t2 = art.text_img(sub, 40, (90, 100, 120), width=w - 230, w="Bold", align="left")
    h = max(ic.height, t1.height + t2.height + 10) + 60
    c = art.card(w, h, fill, radius=40, outline=INK)
    c.alpha_composite(ic, (35, (h - ic.height) // 2))
    y = (h - t1.height - t2.height - 10) // 2
    c.alpha_composite(t1, (190, y)); c.alpha_composite(t2, (190, y + t1.height + 10))
    return art.shadowed(c, 10, 14, 50)

def arrow_down(h=110, color=NAVY):
    im = Image.new("RGBA", (120, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([45, 0, 75, h - 50], fill=color); d.polygon([(10, h - 55), (110, h - 55), (60, h - 2)], fill=color)
    return im

S = []
# 0 hook
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[1], 21), pill=L["pills"][0], els=[
    E(big_card([(L["hook"], 74, INK, "Black")]), 540, 380, at(0, 0, 0), "pop"),
    CH("alex", "surprised", 330, 680, at(0, 0, .15), 1.0),
    CH("kid", "happy", 780, 820, at(0, 0, .3), 0.7, phase=1.1),
    E(rot(chip(L["nom_kid"], (255, 240, 200), size=44, w=520), 4), 780, 690, at(0, 0, .5), "pop"),
    E(art.icon("question", 100), 140, 660, at(0, 0, .7), "pop"),
    E(rot(art.pill(L["miss"], 70, RED, WHITE, padx=50, pady=22), -4), 540, 1110, at(0, 1, 0), "pop", pulse=at(0, 1, .5)),
]))
# 1 the rule
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[2], 22), pill=L["pills"][1], els=[
    CH("kid", "worried", 300, 380, at(1, 0, 0), 0.85, phase=.4),
    E(rot(art.pill(L["u18"], 60, GOLD, NAVY, padx=40, pady=18), -6), 300, 800, at(1, 0, .2), "pop"),
    E(art.icon("moneybag", 190), 760, 420, at(1, 0, .15), "pop"),
    E(art.icon("xmark", 110), 880, 590, at(1, 0, .4), "pop"),
    E(chip(L["cant"], (255, 230, 220), size=50, w=860), 540, 1000, at(1, 0, .3), "slide_b", pulse=at(1, 0, .8)),
    E(row_card("doc", L["someone"], "", w=900), 540, 1150, at(1, 1, 0), "slide_b"),
]))
# 2 the catch
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[4], 23), pill=L["pills"][2], els=[
    E(chip(L["notrustee"], WHITE, size=56, w=600), 540, 380, at(2, 0, 0), "pop"),
    E(arrow_down(), 540, 525, at(2, 0, .3), "fade"),
    CH("mum", "happy", 300, 650, at(2, 0, .4), 0.85, phase=.7),
    E(chip(L["other"], (214, 236, 252), size=44, w=440), 780, 640, at(2, 0, .5), "slide_r"),
    CH("dad", "worried", 790, 810, at(2, 1, 0), 0.62, phase=1.3),
    E(rot(art.pill(L["ex"], 60, RED, WHITE, padx=44, pady=20), -3), 540, 1160, at(2, 1, 0), "pop", pulse=at(2, 1, .5)),
]))
# 3 worst case
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[3], 24), pill=L["pills"][3], els=[
    E(chip(L["both"], WHITE, size=56, w=700), 540, 380, at(3, 0, 0), "pop"),
    E(art.icon("padlock", 170), 190, 560, at(3, 0, .3), "pop"),
    E(big_card([(L["pt"], 62, NAVY, "Black"), (L["pt_sub"], 40, (90, 100, 120), "Bold")], w=640), 620, 550, at(3, 0, .35), "pop", pulse=at(3, 0, .8)),
    CH("uncle", "worried", 220, 870, at(3, 1, 0), 0.8, phase=.2),
    CH("mum", "worried", 450, 900, at(3, 1, .1), 0.72, phase=1.4),
    E(chip(L["say"], (255, 230, 220), size=46, w=500), 835, 1030, at(3, 1, .2), "slide_r"),
]))
# 4 plan B: brother
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[0], 25), pill=L["pills"][4], els=[
    CH("uncle", "happy", 280, 390, at(4, 0, 0), 0.85, phase=.6),
    E(rot(chip(L["nom_bro"], (255, 240, 200), size=46, w=560), 3), 740, 500, at(4, 0, .3), "pop"),
    E(row_card("doc", L["exec"], L["exec_sub"], w=900), 540, 900, at(4, 1, 0), "slide_b"),
    E(art.icon("xmark", 120), 150, 1150, at(4, 2, 0), "pop"),
    E(chip(L["notauto"], (255, 230, 220), size=46, w=780), 610, 1150, at(4, 2, .1), "slide_r", pulse=at(4, 2, .6)),
]))
# 5 CTA (dark) - Alex hosts
S.append(dict(bg=art.stars_bg(W, H, (22, 38, 62), NAVY), pill=None, dark=True, els=[
    E(art.logo_badge(True), 540, 210, 0.1, "pop"),
    E(art.text_img(L["q"], 76, WHITE, width=960), 540, 360, at(5, 0, 0), "pop"),
    E(art.icon("question", 110), 150, 600, at(5, 0, .3), "pop"),
    E(art.icon("question", 80), 940, 640, at(5, 0, .4), "pop"),
    CH("alex", "happy", 540, 560, at(5, 0, .2), 1.0),
    E(art.pill(L["cta"], 64, GOLD, NAVY, padx=56, pady=24, outline=INK), 540, 1060, at(5, 1, 0), "pop", pulse=at(5, 1, .7)),
    E(art.text_img(L["cta_sub"], 44, (255, 240, 200), width=900, w="Bold"), 540, 1225, at(5, 1, .3), "fade"),
    E(art.pill(L["follow"], 50, WHITE, NAVY, padx=46, pady=18), 540, 1530, at(5, 2, 0), "pop"),
] + [E(art.text_img(dl, 26, (170, 180, 200), width=960, w="Regular"), 540, 1680 + 38 * k, at(5, 2, .2), "fade")
     for k, dl in enumerate(L["disclaimer"].split("|"))]))
