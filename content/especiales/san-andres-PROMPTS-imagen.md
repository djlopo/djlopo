# Pack de prompts de imagen — Especial San Andrés (personaje consistente)

## Método (pégalo al principio en Grok)
```
Trabaja POCO A POCO, imagen por imagen, ordenado y etiquetado. Da 2 MUESTRAS por imagen.
Si decido hacer vídeo de alguna: muéstrame PRIMERO la imagen, pregunta si me gusta, y SOLO si
digo que sí, genera el vídeo (image→video) a partir de ESA imagen.
CONSISTENCIA DE PERSONAJE: primero generamos un RETRATO CANÓNICO de Andrés (PROMPT 0). En TODAS
las imágenes siguientes ADJUNTA ese retrato como imagen de referencia y respeta EXACTAMENTE el mismo
rostro y rasgos; cambia solo la escena, la pose y la EDAD indicada.
```

## Ficha de personaje (repetir en cada prompt)
```
PERSONAJE (idéntico en todas las imágenes): Andrés, pescador judío de Galilea del siglo I.
Rostro mediterráneo, piel olivácea curtida por el sol y el mar; ojos castaños cálidos y vivos;
nariz recta; pómulos marcados; cejas pobladas; barba y cabello castaño oscuro. Complexión fibrosa
de pescador, manos fuertes y encallecidas. Expresión humilde, sincera, buscadora. Túnica sencilla
de lino sin teñir y mantón de lana. Estética fotorrealista y elegante, claroscuro, luz cálida,
fondo oscuro con bokeh dorado. Sin texto, sin marca de agua. Relación 16:9.
EDAD JOVEN (ministerio, ~30 años): cabello y barba castaño oscuro, vigoroso.
EDAD ANCIANO (martirio, ~70 años): el MISMO rostro décadas después — cabello y barba canos,
arrugas profundas, más delgado, pero mismos ojos y estructura ósea.
```

## Prompts por escena

**PROMPT 0 — Retrato canónico (JOVEN). Generar PRIMERO. 2 muestras.**
```
[Ficha de personaje, edad JOVEN]. Retrato de medio cuerpo de Andrés, pescador galileo joven, mirando
levemente fuera de cámara, sereno. Fondo oscuro con un rayo de luz cálida lateral (claroscuro).
Primerísimo cuidado del rostro: este retrato será la REFERENCIA de todas las demás imágenes. 16:9.
```

**PROMPT 1 — Pescador en Betsaida (JOVEN).** *(adjunta el retrato 0)*
```
Mismo hombre que la imagen de referencia, mismo rostro, edad JOVEN. Andrés remendando las redes al
amanecer junto al mar de Galilea; barcas de madera, redes, orilla; luz dorada del alba sobre el agua
en calma. Plano general con él como protagonista. 16:9, fotorrealista, elegante. Sin texto.
```

**PROMPT 2 — El encuentro / «He ahí el Cordero de Dios» (JOVEN).** *(adjunta el retrato 0)*
```
Mismo hombre que la referencia, edad JOVEN. Andrés, de pie junto a Juan el Bautista a la orilla del
Jordán, mira con asombro hacia Jesús que pasa a lo lejos, iluminado. Atardecer, luz cálida (la hora
décima, hacia las cuatro de la tarde). Ambiente íntimo, claroscuro. 16:9. Sin texto.
```

**PROMPT 3 — Lleva a su hermano Pedro (JOVEN).** *(adjunta el retrato 0)*
```
Mismo hombre que la referencia, edad JOVEN. Andrés, lleno de alegría, agarra del hombro a su hermano
Simón Pedro (otro pescador, algo más corpulento) y le habla con entusiasmo señalando hacia Jesús.
Dos hermanos, emoción y cercanía. Luz cálida, fondo oscuro. 16:9, fotorrealista. Sin texto.
```

**PROMPT 4 — La llamada junto al lago (JOVEN).** *(adjunta el retrato 0)*
```
Mismo hombre que la referencia, edad JOVEN. Jesús, de pie en la orilla, extiende la mano llamando a
Andrés y a Pedro, que sueltan las redes desde la barca para seguirlo. Amanecer glorioso sobre el mar
de Galilea, rayos de luz. Escena cinematográfica, fotorrealista, elegante. 16:9. Sin texto.
```

**PROMPT 5 — Martirio en Patras (ANCIANO).** *(adjunta el retrato 0 + nota de envejecer)*
```
El MISMO hombre de la referencia, pero ANCIANO (~70 años): cabello y barba canos, rostro arrugado,
mismos ojos y estructura. Andrés abrazado a una gran cruz en forma de aspa (equis), sereno y en paz,
luz cálida con matices rojos (color del martirio), fondo oscuro con bokeh. 16:9, fotorrealista,
pictórico. Sin texto. (Si prefieres, usamos la imagen de anciano que ya tienes.)
```

> Mapa del viaje (Galilea → Grecia → Patras) y los sellos los hago yo en Remotion; no necesitan Grok.

## Notas
- Aun con referencia, la IA no clava el rostro al 100%: generamos 2 muestras y elegimos la mejor.
- Para los planos con más fuerza (llamada, correr a Pedro, martirio) podemos pedir luego el vídeo
  (image→video) con el método de arriba.
