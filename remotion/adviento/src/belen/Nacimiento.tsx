import React from "react";
import { Easing, interpolate } from "remotion";

/* Belén (nacimiento) estilizado e iconográfico, estilo del canal.
   Centrado en (0,0); el suelo está en y≈150. */

const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const back = (p: number) => Easing.out(Easing.back(1.8))(Math.min(1, Math.max(0, p)));
const ap = (v: number, o = 0, d = 1) => back(interpolate(v, [o, o + d], [0, 1], CL));

export type EstadoBelen = {
  portal: number; estrella: number; pesebre: number; sagrada: number;
  animales: number; angel: number; pastores: number; reyes: number; entorno: number;
};

// --- Figura con túnica (bell) + cabeza + nimbo opcional ---
const Figura: React.FC<{ x: number; y: number; h?: number; w?: number; robe: string; robe2?: string; veil?: string; halo?: boolean; lean?: number; p: number }> =
({ x, y, h = 130, w = 46, robe, robe2, veil, halo = false, lean = 0, p }) => {
  if (p <= 0) return null;
  const s = back(p);
  const hr = w * 0.44;
  const hy = y - h - hr * 0.5;
  return (
    <g transform={`translate(${x} ${y + (1 - s) * 40}) scale(${s}) rotate(${lean})`} style={{ transformOrigin: `0px ${y}px` }} opacity={Math.min(1, p * 2)}>
      <ellipse cx={0} cy={0} rx={w * 0.95} ry={10} fill="#000" opacity={0.25} />
      <path d={`M ${-w},0 Q ${-w},${-h * 0.72} ${-w * 0.42},${-h * 0.93} Q 0,${-h} ${w * 0.42},${-h * 0.93} Q ${w},${-h * 0.72} ${w},0 Z`} fill={robe} />
      {robe2 && <path d={`M ${-w * 0.2},0 Q 0,${-h * 0.9} ${w * 0.2},0 Z`} fill={robe2} opacity={0.6} />}
      {halo && <circle cx={0} cy={-h - hr * 0.5} r={hr * 1.5} fill="none" stroke="#f4c46a" strokeWidth={5} opacity={0.9} />}
      <circle cx={0} cy={-h - hr * 0.5} r={hr} fill="#e9c9a3" />
      {veil && <path d={`M ${-hr * 1.2},${-h - hr * 0.3} Q 0,${-h - hr * 2.1} ${hr * 1.2},${-h - hr * 0.3} Q ${hr * 0.9},${-h + hr * 0.2} 0,${-h + hr * 0.1} Q ${-hr * 0.9},${-h + hr * 0.2} ${-hr * 1.2},${-h - hr * 0.3} Z`} fill={veil} />}
    </g>
  );
};

const Animal: React.FC<{ x: number; y: number; flip?: number; color: string; cuernos?: boolean; p: number }> = ({ x, y, flip = 1, color, cuernos, p }) => {
  if (p <= 0) return null;
  const s = back(p);
  return (
    <g transform={`translate(${x} ${y}) scale(${s * flip} ${s})`} opacity={Math.min(1, p * 2)}>
      <ellipse cx={0} cy={-28} rx={48} ry={30} fill={color} />
      <ellipse cx={42} cy={-46} rx={18} ry={22} fill={color} />
      <rect x={-34} y={-14} width={9} height={18} rx={3} fill={color} />
      <rect x={22} y={-14} width={9} height={18} rx={3} fill={color} />
      {cuernos ? (
        <>
          <path d="M36,-64 q-8,-10 2,-16" stroke="#d9c7a0" strokeWidth={4} fill="none" />
          <path d="M50,-64 q8,-10 -2,-16" stroke="#d9c7a0" strokeWidth={4} fill="none" />
        </>
      ) : (
        <>
          <ellipse cx={38} cy={-66} rx={4} ry={11} fill={color} />
          <ellipse cx={48} cy={-66} rx={4} ry={11} fill={color} />
        </>
      )}
      <circle cx={50} cy={-44} r={2.6} fill="#2a1d14" />
    </g>
  );
};

const Estrella: React.FC<{ x: number; y: number; p: number; f: number }> = ({ x, y, p, f }) => {
  if (p <= 0) return null;
  const s = back(p);
  const pts = Array.from({ length: 10 }, (_, k) => { const r = k % 2 ? 13 : 34; const a = (k * Math.PI) / 5 - Math.PI / 2; return `${r * Math.cos(a)},${r * Math.sin(a)}`; }).join(" ");
  const tw = 0.8 + 0.2 * Math.sin(f * 0.14);
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`} opacity={Math.min(1, p * 2)}>
      <circle r={120} fill="url(#belenGlow)" opacity={tw} />
      <line x1={0} y1={34} x2={0} y2={150} stroke="#ffe9a8" strokeWidth={4} opacity={0.5 * tw} />
      <polygon points={pts} fill="#f7d98b" />
      <polygon points={pts} fill="#fff6dc" transform="scale(0.5)" />
    </g>
  );
};

export const BelenDefs: React.FC = () => (
  <defs>
    <radialGradient id="belenGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stopColor="#ffe9a8" stopOpacity="0.85" />
      <stop offset="0.4" stopColor="#f4c46a" stopOpacity="0.35" />
      <stop offset="1" stopColor="#f4c46a" stopOpacity="0" />
    </radialGradient>
    <radialGradient id="ninoGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stopColor="#fff6da" stopOpacity="0.95" />
      <stop offset="0.5" stopColor="#ffd56a" stopOpacity="0.4" />
      <stop offset="1" stopColor="#ffd56a" stopOpacity="0" />
    </radialGradient>
  </defs>
);

const Entorno: React.FC<{ p: number }> = ({ p }) => {
  if (p <= 0) return null;
  return (
    <g opacity={0.5 * Math.min(1, p)}>
      {[-430, -360, 400, 470].map((x, i) => (
        <g key={i} opacity={ap(p, i * 0.1, 0.5)}>
          <rect x={x - 26} y={100 - (i % 2 ? 40 : 10)} width={52} height={60 + (i % 2 ? 40 : 10)} fill="#241a3d" />
          <path d={`M ${x - 32},${100 - (i % 2 ? 40 : 10)} L ${x},${70 - (i % 2 ? 40 : 10)} L ${x + 32},${100 - (i % 2 ? 40 : 10)} Z`} fill="#2e2350" />
        </g>
      ))}
    </g>
  );
};

export const Nacimiento: React.FC<{ cx: number; cy: number; escala?: number; e: EstadoBelen; f: number; opacidad?: number }> = ({ cx, cy, escala = 1, e, f, opacidad = 1 }) => (
  <g transform={`translate(${cx} ${cy}) scale(${escala})`} opacity={opacidad}>
    <Entorno p={e.entorno} />
    {/* suelo */}
    <ellipse cx={0} cy={150} rx={520 * Math.min(1, e.portal * 2)} ry={48} fill="#000" opacity={0.3} />
    {/* estrella sobre el portal */}
    <Estrella x={0} y={-430} p={e.estrella} f={f} />
    {/* portal / establo */}
    {e.portal > 0 && (() => {
      const s = back(e.portal);
      return (
        <g transform={`scale(${s})`} opacity={Math.min(1, e.portal * 2)} style={{ transformOrigin: "0px 150px" }}>
          <path d="M -210,150 L -150,-250 L 150,-250 L 210,150 Z" fill="#1a1230" />
          <path d="M -230,-235 L 0,-320 L 230,-235 L 205,-200 L 0,-280 L -205,-200 Z" fill="#6b4a2a" />
          <rect x={-180} y={-210} width={22} height={360} fill="#5b3f24" />
          <rect x={158} y={-210} width={22} height={360} fill="#5b3f24" />
        </g>
      );
    })()}
    {/* animales detrás */}
    <Animal x={-120} y={120} flip={1} color="#b08d5a" cuernos p={e.animales} />
    <Animal x={120} y={120} flip={-1} color="#8a8f98" p={e.animales} />
    {/* Sagrada Familia */}
    <Figura x={-120} y={150} h={150} robe="#6b4a86" veil="#d9b3e0" halo lean={6} p={e.sagrada} />
    <Figura x={120} y={150} h={168} robe="#9a6a34" robe2="#b88a4a" halo lean={-4} p={e.sagrada} />
    {/* pesebre + Niño */}
    {e.pesebre > 0 && (() => {
      const s = back(e.pesebre);
      return (
        <g transform={`translate(0 92) scale(${s})`} opacity={Math.min(1, e.pesebre * 2)} style={{ transformOrigin: "0px 0px" }}>
          <circle cx={0} cy={-6} r={90} fill="url(#ninoGlow)" />
          <path d="M -60,30 L 60,30 L 44,-6 L -44,-6 Z" fill="#8a6230" />
          <path d="M -44,-6 L 44,-6 L 36,-20 L -36,-20 Z" fill="#e7cf84" />
          <line x1={-54} y1={30} x2={-30} y2={56} stroke="#6b4a24" strokeWidth={7} />
          <line x1={54} y1={30} x2={30} y2={56} stroke="#6b4a24" strokeWidth={7} />
          <g transform="translate(0 -16)">
            <circle cx={0} cy={0} r={13} fill="none" stroke="#f4c46a" strokeWidth={3} />
            <ellipse cx={0} cy={6} rx={22} ry={12} fill="#f7f1e2" />
            <circle cx={0} cy={-4} r={9} fill="#f3dcc0" />
          </g>
        </g>
      );
    })()}
    {/* ángel arriba-izquierda */}
    {e.angel > 0 && (() => {
      const s = back(e.angel);
      const fl = 1 + 0.03 * Math.sin(f * 0.1);
      return (
        <g transform={`translate(-300 -320) scale(${s * fl})`} opacity={Math.min(1, e.angel * 2)}>
          <path d="M -8,-70 Q -70,-96 -86,-48 Q -46,-56 -16,-26 Z" fill="#f3ead7" opacity={0.9} />
          <path d="M 8,-70 Q 70,-96 86,-48 Q 46,-56 16,-26 Z" fill="#f3ead7" opacity={0.9} />
          <Figura x={0} y={0} h={120} w={38} robe="#f3ead7" halo p={1} />
        </g>
      );
    })()}
    {/* pastores a la izquierda */}
    <g opacity={Math.min(1, e.pastores)}>
      <Figura x={-330} y={150} h={132} w={42} robe="#6b5235" p={ap(e.pastores, 0, 0.6)} />
      {e.pastores > 0 && <line x1={-296} y1={30} x2={-286} y2={150} stroke="#4a3620" strokeWidth={6} opacity={Math.min(1, e.pastores)} transform={`scale(${back(ap(e.pastores,0,0.6))})`} style={{ transformOrigin: "-330px 150px" }} />}
      <Figura x={-250} y={150} h={110} w={36} robe="#7d6342" p={ap(e.pastores, 0.3, 0.6)} />
    </g>
    {/* Reyes Magos a la derecha, acercándose */}
    <g opacity={Math.min(1, e.reyes)}>
      {[["#5a3b86", 300, 150, 0], ["#2f6d49", 360, 150, 0.2], ["#8a2f3a", 420, 150, 0.4]].map(([c, x, y, dly], i) => {
        const pp = ap(e.reyes, dly as number, 0.6);
        const sx = interpolate(e.reyes, [0, 1], [120, 0], CL);
        return (
          <g key={i} transform={`translate(${sx} 0)`}>
            <Figura x={x as number} y={y as number} h={130 + i * 6} w={40} robe={c as string} p={pp} />
            {pp > 0 && <g transform={`translate(${x} ${(y as number) - 150}) scale(${back(pp)})`}><polygon points="-16,0 -8,-16 0,-6 8,-16 16,0" fill="#f4c46a" /></g>}
          </g>
        );
      })}
    </g>
  </g>
);
