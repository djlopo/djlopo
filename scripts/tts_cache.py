#!/usr/bin/env python3
"""Caché de audio TTS: 'memoria de salmos'.

Cada fragmento se identifica por sha1(voz + ajustes + texto). Antes de pedir audio
a ElevenLabs, se mira la caché: si existe, se reutiliza; si no, se genera, se
normaliza (loudnorm) y se guarda. Así los salmos, oraciones, respuestas y lecturas
que ya se dijeron NO se vuelven a generar (ahorro de créditos y tokens).

Ubicación durable (en el repo, versionado):
  audio_cache/<clave>.mp3   -> el audio cacheado
  audio_cache/index.json    -> registro legible {clave: voz, texto (recorte), fecha}
"""
import hashlib, json, os, shutil, subprocess, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(REPO, "audio_cache")
INDEX = os.path.join(CACHE_DIR, "index.json")
MODEL_DEFAULT = "eleven_multilingual_v2"


def cache_key(voice_id, settings, text):
    raw = voice_id + "|" + json.dumps(settings, sort_keys=True, ensure_ascii=False) + "|" + text
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def _loudnorm(path):
    tmp = path + ".n.mp3"
    r = subprocess.run(["ffmpeg", "-y", "-i", path, "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", tmp], capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 800:
        os.replace(tmp, path)


def _index_add(key, voice_id, text):
    try:
        data = json.load(open(INDEX)) if os.path.exists(INDEX) else {}
    except Exception:
        data = {}
    data[key] = {"voice": voice_id, "text": text[:90], "chars": len(text),
                 "date": time.strftime("%Y-%m-%d")}
    json.dump(data, open(INDEX, "w"), ensure_ascii=False, indent=1)


def get_or_generate(voice_id, settings, text, out_path, model=MODEL_DEFAULT):
    """Devuelve 'cache' si se reutilizó, 'new' si se generó, None si falló.
    Deja el audio final en out_path."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = cache_key(voice_id, settings, text)
    cpath = os.path.join(CACHE_DIR, key + ".mp3")
    if os.path.exists(cpath) and os.path.getsize(cpath) > 1500:
        shutil.copy(cpath, out_path)
        return "cache"
    payload = json.dumps({"text": text, "model_id": model, "voice_settings": settings})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    r = subprocess.run(["curl", "-sS", "-X", "POST", url, "-H", "Content-Type: application/json",
                        "-d", payload, "-o", out_path, "-w", "%{http_code}"], capture_output=True, text=True)
    if r.stdout.strip() != "200" or (os.path.getsize(out_path) if os.path.exists(out_path) else 0) < 1500:
        return None
    _loudnorm(out_path)
    shutil.copy(out_path, cpath)
    _index_add(key, voice_id, text)
    return "new"


def stats():
    n = len([f for f in os.listdir(CACHE_DIR) if f.endswith(".mp3")]) if os.path.isdir(CACHE_DIR) else 0
    return {"cached_segments": n, "dir": CACHE_DIR}
