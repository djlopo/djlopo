#!/usr/bin/env python3
"""Reconstruye las 9 voces con el GUION ORIGINAL del usuario:
 - Carlota (impares): se reutiliza su audio original + su alineacion.
 - Hombre (pares): se regenera con Javi Rojas usando el texto original;
   la linea 04 incluye los frutos rojos (simbologia del Eden corregida).
Guarda voz-adv-0X.mp3 + adv-0X-words.json (formato {t,a,b})."""
import json, base64, subprocess, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = "/tmp/claude-0/-home-user-djlopo/1cc18098-18ee-502f-ac16-c6dca5124e55/scratchpad/paquete_adv_ref/contenido/adviento"
JR = "aYbngTsp5kp0sibI3Z0T"  # Javi Rojas (SyncState)
SET = {"stability": 0.4, "similarity_boost": 0.85, "style": 0.25, "use_speaker_boost": True, "speed": 1.08}

# Texto original del hombre (pares); 04 con frutos rojos (Eden) añadido.
HOMBRE = {
 2: 'La corona de Adviento cuenta los cuatro domingos que faltan para Navidad. Adviento significa "venida": es tiempo de esperar.',
 4: 'El círculo no tiene principio ni fin, como el amor de Dios. Y el verde de las ramas es vida y esperanza. Y los frutos rojos recuerdan el Edén: el pecado, y la promesa del Salvador.',
 6: 'Primer domingo: la esperanza. Segundo: la paz, y vuelves a encender la primera. Tercero, la rosa: la alegría, porque ya queda poco. Y el cuarto: el amor. Las cuatro juntas.',
 8: 'Para hacerla necesitas un aro, ramas de abeto, unas piñas y cuatro velas. Y nunca la dejes encendida sin nadie delante.',
}

def chars_to_words(chars, start, end):
    """Palabras {t,a,b}, saltando etiquetas entre corchetes [ ... ]."""
    out = []; cur = ""; a = None; b = None; in_tag = False
    for c, s, e in zip(chars, start, end):
        if c == "[":
            in_tag = True; continue
        if c == "]":
            in_tag = False; continue
        if in_tag:
            continue
        if c.isspace():
            if cur:
                out.append({"t": cur, "a": round(a, 3), "b": round(b, 3)}); cur = ""; a = None
            continue
        if not cur:
            a = s
        cur += c; b = e
    if cur:
        out.append({"t": cur, "a": round(a, 3), "b": round(b, 3)})
    return out

def gen_javi(idx, text):
    payload = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": SET})
    resp = f"_jr{idx}.json"
    code = subprocess.run(["curl","-sS","-o",resp,"-w","%{http_code}","-X","POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{JR}/with-timestamps?output_format=mp3_44100_128",
        "-H","Content-Type: application/json","-d",payload], capture_output=True, text=True).stdout.strip()
    if code != "200":
        print("  FALLO", idx, code, open(resp).read()[:200]); return
    d = json.load(open(resp))
    open(os.path.join(HERE, f"voz-adv-{idx:02d}.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    al = d["alignment"]
    w = chars_to_words(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"])
    json.dump(w, open(os.path.join(HERE, f"adv-{idx:02d}-words.json"), "w"), ensure_ascii=False)
    os.remove(resp)
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",
        os.path.join(HERE, f"voz-adv-{idx:02d}.mp3")], capture_output=True, text=True).stdout.strip() or 0)
    print(f"  voz-adv-{idx:02d} [Javi Rojas] {dur:.2f}s ({len(w)}p)")

if __name__ == "__main__":
    # Carlota: reutilizar audio + alineacion originales
    for idx in (1, 3, 5, 7, 9):
        subprocess.run(["cp", f"{PKG}/public/voz-adv-{idx:02d}.mp3", os.path.join(HERE, f"voz-adv-{idx:02d}.mp3")])
        al = json.load(open(f"{PKG}/voz/adv-{idx:02d}-alineacion.json"))
        w = chars_to_words(al["chars"], al["start"], al["end"])
        json.dump(w, open(os.path.join(HERE, f"adv-{idx:02d}-words.json"), "w"), ensure_ascii=False)
        dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",
            os.path.join(HERE, f"voz-adv-{idx:02d}.mp3")], capture_output=True, text=True).stdout.strip() or 0)
        print(f"  voz-adv-{idx:02d} [Carlota orig] {dur:.2f}s ({len(w)}p)")
    # Hombre: Javi Rojas
    for idx, text in HOMBRE.items():
        gen_javi(idx, text)
