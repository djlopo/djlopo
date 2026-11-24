#!/usr/bin/env python3
"""Short (vertical) — I DOMINGO DE ADVIENTO, 29 nov 2026. ~40 s.

Mensaje breve a partir del Evangelio del día (Mc 13,33-37: «Velad»).
Voces: C (cálida, presenta) · R (grave, la palabra clave). Usa caché.
Uso: python3 -I gen_short_dom29adv.py <carpeta_salida>
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

add("C", "Hoy empieza el Adviento, y el Evangelio nos deja una sola palabra.")
add("R", "Velad.")
add("C", "No sabemos el día ni la hora en que vendrá el Señor. " + BR + " Por eso vigilar no es vivir con miedo: es mantener el corazón despierto y la lámpara encendida, esperándolo con alegría.")
add("C", "Esta semana, enciende una luz y prepara su llegada. " + BR + " Suscríbete a Tu Oración Diaria y reza cada día con nosotros.")

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
            print(f"  [{i+1}/{len(SEG)}] {role} ERROR");  continue
        ok += 1; mp3s.append(p); reused += (r == "cache")
        print(f"  [{i+1}/{len(SEG)}] {role} ({r})")
        if i < len(SEG) - 1: mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s: f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "short_dom29_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
