# Pipeline de audio y caché ("memoria de salmos")

Dónde vive todo (repo `djlopo/djlopo`, rama de trabajo):

```
scripts/
  tts_cache.py              Caché de audio: sha1(voz+ajustes+texto) -> mp3 reutilizable
  library.py                Biblioteca de partes fijas (Gloria, Padrenuestro, Avemaría, respuestas, Benedictus, Magníficat, Salve...)
  generate_laudes_audio.py  Genera el audio de Laudes (usa la caché)
  generate_lecturas_audio.py Genera Lecturas + Evangelio + Reflexión (usa la caché)
  build_srt.py              Subtítulos sincronizados (.srt) desde los segmentos
audio_cache/
  <sha1>.mp3                Un archivo por fragmento único de audio (se reutiliza siempre)
  index.json                Registro legible: qué voz y qué texto es cada clave
content/                    Guiones (p. ej. Rosario)
```

## Cómo funciona la caché

1. El generador trocea el oficio en segmentos (voz + texto).
2. Por cada segmento llama a `tts_cache.get_or_generate(voz, ajustes, texto, salida)`.
3. La función calcula `sha1(voz + ajustes + texto)`:
   - si existe `audio_cache/<sha1>.mp3` -> **lo copia** (reutiliza, 0 créditos).
   - si no -> lo genera con ElevenLabs, lo **normaliza** (loudnorm) y lo **guarda** en `audio_cache/`.
4. Resultado: salmos, oraciones, respuestas y lecturas repetidas **no se regeneran**.

## Dónde revisarlo

- **El código** del pipeline: carpeta `scripts/`.
- **Qué hay cacheado**: `audio_cache/index.json` (voz + recorte del texto de cada clave).
- Todo está **versionado en Git**, así que persiste entre sesiones y se puede auditar.

## Vídeo (tiempo de Adviento)

`scripts/build_video_adviento.py` es la **plantilla estándar de Adviento** (solo Adviento):
mezcla el audio (voz + música `pad` en bucle muy baja + `chime` al entrar/cerrar),
genera los subtítulos quemados y renderiza con movimiento lento, capa de luz,
parpadeo de velas, viñeta animada y tipografía dorada/blanca sin borde.

```
python3 -I scripts/build_srt.py <carpeta> <carpeta>/subs.srt <modulo_generador>
python3 -I scripts/build_video_adviento.py \
    --audio final.mp3 --srt subs.srt --img corona.png --out video.mp4 \
    --title LAUDES --subtitle "Domingo · I Semana de Adviento" --date "29 de Noviembre de 2026" \
    --pad pad.wav --chime chime.wav
```

IMPORTANTE: se fija `format=gbrp` en toda la cadena de vídeo. `gradients`+`blend`
trabajan en RGB y una conversión implícita a YUV en `eq`/`vignette` lavaba el color
a magenta; con `gbrp` el color queda correcto (oscuro y cálido).

### Generadores de un día (I Domingo de Adviento, 29 nov 2026, Ciclo B)
- `gen_laudes_dom29adv.py`      Laudes del I Domingo
- `gen_lecturas_dom29adv.py`    Lecturas + Evangelio (Mc 13, «Velad») + Reflexión (fray Miguel de Burgos, O.P.)
- `gen_rosario_dom29adv.py`     Santo Rosario, misterios Gozosos
- `gen_short_dom29adv.py`       Short vertical (~26 s)
- `gen_especial_vela1.py`       Especial: Encendido de la 1ª vela en familia

Las lecturas de la Misa se obtienen de dominicos.org con Playwright
(`scratchpad/dominicos/fetch3.js <url> <salida>`), navegando por URL directa
`/predicacion/homilia/DD-MM-AAAA/{lecturas,comentario-biblico,pautas-para-la-homilia}/`.

## Notas

- Para que un mismo texto se reutilice entre tipos de vídeo, debe ser **idéntico**: por eso
  los textos fijos se centralizan en `library.py`.
- Si `audio_cache/` crece mucho con el tiempo, se puede mover a Notion/Drive manteniendo el índice.
- Los audios/vídeos finales de cada día son temporales (scratchpad); lo que persiste es el
  **código**, la **biblioteca** y la **caché**.
