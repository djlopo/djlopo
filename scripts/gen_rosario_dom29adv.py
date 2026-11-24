#!/usr/bin/env python3
"""Santo Rosario — I DOMINGO DE ADVIENTO (29 nov 2026). MISTERIOS GOZOSOS.

En Adviento los domingos se rezan tradicionalmente los misterios Gozosos
(Encarnación y Nacimiento del Señor), muy propios de este tiempo.

Estructura: señal de la cruz, acto de contrición breve, oración inicial;
por cada misterio: enunciado + meditación breve, Padrenuestro, 10 Avemarías
(A proclama la 1ª mitad / B responde la 2ª), Gloria y jaculatoria de Fátima;
al final, Salve y oración.

La caché (tts_cache) reutiliza las partes fijas (Avemaría, Padrenuestro, Gloria,
Fátima, Salve) desde library.py: el Avemaría se reutiliza ~50 veces -> 0 créditos.
Voces: C (enuncia misterios) · A (guía: Padrenuestro + Avemaría 1ª mitad + Fátima) · B (pueblo: Avemaría 2ª mitad + Gloria).
Uso: python3 -I gen_rosario_dom29adv.py <carpeta_salida>
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache, library  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
MODEL = "eleven_multilingual_v2"
BR = library.BR

VOICES = {
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.60, "similarity_boost": 0.85, "style": 0.26, "use_speaker_boost": True, "speed": 0.96}),
    "A": ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.82, "similarity_boost": 0.85, "style": 0.0,  "use_speaker_boost": True, "speed": 0.93}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.93}),
}

# Misterios Gozosos: (enunciado, meditación breve, fruto)
GOZOSOS = [
    ("En el primer misterio gozoso contemplamos la Encarnación del Hijo de Dios.",
     "El ángel anuncia a María que será Madre del Salvador, y ella responde: «Hágase en mí según tu palabra». Así comienza el Adviento del mundo.",
     "Pidamos la humildad y un corazón disponible como el de María."),
    ("En el segundo misterio gozoso contemplamos la Visitación de Nuestra Señora a su prima santa Isabel.",
     "María, llevando a Jesús en su seno, se apresura a servir; e Isabel la proclama bendita entre las mujeres.",
     "Pidamos la caridad que corre a servir y lleva a Cristo a los demás."),
    ("En el tercer misterio gozoso contemplamos el Nacimiento del Hijo de Dios en Belén.",
     "El Señor del cielo nace pobre en un pesebre; la luz verdadera viene al mundo en el silencio de la noche.",
     "Pidamos el desprendimiento y hacer sitio a Jesús en nuestra casa y en nuestro corazón."),
    ("En el cuarto misterio gozoso contemplamos la Presentación de Jesús en el templo.",
     "María y José ofrecen al Niño al Padre, y el anciano Simeón lo reconoce como luz de las naciones.",
     "Pidamos la obediencia y ofrecer nuestra vida al Señor."),
    ("En el quinto misterio gozoso contemplamos al Niño Jesús perdido y hallado en el templo.",
     "Después de tres días de búsqueda, María y José lo encuentran en la casa de su Padre, entre los doctores.",
     "Pidamos la gracia de buscar siempre a Jesús y no perderlo nunca."),
]

seg = []
def add(role, text): seg.append((role, text))

# --- Apertura ---
add("C", "Bienvenido a Tu Oración Diaria. Hoy, Primer Domingo de Adviento, rezamos juntos el Santo Rosario, meditando los misterios gozosos, tan propios de este tiempo de espera del Señor. " + BR + " Deja en los comentarios tu intención, para rezarla todos. Comencemos.")
add("A", library.SENAL_CRUZ)
add("A", "Señor mío Jesucristo, me pesa de todo corazón haberte ofendido; propongo no volver a pecar y confío en tu misericordia. " + BR + " Abre, Señor, nuestros labios, y nuestra boca proclamará tu alabanza.")

# --- Cinco misterios ---
for idx, (enunciado, medit, fruto) in enumerate(GOZOSOS, start=1):
    add("C", enunciado + " " + BR + " " + medit + " " + BR + " " + fruto)
    add("A", library.PADRENUESTRO)
    for n in range(10):
        add("A", library.AVEMARIA_1)
        add("B", library.AVEMARIA_2)
    add("B", library.GLORIA)
    add("A", library.JACULATORIA_FATIMA)
    if idx < 5:
        add("PAUSE", "1.2|")

# --- Cierre ---
add("C", "Terminamos encomendándonos a nuestra Madre.")
add("B", library.SALVE)
add("A", "Ruega por nosotros, santa Madre de Dios, para que seamos dignos de alcanzar las promesas de nuestro Señor Jesucristo. Amén.")
add("C", "Gracias por rezar el Rosario con Tu Oración Diaria. Si te ayuda a preparar el Adviento, suscríbete y compártelo. Que la Virgen María te acompañe; hasta mañana.")

SEG = seg
SILENCE = 0.35

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
        if i % 10 == 0 or role != "A":
            print(f"  [{i+1}/{len(SEG)}] {tag}")
        if i < len(SEG) - 1: mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s: f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "rosario_dom29_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
