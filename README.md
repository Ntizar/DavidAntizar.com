# DavidAntizar.com

La web de David Antizar, que es un iPhone.

Un único `index.html` sin dependencias: pantalla de bloqueo, Face ID de mentira
(sin cámara ni permisos), escritorio con tres páginas deslizables, biblioteca de
apps, centro de control y veinte apps que abren contenido real.

## Qué hay dentro

- `index.html` — la web entera: HTML, CSS y JS en un solo fichero (~100 KB).
- `assets/img/` — fondos (`wall-*.svg` dibujados, `wallpaper-*.jpg` de foto) e
  imágenes del blog original.
- `content/blog.json` — índice del archivo (27 artículos, 2015-2018).
- `content/posts/` — el HTML de cada artículo, que se lee dentro de la app Blog.
- `scripts/build-blog.py` — regenera `content/blog.json` desde `content/posts/`.
- `scripts/gen-fondos.py` — regenera los fondos SVG (`assets/img/wall-*.svg`).

## Regenerar

```bash
python3 scripts/build-blog.py   # índice del blog
python3 scripts/gen-fondos.py   # fondos dibujados
```

## Deploy

GitHub Pages sirve `main` en la raíz (workflow `.github/workflows/pages.yml`) y
el dominio `davidantizar.com` apunta ahí. Push a `main` = publicado.

Hecho con ❤️ por David Antizar
