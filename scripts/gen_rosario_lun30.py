#!/usr/bin/env python3
"""Santo Rosario — Lunes 30 nov 2026 (San Andrés). MISTERIOS GOZOSOS.

Mejoras: Padrenuestro y Gloria a DOS VOCES (guía A / pueblo B), y antes de meditar
cada misterio se PROCLAMA su pasaje bíblico (Palabra de Dios). Avemaría a dos voces.
La caché reutiliza las partes fijas (Avemaría, mitades del Padrenuestro y Gloria, Fátima...).
Voces: C (enuncia) · A (guía) · B (pueblo). Uso: python3 -I gen_rosario_lun30.py <carpeta>
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

# (enunciado, PALABRA bíblica literal breve, meditación+fruto)
GOZOSOS = [
    ("En el primer misterio gozoso contemplamos la Encarnación del Hijo de Dios. La Anunciación del ángel a María.",
     "El ángel Gabriel fue enviado por Dios a una virgen desposada con un hombre llamado José; la virgen se llamaba María. Y le dijo: «Alégrate, llena de gracia, el Señor está contigo. Concebirás en tu vientre y darás a luz un hijo, y le pondrás por nombre Jesús». " + BR + " Y María contestó: «Aquí está la esclava del Señor; hágase en mí según tu palabra».",
     "Pidamos la humildad y un corazón disponible como el de María."),
    ("En el segundo misterio gozoso contemplamos la Visitación de Nuestra Señora a su prima santa Isabel.",
     "En aquellos días, María se puso en camino y entró en casa de Isabel y la saludó. Al oír Isabel el saludo, saltó la criatura en su vientre; e Isabel, llena del Espíritu Santo, exclamó a voz en grito: «¡Bendita tú entre las mujeres, y bendito el fruto de tu vientre!».",
     "Pidamos la caridad que corre a servir y lleva a Cristo a los demás."),
    ("En el tercer misterio gozoso contemplamos el Nacimiento del Hijo de Dios en Belén.",
     "Le llegó a María el tiempo del parto y dio a luz a su hijo primogénito, lo envolvió en pañales y lo acostó en un pesebre, porque no tenían sitio en la posada. " + BR + " Y el ángel dijo a los pastores: «Os ha nacido hoy, en la ciudad de David, un Salvador: el Mesías, el Señor».",
     "Pidamos el desprendimiento y hacer sitio a Jesús en nuestra casa y en nuestro corazón."),
    ("En el cuarto misterio gozoso contemplamos la Presentación de Jesús en el templo.",
     "Llevaron al niño a Jerusalén para presentarlo al Señor. El anciano Simeón lo tomó en brazos y bendijo a Dios diciendo: «Ahora, Señor, según tu promesa, puedes dejar a tu siervo irse en paz, porque mis ojos han visto a tu Salvador, luz para alumbrar a las naciones».",
     "Pidamos la obediencia y ofrecer nuestra vida al Señor."),
    ("En el quinto misterio gozoso contemplamos al Niño Jesús perdido y hallado en el templo.",
     "Al cabo de tres días lo encontraron en el templo, sentado en medio de los maestros, escuchándolos y haciéndoles preguntas. Su madre le dijo: «Hijo, ¿por qué nos has tratado así?». Él les contestó: «¿No sabíais que yo debía estar en la casa de mi Padre?».",
     "Pidamos la gracia de buscar siempre a Jesús y no perderlo nunca."),
]

seg = []
def add(role, text): seg.append((role, text))

# --- Apertura ---
add("C", "Bienvenido a Tu Oración Diaria. Hoy, lunes, fiesta del apóstol san Andrés, rezamos juntos el Santo Rosario meditando los misterios gozosos. " + BR + " Deja en los comentarios tu intención, para rezarla todos. Comencemos.")
add("A", library.SENAL_CRUZ)
add("A", "Señor mío Jesucristo, me pesa de todo corazón haberte ofendido; propongo no volver a pecar y confío en tu misericordia. " + BR + " Abre, Señor, nuestros labios, y nuestra boca proclamará tu alabanza.")

# --- Cinco misterios ---
for idx, (enunciado, palabra, medit) in enumerate(GOZOSOS, start=1):
    add("C", enunciado)
    add("A", "Escuchemos la Palabra de Dios. " + BR + " " + palabra)
    add("C", medit)
    add("A", library.PADRENUESTRO_1)
    add("B", library.PADRENUESTRO_2)
    for n in range(10):
        add("A", library.AVEMARIA_1)
        add("B", library.AVEMARIA_2)
    add("A", library.GLORIA_1)
    add("B", library.GLORIA_2)
    add("A", library.JACULATORIA_FATIMA)
    if idx < 5:
        add("PAUSE", "1.2|")

# --- Cierre ---
add("C", "Terminamos encomendándonos a nuestra Madre.")
add("B", library.SALVE)
add("A", "Ruega por nosotros, santa Madre de Dios, para que seamos dignos de alcanzar las promesas de nuestro Señor Jesucristo. Amén.")
add("C", "Gracias por rezar el Rosario con Tu Oración Diaria. Si te ayuda, suscríbete y compártelo. Que la Virgen María y el apóstol san Andrés intercedan por ti; hasta mañana.")

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
        if i % 12 == 0 or role != "A":
            print(f"  [{i+1}/{len(SEG)}] {tag}")
        if i < len(SEG) - 1: mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s: f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "rosario_lun30_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
