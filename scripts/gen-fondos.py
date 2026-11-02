#!/usr/bin/env python3
"""Genera los fondos SVG del iPhone (assets/img/wall-*.svg).

Son degradados radiales suaves al estilo iOS 26: baratos (<3 KB), nítidos a
cualquier resolución y con la zona superior oscura para que la hora se lea.

Uso:  python3 scripts/gen-fondos.py
"""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "img")

# nombre: (base_top, base_mid, base_bottom, [(cx, cy, rx, ry, color, opacidad)])
FONDOS = {
    "wall-aurora": (
        "#060a18", "#0b1430", "#03040a",
        [
            (0.10, 0.16, 0.85, 0.42, "#1de9c8", 0.55),
            (0.95, 0.30, 0.80, 0.40, "#6a5cff", 0.50),
            (0.50, 0.62, 1.10, 0.30, "#ff4fa3", 0.30),
            (0.20, 0.92, 0.90, 0.35, "#0f6bff", 0.35),
        ],
    ),
    "wall-oceano": (
        "#020814", "#04223a", "#010409",
        [
            (0.15, 0.22, 0.90, 0.40, "#12b0e8", 0.50),
            (0.90, 0.55, 0.95, 0.45, "#0b5cff", 0.45),
            (0.40, 0.95, 1.10, 0.35, "#00d4b0", 0.30),
        ],
    ),
    "wall-cobre": (
        "#140a06", "#2a1206", "#080403",
        [
            (0.20, 0.20, 0.95, 0.45, "#ff9d3d", 0.42),
            (0.92, 0.62, 0.90, 0.45, "#ff4d1a", 0.35),
            (0.35, 1.00, 1.20, 0.40, "#8a3b12", 0.45),
        ],
    ),
    "wall-bosque": (
        "#04100a", "#0a2318", "#020705",
        [
            (0.80, 0.15, 0.95, 0.42, "#2ecc71", 0.35),
            (0.12, 0.70, 1.00, 0.45, "#0f7a52", 0.50),
            (0.70, 1.05, 1.10, 0.35, "#9ee06a", 0.22),
        ],
    ),
    "wall-violeta": (
        "#0a0518", "#1a0b33", "#04020a",
        [
            (0.15, 0.25, 0.95, 0.45, "#8b5cf6", 0.50),
            (0.90, 0.45, 0.95, 0.45, "#e0399b", 0.42),
            (0.45, 0.95, 1.15, 0.40, "#4f2dff", 0.35),
        ],
    ),
    "wall-arena": (
        "#1b130c", "#3a2517", "#0c0805",
        [
            (0.85, 0.12, 0.95, 0.40, "#ffd27a", 0.35),
            (0.10, 0.55, 1.00, 0.45, "#ff9e6b", 0.30),
            (0.60, 1.05, 1.20, 0.40, "#c26a3a", 0.35),
        ],
    ),
    "wall-titanio": (
        "#0d0d10", "#1c1c22", "#050507",
        [
            (0.25, 0.10, 0.90, 0.35, "#9ea3ad", 0.35),
            (0.80, 0.60, 0.95, 0.45, "#6f747d", 0.30),
            (0.35, 1.00, 1.10, 0.35, "#cfd3da", 0.12),
        ],
    ),
}

PLANTILLA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1170 2532" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="b" x1="0" y1="0" x2=".25" y2="1">
<stop offset="0" stop-color="{top}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{bot}"/>
</linearGradient>
{grads}
<linearGradient id="v" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset=".35" stop-color="#000" stop-opacity="0"/>
<stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/>
</linearGradient>
</defs>
<rect width="1170" height="2532" fill="url(#b)"/>
{blobs}
<rect width="1170" height="2532" fill="url(#v)"/>
</svg>
"""


def generar(nombre, datos):
    top, mid, bot, blobs = datos
    grads, formas = [], []
    for i, (cx, cy, rx, ry, color, op) in enumerate(blobs):
        grads.append(
            f'<radialGradient id="g{i}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset=".55" stop-color="{color}" stop-opacity="{op * 0.45:.2f}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
        )
        formas.append(
            f'<ellipse cx="{cx * 1170:.0f}" cy="{cy * 2532:.0f}" '
            f'rx="{rx * 1170:.0f}" ry="{ry * 2532:.0f}" fill="url(#g{i})"/>'
        )
    svg = PLANTILLA.format(
        top=top, mid=mid, bot=bot, grads="\n".join(grads), blobs="\n".join(formas)
    )
    ruta = os.path.join(DESTINO, nombre + ".svg")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(svg)
    return ruta, os.path.getsize(ruta)


if __name__ == "__main__":
    for nombre, datos in FONDOS.items():
        ruta, tam = generar(nombre, datos)
        print(f"{nombre:<14} {tam / 1024:5.1f} KB")
