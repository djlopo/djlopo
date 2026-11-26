#!/usr/bin/env python3
"""Genera src/subs/adviento.json (formato de la referencia: Palabra[][]).

Cada 'trozo' (chunk) es una caja de subtítulo; dentro, cada palabra lleva
{t, a, b} en segundos del timeline de la locucion (la composicion suma V=0.3).

Guion reconstruido a partir de las escenas de la referencia + el detalle de
las bayas rojas. Impares = Carlota, pares = Adolfo. Los tiempos se reparten
proporcionalmente dentro de la ventana de cada escena; cuando lleguen las
voces reales se regenera con las duraciones medidas.
"""
import json, os

# (ventana_raw_inicio, ventana_raw_fin, [chunks de palabras])
GUION = [
    # 1 Gancho (Carlota)
    (0.15, 3.45, [
        "Este domingo se enciende",
        "la primera vela.",
        "¿Sabes por qué?",
    ]),
    # 2 Que es (Adolfo)
    (3.95, 11.2, [
        "La corona de Adviento.",
        "Del latín «adventus»:",
        "venida.",
        "Es tiempo de esperar.",
    ]),
    # 3 Origen (Carlota)
    (11.7, 21.2, [
        "Hamburgo, 1839.",
        "El pastor Wichern",
        "puso una vela",
        "por cada día",
        "hasta la Navidad.",
    ]),
    # 4 Circulo + bayas rojas (Adolfo)
    (21.7, 28.0, [
        "Un círculo sin fin,",
        "como el amor de Dios.",
        "El verde: vida y esperanza.",
        "Las bayas rojas:",
        "la sangre de Cristo.",
    ]),
    # 5 Velas (Carlota)
    (28.5, 33.0, [
        "Cuatro velas:",
        "tres moradas y una rosa.",
        "Una por cada domingo.",
    ]),
    # 6 Encender (Adolfo)
    (33.5, 45.5, [
        "Cada domingo, una más:",
        "esperanza, paz,",
        "alegría y amor.",
        "Y vuelves a encender",
        "las anteriores.",
    ]),
    # 7 Blanca (Carlota)
    (46.0, 49.6, [
        "Y en el centro,",
        "una vela blanca:",
        "la noche de Navidad.",
    ]),
    # 8 Hacer (Adolfo)
    (50.1, 57.4, [
        "¿Quieres hacerla?",
        "Un aro, ramas de abeto,",
        "piñas y cuatro velas.",
        "Nunca la dejes sola.",
    ]),
    # 9 Cierre (Carlota)
    (58.0, 63.6, [
        "Este domingo,",
        "enciende la primera.",
        "Reza con nosotros",
        "este Adviento.",
    ]),
]

GAP = 0.12  # pequeño silencio entre palabras

def build():
    trozos = []
    for a0, b0, chunks in GUION:
        # repartir la ventana entre chunks segun nº de palabras
        counts = [len(c.split()) for c in chunks]
        total = sum(counts)
        span = b0 - a0
        t = a0
        for c, n in zip(chunks, counts):
            dur = span * (n / total)
            # dentro del chunk, palabras uniformes
            words = c.split()
            wdur = (dur - GAP * max(0, len(words) - 1)) / len(words)
            palabras = []
            wt = t
            for w in words:
                palabras.append({"t": w, "a": round(wt, 3), "b": round(wt + wdur, 3)})
                wt += wdur + GAP
            trozos.append(palabras)
            t += dur
    return trozos

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "src", "subs")
    os.makedirs(out, exist_ok=True)
    trozos = build()
    with open(os.path.join(out, "adviento.json"), "w", encoding="utf-8") as f:
        json.dump(trozos, f, ensure_ascii=False, indent=0)
    print(f"{len(trozos)} trozos, {sum(len(t) for t in trozos)} palabras")
    print("ultimo b:", trozos[-1][-1]["b"])
