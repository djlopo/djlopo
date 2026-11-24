#!/usr/bin/env python3
"""Especial: Encendido de la Primera Vela de Adviento (en familia) - I Domingo.
Usa caché + biblioteca. python3 -I gen_especial_vela1.py <carpeta_salida>
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache, library  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
MODEL = "eleven_multilingual_v2"
BR = library.BR

VOICES = {
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.60, "similarity_boost": 0.85, "style": 0.28, "use_speaker_boost": True, "speed": 0.97}),
    "R": ("Syqs6p4s6hxhfAyhhlbS", {"stability": 0.55, "similarity_boost": 0.80, "style": 0.12, "use_speaker_boost": True, "speed": 0.96}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
}

seg = []
def add(role, text): seg.append((role, text))

add("C", "Bienvenidos a Tu Oración Diaria. Hoy, Primer Domingo de Adviento, comenzamos a preparar nuestro corazón para la venida del Señor encendiendo en familia la primera vela de la corona de Adviento. " + BR + " Reúnete con los tuyos, y empecemos.")
add("R", library.SENAL_CRUZ)
add("C", "La corona de Adviento, verde como la esperanza, tiene cuatro velas: una por cada semana. " + BR + " Hoy encendemos la primera, la vela de la Esperanza, que anuncia que el Señor viene. Su pequeña luz nos recuerda que, aunque el mundo esté a oscuras, Cristo es la luz que vence las tinieblas.")
add("R", "Escuchemos la Palabra de Dios. De la carta del apóstol san Pablo a los Romanos. " + BR + " Hermanos: Ya es hora de que despertéis del sueño, pues la salvación está ahora más cerca que cuando abrazamos la fe. La noche va pasando, el día está encima; desnudémonos de las obras de las tinieblas y vistámonos de las armas de la luz. " + BR + " Palabra de Dios.")
add("B", library.R_TE_ALABAMOS)
add("R", "Oremos. " + BR + " Señor, Dios nuestro, bendice esta corona y estas velas; que su luz creciente ilumine nuestro hogar y nuestro corazón, y nos prepare para recibir a Cristo, que viene a salvarnos. Él, que vive y reina por los siglos de los siglos.")
add("B", library.R_AMEN)
add("C", "Ahora, uno de vosotros, el padre, la madre o uno de los hijos, enciende despacio la primera vela de la corona.")
add("PAUSE", "6|Encended la primera vela de Adviento")
add("C", "Mientras arde esta luz, repetimos juntos, con el corazón abierto:")
add("B", "Ven, Señor Jesús.")
add("R", "Oremos. " + BR + " Señor, despierta en nosotros el deseo de prepararnos a la venida de Cristo por la práctica de las buenas obras, para que, colocados un día a su derecha, merezcamos poseer el reino celestial. Por Jesucristo nuestro Señor.")
add("B", library.R_AMEN)
add("C", "Y recemos juntos, como Jesús nos enseñó:")
add("R", library.PADRENUESTRO)
add("C", "Que el Señor que viene os bendiga y os guarde durante esta primera semana de Adviento. " + BR + " Nos vemos cada día en Tu Oración Diaria. Buen domingo, y buen comienzo de Adviento.")

SEG = seg
SILENCE = 0.5

def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(secs), "-q:a", "9", path], capture_output=True)

def main():
    sil = os.path.join(OUT, "sil.mp3"); silence(sil, SILENCE)
    mp3s, ok, reused = [], 0, 0
    for i, (role, text) in enumerate(SEG):
        p = os.path.join(OUT, f"seg_{i:03d}_{role}.mp3")
        if role == "PAUSE":
            silence(p, float(text.split("|", 1)[0])); mp3s.append(p); ok += 1; tag = "PAUSE"
        else:
            r = tts_cache.get_or_generate(VOICES[role][0], VOICES[role][1], text, p, MODEL)
            if r is None:
                print(f"  [{i+1}/{len(SEG)}] {role} ERROR")
                if i < len(SEG) - 1: mp3s.append(sil)
                continue
            ok += 1; mp3s.append(p); reused += (r == "cache"); tag = f"{role} ({r})"
        print(f"  [{i+1}/{len(SEG)}] {tag}")
        if i < len(SEG) - 1: mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s: f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "especial_vela1_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
