import React from 'react';
import {AbsoluteFill, Img, staticFile, interpolate, useCurrentFrame, useVideoConfig, spring, Sequence, Easing} from 'remotion';

const NAVY = '#140a2a';
const GOLD = '#d7b26e';
const CREAM = '#f3ecdd';
const FONT = 'DejaVu Serif, Georgia, serif';
const SCENE2_DUR = 400;

// ---------- Sello de apertura ----------
const Saltire: React.FC<{progress: number}> = ({progress}) => {
  const len = 400;
  const off = (1 - progress) * len;
  return (
    <svg width="360" height="360" viewBox="0 0 360 360">
      <g stroke={GOLD} strokeWidth="9" strokeLinecap="round" fill="none"
         style={{filter: 'drop-shadow(0 0 14px rgba(215,178,110,0.4))'}}>
        <line x1="70" y1="70" x2="290" y2="290" strokeDasharray={len} strokeDashoffset={off} />
        <line x1="290" y1="70" x2="70" y2="290" strokeDasharray={len} strokeDashoffset={off} />
      </g>
    </svg>
  );
};

const Sello: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const draw = interpolate(frame, [8, 58], [0, 1], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const titleS = spring({frame: frame - 32, fps, config: {damping: 200}});
  const titleScale = interpolate(titleS, [0, 1], [0.86, 1]);
  const titleOp = interpolate(frame, [32, 58], [0, 1], {extrapolateRight: 'clamp'});
  const subOp = interpolate(frame, [58, 84], [0, 1], {extrapolateRight: 'clamp'});
  const topOp = interpolate(frame, [12, 42], [0, 1], {extrapolateRight: 'clamp'});
  const out = interpolate(frame, [120, 150], [1, 0], {extrapolateLeft: 'clamp'});
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 42%, #251646 0%, ${NAVY} 58%, #0b0520 100%)`, opacity: out, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{position: 'absolute', top: 128, color: CREAM, opacity: topOp * 0.8, fontFamily: FONT, letterSpacing: 16, fontSize: 28}}>VIDAS DE SANTOS</div>
      <div style={{marginTop: -30}}><Saltire progress={draw} /></div>
      <div style={{transform: `scale(${titleScale})`, opacity: titleOp, color: GOLD, fontFamily: FONT, fontWeight: 'bold', fontSize: 112, letterSpacing: 6, marginTop: 6, textShadow: '0 4px 26px rgba(0,0,0,0.6)'}}>SAN ANDRÉS</div>
      <div style={{opacity: subOp, color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 40, marginTop: 10}}>«el Protóclito» — el primero llamado</div>
      <div style={{opacity: subOp * 0.72, color: CREAM, fontFamily: FONT, fontSize: 26, marginTop: 18, letterSpacing: 2}}>30 de noviembre</div>
    </AbsoluteFill>
  );
};

// ---------- Partículas doradas (profundidad) ----------
const Particles: React.FC = () => {
  const frame = useCurrentFrame();
  const parts = Array.from({length: 45}).map((_, i) => {
    const seed = i * 978.233;
    const x = (Math.sin(seed) * 0.5 + 0.5) * 1920;
    const speed = 0.3 + Math.abs(Math.cos(seed * 1.3)) * 0.9;
    const size = 1.5 + Math.abs(Math.sin(seed * 2.1)) * 3.5;
    const baseY = Math.abs(Math.sin(seed * 0.7)) * 1080;
    const y = (((baseY - frame * speed) % 1120) + 1120) % 1120 - 20;
    const tw = 0.3 + 0.5 * (Math.sin(frame * 0.08 + i) * 0.5 + 0.5);
    const drift = Math.sin(frame * 0.02 + i) * 18;
    return <div key={i} style={{position: 'absolute', left: x + drift, top: y, width: size, height: size, borderRadius: '50%', background: GOLD, opacity: tw * 0.5, boxShadow: `0 0 ${size * 2}px rgba(215,178,110,0.6)`}} />;
  });
  return <AbsoluteFill>{parts}</AbsoluteFill>;
};

const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{opacity: 0.055, mixBlendMode: 'overlay'}}>
      <svg width="1920" height="1080">
        <filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={frame % 40} /></filter>
        <rect width="1920" height="1080" filter="url(#noise)" />
      </svg>
    </AbsoluteFill>
  );
};

// ---------- Plano 2.5D sobre la imagen ----------
const Scene2: React.FC = () => {
  const frame = useCurrentFrame();
  const inOp = interpolate(frame, [0, 22], [0, 1], {extrapolateRight: 'clamp'});
  const outOp = interpolate(frame, [SCENE2_DUR - 28, SCENE2_DUR], [1, 0], {extrapolateLeft: 'clamp'});
  const scale = interpolate(frame, [0, SCENE2_DUR], [1.08, 1.22]);
  const ty = interpolate(frame, [0, SCENE2_DUR], [0, -24]);
  const bgScale = interpolate(frame, [0, SCENE2_DUR], [1.4, 1.5]);
  const bgX = interpolate(frame, [0, SCENE2_DUR], [-20, 20]);
  const l1 = interpolate(frame, [22, 48], [0, 1], {extrapolateRight: 'clamp'});
  const l1y = interpolate(frame, [22, 48], [22, 0], {extrapolateRight: 'clamp'});
  const big = spring({frame: frame - 58, fps: 30, config: {damping: 200}});
  const bigScale = interpolate(big, [0, 1], [0.8, 1]);
  const bigOp = interpolate(frame, [58, 80], [0, 1], {extrapolateRight: 'clamp'});
  const txtOut = interpolate(frame, [175, 200], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const ety = interpolate(frame, [215, 240], [0, 1], {extrapolateRight: 'clamp'});
  const etyX = interpolate(frame, [215, 240], [-60, 0], {extrapolateRight: 'clamp'});
  const etyOut = interpolate(frame, [360, 385], [1, 0], {extrapolateLeft: 'clamp'});

  return (
    <AbsoluteFill style={{background: '#000', opacity: inOp * outOp}}>
      <AbsoluteFill style={{transform: `scale(${bgScale}) translateX(${bgX}px)`, filter: 'blur(26px) brightness(0.5)'}}>
        <Img src={staticFile('sanandres.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `scale(${scale}) translateY(${ty}px)`}}>
        <Img src={staticFile('sanandres.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(60% 50% at 50% 0%, rgba(255,200,120,0.18), transparent 70%)'}} />
      <Particles />
      <AbsoluteFill style={{boxShadow: 'inset 0 0 420px 120px rgba(0,0,0,0.82)'}} />
      <Grain />
      <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', paddingTop: 110, opacity: txtOut}}>
        <div style={{opacity: l1, transform: `translateY(${l1y}px)`, color: CREAM, fontFamily: FONT, fontSize: 46, textShadow: '0 2px 16px rgba(0,0,0,0.85)'}}>Al que Jesús llamó</div>
        <div style={{opacity: bigOp, transform: `scale(${bigScale})`, color: GOLD, fontFamily: FONT, fontWeight: 'bold', fontSize: 120, letterSpacing: 4, marginTop: 2, textShadow: '0 4px 26px rgba(0,0,0,0.9)'}}>EL PRIMERO</div>
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 92, bottom: 128, opacity: ety * etyOut, transform: `translateX(${etyX}px)`, borderLeft: `3px solid ${GOLD}`, paddingLeft: 24}}>
        <div style={{color: GOLD, fontFamily: FONT, fontWeight: 'bold', fontSize: 40, letterSpacing: 3}}>ANDRÉS</div>
        <div style={{color: CREAM, fontFamily: FONT, fontStyle: 'italic', fontSize: 30, marginTop: 6, opacity: 0.92}}>del griego <span style={{color: GOLD}}>andréas</span> — «el valiente»</div>
      </div>
    </AbsoluteFill>
  );
};

export const Sample: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <Sequence durationInFrames={150}><Sello /></Sequence>
      <Sequence from={135} durationInFrames={SCENE2_DUR}><Scene2 /></Sequence>
    </AbsoluteFill>
  );
};
