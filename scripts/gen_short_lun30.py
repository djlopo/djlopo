#!/usr/bin/env python3
"""Short (vertical) — Lunes 30 nov 2026, San Andrés Apóstol. ~35 s.
A partir de Mt 4,18-22 («Venid y seguidme») y del gesto de Andrés con su hermano Pedro.
Voces: C (cálida) · R (grave, la llamada). Usa caché.
Uso: python3 -I gen_short_lun30.py <carpeta_salida>
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache, library  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
MODEL = "eleven_multilingual_v2"
BR = library.BR

VOICES = {
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.58, "similarity_boost": 0.85, "style": 0.30, "use_speaker_boost": True, "speed": 0.98}),
    "R": ("Syqs6p4s6hxhfAyhhlbS", {"stability": 0.55, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True, "speed": 0.95}),
}

seg = []
def add(role, text): seg.append((role, text))

add("C", "San Andrés estaba remendando sus redes cuando Jesús pasó y le dijo cuatro palabras:")
add("R", "Venid y seguidme.")
add("C", "Y lo dejó todo al instante. " + BR + " Pero antes había hecho algo todavía más valiente: correr a buscar a su hermano Pedro y decirle: «hemos encontrado al Mesías».")
add("C", "Eso es la fe: no guardarla, sino llevársela a quien quieres. " + BR + " ¿A quién vas a acercar hoy a Jesús? " + BR + " Suscríbete a Tu Oración Diaria.")

SEG = seg
SILENCE = 0.4

def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(secs), "-q:a", "9", path], capture_output=True)

def main():
    sil = os.path.join(OUT, "sil.mp3"); silence(sil, SILENCE)
    mp3s, ok, reused = [], 0, 0
    for i, (role, text) in enumerate(SEG):
        p = os.path.join(OUT, f"seg_{i:03d}_{role}.mp3")
        r = tts_cache.get_or_generate(VOICES[role][0], VOICES[role][1], text, p, MODEL)
        if r is None:
            print(f"  [{i+1}/{len(SEG)}] {role} ERROR"); continue
        ok += 1; mp3s.append(p); reused += (r == "cache")
        print(f"  [{i+1}/{len(SEG)}] {role} ({r})")
        if i < len(SEG) - 1: mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s: f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "short_lun30_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
