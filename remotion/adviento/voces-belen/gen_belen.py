#!/usr/bin/env python3
"""Voces del reel «El belén: qué significa cada figura».
Carlota (impares) / Javi Rojas (pares). Tono cálido con chispa."""
import json, base64, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
CARLOTA = "ODQQw99uvxi7piSglbBJ"
JAVI = "aYbngTsp5kp0sibI3Z0T"
S_C = {"stability": 0.42, "similarity_boost": 0.85, "style": 0.32, "use_speaker_boost": True, "speed": 1.0}
S_J = {"stability": 0.4,  "similarity_boost": 0.85, "style": 0.3,  "use_speaker_boost": True, "speed": 1.05}

LINEAS = [
 (CARLOTA, "¿Sabes qué significa cada figura del belén? No es solo un adorno: es el Evangelio hecho barro."),
 (JAVI,    "Lo inventó San Francisco de Asís, en Greccio, hace ochocientos años. Quiso ver con sus ojos la pobreza de Belén."),
 (CARLOTA, "En el centro, el portal: una cueva, un establo. Porque Dios no nace en un palacio, sino entre los pobres."),
 (JAVI,    "La Virgen María y San José velan la cuna. Y al Niño se le coloca en Nochebuena: es Dios con nosotros."),
 (CARLOTA, "La mula y el buey no salen en los evangelios. Los puso la tradición, leyendo a Isaías: «el buey conoce a su dueño». Ellos sí lo reconocen."),
 (JAVI,    "Un ángel anuncia la noticia, y los pastores son los primeros en adorar. ¡Los sencillos, los primeros!"),
 (CARLOTA, "Una estrella guía a los Reyes Magos, que llegan el seis de enero con oro, incienso y mirra."),
 (JAVI,    "Y alrededor, el río, el molino, las casas… la vida de cada día, donde Dios quiere nacer."),
 (CARLOTA, "Así que este año, monta el belén con los tuyos y coloca al Niño en Nochebuena. Reza con nosotros esta Navidad, en Tu Oración Diaria. Guárdalo."),
]

def words(al):
    ch=al["characters"];st=al["character_start_times_seconds"];et=al["character_end_times_seconds"]
    out=[];cur="";a=None;b=None
    for c,s,e in zip(ch,st,et):
        if c.isspace():
            if cur: out.append({"t":cur,"a":round(a,3),"b":round(b,3)});cur="";a=None
            continue
        if not cur: a=s
        cur+=c;b=e
    if cur: out.append({"t":cur,"a":round(a,3),"b":round(b,3)})
    return out
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip() or 0)

if __name__ == "__main__":
    man=[]
    for i,(v,t) in enumerate(LINEAS,1):
        who="Carlota" if v==CARLOTA else "Javi"; SET=S_C if v==CARLOTA else S_J
        payload=json.dumps({"text":t,"model_id":"eleven_multilingual_v2","voice_settings":SET})
        resp=f"_b{i}.json"
        code=subprocess.run(["curl","-sS","-o",resp,"-w","%{http_code}","-X","POST",
            f"https://api.elevenlabs.io/v1/text-to-speech/{v}/with-timestamps?output_format=mp3_44100_128",
            "-H","Content-Type: application/json","-d",payload],capture_output=True,text=True).stdout.strip()
        if code!="200":
            print("FALLO",i,code,open(resp).read()[:200]); break
        d=json.load(open(resp))
        open(f"voz-bel-{i:02d}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
        json.dump(words(d["alignment"]),open(f"bel-{i:02d}-words.json","w"),ensure_ascii=False)
        os.remove(resp); dd=dur(f"voz-bel-{i:02d}.mp3")
        man.append({"i":i,"who":who,"dur":round(dd,2),"text":t}); print(f"  voz-bel-{i:02d} [{who}] {dd:.2f}s")
    json.dump(man,open("manifest.json","w"),ensure_ascii=False,indent=1)
    print("TOTAL voz:", round(sum(m['dur'] for m in man),1),"s")
