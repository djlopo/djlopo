# Reel «La corona de Adviento» (vertical 1080×1920)

Proyecto Remotion. Estilo noche ciruela + oro, tipografía del canal (Fraunces/Nunito
autoalojada), corona SVG con bayas rojas, subtítulos palabra a palabra sincronizados y
cierre de marca «Tu Oración Diaria».

## Reconstruir
1. `npm i` (o reutilizar node_modules de ../). Requiere @remotion/cli, @remotion/media, remotion 4.0.547.
2. Voces: `python3 -I voces-adv/gen_voces.py` (ElevenLabs, Carlota + Adolfo Banderas).
3. Audio+subs+tiempos: `python3 -I build_audio_subs.py` (genera public/voz-adviento.mp3,
   src/subs/adviento.json, src/datos.json y extiende la música).
4. Render: `remotion render src/index.ts adviento out/adviento.mp4 --browser-executable=/opt/pw-browsers/chromium --codec=h264 --pixel-format=yuv420p --crf=20`

datos.json remapea los tiempos de la referencia a la duración real de cada voz.
