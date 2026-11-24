#!/usr/bin/env python3
"""Lecturas del día + Evangelio + Reflexión — I DOMINGO DE ADVIENTO (Ciclo B), 29 nov 2026.

Lecturas de la Misa (dominicos.org):
  1ª  Isaías 63,16b-17.19b;64,2b-7   ·  Salmo 79  ·  2ª 1 Cor 1,3-9  ·  Ev. Marcos 13,33-37 («Velad»)
Reflexión ORIGINAL, inspirada en el comentario de Fray Miguel de Burgos Núñez, O.P. (dominicos.org), atribuida.

Voces: C (presenta) · A (guía: lecturas/salmo/Evangelio) · B (pueblo/respuestas) · R (reflexión, varón mayor).
Usa caché (tts_cache) + biblioteca (library). PAUSE = silencio con texto en pantalla.
Uso: python3 -I gen_lecturas_dom29adv.py <carpeta_salida>
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
ANT = "Oh, Dios, restáuranos, que brille tu rostro y nos salve."

seg = []
def add(role, text): seg.append((role, text))

add("C", "Bienvenido a Tu Oración Diaria. Hoy, Primer Domingo de Adviento, comienza un nuevo año litúrgico y escuchamos juntos las lecturas de la Palabra de Dios y una breve reflexión. " + BR + " Antes de empezar, deja en los comentarios por quién lo ofreces, para que toda la comunidad lo presente al Señor.")
add("A", "Nos ponemos en presencia de Dios. En el nombre del Padre, y del Hijo, y del Espíritu Santo. Amén. " + BR + " Señor, que comenzamos el Adviento, abre nuestro corazón para escuchar hoy tu Palabra.")
# PRIMERA LECTURA — Isaías 63-64
add("A", "Primera lectura. Lectura del libro de Isaías.")
add("A", "Tú, Señor, eres nuestro padre, tu nombre desde siempre es «nuestro Libertador». " + BR +
         " ¿Por qué nos extravías, Señor, de tus caminos, y endureces nuestro corazón para que no te tema? Vuélvete, por amor a tus siervos y a las tribus de tu heredad. " + BR +
         " ¡Ojalá rasgases el cielo y descendieses! En tu presencia se estremecerían las montañas. Jamás se oyó ni se escuchó, ni ojo vio un Dios, fuera de ti, que hiciera tanto por quien espera en él. " + BR +
         " Sales al encuentro de quien practica con alegría la justicia y, andando en tus caminos, se acuerda de ti. He aquí que tú estabas airado y nosotros hemos pecado. " + BR +
         " Todos éramos impuros, nuestra justicia era un vestido manchado; todos nos marchitábamos como hojas, nuestras culpas nos arrebataban como el viento. Nadie invocaba tu nombre, nadie salía del letargo para adherirse a ti. " + BR +
         " Y, sin embargo, Señor, tú eres nuestro padre, nosotros la arcilla y tú nuestro alfarero: todos somos obra de tu mano.")
add("A", "Palabra de Dios.")
add("PAUSE", "2.5|Te alabamos, Señor")
# SALMO 79
add("A", "Salmo responsorial. Del salmo setenta y nueve.")
add("B", ANT)
add("A", "Pastor de Israel, escucha; tú que te sientas sobre querubines, resplandece; despierta tu poder y ven a salvarnos.")
add("B", ANT)
add("A", "Dios de los ejércitos, vuélvete: mira desde el cielo, fíjate, ven a visitar tu viña. Cuida la cepa que tu diestra plantó, y al hijo del hombre que tú has fortalecido.")
add("B", ANT)
add("A", "Que tu mano proteja a tu escogido, al hombre que tú fortaleciste. No nos alejaremos de ti: danos vida, para que invoquemos tu nombre.")
add("B", ANT)
# SEGUNDA LECTURA — 1 Cor 1,3-9
add("A", "Segunda lectura. Lectura de la primera carta del apóstol san Pablo a los Corintios.")
add("A", "Hermanos: A vosotros gracia y paz de parte de Dios nuestro Padre y del Señor Jesucristo. " + BR +
         " Doy gracias a mi Dios continuamente por vosotros, por la gracia de Dios que se os ha dado en Cristo Jesús; pues en él habéis sido enriquecidos en todo: en toda palabra y en toda ciencia; porque en vosotros se ha probado el testimonio de Cristo, de modo que no carecéis de ningún don gratuito, mientras aguardáis la manifestación de nuestro Señor Jesucristo. " + BR +
         " Él os mantendrá firmes hasta el final, para que seáis irreprensibles el día de nuestro Señor Jesucristo. Fiel es Dios, el cual os llamó a la comunión con su Hijo, Jesucristo nuestro Señor.")
add("A", "Palabra de Dios.")
add("PAUSE", "2.5|Te alabamos, Señor")
# EVANGELIO — Marcos 13,33-37
add("B", library.R_ALELUYA)
add("A", "Lectura del santo Evangelio según san Marcos.")
add("B", "Gloria a ti, Señor.")
add("A", "En aquel tiempo, dijo Jesús a sus discípulos: " + BR +
         " «Estad atentos, vigilad: pues no sabéis cuándo es el momento. " + BR +
         " Es igual que un hombre que se fue de viaje, y dejó su casa y dio a cada uno de sus criados su tarea, encargando al portero que velara. " + BR +
         " Velad entonces, pues no sabéis cuándo vendrá el señor de la casa, si al atardecer, o a medianoche, o al canto del gallo, o al amanecer: no sea que venga inesperadamente y os encuentre dormidos. " + BR +
         " Lo que os digo a vosotros, lo digo a todos: ¡Velad!».")
add("A", "Palabra del Señor.")
add("PAUSE", "2.5|Gloria a ti, Señor Jesús")
# MEDITACIÓN
add("PAUSE", "8|Un momento de silencio para meditar")
# REFLEXIÓN (R) — original, inspirada en Fray Miguel de Burgos Núñez, O.P.
add("R", "Hermanos, comenzamos el Adviento, y la Palabra de hoy nos regala dos actitudes que van juntas: la esperanza y la vigilancia. " + BR +
         " El profeta Isaías pone en nuestros labios un grito hondo: «¡Ojalá rasgases el cielo y descendieses!». Es el deseo del que sabe que, sin Dios, la vida no tiene futuro. Y añade una imagen preciosa: «nosotros somos la arcilla y tú nuestro alfarero». Aunque nuestra justicia sea un vestido manchado, Dios no es un juez que se venga, sino un Padre y Redentor que baja a buscarnos, que no deja a los suyos en manos de su culpa. " + BR +
         " Ese anhelo del profeta ya se ha cumplido: Dios rasgó el cielo y descendió, se hizo uno de nosotros en Jesús. Por eso san Pablo nos asegura que no nos falta ningún don mientras aguardamos su manifestación, y que el Dios fiel nos mantendrá firmes hasta el final. " + BR +
         " Y el Evangelio nos dice cómo esperar: «Velad». Vigilar no es vivir con miedo al día ni a la hora, sino todo lo contrario; es la forma despierta de la esperanza. Como el portero que guarda la casa, cada uno tiene su tarea, y el Señor puede llegar en cualquier momento, también hoy, en lo pequeño de nuestra jornada. " + BR +
         " Que este Adviento no nos encuentre dormidos, sino con el corazón despierto, trabajando en lo nuestro y esperando con alegría al que viene a salvarnos. " + BR +
         " Esta reflexión está inspirada en el comentario de fray Miguel de Burgos Núñez, de la Orden de Predicadores.")
add("A", "Oremos. Dios todopoderoso, despierta en nosotros el deseo de salir al encuentro de Cristo que viene; que, vigilantes en la oración y alegres en la alabanza, merezcamos recibirlo cuando llame a nuestra puerta. Por Jesucristo nuestro Señor. Amén.")
add("C", "Gracias por rezar con Tu Oración Diaria. Si esta Palabra te ha ayudado, suscríbete y compártela, y deja tu intención en los comentarios. Reza también los Laudes de hoy: te dejo el enlace. Hasta mañana; que Dios te bendiga y tengas un buen comienzo de Adviento.")

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
    final = os.path.join(OUT, "lecturas_dom29_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
