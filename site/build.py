"""Package the site for publishing as a claude.ai Artifact or a website.

The artifact's main page is wrapped in its own <html>/<head>/<body> skeleton at
publish time, so index.html is converted to a fragment (head tags + body content,
with the body's class/data-page set by script). Every other page is served as-is.
Output: ../dist/

Use --web for a standalone website suitable for GitHub Pages.
"""
import argparse, hashlib, re, shutil, pathlib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--web", action="store_true", help="Build standalone HTML pages")
args = parser.parse_args()

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent / "dist"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(SRC / "assets", OUT / "assets")
for page in SRC.glob("*.html"):
    if page.name.startswith("_") or (args.web and page.name == "print-cover.html"):
        continue
    shutil.copy(page, OUT / page.name)

# A changed asset gets a new URL so returning readers receive matching HTML,
# styles and navigation rather than a previously cached version.
def version_asset(match):
    path = match.group(2)
    asset = OUT / path
    digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
    return '%s%s?v=%s%s' % (match.group(1), path, digest, match.group(3))

for page in OUT.glob('*.html'):
    page.write_text(re.sub(r'((?:src|href)=")((?:assets/)[^"?]+\.(?:js|css))(")', version_asset, page.read_text()))

if args.web:
    (OUT / ".nojekyll").touch()
else:
    html = (OUT / "index.html").read_text()
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    head = re.sub(r'<meta (charset|name="viewport")[^>]*>\s*', "", head)
    body_tag = re.search(r"<body([^>]*)>", html).group(1)
    body = re.search(r"<body[^>]*>(.*)</body>", html, re.S).group(1)
    cls = re.search(r'class="([^"]*)"', body_tag)
    page = re.search(r'data-page="([^"]*)"', body_tag)
    boot = "<script>document.body.className=%r;document.body.dataset.page=%r;</script>\n" % (
        cls.group(1) if cls else "", page.group(1) if page else "")
    (OUT / "index.html").write_text(head.strip() + "\n" + boot + body.strip() + "\n")
print("built", sorted(p.name for p in OUT.rglob("*") if p.is_file()))
