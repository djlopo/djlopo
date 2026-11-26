import React from "react";
import { Easing, interpolate, random } from "remotion";

/*
 * Árbol de Navidad (abeto) dibujado en SVG, estilo del canal: verde abeto,
 * esferas rojas (manzanas del Edén), hostias blancas, luces cálidas y
 * estrella dorada. Centrado en (0,0); altura ~820.
 */

export const ALTO = 760;
const VERDES = ["#1f5a35", "#2b7244", "#17492a", "#2f7d49"];

const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const back = (p: number) => Easing.out(Easing.back(2))(Math.min(1, Math.max(0, p)));

// ---- Tiers del abeto (de abajo arriba): [ancho, yTop, yBase] ----
const TIERS = [
  { w: 300, yTop: -70, yBase: 110 },
  { w: 250, yTop: -210, yBase: 10 },
  { w: 195, yTop: -340, yBase: -100 },
  { w: 135, yTop: -450, yBase: -210 },
];

/** Un piso del abeto con borde inferior festoneado (ramas colgantes). */
const Tier: React.FC<{ w: number; yTop: number; yBase: number; p: number; i: number }> = ({ w, yTop, yBase, p, i }) => {
  if (p <= 0) return null;
  const s = back(p);
  const n = 5; // festones
  let d = `M0 ${yTop} L ${-w} ${yBase} `;
  for (let k = 0; k < n; k++) {
    const x0 = -w + (2 * w * k) / n;
    const x1 = -w + (2 * w * (k + 1)) / n;
    const mid = (x0 + x1) / 2;
    d += `Q ${mid} ${yBase + 34} ${x1} ${yBase} `;
  }
  d += "Z";
  return (
    <g transform={`translate(0 ${(1 - s) * 30}) scale(${s})`} style={{ transformOrigin: `0px ${yTop}px` }} opacity={Math.min(1, p * 2)}>
      <path d={d} fill={VERDES[i % VERDES.length]} />
      <path d={d} fill="url(#arbolSombra)" opacity={0.5} />
      <path d={`M0 ${yTop} L ${-w * 0.5} ${yBase - 4}`} stroke="#3f9a5e" strokeWidth={6} opacity={0.35} strokeLinecap="round" />
    </g>
  );
};

export type EstadoArbol = {
  crece: number;    // 0→1 crecen los pisos
  esferas: number;  // 0→1 aparecen manzanas rojas
  hostias: number;  // 0→1 aparecen hostias blancas
  luces: number;    // 0→1 fracción de luces encendidas
  estrella: number; // 0→1 estrella
  opacidad?: number;
};

const LUCES = Array.from({ length: 22 }, (_, k) => {
  const tier = Math.floor(random("lt" + k) * 4);
  const t = TIERS[tier];
  const fx = (random("lx" + k) - 0.5) * 2;
  const y = interpolate(random("ly" + k), [0, 1], [t.yTop + 30, t.yBase - 6]);
  const wAt = t.w * (1 - (y - t.yTop) / (t.yBase - t.yTop)) * 0; // no usado
  const x = fx * (t.w * (0.85 - 0.6 * ((y - t.yTop) / (t.yBase - t.yTop))));
  return { x, y, o: k / 22, r: 5 + random("lr" + k) * 3 };
});

const ESFERAS = Array.from({ length: 11 }, (_, k) => {
  const tier = Math.floor(random("et" + k) * 4);
  const t = TIERS[tier];
  const y = interpolate(random("ey" + k), [0, 1], [t.yTop + 46, t.yBase - 10]);
  const x = (random("ex" + k) - 0.5) * 2 * (t.w * (0.8 - 0.55 * ((y - t.yTop) / (t.yBase - t.yTop))));
  return { x, y, o: k / 11, r: 13 + random("er" + k) * 4 };
});

const HOSTIAS = Array.from({ length: 8 }, (_, k) => {
  const tier = Math.floor(random("ht" + k) * 4);
  const t = TIERS[tier];
  const y = interpolate(random("hy" + k), [0, 1], [t.yTop + 46, t.yBase - 10]);
  const x = (random("hx" + k) - 0.5) * 2 * (t.w * (0.78 - 0.5 * ((y - t.yTop) / (t.yBase - t.yTop))));
  return { x, y, o: k / 8 };
});

export const TreeDefs: React.FC = () => (
  <defs>
    <linearGradient id="arbolSombra" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stopColor="#0c2a18" stopOpacity="0.7" />
      <stop offset="0.5" stopColor="#0c2a18" stopOpacity="0" />
      <stop offset="1" stopColor="#0c2a18" stopOpacity="0.5" />
    </linearGradient>
    <radialGradient id="luzCalida" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stopColor="#fff3cf" />
      <stop offset="0.4" stopColor="#ffd56a" />
      <stop offset="1" stopColor="#ffb028" stopOpacity="0" />
    </radialGradient>
    <radialGradient id="esferaRoja" cx="0.38" cy="0.34" r="0.7">
      <stop offset="0" stopColor="#ff7a86" />
      <stop offset="0.5" stopColor="#d7303f" />
      <stop offset="1" stopColor="#8e1620" />
    </radialGradient>
    <radialGradient id="estrellaGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stopColor="#ffe9a8" stopOpacity="0.9" />
      <stop offset="0.4" stopColor="#f4c46a" stopOpacity="0.4" />
      <stop offset="1" stopColor="#f4c46a" stopOpacity="0" />
    </radialGradient>
  </defs>
);

const Estrella: React.FC<{ p: number; f: number }> = ({ p, f }) => {
  if (p <= 0) return null;
  const s = back(p);
  const pts = Array.from({ length: 10 }, (_, k) => {
    const r = k % 2 ? 20 : 52;
    const a = (k * Math.PI) / 5 - Math.PI / 2;
    return `${r * Math.cos(a)},${r * Math.sin(a)}`;
  }).join(" ");
  const tw = 0.85 + 0.15 * Math.sin(f * 0.12);
  return (
    <g transform={`translate(0 ${-520}) scale(${s})`} opacity={Math.min(1, p * 2)}>
      <circle r={150} fill="url(#estrellaGlow)" opacity={tw} />
      <polygon points={pts} fill="#f7d98b" transform={`rotate(${(1 - p) * -120})`} />
      <polygon points={pts} fill="#fff6dc" transform="scale(0.5)" />
    </g>
  );
};

export const Tree: React.FC<{ cx: number; cy: number; escala?: number; e: EstadoArbol; f: number }> = ({ cx, cy, escala = 1, e, f }) => {
  const pTier = (i: number) => interpolate(e.crece, [i * 0.2, i * 0.2 + 0.45], [0, 1], CL);
  const op = e.opacidad ?? 1;
  return (
    <g transform={`translate(${cx} ${cy}) scale(${escala})`} opacity={op}>
      {/* sombra en el suelo */}
      <ellipse cx={0} cy={150} rx={240 * Math.min(1, e.crece * 2)} ry={44} fill="#000" opacity={0.3} />
      {/* tronco */}
      <rect x={-26} y={96} width={52} height={90} rx={8} fill="#6b4423" opacity={Math.min(1, e.crece * 3)} />
      {/* pisos */}
      {TIERS.map((t, i) => (
        <Tier key={i} {...t} i={i} p={pTier(i)} />
      ))}
      {/* hostias (discos blancos) */}
      {HOSTIAS.map((h, k) => {
        const p = interpolate(e.hostias, [h.o * 0.7, h.o * 0.7 + 0.3], [0, 1], CL);
        if (p <= 0) return null;
        return (
          <g key={"h" + k} transform={`translate(${h.x} ${h.y}) scale(${back(p)})`}>
            <circle r={13} fill="#f7f1e2" stroke="#d8c9a8" strokeWidth={2} />
            <circle r={6} fill="none" stroke="#cdbb92" strokeWidth={1.5} />
          </g>
        );
      })}
      {/* esferas rojas (manzanas del Edén) */}
      {ESFERAS.map((s, k) => {
        const p = interpolate(e.esferas, [s.o * 0.7, s.o * 0.7 + 0.3], [0, 1], CL);
        if (p <= 0) return null;
        return (
          <g key={"e" + k} transform={`translate(${s.x} ${s.y}) scale(${back(p)})`}>
            <ellipse cx={0} cy={s.r + 3} rx={s.r * 0.7} ry={3} fill="#000" opacity={0.25} />
            <circle r={s.r} fill="url(#esferaRoja)" />
            <circle cx={-s.r * 0.3} cy={-s.r * 0.35} r={s.r * 0.22} fill="#ffd0d4" opacity={0.85} />
          </g>
        );
      })}
      {/* luces cálidas */}
      {LUCES.map((l, k) => {
        const lit = interpolate(e.luces, [l.o * 0.85, l.o * 0.85 + 0.18], [0, 1], CL);
        if (lit <= 0) return null;
        const tw = 0.7 + 0.3 * Math.sin(f * 0.3 + k);
        return (
          <g key={"l" + k} transform={`translate(${l.x} ${l.y})`}>
            <circle r={26 * lit} fill="url(#luzCalida)" opacity={0.8 * lit * tw} style={{ mixBlendMode: "screen" }} />
            <circle r={l.r * (0.5 + 0.5 * lit)} fill="#fff4cf" opacity={lit} />
          </g>
        );
      })}
      <Estrella p={e.estrella} f={f} />
    </g>
  );
};
