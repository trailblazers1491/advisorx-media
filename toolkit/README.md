# AdvisorX cartoon shorts toolkit

Weekly TikTok / YouTube Shorts for @advisorx.my and @advisorx-my.

- `art.py` – flat 2D cartoon kit: cartoon Alex mascot (`character("alex", mood)`; black suit, white shirt, black tie, arms at sides), family characters, icons, real AdvisorX logo.
- `*_content.py` – script per episode: EN + ZH lines (same count per scene), on-screen labels. Facts only from the advisorx.my blog post.
- `tts_all.py` – voiceover (edge-tts; EN `en-US-AndrewMultilingualNeural`, ZH `zh-CN-YunxiNeural`). Env: `CONTENT=<module> VOPREFIX=<dir>`.
- `render_short.py` – renders 1080x1920 video with music, pops, captions, SRT. Scenes are defined in the `# ---------- scenes` block (`p2_scenes.py` is an example of swapping scenes in).
- `cover.py` / `cover_p2.py` – vertical covers. `checklist.py` – DM checklist image.

Format: 40–70s, curiosity hook in first 3s, open question / "Comment KEYWORD" CTA, disclaimer.
Posting: Saturday 8:30pm MYT – TikTok (EN) + YouTube Shorts EN 8:30pm, ZH 9:00pm. Media uploaded to `tiktok/epNN/`.
