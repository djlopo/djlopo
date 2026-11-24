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

## Notas

- Para que un mismo texto se reutilice entre tipos de vídeo, debe ser **idéntico**: por eso
  los textos fijos se centralizan en `library.py`.
- Si `audio_cache/` crece mucho con el tiempo, se puede mover a Notion/Drive manteniendo el índice.
- Los audios/vídeos finales de cada día son temporales (scratchpad); lo que persiste es el
  **código**, la **biblioteca** y la **caché**.
