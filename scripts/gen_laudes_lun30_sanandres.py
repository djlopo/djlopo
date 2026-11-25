#!/usr/bin/env python3
"""Laudes — SAN ANDRÉS APÓSTOL (Fiesta), lunes 30 nov 2026. Oficio PROPIO.
Textos tomados de la Liturgia de las Horas (sync/2026/nov/30/laudes.htm).
Antífonas propias en eco (A proclama / B responde). Padrenuestro a dos voces.
Voces: C (presenta) · A (guía) · B (pueblo/eco). Usa caché + biblioteca.
Uso: python3 -I gen_laudes_lun30_sanandres.py <carpeta_salida>
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache, library  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
MODEL = "eleven_multilingual_v2"
BR = library.BR
GLORIA = library.GLORIA

VOICES = {
    "A": ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.82, "similarity_boost": 0.85, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.92}),
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.62, "similarity_boost": 0.85, "style": 0.22, "use_speaker_boost": True, "speed": 0.96}),
}

seg = []
def add(role, text): seg.append((role, text))
def ant(text):
    add("A", "Antífona. " + text)
    add("B", text)

add("C", "Bienvenido a Tu Oración Diaria. Hoy, lunes 30 de noviembre, fiesta del apóstol san Andrés, rezamos juntos los Laudes, la oración de la mañana de la Iglesia. " + BR + " Deja tu intención en los comentarios. Comencemos.")
add("A", "Señor, abre mis labios.")
add("B", "Y mi boca proclamará tu alabanza.")
# INVITATORIO
ant("Venid, adoremos al Señor, rey de los apóstoles.")
add("A", "Salmo noventa y cuatro. Invitación a la alabanza divina. " + BR +
         " Venid, aclamemos al Señor, demos vítores a la Roca que nos salva; entremos a su presencia dándole gracias, aclamándolo con cantos. " + BR +
         " Porque el Señor es un Dios grande, soberano de todos los dioses: tiene en su mano las simas de la tierra, son suyas las cumbres de los montes; suyo es el mar, porque él lo hizo, la tierra firme que modelaron sus manos. " + BR +
         " Venid, postrémonos por tierra, bendiciendo al Señor, creador nuestro. Porque él es nuestro Dios, y nosotros su pueblo, el rebaño que él guía. " + BR +
         " Ojalá escuchéis hoy su voz: «No endurezcáis el corazón como en Meribá, como el día de Masá en el desierto; cuando vuestros padres me pusieron a prueba y dudaron de mí, aunque habían visto mis obras. " + BR +
         " Durante cuarenta años aquella generación me repugnó, y dije: Es un pueblo de corazón extraviado, que no reconoce mi camino; por eso he jurado en mi cólera que no entrarán en mi descanso». " + BR + " " + GLORIA)
add("B", "Venid, adoremos al Señor, rey de los apóstoles.")
# HIMNO
add("A", "Himno. Vosotros que escuchasteis la llamada. " + BR +
         " Vosotros, que escuchasteis la llamada de viva voz que Cristo os dirigía, abrid nuestro vivir y nuestra alma al mensaje de amor que él nos envía. " + BR +
         " Vosotros, que invitados al banquete gustasteis el sabor del nuevo vino, llenad el vaso del amor que ofrece al sediento de Dios en su camino. " + BR +
         " Vosotros, que tuvisteis tan gran suerte de verle dar a muertos nueva vida, no dejéis que el pecado y que la muerte nos priven de la vida recibida. " + BR +
         " Vosotros, que lo visteis ya glorioso, hecho Señor de gloria sempiterna, haced que nuestro amor conozca el gozo de vivir junto a él la vida eterna. Amén.")
# SALMODIA
ant("Uno de los dos que había ido en seguimiento de Jesús era Andrés, el hermano de Simón Pedro.")
add("A", "Salmo sesenta y dos. El alma sedienta de Dios. " + BR +
         " ¡Oh Dios!, tú eres mi Dios, por ti madrugo, mi alma está sedienta de ti; mi carne tiene ansia de ti, como tierra reseca, agostada, sin agua. " + BR +
         " ¡Cómo te contemplaba en el santuario viendo tu fuerza y tu gloria! Tu gracia vale más que la vida, te alabarán mis labios. Toda mi vida te bendeciré y alzaré las manos invocándote. " + BR +
         " Me saciaré de manjares exquisitos, y mis labios te alabarán jubilosos. En el lecho me acuerdo de ti y velando medito en ti, porque fuiste mi auxilio, y a la sombra de tus alas canto con júbilo; mi alma está unida a ti, y tu diestra me sostiene. " + BR + " " + GLORIA)
add("B", "Uno de los dos que había ido en seguimiento de Jesús era Andrés, el hermano de Simón Pedro.")
ant("El Señor amó a Andrés con singular predilección.")
add("A", "Cántico. Toda la creación alabe al Señor. Daniel capítulo tres. " + BR +
         " Creaturas todas del Señor, bendecid al Señor, ensalzadlo con himnos por los siglos. Ángeles del Señor, bendecid al Señor; cielos, bendecid al Señor. " + BR +
         " Aguas del espacio, bendecid al Señor; ejércitos del Señor, bendecid al Señor. Sol y luna, bendecid al Señor; astros del cielo, bendecid al Señor. " + BR +
         " Lluvia y rocío, bendecid al Señor; vientos todos, bendecid al Señor. Fuego y calor, bendecid al Señor; fríos y heladas, bendecid al Señor. " + BR +
         " Noche y día, bendecid al Señor; luz y tinieblas, bendecid al Señor. Bendiga la tierra al Señor, ensálcelo con himnos por los siglos. " + BR +
         " Montes y cumbres, bendecid al Señor; manantiales, mares y ríos, bendecid al Señor. Hijos de los hombres, bendecid al Señor; bendiga Israel al Señor. " + BR +
         " Sacerdotes del Señor, bendecid al Señor; siervos del Señor, bendecid al Señor. Almas y espíritus justos, bendecid al Señor; santos y humildes de corazón, bendecid al Señor. " + BR +
         " Bendigamos al Padre, al Hijo y al Espíritu Santo, ensalcémoslo con himnos por los siglos. Bendito el Señor en la bóveda del cielo, alabado y glorioso y ensalzado por los siglos.")
add("B", "El Señor amó a Andrés con singular predilección.")
ant("Dijo Andrés a su hermano Simón: «Hemos encontrado al Mesías»; y lo presentó a Jesús.")
add("A", "Salmo ciento cuarenta y nueve. Alegría de los santos. " + BR +
         " Cantad al Señor un cántico nuevo, resuene su alabanza en la asamblea de los fieles; que se alegre Israel por su Creador, los hijos de Sión por su Rey. " + BR +
         " Alabad su nombre con danzas, cantadle con tambores y cítaras; porque el Señor ama a su pueblo y adorna con la victoria a los humildes. " + BR +
         " Que los fieles festejen su gloria y canten jubilosos; la alabanza de Dios en su boca. Es un honor para todos sus fieles. " + BR + " " + GLORIA)
add("B", "Dijo Andrés a su hermano Simón: «Hemos encontrado al Mesías»; y lo presentó a Jesús.")
# LECTURA BREVE
add("A", "Lectura breve. De la carta del apóstol san Pablo a los Efesios. " + BR +
         " Ya no sois extranjeros ni forasteros, sino que sois ciudadanos del pueblo de Dios y miembros de la familia de Dios. Estáis edificados sobre el cimiento de los apóstoles y profetas, y el mismo Cristo Jesús es la piedra angular. " + BR +
         " Por él todo el edificio queda ensamblado, y se va levantando hasta formar un templo consagrado al Señor. Por él también vosotros os vais integrando en la construcción, para ser morada de Dios por el Espíritu.")
# RESPONSORIO BREVE
add("A", "Los nombrarás príncipes sobre toda la tierra.")
add("B", "Los nombrarás príncipes sobre toda la tierra.")
add("A", "Harán memorable tu nombre, Señor.")
add("B", "Sobre toda la tierra.")
# BENEDICTUS
ant("Salve, oh cruz preciosa, recibe al discípulo de aquel que en ti estuvo clavado, Cristo, mi maestro.")
add("A", library.BENEDICTUS)
add("B", "Salve, oh cruz preciosa, recibe al discípulo de aquel que en ti estuvo clavado, Cristo, mi maestro.")
# PRECES
add("A", "Demos gracias a nuestro Padre que está en los cielos, porque por medio de los apóstoles nos ha dado parte en la herencia de los elegidos, y aclamémosle diciendo:")
add("B", "El coro de los apóstoles te alaba, Señor.")
add("A", "Te alabamos, Señor, porque por medio de los apóstoles nos has dado la mesa de tu cuerpo y de tu sangre: en ella encontramos nuestra fuerza y nuestra vida.")
add("B", "El coro de los apóstoles te alaba, Señor.")
add("A", "Porque por medio de los apóstoles nos has preparado la mesa de tu palabra: por ella crecemos en el conocimiento de la verdad.")
add("B", "El coro de los apóstoles te alaba, Señor.")
add("A", "Porque por medio de los apóstoles has fundado tu Iglesia: por ella nos edificas en la unidad de tu pueblo.")
add("B", "El coro de los apóstoles te alaba, Señor.")
add("A", "Porque por medio de los apóstoles nos has dado el bautismo y la penitencia: por ellos nos purificas de todas nuestras culpas.")
add("B", "El coro de los apóstoles te alaba, Señor.")
add("C", "Ahora, en silencio, presenta al Señor tus propias intenciones.")
add("PAUSE", "9|Puedes pausar el vídeo para presentar tus intenciones")
# PADRENUESTRO (dos voces)
add("A", "Concluyamos nuestra oración con la plegaria que Jesús enseñó a los apóstoles: " + BR + " " + library.PADRENUESTRO_1)
add("B", library.PADRENUESTRO_2)
# ORACION
add("A", "Oremos. Dios todopoderoso y eterno, escucha la oración de tu pueblo y concédenos que, así como el apóstol san Andrés fue en la tierra predicador del Evangelio y pastor de tu Iglesia, así ahora en el cielo sea nuestro poderoso abogado ante ti. Por Jesucristo nuestro Señor. Amén.")
add("A", "El Señor nos bendiga, nos guarde de todo mal y nos lleve a la vida eterna.")
add("B", "Amén.")
add("C", "Gracias por rezar los Laudes con Tu Oración Diaria. Que san Andrés interceda por ti. Hasta luego; nos vemos en el Evangelio de hoy.")

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
    final = os.path.join(OUT, "laudes_lun30_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
