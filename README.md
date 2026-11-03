# DavidAntizar.com

La web de David Antizar, que es un Windows Phone.

Un único `index.html` sin dependencias: pantalla de bloqueo con reloj real y
**lector de iris** (Windows Hello simulado: se toca el ojo, escanea y entra) y
pantalla de inicio con **Live Tiles** de cristal que giran solas.
Cinco fichas, solo las que existen:

- Kit72h — kits de 72 horas de afiliación en Amazon
- LinkedIn — `in/davidantizar`
- GitHub — `@Ntizar`, con el número de repositorios y el último repo actualizado
  en vivo contra la API pública de GitHub (texto de reserva si no hay red)
- Instagram
- X — `@DNtizar`
- El poni de Von der Leyen — su libro, en Amazon

## Qué hay dentro

- `index.html` — la web entera: HTML, CSS y JS en un solo fichero (~24 KB).
- `assets/fonts/` — Open Sans (300/400/600/700) auto-hospedada; Windows usa
  Segoe UI nativa si la tiene.
- `assets/img/` — fondos e imágenes del archivo antiguo, e iconos de la app.
- `iphone.html` — la versión anterior (escritorio iPhone con 20 apps). Se queda
  como legado; no se enlaza desde la portada.
- `content/blog.json` y `content/posts/` — archivo del blog (2015-2018).
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
