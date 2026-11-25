#!/usr/bin/env python3
"""Genera una miniatura (thumbnail) de Adviento: corona oscura + texto grande dorado.
Uso: python3 -I make_thumb.py <img> <salida.png> <PALABRA> <subtitulo> [vertical]
"""
import subprocess, sys

img, out, word, sub = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
vertical = len(sys.argv) > 5 and sys.argv[5] == "vertical"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
GOLD, CREAM = "0xEAC978", "0xF3ECDD"

def esc(t): return t.replace(":", "\\:").replace("'", "’")

if vertical:
    W, H = 1080, 1920
    scale = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    wsize, ssize, brsize = 150, 60, 44
    wy, sy, bry = "H*0.60", "H*0.72", "H*0.52"
else:
    W, H = 1280, 720
    scale = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    wsize, ssize, brsize = 150, 58, 40
    wy, sy, bry = "(H-text_h)/2-30", "(H-text_h)/2+100", "(H-text_h)/2-130"

# ajustar la palabra grande al ancho (serif bold en mayúsculas ~0.72*fontsize por carácter)
maxw = W * 0.90
fit = int(maxw / max(1, len(word) * 0.72))
wsize = min(wsize, fit)
# el subtítulo también, por si es largo
sfit = int(maxw / max(1, len(sub) * 0.50))
ssize = min(ssize, sfit)

# oscurecer para contraste + viñeta + textos con sombra fuerte
vf = (
    f"{scale},eq=brightness=-0.10:contrast=1.06:saturation=1.05,"
    f"vignette=angle=PI/4,"
    f"drawbox=x=0:y=0:w={W}:h={H}:color=black@0.28:t=fill,"
    f"drawtext=fontfile={FR}:text='TU ORACIÓN DIARIA':fontcolor={CREAM}@0.92:fontsize={brsize}:"
    f"x=(w-text_w)/2:y={bry}:shadowcolor=black@0.8:shadowx=0:shadowy=3,"
    f"drawtext=fontfile={FB}:text='{esc(word)}':fontcolor={GOLD}:fontsize={wsize}:"
    f"x=(w-text_w)/2:y={wy}:shadowcolor=black@0.85:shadowx=0:shadowy=5,"
    f"drawtext=fontfile={FR}:text='{esc(sub)}':fontcolor={CREAM}:fontsize={ssize}:"
    f"x=(w-text_w)/2:y={sy}:shadowcolor=black@0.8:shadowx=0:shadowy=3"
)
subprocess.run(["ffmpeg", "-y", "-i", img, "-vf", vf, "-frames:v", "1", out],
               check=True, capture_output=True)
print("OK", out)
