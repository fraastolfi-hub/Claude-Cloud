#!/usr/bin/env python3
"""Compone il sito statico di Hotel Positioning.

src/pages/**/*.html  ->  public/**/*.html
  <!-- @include nome -->   inserisce src/partials/nome.html
Poi copia src/assets, segna la voce di menu attiva, scrive sitemap.xml e _redirects.

Uso:  python3 build.py            (build)
      python3 build.py --serve    (build + anteprima su http://localhost:8000)
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = Path(os.environ.get("HP_OUT", ROOT / "public"))  # HP_OUT: cartella di uscita alternativa (anteprime parallele)
DOMAIN = "https://hotelpositioning.com"
INCLUDE = re.compile(r"<!--\s*@include\s+([\w-]+)\s*-->")

# vecchi URL -> nuovi (le querystring UTM passano da sole con lo status 301 di Netlify/Cloudflare)
REDIRECTS = {
    "/analisi-gratuita.html": "/#richiedi",
    "/analisi-gratuita": "/#richiedi",
    "/landing-booking": "/problemi/booking/",
    "/landing-prezzi": "/problemi/prezzi/",
    "/landing-sostituibili": "/problemi/sostituibili/",
    "/landing-agenzie": "/problemi/agenzie/",
    "/landing-valore": "/problemi/valore/",
    "/landing-apertura": "/problemi/apertura/",
    "/libro": "/libro/",
    "/bonus": "/bonus/",
    "/quiz": "/quiz/",
    "/smontaggio": "/smontaggio/",
    "/library": "/library/",
    "/francesco": "/francesco/",
    "/privacy-policy": "/privacy-policy/",
}


def url_for(rel: Path) -> str:
    """src/pages/libro/index.html -> /libro/ ; pages/foo.html -> /foo.html"""
    p = "/" + rel.as_posix()
    return p[: -len("index.html")] if p.endswith("index.html") else p


def render(text: str, partials: dict, url: str) -> str:
    for _ in range(3):  # include annidati
        text = INCLUDE.sub(lambda m: partials[m.group(1)], text)
    # voce di menu attiva: la sezione più lunga che contiene l'URL della pagina
    def mark(m):
        href = m.group(1)
        active = href != "/" and url.startswith(href)
        return m.group(0) if not active else m.group(0).replace("<a ", '<a aria-current="page" ', 1)
    return re.sub(r'<a href="(/[^"#]*)"', mark, text)


def asset_versions() -> dict:
    """Impronta corta di ogni CSS e JS: /assets/site.js -> /assets/site.js?v=1a2b3c4d.
    Così dopo ogni pubblicazione il browser scarica i file nuovi invece di usare quelli in cache."""
    import hashlib
    out = {}
    for f in (SRC / "assets").glob("*"):
        if f.suffix in (".css", ".js"):
            out["/assets/" + f.name] = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
    return out


def bust(html: str, versions: dict) -> str:
    for path, v in versions.items():
        html = html.replace(f'"{path}"', f'"{path}?v={v}"')
    return html


def social_image(html: str) -> str:
    """Ogni pagina ha un'immagine per le condivisioni: la sua, se c'è, altrimenti quella del sito."""
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    img = m.group(1) if m else "/assets/img/og-hotel-positioning.jpg"
    if img.startswith("/"):
        img = DOMAIN + img
    tags = f'<meta name="twitter:image" content="{img}">\n'
    if not m:
        tags = f'<meta property="og:image" content="{img}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n' + tags
    else:
        html = html.replace(m.group(0), f'<meta property="og:image" content="{img}"', 1)
    return html.replace('<meta name="twitter:card"', tags + '<meta name="twitter:card"', 1)


def build():
    partials = {p.stem: p.read_text() for p in (SRC / "partials").glob("*.html")}
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    urls = []
    versions = asset_versions()
    for page in sorted((SRC / "pages").rglob("*.html")):
        rel = page.relative_to(SRC / "pages")
        url = url_for(rel)
        html = render(page.read_text(), partials, url)
        html = bust(social_image(html), versions)
        missing = INCLUDE.findall(html)
        if missing:
            sys.exit(f"{rel}: include mancanti {missing}")
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        if 'name="robots" content="noindex' not in html:
            urls.append(url)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMAIN}{u}</loc></url>\n" for u in urls)
        + "</urlset>\n"
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    (OUT / "_redirects").write_text("".join(f"{a}  {b}  301\n" for a, b in REDIRECTS.items()))
    print(f"{len(urls)} pagine in {OUT}/")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Anteprima su http://localhost:8000")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()
