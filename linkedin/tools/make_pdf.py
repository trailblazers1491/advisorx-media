"""Combine carousel slide images (URLs) into one PDF for a LinkedIn document post.
Usage: python3 make_pdf.py out.pdf URL1 URL2 ...
"""
import sys, urllib.request, tempfile, os, img2pdf
out, urls = sys.argv[1], sys.argv[2:]
d = tempfile.mkdtemp()
files = []
for i, u in enumerate(urls, 1):
    p = os.path.join(d, f"{i:02d}.jpg")
    urllib.request.urlretrieve(u, p)
    files.append(p)
open(out, "wb").write(img2pdf.convert(files))
print(out, os.path.getsize(out), "bytes,", len(files), "pages")
