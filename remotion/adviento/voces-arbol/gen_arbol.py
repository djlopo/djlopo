#!/usr/bin/env python3
"""Voces del reel «El árbol de Navidad, ¿es cristiano?».
Carlota (impares) / Javi Rojas (pares). Tono un pelín más entusiasta
(style algo más alto + alguna exclamación), sin etiquetas literales."""
import json, base64, subprocess, os

HERE = os.path.dirname(os.path.abspath(__file__))
CARLOTA = "ODQQw99uvxi7piSglbBJ"
JAVI = "aYbngTsp5kp0sibI3Z0T"
# un poco más de style para entusiasmo contenido
S_CARLOTA = {"stability": 0.42, "similarity_boost": 0.85, "style": 0.32, "use_speaker_boost": True, "speed": 1.0}
S_JAVI    = {"stability": 0.4,  "similarity_boost": 0.85, "style": 0.3,  "use_speaker_boost": True, "speed": 1.05}

LINEAS = [
 (CARLOTA, "El árbol de Navidad… ¿es cristiano? Mucha gente cree que es pagano. ¡Pero espera, que su historia es preciosa!"),
 (JAVI,    "Todo empieza en la Edad Media, con los autos de Navidad. El veinticuatro de diciembre, la Iglesia recuerda a Adán y Eva."),
 (CARLOTA, "Y para contarlo montaban un abeto: el árbol del Paraíso. Lo adornaban con manzanas rojas, el fruto del Edén."),
 (JAVI,    "Pero también colgaban hostias, signo de Cristo que nos redime. Del pecado… a la promesa cumplida."),
 (CARLOTA, "Y cuenta la tradición que San Bonifacio taló un roble pagano, y en su lugar creció un abeto. «¡Así es Cristo!», dijo: el árbol de la vida."),
 (JAVI,    "Por eso es de hoja perenne: siempre verde, como la vida eterna que Dios nos regala."),
 (CARLOTA, "Y sus luces no son un simple adorno: recuerdan a Cristo, la luz del mundo. Y la estrella de la cima, ¡la que guió hasta Belén!"),
 (JAVI,    "¿Que es pagano? El mismísimo Vaticano levanta su árbol en la plaza de San Pedro cada Navidad."),
 (CARLOTA, "Así que este año, al encender tu árbol, míralo con otros ojos: es un signo de Cristo. Móntalo con los tuyos y reza con nosotros esta Navidad, en Tu Oración Diaria. Guárdalo."),
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
        who="Carlota" if v==CARLOTA else "Javi"
        SET=S_CARLOTA if v==CARLOTA else S_JAVI
        payload=json.dumps({"text":t,"model_id":"eleven_multilingual_v2","voice_settings":SET})
        resp=f"_a{i}.json"
        code=subprocess.run(["curl","-sS","-o",resp,"-w","%{http_code}","-X","POST",
            f"https://api.elevenlabs.io/v1/text-to-speech/{v}/with-timestamps?output_format=mp3_44100_128",
            "-H","Content-Type: application/json","-d",payload],capture_output=True,text=True).stdout.strip()
        if code!="200":
            print("FALLO",i,code,open(resp).read()[:200]); break
        d=json.load(open(resp))
        open(f"voz-arb-{i:02d}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
        json.dump(words(d["alignment"]),open(f"arb-{i:02d}-words.json","w"),ensure_ascii=False)
        os.remove(resp)
        dd=dur(f"voz-arb-{i:02d}.mp3")
        man.append({"i":i,"who":who,"dur":round(dd,2),"text":t})
        print(f"  voz-arb-{i:02d} [{who}] {dd:.2f}s")
    json.dump(man,open("manifest.json","w"),ensure_ascii=False,indent=1)
    print("TOTAL voz:", round(sum(m['dur'] for m in man),1),"s ·", sum(len(l[1]) for l in LINEAS),"chars")
