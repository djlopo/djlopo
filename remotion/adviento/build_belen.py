#!/usr/bin/env python3
"""Audio+subs+datos del reel del árbol. Tiempos directos por escena (sin remap):
cada escena = su línea de voz. Nivela, recorta silencio de cola, encadena con
0,35 s, construye subs globales y datos.json {V, scenes:[{a,b}], fin}."""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
VOCES = os.path.abspath(os.path.join(HERE, "..", "voces-belen"))
PUB = os.path.join(HERE, "public")
GAP = 0.35
TAIL = 2.2
V = 0.3
N = 9

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],
        capture_output=True, text=True).stdout.strip() or 0)

def chain():
    sil = os.path.join(VOCES, "_sil.mp3")
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",str(GAP),
        "-c:a","libmp3lame","-q:a","9", sil], capture_output=True)
    niv=[]; durs=[]
    for i in range(1, N+1):
        src=os.path.join(VOCES, f"voz-bel-{i:02d}.mp3"); dst=os.path.join(VOCES, f"_lvl-{i:02d}.mp3")
        af=("loudnorm=I=-16:TP=-1.5:LRA=11,"
            "areverse,silenceremove=start_periods=1:start_duration=0.06:start_threshold=-45dB,areverse")
        subprocess.run(["ffmpeg","-y","-i",src,"-af",af,"-ar","44100","-ac","1","-c:a","libmp3lame","-q:a","2",dst],capture_output=True)
        use=dst if os.path.exists(dst) and os.path.getsize(dst)>1000 else src
        niv.append(use); durs.append(dur(use))
    lst=os.path.join(VOCES,"_list.txt")
    with open(lst,"w") as f:
        for i in range(N):
            f.write(f"file '{niv[i]}'\n")
            if i<N-1: f.write(f"file '{sil}'\n")
    out=os.path.join(PUB,"voz-belen.mp3")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c:a","libmp3lame","-q:a","2",out],capture_output=True)
    offs=[]; o=0.0
    for i in range(N):
        offs.append(round(o,3)); o+=durs[i]+GAP
    return offs, durs, dur(out)

def subs(offs):
    trozos=[]; PUNT=".?!:;»"
    for i in range(1, N+1):
        words=json.load(open(os.path.join(VOCES, f"bel-{i:02d}-words.json")))
        o=offs[i-1]; chunk=[]
        for w in words:
            chunk.append({"t":w["t"],"a":round(o+w["a"],3),"b":round(o+w["b"],3)})
            if len(chunk)>=5 or (w["t"][-1:] in PUNT and len(chunk)>=3):
                trozos.append(chunk); chunk=[]
        if chunk: trozos.append(chunk)
    os.makedirs(os.path.join(HERE,"src","belen"),exist_ok=True)
    json.dump(trozos,open(os.path.join(HERE,"src","belen","subs.json"),"w"),ensure_ascii=False,indent=0)
    return trozos

def datos(offs,durs):
    scenes=[]
    for i in range(N):
        a=offs[i]; b=offs[i+1] if i<N-1 else offs[i]+durs[i]+TAIL
        scenes.append({"a":round(a,3),"b":round(b,3)})
    fin=round(V+scenes[-1]["b"]+0.2,3)
    json.dump({"V":V,"scenes":scenes,"fin":fin},open(os.path.join(HERE,"src","belen","datos.json"),"w"),ensure_ascii=False,indent=1)
    return scenes,fin

def music(fin):
    base=os.path.join(PUB,"adviento","musica_base.mp3")
    os.makedirs(os.path.join(PUB,"belen"),exist_ok=True)
    dst=os.path.join(PUB,"belen","musica.mp3")
    need=fin+1.0
    if dur(base)>=need:
        subprocess.run(["ffmpeg","-y","-i",base,"-t",str(need),"-c:a","libmp3lame","-q:a","3",dst],capture_output=True)
        return dur(dst)
    cur=base; tmp=[]; k=0
    while dur(cur)<need and k<8:
        k+=1; nxt=os.path.join(PUB,"belen",f"_m{k}.mp3")
        subprocess.run(["ffmpeg","-y","-i",cur,"-i",base,"-filter_complex","[0][1]acrossfade=d=3:c1=tri:c2=tri","-c:a","libmp3lame","-q:a","3",nxt],capture_output=True)
        cur=nxt; tmp.append(nxt)
    subprocess.run(["ffmpeg","-y","-i",cur,"-t",str(need),"-c:a","libmp3lame","-q:a","3",dst],capture_output=True)
    for t in tmp:
        try: os.remove(t)
        except OSError: pass
    return dur(dst)

if __name__ == "__main__":
    offs,durs,tot=chain()
    trozos=subs(offs); scenes,fin=datos(offs,durs); mlen=music(fin)
    print(f"voz: {tot:.2f}s · fin: {fin:.2f}s · musica: {mlen:.2f}s · subs: {len(trozos)} cajas")
    for i,s in enumerate(scenes,1):
        print(f"  esc {i}: {s['a']:.2f}–{s['b']:.2f} ({s['b']-s['a']:.2f}s)")
