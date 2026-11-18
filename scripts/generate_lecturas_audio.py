#!/usr/bin/env python3
"""Audio del vídeo 'Lecturas del día + Reflexión' (plantilla estándar).

Voces: C (presenta) · A (guía: lecturas, salmo, Evangelio) · B (pueblo) · R (reflexión, varón mayor).
Contenido (jue 19 nov 2026): lecturas de la Misa de dominicos.org + reflexión original "Inspirada en" su comentario.
PAUSE = silencio con texto en pantalla (respuesta del pueblo / meditación).

Uso: python3 -I generate_lecturas_audio.py <carpeta_salida>
"""
import json, os, subprocess, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

MODEL = "eleven_multilingual_v2"
VOICES = {
    "A": ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.82, "similarity_boost": 0.85, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.62, "similarity_boost": 0.85, "style": 0.22, "use_speaker_boost": True, "speed": 0.96}),
    "R": ("Syqs6p4s6hxhfAyhhlbS", {"stability": 0.52, "similarity_boost": 0.80, "style": 0.12, "use_speaker_boost": True, "speed": 0.97}),
}
BR = '<break time="0.6s" />'
ANT = "Has hecho de nosotros, para nuestro Dios, un reino de sacerdotes."

seg = []
def add(role, text): seg.append((role, text))

add("C", "Bienvenido a Tu Oración Diaria. Hoy, jueves 19 de noviembre, escuchamos juntos las lecturas de la Palabra de Dios y una breve reflexión. " + BR + " Antes de empezar, deja en los comentarios por quién lo ofreces, para que toda la comunidad lo presente al Señor.")
add("A", "Nos ponemos en presencia de Dios. En el nombre del Padre, y del Hijo, y del Espíritu Santo. Amén. " + BR + " Señor, abre nuestro corazón para escuchar hoy tu Palabra.")
# PRIMERA LECTURA — Apocalipsis 5, 1-10
add("A", "Primera lectura. Lectura del libro del Apocalipsis.")
add("A", "Yo, Juan, vi en la mano derecha del que está sentado en el trono un libro escrito por dentro y por fuera, sellado con siete sellos. " + BR +
         " Y vi a un ángel poderoso que pregonaba en alta voz: «¿Quién es digno de abrir el libro y desatar sus sellos?». Y nadie, ni en el cielo ni en la tierra ni debajo de la tierra, podía abrir el libro ni mirarlo. Y yo lloraba mucho, porque no se había encontrado a nadie digno de abrir el libro y de mirarlo. " + BR +
         " Pero uno de los ancianos me dijo: «Deja de llorar, pues ha vencido el león de la tribu de Judá, el retoño de David, y es capaz de abrir el libro y sus siete sellos». " + BR +
         " Y vi, en medio del trono y de los cuatro vivientes, y en medio de los ancianos, a un Cordero de pie, como degollado; tenía siete cuernos y siete ojos, que son los siete espíritus de Dios enviados a toda la tierra. Se acercó y recibió el libro de la mano derecha del que está sentado en el trono. " + BR +
         " Cuando recibió el libro, los cuatro vivientes y los veinticuatro ancianos se postraron ante el Cordero; tenían cítaras y copas de oro llenas de perfume, que son las oraciones de los santos. Y cantaban un cántico nuevo: «Eres digno de recibir el libro y de abrir sus sellos, porque fuiste degollado, y con tu sangre has adquirido para Dios hombres de toda tribu, lengua, pueblo y nación; y has hecho de ellos, para nuestro Dios, un reino de sacerdotes, y reinarán sobre la tierra».")
add("A", "Palabra de Dios.")
add("PAUSE", "2.5|Te alabamos, Señor")
# SALMO RESPONSORIAL — Salmo 149
add("A", "Salmo responsorial. Del salmo ciento cuarenta y nueve.")
add("B", ANT)
add("A", "Cantad al Señor un cántico nuevo, resuene su alabanza en la asamblea de los fieles; que se alegre Israel por su Creador, los hijos de Sión por su Rey.")
add("B", ANT)
add("A", "Alabad su nombre con danzas, cantadle con tambores y cítaras; porque el Señor ama a su pueblo y adorna con la victoria a los humildes.")
add("B", ANT)
add("A", "Que los fieles festejen su gloria y canten jubilosos en sus puestos, con vítores a Dios en la boca. Es un honor para todos sus fieles.")
add("B", ANT)
# EVANGELIO — Lucas 19, 41-44
add("B", "Aleluya, aleluya, aleluya.")
add("A", "Lectura del santo Evangelio según san Lucas.")
add("B", "Gloria a ti, Señor.")
add("A", "En aquel tiempo, al acercarse Jesús a Jerusalén y ver la ciudad, lloró sobre ella, diciendo: " + BR +
         " «¡Si también tú reconocieras en este día lo que conduce a la paz! Pero ahora está escondido a tus ojos. " + BR +
         " Vendrán días sobre ti en que tus enemigos te rodearán de trincheras, te sitiarán, te apretarán el cerco por todas partes; te arrasarán a ti y a tus hijos dentro de ti, y no dejarán en ti piedra sobre piedra, porque no reconociste el tiempo de tu visita».")
add("A", "Palabra del Señor.")
add("PAUSE", "2.5|Gloria a ti, Señor Jesús")
# MEDITACIÓN
add("PAUSE", "8|Un momento de silencio para meditar")
# REFLEXIÓN (R) — original, inspirada en el comentario de dominicos.org
add("R", "Hermanos, el Evangelio de hoy nos muestra a Jesús llorando sobre Jerusalén. No llora por sí mismo, sino por una ciudad que no ha sabido reconocer el tiempo de su visita, aquello que conducía a su paz. " + BR +
         " También a nosotros, muchas veces, la paz verdadera se nos esconde a los ojos, ocupados en tantas cosas. Pero Dios sigue pasando por nuestra vida; hay un momento oportuno, un tiempo de gracia, en el que podemos bajar nuestras resistencias y dejar que el Señor entre. " + BR +
         " La primera lectura nos da la clave de la esperanza: el Cordero, que estaba degollado pero vive, es capaz de abrir el libro de la historia, y con su sangre nos ha hecho un reino de sacerdotes. Nada está perdido mientras él reina. " + BR +
         " Reconozcamos hoy el tiempo de su visita, no endurezcamos el corazón, y dejemos que su Palabra nos conduzca por el camino de la paz. " + BR +
         " Esta reflexión está inspirada en el comentario de sor Inmaculada López Miró, monja dominica.")
add("A", "Oremos. Señor Jesús, que lloraste sobre la ciudad que no supo reconocerte, abre hoy nuestros ojos al tiempo de tu visita; haz que acojamos tu gracia y caminemos en tu paz. Tú que vives y reinas por los siglos de los siglos. Amén.")
add("C", "Gracias por rezar con Tu Oración Diaria. Si esta Palabra te ha ayudado, suscríbete y compártela, y deja tu intención en los comentarios. Reza también los Laudes de hoy: te dejo el enlace al final. Hasta mañana; que Dios te bendiga.")

SEG = seg
SILENCE = 0.45

def norm(path):
    tmp = path + ".n.mp3"
    r = subprocess.run(["ffmpeg", "-y", "-i", path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", tmp], capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 800:
        os.replace(tmp, path)

def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(secs), "-q:a", "9", path], capture_output=True)

def tts(role, text, path):
    vid, settings = VOICES[role]
    payload = json.dumps({"text": text, "model_id": MODEL, "voice_settings": settings})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
    r = subprocess.run(["curl", "-sS", "-X", "POST", url, "-H", "Content-Type: application/json",
                        "-d", payload, "-o", path, "-w", "%{http_code}"], capture_output=True, text=True)
    if r.stdout.strip() != "200" or (os.path.getsize(path) if os.path.exists(path) else 0) < 1500:
        print(f"  ERROR {path}: HTTP {r.stdout.strip()}")
        return False
    norm(path)
    return True

def main():
    sil = os.path.join(OUT, "sil.mp3"); silence(sil, SILENCE)
    mp3s, ok = [], 0
    for i, (role, text) in enumerate(SEG):
        p = os.path.join(OUT, f"seg_{i:03d}_{role}.mp3")
        if role == "PAUSE":
            silence(p, float(text.split("|", 1)[0])); mp3s.append(p); ok += 1
            print(f"  [{i+1}/{len(SEG)}] PAUSE")
        else:
            if tts(role, text, p):
                ok += 1; mp3s.append(p)
            print(f"  [{i+1}/{len(SEG)}] {role} ({len(text)} chars)")
        if i < len(SEG) - 1:
            mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s:
            f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "lecturas_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)}  FINAL {final}  {os.path.getsize(final)//1024}KB  {dur}s")

if __name__ == "__main__":
    main()
