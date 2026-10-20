import sys, asyncio, json, subprocess, os, certifi
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"   # trust the session proxy CA
import edge_tts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib; content = importlib.import_module(os.environ.get("CONTENT","content"))
lang = sys.argv[1]; C = getattr(content, lang.upper())
P = os.environ.get("VOPREFIX","vo"); os.makedirs(f"{P}_{lang}", exist_ok=True)
async def one(path, text):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, C["voice"], rate=C["rate"]).save(path)
            if os.path.getsize(path) > 1000: return
        except Exception as e: print("retry", path, e)
        await asyncio.sleep(2)
    raise SystemExit("failed " + path)
async def main():
    durs = []
    for si, sc in enumerate(C["lines"]):
        row = []
        for li, ln in enumerate(sc):
            p = f"{P}_{lang}/s{si:02d}_l{li}.mp3"
            if not os.path.exists(p) or os.path.getsize(p) < 1000:
                await one(p, ln[-1])
            d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
            row.append(round(d, 3))
        durs.append(row)
    json.dump(durs, open(f"{P}_{lang}/durs.json","w"))
    print(lang, "total speech", round(sum(map(sum,durs)),1), [round(sum(r),1) for r in durs])
asyncio.run(main())
