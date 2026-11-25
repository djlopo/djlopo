import React from 'react';
import {AbsoluteFill, Img, Audio, staticFile, interpolate, useCurrentFrame, spring, Sequence, Easing} from 'remotion';
import {FPS, SELLO, HEAD, TAIL, CLOSE, SECTIONS, sceneFrames, TOTAL} from './layout';

const NAVY = '#140a2a';
const GOLD = '#d7b26e';
const CREAM = '#f3ecdd';
const FONT = 'DejaVu Serif, Georgia, serif';

// ---- metadatos visuales por sección ----
const META: Record<string, {label?: string; callouts?: {at: number; word: string; sub: string}[]; map?: boolean}> = {
  gancho: {},
  quienfue: {label: '¿Quién fue?', callouts: [
    {at: 5, word: 'ANDRÉS', sub: 'del griego andréas — «el valiente»'},
    {at: 24, word: 'BETSAIDA', sub: 'en hebreo — «casa de la pesca»'},
  ]},
  encuentro: {label: 'El encuentro'},
  respuesta: {label: 'Lleva a su hermano Pedro'},
  llamada: {label: '«Venid y seguidme»'},
  cruz: {label: 'La cruz'},
  hoy: {label: 'El Protóclito — el primero llamado'},
  mision: {map: true},
  cierre: {},
};

const Saltire: React.FC<{progress: number; size?: number}> = ({progress, size = 360}) => {
  const len = 400;
  const off = (1 - progress) * len;
  return (
    <svg width={size} height={size} viewBox="0 0 360 360">
      <g stroke={GOLD} strokeWidth="9" strokeLinecap="round" fill="none" style={{filter: 'drop-shadow(0 0 14px rgba(215,178,110,0.4))'}}>
        <line x1="70" y1="70" x2="290" y2="290" strokeDasharray={len} strokeDashoffset={off} />
        <line x1="290" y1="70" x2="70" y2="290" strokeDasharray={len} strokeDashoffset={off} />
      </g>
    </svg>
  );
};

const Particles: React.FC = () => {
  const frame = useCurrentFrame();
  const parts = Array.from({length: 40}).map((_, i) => {
    const seed = i * 978.233;
    const x = (Math.sin(seed) * 0.5 + 0.5) * 1920;
    const speed = 0.3 + Math.abs(Math.cos(seed * 1.3)) * 0.8;
    const size = 1.5 + Math.abs(Math.sin(seed * 2.1)) * 3;
    const baseY = Math.abs(Math.sin(seed * 0.7)) * 1080;
    const y = (((baseY - frame * speed) % 1120) + 1120) % 1120 - 20;
    const tw = 0.3 + 0.5 * (Math.sin(frame * 0.08 + i) * 0.5 + 0.5);
    const drift = Math.sin(frame * 0.02 + i) * 16;
    return <div key={i} style={{position: 'absolute', left: x + drift, top: y, width: size, height: size, borderRadius: '50%', background: GOLD, opacity: tw * 0.45, boxShadow: `0 0 ${size * 2}px rgba(215,178,110,0.6)`}} />;
  });
  return <AbsoluteFill>{parts}</AbsoluteFill>;
};

const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{opacity: 0.05, mixBlendMode: 'overlay'}}>
      <svg width="1920" height="1080">
        <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={frame % 40} /></filter>
        <rect width="1920" height="1080" filter="url(#n)" />
      </svg>
    </AbsoluteFill>
  );
};

// ---- Escena 2.5D sobre imagen ----
const Scene: React.FC<{img: string; audio: string; frames: number; meta: any}> = ({img, audio, frames, meta}) => {
  const frame = useCurrentFrame();
  const fin = interpolate(frame, [0, 16], [0, 1], {extrapolateRight: 'clamp'});
  const fout = interpolate(frame, [frames - 16, frames], [1, 0], {extrapolateLeft: 'clamp'});
  const scale = interpolate(frame, [0, frames], [1.07, 1.2]);
  const ty = interpolate(frame, [0, frames], [0, -20]);
  const bgScale = interpolate(frame, [0, frames], [1.4, 1.5]);
  const bgX = interpolate(frame, [0, frames], [-18, 18]);
  const src = staticFile('img/' + img);
  const labelOp = interpolate(frame, [20, 40, frames - 40, frames - 20], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000', opacity: fin * fout}}>
      <AbsoluteFill style={{transform: `scale(${bgScale}) translateX(${bgX}px)`, filter: 'blur(26px) brightness(0.5)'}}>
        <Img src={src} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `scale(${scale}) translateY(${ty}px)`}}>
        <Img src={src} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(60% 50% at 50% 0%, rgba(255,200,120,0.16), transparent 70%)'}} />
      <Particles />
      <AbsoluteFill style={{boxShadow: 'inset 0 0 440px 130px rgba(0,0,0,0.82)'}} />
      <Grain />
      {/* etiqueta lower-third */}
      {meta.label && (
        <div style={{position: 'absolute', left: 90, bottom: 72, opacity: labelOp, borderLeft: `3px solid ${GOLD}`, paddingLeft: 22}}>
          <div style={{color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 34, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{meta.label}</div>
        </div>
      )}
      {/* callouts de etimología */}
      {(meta.callouts || []).map((c: any, i: number) => {
        const start = HEAD + Math.round(c.at * FPS);
        const o = interpolate(frame, [start, start + 18, start + 150, start + 170], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const x = interpolate(frame, [start, start + 18], [-50, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <div key={i} style={{position: 'absolute', right: 90, top: 150 + i * 150, opacity: o, transform: `translateX(${x}px)`, textAlign: 'right', borderRight: `3px solid ${GOLD}`, paddingRight: 22}}>
            <div style={{color: GOLD, fontFamily: FONT, fontWeight: 'bold', fontSize: 42, letterSpacing: 3}}>{c.word}</div>
            <div style={{color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 28, marginTop: 4, opacity: 0.92}}>{c.sub}</div>
          </div>
        );
      })}
      <Sequence from={HEAD}><Audio src={staticFile(audio)} /></Sequence>
    </AbsoluteFill>
  );
};

// ---- Escena de mapa (misión) ----
const MapScene: React.FC<{audio: string; frames: number}> = ({audio, frames}) => {
  const frame = useCurrentFrame();
  const fin = interpolate(frame, [0, 16], [0, 1], {extrapolateRight: 'clamp'});
  const fout = interpolate(frame, [frames - 16, frames], [1, 0], {extrapolateLeft: 'clamp'});
  // puntos: Galilea -> Asia Menor -> Grecia (Patras)
  const pts = [{x: 1480, y: 430, n: 'Galilea'}, {x: 1080, y: 500, n: 'Asia Menor'}, {x: 760, y: 560, n: 'Grecia · Patras'}];
  const draw = interpolate(frame, [HEAD + 20, HEAD + 220], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const path = `M ${pts[0].x} ${pts[0].y} Q ${(pts[0].x + pts[1].x) / 2} ${pts[0].y - 70}, ${pts[1].x} ${pts[1].y} T ${pts[2].x} ${pts[2].y}`;
  const LEN = 1100;
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 45% 45%, #221340 0%, ${NAVY} 55%, #090417 100%)`, opacity: fin * fout}}>
      <Particles />
      <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', paddingTop: 90}}>
        <div style={{color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 40, opacity: 0.85}}>De Galilea al confín del mundo griego</div>
      </AbsoluteFill>
      <svg width="1920" height="1080" style={{position: 'absolute'}}>
        <path d={path} fill="none" stroke={GOLD} strokeWidth="4" strokeDasharray={LEN} strokeDashoffset={(1 - draw) * LEN} strokeLinecap="round" style={{filter: 'drop-shadow(0 0 8px rgba(215,178,110,0.5))'}} />
        {pts.map((p, i) => {
          const ap = interpolate(frame, [HEAD + 20 + i * 70, HEAD + 50 + i * 70], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <g key={i} opacity={ap}>
              <circle cx={p.x} cy={p.y} r={10} fill={GOLD} style={{filter: 'drop-shadow(0 0 10px rgba(215,178,110,0.8))'}} />
              <text x={p.x} y={p.y + 44} fill={CREAM} fontFamily={FONT} fontSize={30} textAnchor="middle">{p.n}</text>
            </g>
          );
        })}
      </svg>
      {/* cruz en aspa en Patras cuando se completa */}
      <div style={{position: 'absolute', left: pts[2].x - 55, top: pts[2].y - 150, opacity: interpolate(frame, [HEAD + 200, HEAD + 240], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
        <Saltire progress={1} size={90} />
      </div>
      <Grain />
      <Sequence from={HEAD}><Audio src={staticFile(audio)} /></Sequence>
    </AbsoluteFill>
  );
};

const SelloOpen: React.FC = () => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [8, 58], [0, 1], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const ts = spring({frame: frame - 32, fps: FPS, config: {damping: 200}});
  const tScale = interpolate(ts, [0, 1], [0.86, 1]);
  const tOp = interpolate(frame, [32, 58], [0, 1], {extrapolateRight: 'clamp'});
  const sOp = interpolate(frame, [58, 84], [0, 1], {extrapolateRight: 'clamp'});
  const topOp = interpolate(frame, [12, 42], [0, 1], {extrapolateRight: 'clamp'});
  const out = interpolate(frame, [SELLO - 20, SELLO], [1, 0], {extrapolateLeft: 'clamp'});
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 42%, #251646 0%, ${NAVY} 58%, #0b0520 100%)`, opacity: out, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{position: 'absolute', top: 128, color: CREAM, opacity: topOp * 0.8, fontFamily: FONT, letterSpacing: 16, fontSize: 28}}>VIDAS DE SANTOS</div>
      <div style={{marginTop: -30}}><Saltire progress={draw} /></div>
      <div style={{transform: `scale(${tScale})`, opacity: tOp, color: GOLD, fontFamily: FONT, fontWeight: 'bold', fontSize: 112, letterSpacing: 6, marginTop: 6, textShadow: '0 4px 26px rgba(0,0,0,0.6)'}}>SAN ANDRÉS</div>
      <div style={{opacity: sOp, color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 40, marginTop: 10}}>«el Protóclito» — el primero llamado</div>
      <div style={{opacity: sOp * 0.72, color: CREAM, fontFamily: FONT, fontSize: 26, marginTop: 18, letterSpacing: 2}}>30 de noviembre</div>
    </AbsoluteFill>
  );
};

const SelloClose: React.FC = () => {
  const frame = useCurrentFrame();
  const inOp = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});
  const draw = interpolate(frame, [6, 44], [0, 1], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, #251646 0%, ${NAVY} 58%, #0b0520 100%)`, opacity: inOp, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{marginBottom: 6}}><Saltire progress={draw} size={240} /></div>
      <div style={{color: GOLD, fontFamily: FONT, fontWeight: 'bold', fontSize: 58, letterSpacing: 4}}>Tu Oración Diaria</div>
      <div style={{color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 34, marginTop: 10, opacity: 0.9}}>Lista «Vidas de Santos»</div>
      <div style={{color: CREAM, fontFamily: FONT, fontSize: 26, marginTop: 20, opacity: 0.7, letterSpacing: 2}}>Suscríbete · hasta el próximo santo</div>
    </AbsoluteFill>
  );
};

export const Especial: React.FC = () => {
  let off = SELLO;
  const scenes = SECTIONS.map((s) => {
    const fr = sceneFrames(s.dur);
    const node = (
      <Sequence key={s.id} from={off} durationInFrames={fr}>
        {META[s.id]?.map
          ? <MapScene audio={s.audio} frames={fr} />
          : <Scene img={s.img} audio={s.audio} frames={fr} meta={META[s.id] || {}} />}
      </Sequence>
    );
    off += fr;
    return node;
  });
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <Audio src={staticFile('music.mp3')} loop volume={(f) => interpolate(f, [0, 60, TOTAL - 90, TOTAL], [0, 0.09, 0.09, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
      <Sequence durationInFrames={SELLO}><SelloOpen /></Sequence>
      {scenes}
      <Sequence from={off} durationInFrames={CLOSE}><SelloClose /></Sequence>
    </AbsoluteFill>
  );
};
