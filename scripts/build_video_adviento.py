#!/usr/bin/env python3
"""Plantilla ESTÁNDAR de vídeo para TIEMPO DE ADVIENTO (Tu Oración Diaria).

Movimiento lento y litúrgico sobre la imagen de la corona de Adviento:
  - zoompan muy lento (Ken Burns sutil)
  - capa de LUZ en movimiento (degradado con opacidad, blend screen)
  - parpadeo cálido de velas (eq brightness con senos)
  - viñeta que cambia de forma (centro y ángulo animados)
  - grano suave
Tipografía DejaVu Serif, color entre dorado y blanco, SIN borde + sombra ligera.
Fecha y tiempo litúrgico SIEMPRE visibles. Subtítulos propios quemados (nuestros).
Música muy leve (pad) + chime al entrar y al cerrar.

SOLO para Adviento. Uso:
  python3 -I build_video_adviento.py \
      --audio final.mp3 --srt subs.srt --img corona.png --out video.mp4 \
      --title LAUDES --subtitle "Domingo · I Semana de Adviento" \
      --date "29 de Noviembre de 2026"
"""
import argparse, os, subprocess, sys

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
GOLD = "0xEAC978"      # dorado cálido
CREAM = "0xF3ECDD"     # blanco cálido
BRAND = "Tu Oración Diaria"


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def build_mix(audio, pad, chime, out):
    """voz + pad en bucle muy bajo (0.09) con fundidos + chime al inicio y al final."""
    d = dur(audio)
    fo = max(0.0, d - 3.0)
    chime_end = max(0.0, d - 4.2)
    fc = (
        f"[1:a]aloop=loop=-1:size=2e9,atrim=0:{d},volume=0.09,"
        f"afade=t=in:st=0:d=3,afade=t=out:st={fo:.2f}:d=3[mus];"
        f"[2:a]adelay=200|200,volume=0.5[ch1];"
        f"[3:a]adelay={int(chime_end*1000)}|{int(chime_end*1000)},volume=0.42[ch2];"
        f"[0:a]volume=1.0[v];"
        f"[v][mus][ch1][ch2]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,"
        f"alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    )
    cmd = ["ffmpeg", "-y", "-i", audio, "-i", pad, "-i", chime, "-i", chime,
           "-filter_complex", fc, "-map", "[a]", "-c:a", "libmp3lame", "-q:a", "3", out]
    subprocess.run(cmd, check=True, capture_output=True)
    return d


def build_video(img, mix, srt, out, title, subtitle, datetxt, d):
    srt_esc = srt.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    # degradado animado para la capa de luz
    light = (f"gradients=s=1920x1080:c0=0x000000:c1=0x201708:c2=0x3a2a10:c3=0x000000:"
             f"x0=640:y0=120:x1=1300:y1=980:type=linear:speed=0.0016:duration={d:.1f}:d={d:.1f}")
    vf = (
        # fondo: escalar cubriendo 1920x1080, Ken Burns lentísimo. format=gbrp (RGB planar)
        # se mantiene por TODA la cadena: gradients/blend salen en RGB y una conversión
        # implícita a YUV en eq/vignette corrompe el croma (lavado magenta). gbrp lo evita.
        f"[0:v]scale=2304:1296:flags=lanczos,"
        f"zoompan=z='min(zoom+0.00018,1.035)':d={int(d*25)}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25,format=gbrp[bg];"
        f"[1:v]format=gbrp[lt];"
        # capa de luz en movimiento (screen)
        f"[bg][lt]blend=all_mode=screen:shortest=1,format=gbrp[lw];"
        # parpadeo cálido de velas + viñeta que cambia de forma + grano
        f"[lw]eq=eval=frame:brightness='0.02*sin(9*t)+0.013*sin(16*t)':saturation=1.03,"
        f"vignette=eval=frame:x0='w/2+55*sin(n/150)':y0='h/2+34*cos(n/125)':angle='PI/4.5+0.05*sin(n/95)',"
        f"noise=alls=3:allf=t,format=yuv420p[base];"
        # línea dorada bajo el título
        f"[base]drawbox=x=(iw-320)/2:y=226:w=320:h=2:color={GOLD}@0.70:t=fill[ln];"
        # textos (sin borde, sombra ligera)
        f"[ln]drawtext=fontfile={FONT_REG}:text='{esc(BRAND)}':"
        f"fontcolor={CREAM}@0.90:fontsize=32:x=(w-text_w)/2:y=64:shadowcolor=black@0.5:shadowx=0:shadowy=2,"
        f"drawtext=fontfile={FONT_BOLD}:text='{esc(title)}':"
        f"fontcolor={GOLD}:fontsize=82:x=(w-text_w)/2:y=118:shadowcolor=black@0.55:shadowx=0:shadowy=3,"
        f"drawtext=fontfile={FONT_REG}:text='{esc(subtitle)}':"
        f"fontcolor={CREAM}@0.95:fontsize=38:x=(w-text_w)/2:y=240:shadowcolor=black@0.5:shadowx=0:shadowy=2,"
        f"drawtext=fontfile={FONT_REG}:text='{esc(datetxt)}':"
        f"fontcolor={CREAM}@0.80:fontsize=30:x=(w-text_w)/2:y=298:shadowcolor=black@0.45:shadowx=0:shadowy=2,"
        # subtítulos propios quemados (sin borde, sombra ligera)
        f"subtitles='{srt_esc}':force_style='FontName=DejaVu Serif,Fontsize=24,"
        f"PrimaryColour=&H00DDEEFF,Outline=0,Shadow=1,BackColour=&H66000000,"
        f"Alignment=2,MarginV=70,Bold=0'[pre];"
        # fundidos de entrada/salida
        f"[pre]fade=t=in:st=0:d=1.5:color=black,fade=t=out:st={max(0,d-2):.2f}:d=2[v]"
    )
    cmd = ["ffmpeg", "-y",
           "-loop", "1", "-i", img,
           "-f", "lavfi", "-i", light,
           "-i", mix,
           "-filter_complex", vf, "-map", "[v]", "-map", "2:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-r", "25", "-shortest", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit("ffmpeg render failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--img", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--pad", required=True)
    ap.add_argument("--chime", required=True)
    a = ap.parse_args()
    work = os.path.dirname(os.path.abspath(a.out))
    mix = os.path.join(work, "mix.mp3")
    print("  mezclando audio (voz + música leve + chime)...")
    d = build_mix(a.audio, a.pad, a.chime, mix)
    print(f"  render ({d:.1f}s) con plantilla de Adviento...")
    build_video(a.img, mix, a.srt, a.out, a.title, a.subtitle, a.date, d)
    print(f"OK  {a.out}  {os.path.getsize(a.out)//1024}KB")


if __name__ == "__main__":
    main()
