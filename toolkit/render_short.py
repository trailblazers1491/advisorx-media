"""Render the vertical cartoon short. Usage: render_short.py <en|zh> <outdir> [--stills]"""
import sys, os, json, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art, short_content
from art import INK, NAVY, GOLD, WHITE, RED, CREAM

W, H, FPS = 1080, 1920, 30
LANG = sys.argv[1]; OUT = sys.argv[2]; STILLS = "--stills" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
C = getattr(short_content, LANG.upper()); L = C["L"]
DURS = json.load(open(f"{HERE}/svo_{LANG}/durs.json"))
os.makedirs(OUT, exist_ok=True)
LEAD, GAP, TAIL, XF = 0.35, 0.22, 0.55, 0.3

# ---------- timeline ----------
scenes_t, lines_t, t = [], [], 0.0
for si, ds in enumerate(DURS):
    st = t; t += LEAD; row = []
    for d in ds: row.append((t, d)); t += d + GAP
    t += TAIL + (1.6 if si == len(DURS) - 1 else 0)
    scenes_t.append((st, t)); lines_t.append(row)
TOTAL = t

def at(si, li, frac=0.0, plus=0.0):
    s, d = lines_t[si][li]; return s - scenes_t[si][0] + frac * d + plus

# ---------- helpers ----------
def chip(text, fill=WHITE, color=INK, size=44, w=820):
    t = art.text_img(text, size, color, width=w - 80, w="Bold")
    c = art.card(t.width + 70, t.height + 40, fill, radius=34, outline=INK); c.alpha_composite(t, (35, 22))
    return art.shadowed(c, 8, 10, 45)

def big_card(lines, w=880, fill=WHITE):
    """lines: list of (text,size,color,weight)"""
    imgs = [art.text_img(tx, sz, col, width=w - 90, w=wt) for tx, sz, col, wt in lines]
    h = sum(i.height for i in imgs) + 18 * (len(imgs) - 1) + 80
    c = art.card(w, h, fill, radius=46, outline=INK); y = 40
    for i in imgs: c.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height + 18
    return art.shadowed(c, 10, 14, 50)

def bar(label, value, h, color, w=300):
    im = Image.new("RGBA", (w, h + 260), (0, 0, 0, 0))
    v = art.text_img(value, 64, INK, width=w + 80); im.alpha_composite(v, ((w - v.width) // 2, 0))
    b = art.card(w - 60, h, color, radius=30, outline=INK); im.alpha_composite(b, (30, 100))
    lb = art.text_img(label, 38, INK, width=w, w="Bold"); im.alpha_composite(lb, ((w - lb.width) // 2, 120 + h))
    return im

def rot(img, deg): return img.rotate(deg, resample=Image.BICUBIC, expand=True)

E = lambda img, x, y, t0, anim="pop", **kw: dict(img=img, x=x, y=y, t0=t0, anim=anim, **kw)
def CH(kind, mood, x, y, t0, scale=1.0, anim="slide_b", phase=0.0):
    return dict(img=art.character(kind, mood, scale=scale), img2=art.character(kind, mood, True, scale=scale),
                x=x, y=y, t0=t0, anim=anim, char=True, phase=phase)

PASTEL = [(255, 232, 210), (214, 236, 252), (214, 245, 228), (232, 224, 250), (255, 226, 214)]

# ---------- scenes ----------
S = []
# 0 hook
hook = big_card([(L["hook"], 74, INK, "Black")], fill=WHITE)
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[0], 1), pill=None, els=[
    E(hook, 540, 300, 0.15, "pop"),
    CH("dad", "surprised", 520, 760, at(0, 0, .15), 1.25),
    E(rot(chip("Medical card" if LANG == "en" else "医药卡", (190, 225, 255), size=40), 8), 220, 760, at(0, 0, .45), "slide_l"),
    E(art.icon("scissors", 170), 245, 900, at(0, 0, .65), "pop"),
    E(art.icon("question", 110), 820, 700, at(0, 0, .5), "pop"),
    CH("alex", "surprised", 880, 860, at(0, 1, 0) - 0.15, 0.78, anim="slide_r", phase=.4),
    E(rot(art.pill(L["pills"][0], 92, RED, WHITE, padx=60, pady=26), -6), 540, 1180, at(0, 1, 0), "pop", pulse=at(0, 1, 0, .5)),
]))
# 1 story
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[1], 2), pill=L["pills"][1], els=[
    E(big_card([(L["renewal"], 46, (90, 100, 120), "Bold"), (L["premium"] + "  ↑", 84, RED, "Black")], w=560), 330, 420, at(1, 0, 0), "slide_l"),
    E(art.icon("uparrow", 150), 760, 440, at(1, 0, .4), "pop", pulse=at(1, 0, .8)),
    CH("mum", "worried", 280, 820, at(1, 0, .2), 1.05, phase=1.3),
    E(art.icon("phone", 260), 720, 760, at(1, 1, 0), "slide_r"),
    E(chip(L["group"] + ": " + L["chat"], (200, 245, 205), size=42, w=640), 650, 1080, at(1, 1, .15), "slide_b"),
]))
# 2 catch
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[2], 3), pill=L["pills"][2], els=[
    E(bar(L["teras"], "RM100k" if LANG == "en" else "RM10万", 140, (255, 210, 120)), 300, 1060 - 240, at(2, 1, 0), "slide_b"),
    E(chip(L["teras_sub"], size=34, w=420), 300, 1150, at(2, 1, .3), "pop"),
    E(bar(L["card"], "RM1M+" if LANG == "en" else "RM100万+", 470, (130, 200, 150)), 740, 1060 - 570, at(2, 2, 0), "slide_b", pulse=at(2, 2, .6)),
    E(art.icon("sparkle", 90), 900, 420, at(2, 0, .3), "pop"),
    E(art.icon("question", 150), 540, 560, at(2, 0, 0), "pop", out=at(2, 1, 0)),
    E(art.icon("shield", 150), 300, 600, at(2, 0, .2), "pop", color=(255, 190, 90)),
]))
# 3 risk
risk_big = art.pill(L["risk_big"], 78, (255, 140, 90), WHITE, padx=56, pady=24)
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[3], 4), pill=L["pills"][3], els=[
    E(art.icon("hospital", 280), 260, 380, at(3, 0, 0), "pop"),
    E(art.icon("heart", 130), 300, 700, at(3, 0, .05), "pop"),
    E(chip(L["risk"][0], size=44, w=520), 760, 400, at(3, 0, .0), "slide_r"),
    E(chip(L["risk"][1], size=44, w=520), 760, 540, at(3, 0, .18), "slide_r"),
    E(chip(L["risk"][2], size=44, w=520), 760, 680, at(3, 0, .32), "slide_r"),
    CH("dad", "worried", 330, 830, at(3, 0, .25), 1.0, phase=.7),
    E(art.icon("moneybag", 220), 780, 880, at(3, 0, .55), "pop"),
    E(risk_big, 600, 1200, at(3, 0, .62), "pop", pulse=at(3, 0, .9)),
]))
# 4 cancel
S.append(dict(bg=art.pastel_bg(W, H, PASTEL[4], 5), pill=L["pills"][4], els=[
    E(art.icon("doc", 260), 300, 420, at(4, 0, 0), "pop"),
    E(art.icon("scissors", 160), 420, 560, at(4, 0, .08), "pop"),
    E(art.icon("padlock", 230), 760, 420, at(4, 0, .3), "pop", pulse=at(4, 0, .6)),
    E(art.icon("xmark", 120), 860, 400, at(4, 0, .4), "pop"),
    CH("mum", "surprised", 540, 760, at(4, 0, .1), 1.05, phase=2.1),
    E(chip(L["excluded"], (255, 225, 225), size=48, w=860), 540, 1110, at(4, 0, .45), "slide_b"),
]))
# 5 CTA (dark)
cta = art.pill(L["cta"], 70, GOLD, NAVY, padx=60, pady=24, outline=INK)
S.append(dict(bg=art.stars_bg(W, H, (22, 38, 62), NAVY), pill=None, dark=True, els=[
    E(art.logo_badge(True), 540, 230, 0.1, "pop"),
    E(art.text_img(L["q"], 96, WHITE, width=920), 540, 380, at(5, 0, 0), "pop"),
    E(art.icon("question", 110), 160, 520, at(5, 0, .3), "pop"),
    E(art.icon("question", 80), 930, 560, at(5, 0, .4), "pop"),
    CH("alex", "happy", 540, 520, at(5, 0, .2), 1.05),
    E(cta, 540, 1020, at(5, 1, 0), "pop", pulse=at(5, 1, .7)),
    E(art.text_img(L["cta_sub"], 46, CREAM, width=900, w="Bold"), 540, 1205, at(5, 1, .3), "slide_b"),
    E(art.pill(L["follow"], 52, WHITE, NAVY, padx=46, pady=18), 540, 1290, at(5, 2, 0), "pop"),
    E(art.text_img(L["disclaimer"], 24, (170, 180, 200), width=880, w="Regular"), 540, 1580, at(5, 2, .2), "fade"),
]))
for i, sc in enumerate(S):
    sc["start"], sc["end"] = scenes_t[i]
    if sc["pill"]: sc["els"].insert(0, E(art.pill(sc["pill"], 56), 540, 230, 0.05, "pop"))
    if not sc.get("dark"): sc["els"].append(E(art.logo_badge(), 930, 110, 0.0, "none"))

# ---------- animation ----------
def ease_out_back(x, s=1.9):
    x = min(max(x, 0), 1) - 1; return 1 + x * x * ((s + 1) * x + s)
def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def place(frame, el, lt):
    k = (lt - el["t0"]) / 0.45
    if k <= 0: return
    img = el["img"]; x, y = el["x"], el["y"]; sc = 1.0; a = 1.0; dx = dy = 0
    if el.get("char"):
        ph = el["phase"]; y += 6 * math.sin(2 * math.pi * (lt + ph) / 2.2)
        if ((lt + ph) % 4.0) < 0.13: img = el["img2"]
    an = el["anim"]
    if an == "pop" and k < 1: sc = max(0.01, ease_out_back(k))
    elif an.startswith("slide") and k < 1:
        e = ease_out(k); a = e; off = (1 - e) * 360
        dx, dy = {"slide_l": (-off, 0), "slide_r": (off, 0), "slide_b": (0, off)}[an]
    elif an == "fade": a = min(1, k)
    if "out" in el and lt > el["out"]:
        a *= max(0.0, 1 - (lt - el["out"]) / 0.25)
        if a <= 0: return
    if "pulse" in el:
        p = (lt - el["pulse"]) / 0.45
        if 0 < p < 1: sc *= 1 + 0.09 * math.sin(math.pi * p)
    if sc != 1.0:
        img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BICUBIC)
        y += (el["img"].height - img.height) / 2
    if a < 1:
        img = img.copy(); img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(img, (int(x - img.width / 2 + dx), int(y + dy)))

cap_cache = {}
def caption(text):
    if text not in cap_cache:
        t = art.text_img(text, 50, WHITE, width=880, w="Bold")
        bg = Image.new("RGBA", (t.width + 60, t.height + 34), (0, 0, 0, 0))
        ImageDraw.Draw(bg).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], 26, fill=(18, 24, 40, 190))
        bg.alpha_composite(t, (30, 18)); cap_cache[text] = bg
    return cap_cache[text]

def render_scene(si, lt):
    sc = S[si]; fr = sc["bg"].copy()
    for el in sc["els"]: place(fr, el, lt)
    for li, (s, d) in enumerate(lines_t[si]):
        if s <= sc["start"] + lt < s + d + GAP:
            cap = caption(C["lines"][si][li][0]); fr.alpha_composite(cap, ((W - cap.width) // 2, 1440 - cap.height // 2))
    return fr

def frame_at(t):
    si = max(i for i, sc in enumerate(S) if sc["start"] <= t + 1e-9)
    sc = S[si]; lt = t - sc["start"]; fr = render_scene(si, lt)
    if si + 1 < len(S) and t > sc["end"] - XF:
        a = (t - (sc["end"] - XF)) / XF
        fr = Image.blend(fr, render_scene(si + 1, 0.0), a)
    d = ImageDraw.Draw(fr); d.rectangle([0, H - 12, int(W * t / TOTAL), H], fill=GOLD)
    return fr

if STILLS:
    for si, sc in enumerate(S):
        frame_at(sc["end"] - XF - 0.05).convert("RGB").save(f"{OUT}/still_{LANG}_{si}.jpg", quality=88)
    print("stills", TOTAL); sys.exit()

# ---------- audio ----------
SR = 44100; N = int(TOTAL * SR) + SR
def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
voice = np.zeros(N, np.float32)
for si, row in enumerate(lines_t):
    for li, (s, d) in enumerate(row):
        v = load(f"{HERE}/svo_{LANG}/s{si:02d}_l{li}.mp3"); i = int(s * SR); voice[i:i + len(v)] += v[:N - i]
# gentle arpeggio: C - Am - F - G, 8th notes at 100 bpm
music = np.zeros(N, np.float32); step = 60 / 100 / 2
chords = [[261.6, 329.6, 392.0, 523.3], [220.0, 261.6, 329.6, 440.0], [174.6, 220.0, 261.6, 349.2], [196.0, 246.9, 293.7, 392.0]]
nl = int(1.2 * SR); tt = np.arange(nl) / SR
env = np.exp(-tt * 3.2) * np.minimum(1, tt / 0.005)
k = 0; pos = 0.0
while pos < TOTAL + 1:
    ch = chords[(k // 8) % 4]; f = ch[[0, 1, 2, 3, 2, 1, 2, 3][k % 8]]
    note = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) + 0.1 * np.sin(6 * np.pi * f * tt)) * env
    i = int(pos * SR); music[i:i + nl] += note[:max(0, N - i)] * 0.10
    if k % 8 == 0:  # soft bass
        b = np.sin(2 * np.pi * ch[0] / 2 * tt) * np.exp(-tt * 1.5) * 0.12; music[i:i + nl] += b[:max(0, N - i)]
    k += 1; pos += step
fade = np.ones(N, np.float32); fl = int(1.5 * SR); fade[:fl] = np.linspace(0, 1, fl)
end = int(TOTAL * SR); fade[end - 2 * SR:end] = np.linspace(1, 0, 2 * SR); fade[end:] = 0
# duck music under voice
venv = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode="same")
duck = 1 - 0.55 * np.clip(venv * 12, 0, 1)
music *= fade * duck
# pops
pops = np.zeros(N, np.float32); pl = int(0.09 * SR); pt = np.arange(pl) / SR
pop = np.sin(2 * np.pi * (900 - 5000 * pt) * pt) * np.exp(-pt * 45) * 0.22
for sc in S:
    for el in sc["els"]:
        if el["anim"] in ("pop",) and el["t0"] > 0.1:
            i = int((sc["start"] + el["t0"]) * SR); pops[i:i + pl] += pop[:max(0, N - i)]
mix = voice * 1.0 + music + pops
mix = mix[:end + int(0.2 * SR)]
mix = np.clip(mix / max(1e-6, np.abs(mix).max()) * 0.9, -1, 1)
raw_wav = f"{OUT}/mix_{LANG}.wav"
with wave.open(raw_wav, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
norm = f"{OUT}/mix_{LANG}_norm.m4a"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw_wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2", "-c:a", "aac", "-b:a", "160k", norm], check=True)

# ---------- srt ----------
def ts(x): h, r = divmod(x, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
with open(f"{OUT}/mediasas_short_{LANG}.srt", "w") as f:
    n = 1
    for si, row in enumerate(lines_t):
        for li, (s, d) in enumerate(row):
            f.write(f"{n}\n{ts(s)} --> {ts(s + d + 0.1)}\n{C['lines'][si][li][0]}\n\n"); n += 1

# ---------- video ----------
outmp4 = f"{OUT}/mediasas_short_{LANG}.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", norm, "-map", "0:v", "-map", "1:a", "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                      "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", outmp4], stdin=subprocess.PIPE)
for fi in range(int(TOTAL * FPS)):
    p.stdin.write(frame_at(fi / FPS).convert("RGB").tobytes())
p.stdin.close(); p.wait()
print(outmp4, round(TOTAL, 1))
