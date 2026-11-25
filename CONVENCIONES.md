# Convenciones de producción — Tu Oracion Diaria

## Horario de publicación (hora de España)
| Pieza | Hora |
|---|---|
| Laudes | 06:00 |
| Lecturas / Evangelio del día | 07:00 |
| Santo Rosario | 08:00 |
| Especial / otras piezas | 09:00 |
| Short | 20:30 (franja de mayor alcance de Shorts por la tarde-noche) |

> El Short se separa del bloque de mañana a propósito: capta el público de oración de
> la tarde/noche y aprovecha el pico de Shorts. Si se prefiere un único bloque matinal,
> alternativa: 08:30.

## Rosario — rezo a DOS VOCES (guía / pueblo)
Partes fijas en `library.py`:
- **Avemaría**: `AVEMARIA_1` (guía, hasta «…Jesús.») / `AVEMARIA_2` (pueblo, «Santa María…»).
- **Padrenuestro**: `PADRENUESTRO_1` (guía: Nombre, reino, voluntad) / `PADRENUESTRO_2` (pueblo:
  pan, perdón, tentación, mal). El corte separa las tres peticiones «tuyas» de las «nuestras».
- **Gloria**: `GLORIA_1` (guía) / `GLORIA_2` (pueblo).

## Misterios = Palabra de Dios
Antes de meditar cada misterio se **proclama su pasaje bíblico**. Referencias en `library.py`
(`MISTERIOS_GOZOSOS_BIBLIA`, `_DOLOROSOS_`, `_GLORIOSOS_`, `_LUMINOSOS_`). El texto bíblico se
cita literal en cada generador. Misterios por día (`MISTERIOS_POR_DIA`): L y S Gozosos,
M y V Dolorosos, X y D Gloriosos, J Luminosos (los domingos de Adviento/Navidad: Gozosos).

## Método para generar imágenes/vídeos con Grok ("Oro")
Entregar SIEMPRE un único prompt listo para pegar. El prompt debe empezar indicando a Grok:
1. Que trabaje **poco a poco**, idea por idea, de forma ordenada y etiquetada.
2. Que dé **2 muestras por cada imagen** (o por cada idea/estilo).
3. Si se quiere **vídeo**: que **primero muestre la imagen y pregunte** si ha quedado bien; solo
   si el usuario la aprueba, que **genere el vídeo automáticamente** a partir de esa imagen.
Reglas de marca comunes: dorado #d7b26e / azul noche; o paletas de la temporada litúrgica.
Siempre sin texto ni marca de agua en la imagen (los rótulos los pone la plantilla).

## Serie «Vidas de Santos» — voz del narrador
- **Narrador (N):** voz `Syqs6p4s6hxhfAyhhlbS` (la cálida/grave), ajustes
  `stability 0.42 · similarity 0.8 · style 0.26 · speed 1.0`. Elegida para toda la serie.
- **Voz de las citas (V):** pendiente de elegir (para las palabras de Jesús y del santo).
- Los tiempos y tonos por frase se afinarán con marcas (pausas/énfasis) en cada guion.

## Nota litúrgica — días especiales
No todo es feria de Adviento. Ej.: **30 nov = San Andrés Apóstol (Fiesta, rojo)**, con lecturas
y oficio propios. En esos días se usan los textos propios de la fiesta, no los de la feria.
