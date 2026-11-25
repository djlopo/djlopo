#!/usr/bin/env python3
"""Especial del Santo — SAN ANDRÉS. Genera la narración por secciones (voz N narrador +
voz V para las citas), mide duraciones y escribe timings.json para Remotion.
Uso: python3 -I gen_especial_sanandres.py <carpeta_salida>
"""
import os, json, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_cache  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
AUDIO = os.path.join(OUT, "audio"); os.makedirs(AUDIO, exist_ok=True)
MODEL = "eleven_multilingual_v2"

# N = narrador (cálido, speed 1.0) · V = citas (Jesús / Bautista / el santo)
N = ("Syqs6p4s6hxhfAyhhlbS", {"stability": 0.42, "similarity_boost": 0.8, "style": 0.26, "use_speaker_boost": True, "speed": 1.0})
V = ("5IDdqnXnlsZ1FCxoOFYg", {"stability": 0.5, "similarity_boost": 0.85, "style": 0.12, "use_speaker_boost": True, "speed": 0.95})

# Secciones: (id, imagen, [(voz, texto), ...])
SECTIONS = [
 ("gancho", "19.jpg", [
   (N, "Entre los Doce, hubo uno al que Jesús llamó el primero. No era el más sabio, ni el más fuerte, ni el más preparado: era un pescador de Galilea. ¿Por qué a él? Hermano, quédate con esa pregunta, porque en ella se esconde el Evangelio entero.")]),
 ("quienfue", "18.jpg", [
   (N, "Se llamaba Andrés. Y su nombre ya dice mucho: viene del griego, Andréas, de anér, que significa «el varón, el valiente». Fíjate: un nombre griego, no hebreo. Porque Andrés era de Betsaida, un pueblo de pescadores a orillas del lago de Galilea, una tierra abierta al mundo griego; y ese pequeño detalle marcará toda su vida. Betsaida, además, significa en hebreo «casa de la pesca»: el que nació en la casa de la pesca sería hecho, un día, pescador de hombres. Era hijo de Jonás y hermano de Simón, a quien el mundo conocería como Pedro.")]),
 ("encuentro", "17.jpg", [
   (N, "Andrés era un buscador; no se conformaba, y por eso lo encontramos junto a Juan el Bautista, esperando al que había de venir. Y un día el Bautista ve pasar a Jesús y exclama:"),
   (V, "He ahí el Cordero de Dios."),
   (N, "Aquellas palabras le encienden el corazón. Andrés deja a su maestro y se va detrás de Jesús. El Señor se vuelve y le pregunta:"),
   (V, "¿Qué buscáis?"),
   (N, "Y ellos, sin saber qué decir, balbucean: Maestro, ¿dónde vives? Jesús responde:"),
   (V, "Venid y lo veréis."),
   (N, "Y se quedaron con Él aquella tarde. Andrés nunca olvidaría el día ni la hora: era, dice el Evangelio, como las cuatro de la tarde. Porque hay encuentros que parten la vida en dos. Allí descubrió que aquel hombre era el Mesías, en hebreo el Ungido, el tesoro que Dios regalaba al mundo; y que Cristo no cabe en un solo corazón: un gozo así no se puede guardar.")]),
 ("respuesta", "16.jpg", [
   (N, "Por eso lo primero que hace Andrés es correr a buscar a su hermano. Lo encuentra y le dice las palabras más hermosas que un hombre puede decir a otro:"),
   (V, "Hemos encontrado al Mesías."),
   (N, "Y lo lleva a Jesús. Si Andrés no hubiera ido a buscar a Pedro, el primer Papa no habría conocido al Señor. San Juan Crisóstomo dice que Andrés no sabía explicar bien quién era Jesús, así que hizo lo único que importaba: lo llevó a la misma fuente de la luz. Esa será su vida entera: ser puente, acercar a otros a Cristo.")]),
 ("llamada", "15.jpg", [
   (N, "Y un día, junto al lago, llega la llamada definitiva:"),
   (V, "Venid y seguidme, y os haré pescadores de hombres."),
   (N, "Y dice el Evangelio que, al instante, dejaron las redes y lo siguieron. Al instante. A Jesús no se le dice «luego».")]),
 ("cruz", "14.jpg", [
   (N, "Pasados los años, después de Pentecostés, Andrés llevó el Evangelio lejos: a Grecia, a Asia Menor, hasta las costas del Mar Negro. Y en Patras lo esperaba el culmen de su vida. Condenado a muerte, pidió una cruz distinta a la de Jesús, una cruz en aspa, en forma de equis, porque no se creía digno de morir igual que su Señor. Y al verla, no tembló: la saludó con amor:"),
   (V, "¡Salve, oh cruz, tú que recibiste la belleza de los miembros del Señor! Recíbeme en tus brazos y llévame a mi Maestro."),
   (N, "No veía un instrumento de tortura, sino el camino para parecerse al Redentor. Porque Jesús lo había dicho: si el grano de trigo no cae en tierra y muere, queda él solo; pero si muere, da mucho fruto. Andrés fue ese grano de trigo, y su sangre dio una cosecha inmensa.")]),
 ("hoy", "15.jpg", [
   (N, "Por eso la Iglesia de Oriente lo llama el Protóclito: el primero llamado. Y aquí está la buena noticia, hermano: Dios no eligió a Andrés porque fuera bueno; lo eligió primero, por pura gracia. Lo mismo hace contigo: a ti también te ha mirado primero; cuando todavía eras pecador, Cristo pasó a tu lado y te llamó. Su vida nos desarma una excusa muy nuestra: el respeto humano, ese miedo al qué dirán que nos hace esconder la fe. Andrés no callaba: lo primero que hacía con cada persona era llevarla al Señor. ¿A quién vas a acercar tú, hoy, a Jesús? Quizá, como Andrés con Pedro, a alguien de tu propia casa.")]),
 ("mision", "MAP", [
   (N, "Andrés, apóstol del mundo griego, y Pedro, en Roma: dos hermanos, los dos pulmones con que respira la Iglesia. Su nombre se pronuncia aún en el corazón de la Misa; es patrono de los pescadores, de Grecia, de Rusia y de Escocia, cuya bandera lleva todavía su cruz en aspa. Y su fiesta, cada treinta de noviembre, abre las puertas del Adviento: el primer llamado nos pone en camino hacia el que viene.")]),
 ("cierre", "19.jpg", [
   (N, "San Andrés, apóstol, el primero en seguir al Señor y el primero en llevarle a su hermano: alcánzanos un corazón como el tuyo, que se encuentre con Cristo y no sepa callarlo; que, venciendo todo miedo, seamos también nosotros puentes que acerquen a los demás a Jesús. Amén."),
   (N, "Has rezado con Tu Oración Diaria. Si te ha ayudado, suscríbete y guárdalo en nuestra lista «Vidas de Santos». Que san Andrés interceda por ti; hasta el próximo santo.")]),
]

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except: return 0.0

def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(secs), "-q:a", "9", path], capture_output=True)

def main():
    gap = os.path.join(OUT, "gap.mp3"); silence(gap, 0.45)
    gapV = os.path.join(OUT, "gapv.mp3"); silence(gapV, 0.30)
    timings = []
    for si, (sid, img, lines) in enumerate(SECTIONS):
        parts = []
        for li, (voice, text) in enumerate(lines):
            p = os.path.join(OUT, f"s{si:02d}_{sid}_{li:02d}.mp3")
            r = tts_cache.get_or_generate(voice[0], voice[1], text, p, MODEL)
            if r is None:
                print(f"  ERROR {sid} línea {li}"); return
            parts.append(p)
            # pausa: corta tras una cita (V), normal entre párrafos
            parts.append(gapV if voice is V else gap)
        if parts and parts[-1] in (gap, gapV): parts.pop()
        listf = os.path.join(OUT, f"concat_{sid}.txt")
        with open(listf, "w") as f:
            for m in parts: f.write(f"file '{os.path.abspath(m)}'\n")
        secmp3 = os.path.join(AUDIO, f"{si:02d}_{sid}.mp3")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c:a", "libmp3lame", "-q:a", "3", secmp3], capture_output=True)
        d = dur(secmp3)
        timings.append({"id": sid, "img": img, "audio": f"audio/{si:02d}_{sid}.mp3", "dur": round(d, 2)})
        print(f"  [{si+1}/{len(SECTIONS)}] {sid}: {d:.1f}s ({r})")
    json.dump({"fps": 30, "sections": timings}, open(os.path.join(OUT, "timings.json"), "w"), ensure_ascii=False, indent=1)
    total = sum(s["dur"] for s in timings)
    print(f"\nOK  total narración ~{total:.0f}s ({total/60:.1f} min)  -> {OUT}/timings.json")

if __name__ == "__main__":
    main()
