# LinkedIn PDF carousels

LinkedIn cannot post multi-image carousels through Make's free modules, so carousels are posted as
PDF "document" posts (LinkedIn shows them as a swipeable carousel).

- `tools/make_pdf.py out.pdf <slide URLs...>`: combine slides into one PDF (pip install img2pdf).
- `tools/li_escape.py < caption.txt`: prints the caption escaped for LinkedIn's little-text format
  (reserved characters escaped, hashtags as {hashtag|\#|Tag}) as a JSON string.
- PDFs live in this folder; the Make "LinkedIn Scheduler" downloads them from
  https://raw.githubusercontent.com/trailblazers1491/advisorx-media/main/linkedin/<file>.pdf
