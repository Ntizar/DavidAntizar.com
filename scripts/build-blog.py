#!/usr/bin/env python3
"""Genera content/blog.json (índice ligero del archivo del blog) a partir de
content/posts/*.meta.json + content/posts/*.html.

Uso:  python3 scripts/build-blog.py
Salida: content/blog.json  (solo metadatos; el HTML de cada post se sirve aparte)
"""
import glob
import html
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(RAIZ, "content", "posts")
SALIDA = os.path.join(RAIZ, "content", "blog.json")

TAG = re.compile(r"<[^>]+>")
IMG = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)


def limpio(t):
    t = html.unescape(t or "")
    t = TAG.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()


def minutos(texto):
    return max(1, round(len(texto.split()) / 200))


def main():
    posts = []
    for meta_path in sorted(glob.glob(os.path.join(POSTS, "*.meta.json"))):
        with open(meta_path, encoding="utf-8") as f:
            m = json.load(f)
        slug = m.get("slug") or os.path.basename(meta_path).replace(".meta.json", "")
        html_path = os.path.join(POSTS, slug + ".html")
        cuerpo = ""
        if os.path.exists(html_path):
            with open(html_path, encoding="utf-8") as f:
                cuerpo = f.read()
        texto = limpio(cuerpo)
        cats = [c.get("name") for c in (m.get("categories") or {}).values() if c.get("name")]
        imagen = m.get("featured_image") or ""
        if not imagen:
            encontrada = IMG.search(cuerpo)
            if encontrada:
                imagen = html.unescape(encontrada.group(1))
        posts.append(
            {
                "id": m.get("ID"),
                "s": slug,
                "t": limpio(m.get("title")),
                "d": (m.get("date") or "")[:10],
                "c": cats[0] if cats else "Notas",
                "x": limpio(cuerpo)[:210],
                "min": minutos(texto),
                "img": imagen,
                "u": m.get("URL") or "",
            }
        )
    posts.sort(key=lambda p: p["d"], reverse=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(posts)} posts → {os.path.relpath(SALIDA, RAIZ)} "
          f"({os.path.getsize(SALIDA) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
