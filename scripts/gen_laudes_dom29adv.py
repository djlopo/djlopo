#!/usr/bin/env python3
"""Laudes del I Domingo de Adviento (dom 29 nov 2026). Usa caché + biblioteca.

python3 -I gen_laudes_dom29adv.py <carpeta_salida>
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache, library  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
MODEL = "eleven_multilingual_v2"
BR = library.BR
GLORIA = library.GLORIA

VOICES = {
    "A": ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.82, "similarity_boost": 0.85, "style": 0.0,  "use_speaker_boost": True, "speed": 0.90}),
    "B": ("5gLTD5SjO7q6dFtEZlUY", {"stability": 0.88, "similarity_boost": 0.82, "style": 0.0,  "use_speaker_boost": True, "speed": 0.90}),
    "C": ("JngPf0lmRkKhY3qSJz0f", {"stability": 0.62, "similarity_boost": 0.85, "style": 0.22, "use_speaker_boost": True, "speed": 0.95}),
}

PS94 = ("Salmo noventa y cuatro. Invitación a la alabanza divina. " + BR +
        " Venid, aclamemos al Señor, demos vítores a la Roca que nos salva; entremos a su presencia dándole gracias, aclamándolo con cantos. " + BR +
        " Porque el Señor es un Dios grande, soberano de todos los dioses: tiene en su mano las simas de la tierra, son suyas las cumbres de los montes; suyo es el mar, porque él lo hizo, la tierra firme que modelaron sus manos. " + BR +
        " Venid, postrémonos por tierra, bendiciendo al Señor, creador nuestro. Porque él es nuestro Dios, y nosotros su pueblo, el rebaño que él guía. " + BR +
        " Ojalá escuchéis hoy su voz: No endurezcáis el corazón como en Meribá, como el día de Masá en el desierto; cuando vuestros padres me pusieron a prueba y dudaron de mí, aunque habían visto mis obras. " + BR +
        " Durante cuarenta años aquella generación me repugnó, y dije: Es un pueblo de corazón extraviado, que no reconoce mi camino; por eso he jurado en mi cólera que no entrarán en mi descanso. " + BR + " " + GLORIA)

HIMNO = ("Himno. Ven, Señor, no tardes. " + BR +
         " Ven, Señor, no tardes; ven, que te esperamos; ven, Señor, no tardes, ven pronto, Señor. " + BR +
         " El mundo muere de frío, el alma perdió el calor, los hombres no son hermanos porque han matado al Amor. " + BR +
         " Envuelto en noche sombría, gime el mundo de pavor; va en busca de una esperanza, buscando tu fe, Señor. " + BR +
         " Al mundo le falta vida y le falta corazón; le falta cielo en la tierra, si no lo riega tu amor. " + BR +
         " Rompa el cielo su silencio, baje el rocío a la flor; ven, Señor, no tardes tanto, ven, Señor. Amén.")

PS62 = ("Salmo sesenta y dos. El alma sedienta de Dios. " + BR +
        " Oh Dios, tú eres mi Dios, por ti madrugo, mi alma está sedienta de ti; mi carne tiene ansia de ti, como tierra reseca, agostada, sin agua. " + BR +
        " Cómo te contemplaba en el santuario, viendo tu fuerza y tu gloria. Tu gracia vale más que la vida, te alabarán mis labios. " + BR +
        " Toda mi vida te bendeciré y alzaré las manos invocándote. Me saciaré de manjares exquisitos, y mis labios te alabarán jubilosos. " + BR +
        " En el lecho me acuerdo de ti y velando medito en ti, porque fuiste mi auxilio, y a la sombra de tus alas canto con júbilo; mi alma está unida a ti, y tu diestra me sostiene. " + BR + " " + GLORIA)

DN3 = ("Cántico. Toda la creación alabe al Señor. " + BR +
       " Criaturas todas del Señor, bendecid al Señor, ensalzadlo con himnos por los siglos. " + BR +
       " Ángeles del Señor, bendecid al Señor; cielos, bendecid al Señor. Aguas del espacio, bendecid al Señor; ejércitos del Señor, bendecid al Señor. " + BR +
       " Sol y luna, bendecid al Señor; astros del cielo, bendecid al Señor. Lluvia y rocío, bendecid al Señor; vientos todos, bendecid al Señor. " + BR +
       " Fuego y calor, bendecid al Señor; fríos y heladas, bendecid al Señor. Rocíos y nevadas, bendecid al Señor; témpanos y hielos, bendecid al Señor. Escarchas y nieves, bendecid al Señor; noche y día, bendecid al Señor. Luz y tinieblas, bendecid al Señor; rayos y nubes, bendecid al Señor. " + BR +
       " Bendiga la tierra al Señor, ensálcelo con himnos por los siglos. Montes y cumbres, bendecid al Señor; cuanto germina en la tierra, bendiga al Señor. Manantiales, bendecid al Señor; mares y ríos, bendecid al Señor. Cetáceos y peces, bendecid al Señor; aves del cielo, bendecid al Señor. Fieras y ganados, bendecid al Señor, ensalzadlo con himnos por los siglos. " + BR +
       " Hijos de los hombres, bendecid al Señor; bendiga Israel al Señor. Sacerdotes del Señor, bendecid al Señor; siervos del Señor, bendecid al Señor. Almas y espíritus justos, bendecid al Señor; santos y humildes de corazón, bendecid al Señor. Ananías, Azarías y Misael, bendecid al Señor, ensalzadlo con himnos por los siglos. " + BR +
       " Bendigamos al Padre, al Hijo y al Espíritu Santo, ensalcémoslo con himnos por los siglos. Bendito el Señor en la bóveda del cielo, alabado y glorioso y ensalzado por los siglos.")

PS149 = ("Salmo ciento cuarenta y nueve. Alegría de los santos. " + BR +
         " Cantad al Señor un cántico nuevo, resuene su alabanza en la asamblea de los fieles; que se alegre Israel por su Creador, los hijos de Sión por su Rey. " + BR +
         " Alabad su nombre con danzas, cantadle con tambores y cítaras; porque el Señor ama a su pueblo y adorna con la victoria a los humildes. " + BR +
         " Que los fieles festejen su gloria y canten jubilosos en filas: con vítores a Dios en la boca y espadas de dos filos en las manos; para tomar venganza de los pueblos y aplicar el castigo a las naciones, sujetando a los reyes con argollas, a los nobles con esposas de hierro. " + BR +
         " Ejecutar la sentencia dictada es un honor para todos sus fieles. " + BR + " " + GLORIA)

LECTURA = ("Lectura breve. De la carta del apóstol san Pablo a los Romanos. " + BR +
           " Ya es hora de que despertéis del sueño, pues la salvación está ahora más cerca que cuando abrazamos la fe. La noche va pasando, el día está encima; desnudémonos, pues, de las obras de las tinieblas y vistámonos de las armas de la luz.")

ANT_BEN = "El Espíritu Santo descenderá sobre ti, María; no temas, concebirás en tu seno al Hijo de Dios. Aleluya."
REFR = "Muéstranos, Señor, tu misericordia."

seg = []
def add(role, text): seg.append((role, text))
def ant(label, text):
    add("A", f"{label} {text}")
    add("B", text)

add("C", "Bienvenido a Tu Oración Diaria. Hoy, domingo 29 de noviembre, Primer Domingo de Adviento, comenzamos el tiempo de espera del Señor. Rezamos juntos los Laudes. " + BR + " Antes de empezar, deja en los comentarios por quién rezas hoy.")
add("A", "Señor, abre mis labios.")
add("B", "Y mi boca proclamará tu alabanza.")
ant("Antífona.", "Al Rey que viene, al Señor que se acerca, venid, adorémosle.")
add("A", PS94)
add("B", "Al Rey que viene, al Señor que se acerca, venid, adorémosle.")
add("A", HIMNO)
ant("Antífona primera.", "Aquel día los montes destilarán dulzura y las colinas manarán leche y miel. Aleluya.")
add("A", PS62)
add("B", "Aquel día los montes destilarán dulzura y las colinas manarán leche y miel. Aleluya.")
ant("Antífona segunda.", "Los montes y las colinas aclamarán en presencia del Señor, y los árboles del bosque aplaudirán, porque viene el Señor y reinará eternamente. Aleluya.")
add("A", DN3)
add("B", "Los montes y las colinas aclamarán en presencia del Señor, y los árboles del bosque aplaudirán, porque viene el Señor y reinará eternamente. Aleluya.")
ant("Antífona tercera.", "Vendrá el gran profeta y renovará Jerusalén. Aleluya.")
add("A", PS149)
add("B", "Vendrá el gran profeta y renovará Jerusalén. Aleluya.")
add("A", LECTURA)
add("A", "Cristo, Hijo de Dios vivo, ten piedad de nosotros.")
add("B", "Cristo, Hijo de Dios vivo, ten piedad de nosotros.")
add("A", "Tú que has de venir al mundo.")
add("B", "Ten piedad de nosotros.")
ant("Antífona.", ANT_BEN)
add("A", library.BENEDICTUS)
add("B", ANT_BEN)
# PRECES
add("A", "Hacemos las preces. Oremos a Dios Padre, que nos concede la gracia de esperar la revelación de nuestro Señor Jesucristo, y digámosle confiados:")
add("B", REFR)
add("A", "Santifica, Señor, todo nuestro ser, alma y cuerpo, y guárdanos libres de culpa hasta el día de la venida de tu Hijo.")
add("B", REFR)
add("A", "Haz que durante este día caminemos en santidad y llevemos una vida justa y religiosa.")
add("B", REFR)
add("A", "Haz que nos revistamos de nuestro Señor Jesucristo y que nos llenemos del Espíritu Santo.")
add("B", REFR)
add("A", "Concédenos, Señor, que vivamos siempre preparados para el día de la manifestación gloriosa de tu Hijo.")
add("B", REFR)
add("C", "Ahora, en silencio, presenta al Señor tus propias intenciones. Él te escucha, y nada de lo tuyo le es indiferente. " + BR + " Puedes pausar el vídeo el tiempo que necesites y, si quieres, déjalas también en los comentarios.")
add("PAUSE", "9|Puedes pausar el vídeo para presentar tus intenciones")
add("A", "Como nos enseñó el Salvador, nos atrevemos a decir: " + BR + " " + library.PADRENUESTRO)
add("A", "Oremos. Señor, despierta en tus fieles el deseo de prepararse a la venida de Cristo por la práctica de las buenas obras, para que, colocados un día a su derecha, merezcan poseer el reino celestial. Por nuestro Señor Jesucristo, tu Hijo, que vive y reina contigo en la unidad del Espíritu Santo y es Dios, por los siglos de los siglos. Amén.")
add("A", "El Señor nos bendiga, nos guarde de todo mal y nos lleve a la vida eterna.")
add("B", "Amén.")
add("C", "Gracias por rezar con Tu Oración Diaria. Comienza bien este Primer Domingo de Adviento. Si esta oración te ayuda, suscríbete y compártela, y vuelve mañana. Que el Señor que viene te bendiga.")

SEG = seg
SILENCE = 0.45

def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(secs), "-q:a", "9", path], capture_output=True)

def tts(role, text, path):
    vid, settings = VOICES[role]
    return tts_cache.get_or_generate(vid, settings, text, path, MODEL)

def main():
    sil = os.path.join(OUT, "sil.mp3"); silence(sil, SILENCE)
    mp3s, ok, reused = [], 0, 0
    for i, (role, text) in enumerate(SEG):
        p = os.path.join(OUT, f"seg_{i:03d}_{role}.mp3")
        if role == "PAUSE":
            silence(p, float(text.split("|", 1)[0])); mp3s.append(p); ok += 1
            tag = "PAUSE"
        else:
            r = tts(role, text, p)
            if r is None:
                print(f"  [{i+1}/{len(SEG)}] {role} ERROR");
            else:
                ok += 1; mp3s.append(p); reused += (r == "cache")
                tag = f"{role} ({r})"
            if r is None:
                if i < len(SEG) - 1: mp3s.append(sil)
                continue
        print(f"  [{i+1}/{len(SEG)}] {tag}")
        if i < len(SEG) - 1:
            mp3s.append(sil)
    listf = os.path.join(OUT, "concat.txt")
    with open(listf, "w") as f:
        for m in mp3s:
            f.write(f"file '{os.path.abspath(m)}'\n")
    final = os.path.join(OUT, "laudes_dom29_final.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "4", final], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", final], capture_output=True, text=True).stdout.strip()
    print(f"\nOK {ok}/{len(SEG)} (reutilizados de caché: {reused})  FINAL {final}  {dur}s")

if __name__ == "__main__":
    main()
