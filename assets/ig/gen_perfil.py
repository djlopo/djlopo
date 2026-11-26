#!/usr/bin/env python3
"""Foto de perfil + portadas de highlights para @tuoraciondiariatv.
Estetica del canal: noche ciruela + oro. 1080x1080 cada una."""
import os, math
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.dirname(__file__)
LOGO = "/home/user/djlopo/assets/images/watermark_isotipo.png"
NOCHE = (22, 15, 43)
CIRUELA = (44, 28, 77)
ORO = (244, 196, 106)
MARFIL = (248, 238, 221)
S = 1080

def fondo():
    """Plum radial sobre noche, con vineta suave."""
    base = Image.new("RGB", (S, S), NOCHE)
    glow = Image.new("L", (S, S), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy = S // 2, int(S * 0.46)
    for r in range(int(S * 0.62), 0, -2):
        a = int(170 * (1 - r / (S * 0.62)))
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    cir = Image.new("RGB", (S, S), CIRUELA)
    base = Image.composite(cir, base, glow)
    return base

def anillo(d, grosor=10, color=ORO, margen=70, alpha=255):
    d.ellipse([margen, margen, S - margen, S - margen], outline=color + (alpha,), width=grosor)

def guarda(img, nombre):
    img.convert("RGB").save(os.path.join(OUT, nombre), quality=94)
    print("  +", nombre)

# ---------------- Foto de perfil ----------------
def perfil():
    img = fondo().convert("RGBA")
    logo = Image.open(LOGO).convert("RGBA")
    w = int(S * 0.60)
    logo = logo.resize((w, int(w * logo.height / logo.width)), Image.LANCZOS)
    # resplandor dorado tras el logo
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([S//2-w//2-40, S//2-w//2-40, S//2+w//2+40, S//2+w//2+40], fill=ORO + (60,))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img, glow)
    img.alpha_composite(logo, (S//2 - logo.width//2, S//2 - logo.height//2))
    guarda(img, "perfil_tuoraciondiariatv.jpg")

# ---------------- Iconos de highlights ----------------
def icono_estrella(d, cx, cy, r, color):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = math.pi / 2 + k * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy - rr * math.sin(a)))
    d.polygon(pts, fill=color)

def icono_libro(d, cx, cy, r, color):
    w, h = r * 1.7, r * 1.25
    x0, y0 = cx - w, cy - h
    d.line([(cx, y0 + 12), (cx, y0 + 2 * h - 10)], fill=color, width=9)
    for s in (-1, 1):
        d.line([(cx, y0 + 12), (cx + s * w, y0 + 26)], fill=color, width=9)
        d.line([(cx + s * w, y0 + 26), (cx + s * w, y0 + 2 * h)], fill=color, width=9)
        d.line([(cx + s * w, y0 + 2 * h), (cx, y0 + 2 * h - 10)], fill=color, width=9)
        for i in range(1, 4):
            yy = y0 + 26 + i * (2 * h - 40) / 4
            d.line([(cx + s * 22, yy), (cx + s * (w - 18), yy + 6)], fill=color, width=5)

def icono_rosario(d, cx, cy, r, color):
    for k in range(12):
        a = k * math.pi / 6
        x, y = cx + r * math.cos(a), cy - r * math.sin(a) - r * 0.25
        rr = 10 if k % 4 else 15
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color)
    # cruz colgando
    bx, by = cx, cy + r * 0.95
    d.line([(bx, by - 6), (bx, by + 54)], fill=color, width=10)
    d.line([(bx - 22, by + 16), (bx + 22, by + 16)], fill=color, width=10)

def icono_vela(d, cx, cy, r, color):
    w = r * 0.5
    d.rounded_rectangle([cx - w, cy - r * 0.2, cx + w, cy + r], radius=10, fill=color)
    d.line([(cx, cy - r * 0.2), (cx, cy - r * 0.5)], fill=color, width=7)
    # llama
    fl = [(cx, cy - r * 1.05), (cx + 20, cy - r * 0.55), (cx, cy - r * 0.35), (cx - 20, cy - r * 0.55)]
    d.polygon(fl, fill=color)

def icono_halo(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r * 1.05, cx + r, cy - r * 0.35], outline=color, width=12)
    d.ellipse([cx - r * 0.55, cy - r * 0.35, cx + r * 0.55, cy + r * 0.55], outline=color, width=11)
    d.pieslice([cx - r * 0.95, cy + r * 0.25, cx + r * 0.95, cy + r * 1.7], 180, 360, outline=color, width=11)

def icono_play(d, cx, cy, r, color):
    d.rounded_rectangle([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], radius=26, outline=color, width=12)
    t = r * 0.42
    d.polygon([(cx - t, cy - t * 1.2), (cx - t, cy + t * 1.2), (cx + t * 1.3, cy)], fill=color)

ICONOS = [
    ("empieza", icono_estrella),
    ("evangelio", icono_libro),
    ("rosario", icono_rosario),
    ("adviento", icono_vela),
    ("santos", icono_halo),
    ("youtube", icono_play),
]

def cover(nombre, fn):
    img = fondo().convert("RGBA")
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    anillo(d, grosor=8, margen=95, alpha=210)
    fn(d, S // 2, int(S * 0.5), int(S * 0.2), ORO + (255,))
    # leve resplandor del icono
    glow = layer.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, layer)
    guarda(img, f"cover_{nombre}.jpg")

if __name__ == "__main__":
    print("Generando pack de perfil:")
    perfil()
    for nombre, fn in ICONOS:
        cover(nombre, fn)
    print("Listo.")
