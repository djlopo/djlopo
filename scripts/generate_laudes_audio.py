#!/usr/bin/env python3
"""Genera el audio de las Laudes (v2) con 3 voces (ElevenLabs) + ffmpeg.

Mejoras v2:
- VOZ B = chica 2 (más estable).
- Antífonas con ECO: una voz proclama, otra responde (como el pueblo).
- Preces en orden litúrgico: cada petición -> estribillo del pueblo; al final,
  invitación a intenciones personales + PAUSA en silencio; nada de CTAs en medio.
- Normalización de volumen (loudnorm) por segmento para nivel homogéneo.

Uso:  python3 -I generate_laudes_audio.py <carpeta_salida>
"""
import json, os, subprocess, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

MODEL = "eleven_multilingual_v2"
VOICES = {
    "A": ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.82, "similarity_boost": 0.85, "style": 0.0,  "use_speaker_boost": True, "speed": 0.90}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.90}),
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.62, "similarity_boost": 0.85, "style": 0.22, "use_speaker_boost": True, "speed": 0.95}),
}
BR = '<break time="0.6s" />'
GLORIA = ('Gloria al Padre, y al Hijo, y al Espíritu Santo. ' + BR +
          ' Como era en el principio, ahora y siempre, por los siglos de los siglos. Amén.')

PS94 = ("Salmo noventa y cuatro. Invitación a la alabanza divina. " + BR +
        " Venid, aclamemos al Señor, demos vítores a la Roca que nos salva; entremos a su presencia dándole gracias, aclamándolo con cantos. " + BR +
        " Porque el Señor es un Dios grande, soberano de todos los dioses: tiene en su mano las simas de la tierra, son suyas las cumbres de los montes; suyo es el mar, porque él lo hizo, la tierra firme que modelaron sus manos. " + BR +
        " Venid, postrémonos por tierra, bendiciendo al Señor, creador nuestro. Porque él es nuestro Dios, y nosotros su pueblo, el rebaño que él guía. " + BR +
        " Ojalá escuchéis hoy su voz: No endurezcáis el corazón como en Meribá, como el día de Masá en el desierto; cuando vuestros padres me pusieron a prueba y dudaron de mí, aunque habían visto mis obras. " + BR +
        " Durante cuarenta años aquella generación me repugnó, y dije: Es un pueblo de corazón extraviado, que no reconoce mi camino; por eso he jurado en mi cólera que no entrarán en mi descanso. " + BR + " " + GLORIA)

HIMNO = ("Himno. " + BR +
         " Crece la luz bajo tu hermosa mano, Padre celeste, y suben los hombres matutinos al encuentro de Cristo Primogénito. " + BR +
         " Él hizo amanecer ante tus ojos y enalteció la aurora, cuando aún no estaba el hombre sobre el mundo para poder cantarla. " + BR +
         " Él es principio y fin del universo, y el tiempo, en su caída, se acoge al que es la fuerza de las cosas y en él rejuvenece. " + BR +
         " Él es quien nos reanima y fortalece, y hace posible el himno que, ante las maravillas de tus manos, cantamos jubilosos. " + BR +
         " He aquí la nueva luz que asciende y busca su cuerpo misterioso; he aquí, en la claridad de la mañana, el signo de tu rostro. " + BR +
         " Envía, Padre eterno, sobre el mundo el soplo de tu Hijo, potencia de tu diestra y primogénito de todos los que mueren. Amén.")

PS56 = ("Salmo cincuenta y seis. " + BR +
        " Misericordia, Dios mío, misericordia, que mi alma se refugia en ti; me refugio a la sombra de tus alas mientras pasa la calamidad. " + BR +
        " Invoco al Dios Altísimo, al Dios que hace tanto por mí: desde el cielo me enviará la salvación, confundirá a los que ansían matarme, enviará su gracia y su lealtad. " + BR +
        " Estoy echado entre leones devoradores de hombres; sus dientes son lanzas y flechas, su lengua es una espada afilada. Elévate sobre el cielo, Dios mío, y llene la tierra tu gloria. " + BR +
        " Han tendido una red a mis pasos para que sucumbiera; me han cavado delante una fosa, pero han caído en ella. " + BR +
        " Mi corazón está firme, Dios mío, mi corazón está firme. Voy a cantar y a tocar: despierta, gloria mía; despertad, cítara y arpa; despertaré a la aurora. " + BR +
        " Te daré gracias ante los pueblos, Señor; tocaré para ti ante las naciones: por tu bondad, que es más grande que los cielos; por tu fidelidad, que alcanza a las nubes. Elévate sobre el cielo, Dios mío, y llene la tierra tu gloria. " + BR + " " + GLORIA)

JR31 = ("Cántico. Felicidad del pueblo redimido. " + BR +
        " Escuchad, pueblos, la palabra del Señor, anunciadla en las islas remotas: El que dispersó a Israel lo reunirá, lo guardará como un pastor a su rebaño; porque el Señor redimió a Jacob, lo rescató de una mano más fuerte. " + BR +
        " Vendrán con aclamaciones a la altura de Sión, afluirán hacia los bienes del Señor: hacia el trigo y el vino y el aceite, y los rebaños de ovejas y de vacas; su alma será como un huerto regado, y no volverán a desfallecer. " + BR +
        " Entonces se alegrará la doncella en la danza, gozarán los jóvenes y los viejos; convertiré su tristeza en gozo, los alegraré y aliviaré sus penas; alimentaré a los sacerdotes con manjares sustanciosos, y mi pueblo se saciará de mis bienes. " + BR + " " + GLORIA)

PS47 = ("Salmo cuarenta y siete. " + BR +
        " Grande es el Señor y muy digno de alabanza en la ciudad de nuestro Dios, su monte santo, altura hermosa, alegría de toda la tierra: el monte Sión, vértice del cielo, ciudad del gran rey; entre sus palacios, Dios descuella como un alcázar. " + BR +
        " Mirad: los reyes se aliaron para atacarla juntos; pero, al verla, quedaron aterrados y huyeron despavoridos; allí los agarró un temblor y dolores como de parto; como un viento del desierto, que destroza las naves de Tarsis. " + BR +
        " Lo que habíamos oído lo hemos visto en la ciudad del Señor de los ejércitos, en la ciudad de nuestro Dios: que Dios la ha fundado para siempre. " + BR +
        " Oh Dios, meditamos tu misericordia en medio de tu templo: como tu renombre, oh Dios, tu alabanza llega al confín de la tierra; tu diestra está llena de justicia. El monte Sión se alegra, las ciudades de Judá se gozan con tus sentencias. " + BR +
        " Dad la vuelta en torno a Sión, contando sus torreones; fijaos en sus baluartes, observad sus palacios, para poder decirle a la próxima generación: Este es el Señor, nuestro Dios. Él nos guiará por siempre jamás. " + BR + " " + GLORIA)

LECTURA = ("Lectura breve. Del libro de Isaías. " + BR +
           " Así dice el Señor: El cielo es mi trono y la tierra el estrado de mis pies: ¿Qué templo podréis construirme?, ¿o qué lugar para mi descanso? Todo esto lo hicieron mis manos, todo es mío, oráculo del Señor. En ése pondré mis ojos: en el humilde y el abatido que se estremece ante mis palabras.")

BENEDICTUS = ("Cántico de Zacarías. El Mesías y su precursor. " + BR +
              " Bendito sea el Señor, Dios de Israel, porque ha visitado y redimido a su pueblo, suscitándonos una fuerza de salvación en la casa de David, su siervo, según lo había predicho desde antiguo por boca de sus santos profetas. " + BR +
              " Es la salvación que nos libra de nuestros enemigos y de la mano de todos los que nos odian; ha realizado así la misericordia que tuvo con nuestros padres, recordando su santa alianza y el juramento que juró a nuestro padre Abrahán. " + BR +
              " Para concedernos que, libres de temor, arrancados de la mano de los enemigos, le sirvamos con santidad y justicia, en su presencia, todos nuestros días. " + BR +
              " Y a ti, niño, te llamarán Profeta del Altísimo, porque irás delante del Señor a preparar sus caminos, anunciando a su pueblo la salvación, el perdón de sus pecados. " + BR +
              " Por la entrañable misericordia de nuestro Dios, nos visitará el sol que nace de lo alto, para iluminar a los que viven en tiniebla y en sombra de muerte, para guiar nuestros pasos por el camino de la paz. " + BR + " " + GLORIA)

ORACION = ("Oremos. " + BR +
           " Dios todopoderoso y eterno, humildemente acudimos a ti, al empezar el día, a media jornada y al atardecer, para pedirte que, alejando de nosotros las tinieblas del pecado, nos hagas alcanzar la luz verdadera, que es Cristo. Él, que vive y reina contigo en la unidad del Espíritu Santo y es Dios, por los siglos de los siglos. Amén.")

ESTRIBILLO = "Bendícenos y santifícanos, Señor."

seg = []
def add(role, text): seg.append((role, text))
def ant(label, text):            # antífona con eco: A proclama, B responde
    add("A", f"{label} {text}")
    add("B", text)

add("C", "Bienvenido a Tu Oración Diaria. Hoy, jueves 19 de noviembre, rezamos juntos las Laudes, la oración de la mañana de la Iglesia. " + BR + " Antes de empezar, deja en los comentarios por quién rezas hoy, para que toda la comunidad lo presente al Señor.")
add("A", "Señor, abre mis labios.")
add("B", "Y mi boca proclamará tu alabanza.")
ant("Antífona.", "Venid, adoremos al Señor, porque él es nuestro Dios.")
add("A", PS94)
add("B", "Venid, adoremos al Señor, porque él es nuestro Dios.")
add("A", HIMNO)
ant("Antífona primera.", "Despertad, cítara y arpa; despertaré a la aurora.")
add("A", PS56)
add("B", "Despertad, cítara y arpa; despertaré a la aurora.")
ant("Antífona segunda.", "Mi pueblo se saciará de mis bienes, dice el Señor.")
add("A", JR31)
add("B", "Mi pueblo se saciará de mis bienes, dice el Señor.")
ant("Antífona tercera.", "Grande es el Señor y muy digno de alabanza en la ciudad de nuestro Dios.")
add("A", PS47)
add("B", "Grande es el Señor y muy digno de alabanza en la ciudad de nuestro Dios.")
add("A", LECTURA)
add("A", "Te invoco de todo corazón; respóndeme, Señor.")
add("B", "Te invoco de todo corazón; respóndeme, Señor.")
add("A", "Guardaré tus leyes.")
add("B", "Respóndeme, Señor.")
ant("Antífona.", "Sirvamos al Señor con santidad, y nos librará de la mano de nuestros enemigos.")
add("A", BENEDICTUS)
add("B", "Sirvamos al Señor con santidad, y nos librará de la mano de nuestros enemigos.")
# PRECES (orden correcto: petición -> estribillo; sin CTAs en medio)
add("A", "Hacemos las preces. Demos gracias a Cristo, que nos ha dado la luz del día, y supliquémosle diciendo:")
add("B", ESTRIBILLO)
add("A", "Tú que te entregaste como víctima por nuestros pecados, acepta los deseos y las acciones de este día.")
add("B", ESTRIBILLO)
add("A", "Tú que nos alegras con la claridad del nuevo día, sé tú mismo el lucero brillante de nuestros corazones.")
add("B", ESTRIBILLO)
add("A", "Haz que seamos bondadosos y comprensivos con los que nos rodean, para que lleguemos a ser imágenes de tu bondad.")
add("B", ESTRIBILLO)
add("A", "En la mañana haznos escuchar tu gracia, y que tu gozo sea hoy nuestra fortaleza.")
add("B", ESTRIBILLO)
# AHORA sí: intenciones personales + pausa en silencio
add("C", "Ahora, en silencio, presenta al Señor tus propias intenciones. Él te escucha, y nada de lo tuyo le es indiferente. " + BR + " Puedes pausar el vídeo el tiempo que necesites y, si quieres, déjalas también en los comentarios, para que toda la comunidad rece por ellas.")
add("PAUSE", "9|Puedes pausar el vídeo para presentar tus intenciones")
add("A", "Fieles a la recomendación del Salvador, nos atrevemos a decir: " + BR +
         " Padre nuestro, que estás en el cielo, santificado sea tu Nombre; venga a nosotros tu reino; hágase tu voluntad en la tierra como en el cielo. Danos hoy nuestro pan de cada día; perdona nuestras ofensas, como también nosotros perdonamos a los que nos ofenden; no nos dejes caer en la tentación, y líbranos del mal. Amén.")
add("A", ORACION)
add("A", "El Señor nos bendiga, nos guarde de todo mal y nos lleve a la vida eterna.")
add("B", "Amén.")
add("C", "Gracias por rezar con Tu Oración Diaria. Si esta oración te ayuda, suscríbete y compártela, y vuelve mañana: rezamos juntos cada día. Que Dios te bendiga.")

SEG = seg
SILENCE = 0.45

def norm(path):
    tmp = path + ".n.mp3"
    r = subprocess.run(["ffmpeg", "-y", "-i", path, "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", tmp], capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 800:
        os.replace(tmp, path)

def tts(role, text, path):
    vid, settings = VOICES[role]
    payload = json.dumps({"text": text, "model_id": MODEL, "voice_settings": settings})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
    r = subprocess.run(["curl", "-sS", "-X", "POST", url, "-H", "Content-Type: application/json",
                        "-d", payload, "-o", path, "-w", "%{http_code}"], capture_output=True, text=True)
    code = r.stdout.strip()
    size = os.path.getsize(path) if os.path.exists(path) else 0
    if code != "200" or size < 1500:
        print(f"  ERROR {path}: HTTP {code} size {size}")
        return False
    norm(path)
    return True

def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-t", str(secs), "-q:a", "9", path], capture_output=True)

def main():
    sil = os.path.join(OUT, "sil.mp3")
    silence(sil, SILENCE)
    mp3s, ok = [], 0
    for i, (role, text) in enumerate(SEG):
        p = os.path.join(OUT, f"seg_{i:03d}_{role}.mp3")
        if role == "PAUSE":
            secs = float(text.split("|", 1)[0])
            silence(p, secs)
            mp3s.append(p); ok += 1
            print(f"  [{i+1}/{len(SEG)}] PAUSE {secs}s")
        else:
            if tts(role, text, p):
                ok += 1; mp3s.append(p)
            print(f"  [{i+1}/{len(SEG)}] {role}  ({len(text)} chars)")
        if i < len(SEG) - 1:
            mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s:
            f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "laudes_jue19_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf,
                    "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nSegmentos OK: {ok}/{len(SEG)}\nFINAL: {final}  ({os.path.getsize(final)//1024} KB, {dur}s)")

if __name__ == "__main__":
    main()
