#!/usr/bin/env python3
"""Genera los materiales 3D de las cartas de davidantizar.com con los modelos de NaN.

Cada carta lleva un "material" de fondo (fluido, cristal, papel, resina...) renderizado
por el modelo de imagen. El glifo de marca va encima en SVG, así que las imágenes NO
llevan texto: nunca se le pide tipografía a un modelo de imagen.

Uso:
    python3 scripts/gen-cartas.py            # todas las que falten
    python3 scripts/gen-cartas.py agora      # solo una (por id)

Requisitos: variable de entorno NAN_API_KEY (o HERMES_CUSTOM_OPENAI_COMPATIBLE_API_KEY)
y ffmpeg en el PATH. Salida: assets/cartas/<id>.webp (720 px, ~60 KB).
"""
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "cartas")
API = "https://api.nan.builders/v1/images/generations"
MODELO = "flux-2-klein"
LADO = 720
CALIDAD = "86"

# Estilo común: es lo que hace que nueve cartas parezcan del mismo set.
ESTILO = (
    "soft 3D render, single object centered, macro product photography, "
    "warm off-white paper backdrop, very soft diffused studio light, "
    "gentle contact shadow, subtle film grain, premium minimal, "
    "high key, no text, no letters, no watermark"
)

# id: descripción del material
MATERIALES = {
    "linkedin": "a glossy cobalt blue cube with softly rounded corners resting on the surface, single sharp specular highlight",
    "github": "a matte graphite black stone sphere wrapped by one thin chrome orbit ring",
    "x": "a pure black polished glass monolith slab standing upright, razor sharp specular edge highlight, soft reflection underneath",
    "instagram": "a crumpled iridescent holographic foil with pink orange and violet sheen",
    "kit72h": "a signal red matte toolbox lid with one cream diagonal warning stripe",
    "libro": "a closed deep green cloth bound book with aged cream page edges",
    "hipersonicos": "a polished chrome aerodynamic cone pointed upward on a small pale pedestal, sharp specular highlights, clean silhouette",
    "archivo": "a fanned stack of warm sepia paper sheets with deckled edges",
    "agora": "a translucent golden amber resin shard with light caustics and tiny glints",
}


def clave():
    for nombre in ("NAN_API_KEY", "HERMES_CUSTOM_OPENAI_COMPATIBLE_API_KEY"):
        valor = os.environ.get(nombre, "").strip()
        if valor:
            return valor
    sys.exit("Falta NAN_API_KEY en el entorno.")


def generar(carta_id, descripcion, token):
    cuerpo = json.dumps(
        {"model": MODELO, "prompt": f"{ESTILO}: {descripcion}", "n": 1, "size": "1024x1024"}
    ).encode()
    peticion = urllib.request.Request(
        API,
        data=cuerpo,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(peticion, timeout=180) as respuesta:
        datos = json.load(respuesta)
    url = datos["data"][0]["url"]

    os.makedirs(DESTINO, exist_ok=True)
    salida = os.path.join(DESTINO, f"{carta_id}.webp")
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "origen.png")
        urllib.request.urlretrieve(url, png)
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-i", png,
                "-vf", f"crop=1024:1024,scale={LADO}:{LADO}",
                "-quality", CALIDAD, "-compression_level", "6",
                salida,
            ],
            check=True,
        )
    return salida


def main():
    token = clave()
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    for carta_id, descripcion in MATERIALES.items():
        if solo and carta_id != solo:
            continue
        destino = os.path.join(DESTINO, f"{carta_id}.webp")
        if os.path.exists(destino) and not solo:
            print(f"· {carta_id}: ya existe, no se toca")
            continue
        print(f"· {carta_id}: generando…", flush=True)
        ruta = generar(carta_id, descripcion, token)
        print(f"  {os.path.relpath(ruta, RAIZ)} — {os.path.getsize(ruta) // 1024} KB", flush=True)


if __name__ == "__main__":
    main()
