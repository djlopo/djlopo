#!/usr/bin/env python3
"""Voz guía del rito «Encendido de la 1ª vela de la Corona (en familia)».
Una sola voz calmada (Javi Rojas). 8 secciones."""
import json, base64, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
JAVI = "aYbngTsp5kp0sibI3Z0T"
SET = {"stability": 0.52, "similarity_boost": 0.85, "style": 0.12, "use_speaker_boost": True, "speed": 0.97}

SECCIONES = [
 ("Bienvenida", "Bienvenidos. Hoy, primer domingo de Adviento, nos reunimos en familia para encender la primera vela de la corona. Comienza nuestro camino hacia la Navidad."),
 ("Señal de la cruz", "Empezamos con la señal de la cruz. En el nombre del Padre, y del Hijo, y del Espíritu Santo. Amén."),
 ("Palabra de Dios · Isaías 9", "Escuchemos la Palabra de Dios. Del profeta Isaías: «El pueblo que caminaba en tinieblas vio una luz grande; sobre los que vivían en tierra de sombras, una luz brilló»."),
 ("Bendición de la corona", "Bendigamos la corona. Bendice, Señor, esta corona de Adviento. Que su luz, que irá creciendo domingo a domingo, nos recuerde que Tú, luz del mundo, estás cada vez más cerca. Por Jesucristo nuestro Señor. Amén."),
 ("Primera vela · la Esperanza", "Encendemos ahora la primera vela: la vela de la esperanza. Ven, Señor Jesús. En Ti esperamos, y nuestra esperanza no defrauda."),
 ("Padrenuestro", "Y todos juntos oramos como el Señor nos enseñó. Padre nuestro, que estás en el cielo, santificado sea tu Nombre; venga a nosotros tu Reino; hágase tu voluntad en la tierra como en el cielo. Danos hoy nuestro pan de cada día; perdona nuestras ofensas, como también nosotros perdonamos a los que nos ofenden; no nos dejes caer en la tentación, y líbranos del mal. Amén."),
 ("Oración y bendición", "Señor, que esta semana vivamos despiertos, preparando tu venida. Y bendice a todos los que formamos esta familia: en el nombre del Padre, y del Hijo, y del Espíritu Santo. Amén."),
 ("Hasta el próximo domingo", "El próximo domingo encenderemos la segunda vela, la de la paz. Que tengáis un buen Adviento. Rezad con nosotros cada día."),
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
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip() or 0)

if __name__ == "__main__":
    man=[]
    for i,(lab,t) in enumerate(SECCIONES,1):
        payload=json.dumps({"text":t,"model_id":"eleven_multilingual_v2","voice_settings":SET})
        resp=f"_r{i}.json"
        code=subprocess.run(["curl","-sS","-o",resp,"-w","%{http_code}","-X","POST",
            f"https://api.elevenlabs.io/v1/text-to-speech/{JAVI}/with-timestamps?output_format=mp3_44100_128",
            "-H","Content-Type: application/json","-d",payload],capture_output=True,text=True).stdout.strip()
        if code!="200": print("FALLO",i,code,open(resp).read()[:200]); break
        d=json.load(open(resp))
        open(f"voz-rito-{i:02d}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
        json.dump(words(d["alignment"]),open(f"rito-{i:02d}-words.json","w"),ensure_ascii=False)
        os.remove(resp); dd=dur(f"voz-rito-{i:02d}.mp3")
        man.append({"i":i,"label":lab,"dur":round(dd,2)}); print(f"  voz-rito-{i:02d} [{lab}] {dd:.2f}s")
    json.dump({"secciones":[s[0] for s in SECCIONES],"man":man},open("manifest.json","w"),ensure_ascii=False,indent=1)
    print("TOTAL:", round(sum(m['dur'] for m in man),1),"s")
