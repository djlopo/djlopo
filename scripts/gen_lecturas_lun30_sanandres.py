#!/usr/bin/env python3
"""Lecturas + Evangelio + Reflexión — SAN ANDRÉS APÓSTOL (Fiesta), lunes 30 nov 2026.

Lecturas propias de la fiesta: Rom 10,9-18 · Sal 18 · Ev. Mateo 4,18-22 («Venid y seguidme»).
Reflexión propia (aprobada), inspirada en predicaciones sobre la fiesta de san Andrés.
Voces: C (presenta) · A (guía) · B (pueblo) · R (reflexión). Usa caché + biblioteca.
Uso: python3 -I gen_lecturas_lun30_sanandres.py <carpeta_salida>
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache, library  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
MODEL = "eleven_multilingual_v2"
BR = library.BR

VOICES = {
    "A": ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.82, "similarity_boost": 0.85, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.62, "similarity_boost": 0.85, "style": 0.22, "use_speaker_boost": True, "speed": 0.96}),
    "R": ("Syqs6p4s6hxhfAyhhlbS", {"stability": 0.52, "similarity_boost": 0.80, "style": 0.12, "use_speaker_boost": True, "speed": 0.97}),
}
ANT = "A toda la tierra alcanza su pregón."

seg = []
def add(role, text): seg.append((role, text))

add("C", "Bienvenido a Tu Oración Diaria. Hoy, lunes 30 de noviembre, la Iglesia celebra la fiesta del apóstol san Andrés, hermano de Simón Pedro. Escuchamos juntos las lecturas y una breve reflexión. " + BR + " Antes de empezar, deja en los comentarios por quién lo ofreces, para que toda la comunidad lo presente al Señor.")
add("A", "Nos ponemos en presencia de Dios. En el nombre del Padre, y del Hijo, y del Espíritu Santo. Amén. " + BR + " Señor, abre nuestro corazón para escuchar hoy tu Palabra.")
# PRIMERA LECTURA — Romanos 10, 9-18
add("A", "Primera lectura. Lectura de la carta del apóstol san Pablo a los Romanos.")
add("A", "Hermanos: Si profesas con tus labios que Jesús es Señor, y crees con tu corazón que Dios lo resucitó de entre los muertos, serás salvo. " + BR +
         " Pues con el corazón se cree para alcanzar la justicia, y con los labios se profesa para alcanzar la salvación. Pues dice la Escritura: «Nadie que crea en él quedará confundido». " + BR +
         " En efecto, no hay distinción entre judío y griego, porque uno mismo es el Señor de todos, generoso con todos los que lo invocan, pues todo el que invoque el nombre del Señor será salvo. " + BR +
         " Ahora bien, ¿cómo invocarán a aquel en quien no han creído? ¿Y cómo creerán en aquel de quien no han oído hablar? ¿Y cómo oirán hablar de él sin nadie que lo proclame? Y ¿cómo proclamarán, si no son enviados? " + BR +
         " Como está escrito: «¡Qué hermosos los pies de los que anuncian el Evangelio del bien!». Pero no todos han prestado oído al Evangelio. Pues Isaías dice: «Señor, ¿quién ha creído nuestro anuncio?». " + BR +
         " Por tanto, la fe viene de la predicación, y la predicación, por la palabra de Cristo. Pero pregunto yo: ¿Es que no han oído? Desde luego: «A toda la tierra alcanza su pregón y hasta los límites del orbe su lenguaje».")
add("A", "Palabra de Dios.")
add("PAUSE", "2.5|Te alabamos, Señor")
# SALMO 18
add("A", "Salmo responsorial. Del salmo dieciocho.")
add("B", ANT)
add("A", "El cielo proclama la gloria de Dios, el firmamento pregona la obra de sus manos: el día al día le pasa el mensaje, la noche a la noche se lo susurra.")
add("B", ANT)
add("A", "Sin que hablen, sin que pronuncien, sin que resuene su voz, a toda la tierra alcanza su pregón y hasta los límites del orbe su lenguaje.")
add("B", ANT)
# EVANGELIO — Mateo 4, 18-22
add("B", library.R_ALELUYA)
add("A", "Lectura del santo Evangelio según san Mateo.")
add("B", "Gloria a ti, Señor.")
add("A", "En aquel tiempo, paseando Jesús junto al lago de Galilea vio a dos hermanos, a Simón, al que llaman Pedro, y a Andrés, su hermano, que estaban echando el copo en el lago, pues eran pescadores. " + BR +
         " Les dijo: «Venid y seguidme, y os haré pescadores de hombres». Inmediatamente dejaron las redes y lo siguieron. " + BR +
         " Y, pasando adelante, vio a otros dos hermanos, a Santiago, hijo de Zebedeo, y a Juan, su hermano, que estaban en la barca repasando las redes con Zebedeo, su padre. Jesús los llamó también. Inmediatamente dejaron la barca y a su padre y lo siguieron.")
add("A", "Palabra del Señor.")
add("PAUSE", "2.5|Gloria a ti, Señor Jesús")
# MEDITACIÓN
add("PAUSE", "8|Un momento de silencio para meditar")
# REFLEXIÓN (R) — propia, aprobada
add("R", "Hermanos, hoy la Iglesia celebra a san Andrés, el apóstol que fue hermano de Simón Pedro. Y el Evangelio nos lo muestra en dos gestos que lo dicen todo. " + BR +
         " El primero, junto al mar: Jesús pasa, lo llama, «Venid y seguidme, y os haré pescadores de hombres», y Andrés, que estaba remendando las redes con su hermano, lo deja todo al instante y lo sigue. Qué generosidad: no pide explicaciones, no calcula; reconoce al Señor y se fía. Jesús le abre un horizonte inmenso: ya no sacará peces del agua, sino que ayudará a rescatar a los hombres, a salvar almas. " + BR +
         " Pero hay un segundo gesto, quizá el más entrañable. Antes de ser apóstol, Andrés corre a buscar a su hermano Pedro y le dice: «Hemos encontrado al Mesías; ven». Y así, sin grandes discursos, lo lleva a Jesús. Aquí aprendemos lo que de verdad es el apostolado: no empieza dando lecciones desde arriba, como quien se cree bueno y viene a corregir a los demás. Empieza desde el cariño, desde la igualdad. " + BR +
         " Andrés no le habla a Pedro como un maestro, sino como un hermano que lo quiere: me conoces de siempre, con mis defectos; pero tengo que contarte lo mejor que me ha pasado. Solo desde ese cariño verdadero podemos transmitir, con fuerza y sin falsedad, la presencia de Jesús. " + BR +
         " Y no olvidemos: Pedro quedó en Roma; Andrés llevó el Evangelio a Oriente. Son como los dos pulmones con que respira la Iglesia. Pidamos hoy, en su fiesta, por la unidad de todos los cristianos, y por la gracia de llevar a los nuestros al Señor, como Andrés llevó a Pedro. " + BR +
         " Esta reflexión se ha inspirado en predicaciones sobre la fiesta de san Andrés apóstol.")
add("A", "Oremos. Te pedimos humildemente, Señor, que el apóstol san Andrés, que fue predicador y pastor de tu Iglesia, interceda constantemente por nosotros ante ti. Por Jesucristo nuestro Señor. Amén.")
add("C", "Gracias por rezar con Tu Oración Diaria. Si esta Palabra te ha ayudado, suscríbete y compártela, y deja tu intención en los comentarios. Reza también los Laudes de hoy: te dejo el enlace. Hasta mañana; que Dios te bendiga.")

SEG = seg
SILENCE = 0.45

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
    final = os.path.join(OUT, "lecturas_lun30_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
