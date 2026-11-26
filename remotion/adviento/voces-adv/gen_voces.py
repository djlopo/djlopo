#!/usr/bin/env python3
"""Genera las 9 voces del reel de Adviento con ElevenLabs (con marcas de tiempo).
Carlota (impares) / Adolfo Banderas (pares). Guarda mp3 + palabras alineadas."""
import json, base64, subprocess, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CARLOTA = "ODQQw99uvxi7piSglbBJ"
ADOLFO = "IL7GIOA2FIurcXETHVY7"
SET = {"stability": 0.5, "similarity_boost": 0.85, "style": 0.18, "use_speaker_boost": True, "speed": 0.98}

LINEAS = [
    (CARLOTA, "Este domingo se enciende la primera vela del Adviento. ¿Sabes por qué?"),
    (ADOLFO,  "La corona de Adviento. Del latín «adventus»: venida. Es tiempo de esperar."),
    (CARLOTA, "Hamburgo, 1839. El pastor Wichern puso una vela por cada día hasta la Navidad."),
    (ADOLFO,  "Un círculo sin fin, como el amor de Dios. El verde es vida y esperanza; y las bayas rojas, la sangre de Cristo."),
    (CARLOTA, "Cuatro velas: tres moradas y una rosa. Una por cada domingo."),
    (ADOLFO,  "Cada domingo enciendes una más: esperanza, paz, alegría y amor. Y vuelves a encender las anteriores."),
    (CARLOTA, "Y en el centro, una vela blanca, para la noche de Navidad."),
    (ADOLFO,  "¿Quieres hacerla? Un aro, ramas de abeto, piñas y cuatro velas. Nunca la dejes encendida sola."),
    (CARLOTA, "Este domingo, enciende la primera. Reza con nosotros este Adviento."),
]

def palabras_desde_chars(al):
    ch = al["characters"]; st = al["character_start_times_seconds"]; et = al["character_end_times_seconds"]
    words = []
    cur = ""; a = None; b = None
    for c, s, e in zip(ch, st, et):
        if c.isspace():
            if cur:
                words.append({"t": cur, "a": round(a, 3), "b": round(b, 3)}); cur = ""; a = None
            continue
        if not cur:
            a = s
        cur += c; b = e
    if cur:
        words.append({"t": cur, "a": round(a, 3), "b": round(b, 3)})
    return words

def gen(voice, text, idx):
    payload = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": SET})
    resp = os.path.join(HERE, f"_resp_{idx:02d}.json")
    for intento in range(3):
        code = subprocess.run(["curl", "-sS", "-o", resp, "-w", "%{http_code}", "-X", "POST",
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
            "-H", "Content-Type: application/json", "-d", payload], capture_output=True, text=True).stdout.strip()
        if code == "200":
            break
        print(f"  intento {intento+1} HTTP {code}; reintento"); time.sleep(2)
    else:
        print("  FALLO linea", idx); return None
    d = json.load(open(resp))
    mp3 = os.path.join(HERE, f"voz-adv-{idx:02d}.mp3")
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    words = palabras_desde_chars(d["alignment"])
    json.dump(words, open(os.path.join(HERE, f"adv-{idx:02d}-words.json"), "w"), ensure_ascii=False)
    os.remove(resp)
    return words

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],
                                capture_output=True, text=True).stdout.strip() or 0)

if __name__ == "__main__":
    manifest = []
    total_chars = 0
    for i, (v, t) in enumerate(LINEAS, 1):
        who = "Carlota" if v == CARLOTA else "Adolfo"
        w = gen(v, t, i)
        if w is None: sys.exit(1)
        mp3 = os.path.join(HERE, f"voz-adv-{i:02d}.mp3")
        d = dur(mp3)
        total_chars += len(t)
        manifest.append({"i": i, "who": who, "dur": round(d, 3), "nwords": len(w), "text": t})
        print(f"  voz-adv-{i:02d} [{who}] {d:.2f}s {len(w)}p  «{t[:40]}...»")
    json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    print(f"\nTOTAL: {sum(m['dur'] for m in manifest):.1f}s de voz · {total_chars} caracteres (creditos EL)")
