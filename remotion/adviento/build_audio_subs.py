#!/usr/bin/env python3
"""Encadena las 9 voces (0,35 s de pausa), genera voz-adviento.mp3, subs
sincronizados (subs/adviento.json) y datos.json (remapeo de tiempos de escena).
Tambien extiende la musica para cubrir la duracion real."""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
VOCES = os.path.abspath(os.path.join(HERE, "..", "voces-adv"))
PUB = os.path.join(HERE, "public")
GAP = 0.35
TAIL = 2.0
V = 0.3

# ventanas de la referencia (en segundos de narracion, dominio x)
REF_START = [0, 3.7, 11.5, 21.45, 28.3, 33.25, 45.8, 49.85, 57.65]
REF_END   = [3.7, 11.5, 21.45, 28.3, 33.25, 45.8, 49.85, 57.65, 62.7]

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",p], capture_output=True, text=True).stdout.strip() or 0)

def chain_audio():
    """Nivela (-16 LUFS) y recorta el silencio de cola de cada linea, luego
    concatena con GAP de silencio. Devuelve offsets O_i, duracion total y las
    duraciones ya procesadas. loudnorm y el recorte de cola no mueven los
    tiempos de las palabras (estan dentro del habla), asi que los subs valen."""
    sil = os.path.join(VOCES, "_sil.mp3")
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i",f"anullsrc=r=44100:cl=mono","-t",str(GAP),
        "-c:a","libmp3lame","-q:a","9", sil], capture_output=True)
    niv = []; durs = []
    for i in range(1, 10):
        src = os.path.join(VOCES, f"voz-adv-{i:02d}.mp3")
        dst = os.path.join(VOCES, f"_lvl-{i:02d}.mp3")
        # nivelar + recortar SOLO el silencio de cola (areverse -> quitar inicio -> areverse)
        af = ("loudnorm=I=-16:TP=-1.5:LRA=11,"
              "areverse,silenceremove=start_periods=1:start_duration=0.06:start_threshold=-45dB,areverse")
        subprocess.run(["ffmpeg","-y","-i",src,"-af",af,
            "-ar","44100","-ac","1","-c:a","libmp3lame","-q:a","2", dst], capture_output=True)
        use = dst if os.path.exists(dst) and os.path.getsize(dst) > 1000 else src
        niv.append(use); durs.append(dur(use))
    lst = os.path.join(VOCES, "_list.txt")
    with open(lst, "w") as f:
        for i in range(9):
            f.write(f"file '{niv[i]}'\n")
            if i < 8:
                f.write(f"file '{sil}'\n")
    out = os.path.join(PUB, "voz-adviento.mp3")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c:a","libmp3lame","-q:a","2", out],
                   capture_output=True)
    offs = []
    o = 0.0
    for i in range(9):
        offs.append(round(o, 3))
        o += durs[i] + GAP
    return offs, dur(out), durs

def build_subs(offs):
    trozos = []
    PUNT = ".?!:;»"
    for i in range(1, 10):
        words = json.load(open(os.path.join(VOCES, f"adv-{i:02d}-words.json")))
        o = offs[i-1]
        chunk = []
        for w in words:
            g = {"t": w["t"], "a": round(o + w["a"], 3), "b": round(o + w["b"], 3)}
            chunk.append(g)
            fin_frase = w["t"][-1:] in PUNT
            if len(chunk) >= 5 or (fin_frase and len(chunk) >= 3):
                trozos.append(chunk); chunk = []
        if chunk:
            trozos.append(chunk)
    os.makedirs(os.path.join(HERE, "src", "subs"), exist_ok=True)
    json.dump(trozos, open(os.path.join(HERE, "src", "subs", "adviento.json"), "w"),
              ensure_ascii=False, indent=0)
    return trozos

def build_datos(offs, durs):
    scenes = []
    for i in range(9):
        ns = offs[i]
        ne = offs[i+1] if i < 8 else offs[8] + durs[8] + TAIL
        scenes.append({"rs": REF_START[i], "re": REF_END[i], "ns": round(ns,3), "ne": round(ne,3)})
    fin = round(V + scenes[-1]["ne"] + 0.2, 3)
    json.dump({"V": V, "scenes": scenes, "fin": fin},
              open(os.path.join(HERE, "src", "datos.json"), "w"), ensure_ascii=False, indent=1)
    return scenes, fin

def extend_music(fin):
    src = os.path.join(PUB, "adviento", "musica.mp3")
    bak = os.path.join(PUB, "adviento", "musica_base.mp3")
    if not os.path.exists(bak):
        subprocess.run(["cp", src, bak])
    base = dur(bak)
    need = fin + 1.0
    if base >= need:
        subprocess.run(["cp", bak, src]); return base
    # loop con crossfade de 3 s hasta cubrir 'need'
    xf = 3
    cur = bak
    tmps = []
    k = 0
    while dur(cur) < need:
        k += 1
        nxt = os.path.join(PUB, "adviento", f"_m{k}.mp3")
        subprocess.run(["ffmpeg","-y","-i",cur,"-i",bak,"-filter_complex",
            f"[0][1]acrossfade=d={xf}:c1=tri:c2=tri", "-c:a","libmp3lame","-q:a","3", nxt],
            capture_output=True)
        cur = nxt; tmps.append(nxt)
        if k > 6: break
    subprocess.run(["ffmpeg","-y","-i",cur,"-t",str(need),"-c:a","libmp3lame","-q:a","3", src], capture_output=True)
    for t in tmps:
        try: os.remove(t)
        except OSError: pass
    return dur(src)

if __name__ == "__main__":
    offs, total_voz, durs = chain_audio()
    trozos = build_subs(offs)
    scenes, fin = build_datos(offs, durs)
    mlen = extend_music(fin)
    print("offsets:", offs)
    print(f"voz encadenada: {total_voz:.2f}s · fin reel: {fin:.2f}s · musica: {mlen:.2f}s")
    print(f"subs: {len(trozos)} cajas, {sum(len(t) for t in trozos)} palabras")
    print("escenas (ref -> nuevo):")
    for i, s in enumerate(scenes, 1):
        print(f"  {i}: [{s['rs']:.1f},{s['re']:.1f}] -> [{s['ns']:.2f},{s['ne']:.2f}]  ({s['ne']-s['ns']:.2f}s)")
