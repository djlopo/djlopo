#!/usr/bin/env python3
"""Construye un .srt sincronizado a partir de los segmentos de audio ya generados.

Reparte la duración de cada segmento (medida con ffprobe) entre sus frases,
proporcional al número de caracteres. Aproximado pero legible, sin alineador externo.

Uso: python3 -I build_srt.py <carpeta_con_seg_mp3> <salida.srt>
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate_laudes_audio import SEG, SILENCE  # noqa: E402

DIR = sys.argv[1]
OUTSRT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(DIR, "subs.srt")

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def cues_for(text):
    t = re.sub(r"<break[^>]*/>", " ", text)
    t = re.sub(r"\s+", " ", t).strip()
    parts = re.split(r"(?<=[\.\?\!;:])\s+", t)
    cues = []
    for p in parts:
        p = p.strip()
        while len(p) > 62:
            cut = p.rfind(" ", 0, 62)
            if cut <= 0:
                cut = 62
            cues.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            cues.append(p)
    return cues or [t]

def ts(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

clock, idx, out = 0.0, 1, []
for i, (role, text) in enumerate(SEG):
    mp3 = os.path.join(DIR, f"seg_{i:03d}_{role}.mp3")
    dur = probe(mp3)
    if role == "PAUSE":
        label = text.split("|", 1)[1] if "|" in text else text
        out.append(f"{idx}\n{ts(clock)} --> {ts(clock + dur)}\n⏸  {label}\n")
        idx += 1
        clock += dur + SILENCE
        continue
    cs = cues_for(text)
    total = sum(len(c) for c in cs) or 1
    t = clock
    for c in cs:
        d = dur * len(c) / total
        out.append(f"{idx}\n{ts(t)} --> {ts(t + d)}\n{c}\n")
        idx += 1
        t += d
    clock += dur + SILENCE

with open(OUTSRT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"SRT: {OUTSRT}  ({idx-1} subtítulos, {ts(clock)} total)")
