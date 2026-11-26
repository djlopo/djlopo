import React from "react";
import { Easing, interpolate, random } from "remotion";

/*
 * Corona de Adviento dibujada en SVG, vista de frente y un poco desde arriba:
 * el aro es una elipse (rx 300, ry 105) con el centro en (0,0) del grupo.
 * Las velas van en cuatro puntos del aro; el orden de encendido da la vuelta:
 * 1 delante-izquierda, 2 detrás-izquierda, 3 (rosa) detrás-derecha, 4
 * delante-derecha.
 */

export const RX = 300;
export const RY = 105;
const ANG = [158, 248, 338, 68].map((g) => (g * Math.PI) / 180);
export const POS_VELA = ANG.map((a) => ({ x: RX * Math.cos(a), y: RY * Math.sin(a) }));
export const COLOR_VELA = ["morado", "morado", "rosa", "morado"] as const;
export const ALTO_VELA = 210;

const VERDES = ["#1f5a35", "#2b7244", "#3b8a52", "#1a4a2c", "#4f9d5e"];

type Hoja = { x: number; y: number; rot: number; l: number; w: number; c: string; orden: number; delante: boolean };
const N = 190;
const HOJAS: Hoja[] = Array.from({ length: N }, (_, i) => {
  const th = (i / N) * Math.PI * 2 + (random("h" + i) - 0.5) * 0.06;
  const r = (random("r" + i) - 0.5) * 92;
  const x = (RX + r) * Math.cos(th);
  const y = (RY + r * 0.36) * Math.sin(th) - random("z" + i) * 24;
  const tang = (Math.atan2(RY * Math.cos(th), -RX * Math.sin(th)) * 180) / Math.PI;
  return {
    x,
    y,
    rot: tang + (random("o" + i) - 0.5) * 100,
    l: 44 + random("l" + i) * 26,
    w: 13 + random("w" + i) * 8,
    c: VERDES[Math.floor(random("c" + i) * VERDES.length)],
    orden: Math.min(0.999, i / N + random("d" + i) * 0.04),
    delante: Math.sin(th) >= -0.05,
  };
}).sort((a, b) => a.y - b.y);

const BAYAS = Array.from({ length: 14 }, (_, i) => {
  const th = (i / 14) * Math.PI * 2 + 0.2 + random("b" + i) * 0.3;
  return { x: (RX + 18) * Math.cos(th), y: (RY + 6) * Math.sin(th) - 14, orden: i / 14, delante: Math.sin(th) >= 0 };
});
const PINAS = [20, 100, 170, 250, 290].map((g, i) => {
  const th = (g * Math.PI) / 180;
  return { x: (RX - 4) * Math.cos(th), y: RY * Math.sin(th) - 10, rot: g + 70, orden: i / 5, delante: Math.sin(th) >= 0 };
});

export const Defs: React.FC = () => (
  <defs>
    {(
      [
        ["morado", "#4a2378", "#9a6dd0"],
        ["rosa", "#c45486", "#f6b4d0"],
        ["blanca", "#cfc3b1", "#fffaf1"],
      ] as const
    ).map(([id, osc, luz]) => (
      <linearGradient key={id} id={`vela-${id}`} x1="0" x2="1" y1="0" y2="0">
        <stop offset="0" stopColor={osc} />
        <stop offset="0.42" stopColor={luz} />
        <stop offset="1" stopColor={osc} />
      </linearGradient>
    ))}
    <radialGradient id="llama" cx="0.5" cy="0.72" r="0.6">
      <stop offset="0" stopColor="#fffbe8" />
      <stop offset="0.35" stopColor="#ffd56a" />
      <stop offset="0.75" stopColor="#ff8a24" />
      <stop offset="1" stopColor="#ff5a10" stopOpacity="0" />
    </radialGradient>
    <radialGradient id="brillo">
      <stop offset="0" stopColor="#ffd89a" stopOpacity="0.85" />
      <stop offset="0.35" stopColor="#ffb85a" stopOpacity="0.3" />
      <stop offset="1" stopColor="#ff9a3a" stopOpacity="0" />
    </radialGradient>
  </defs>
);

/** Llama con su brillo. `luz` 0→1 la hace crecer (con un pequeño rebote). */
export const Llama: React.FC<{ x: number; y: number; luz: number; f: number; semilla: number; escala?: number }> = ({
  x,
  y,
  luz,
  f,
  semilla,
  escala = 1,
}) => {
  if (luz <= 0) return null;
  const crece = Easing.out(Easing.back(2.2))(Math.min(1, luz));
  const sy = (1 + 0.07 * Math.sin(f * 0.83 + semilla) + 0.04 * Math.sin(f * 2.1 + semilla * 3)) * crece * escala;
  const sx = (1 + 0.05 * Math.sin(f * 1.3 + semilla * 2)) * crece * escala;
  const rot = 3.5 * Math.sin(f * 0.6 + semilla);
  return (
    <g transform={`translate(${x} ${y})`}>
      <circle r={190 * escala} fill="url(#brillo)" opacity={0.75 * Math.min(1, luz)} style={{ mixBlendMode: "screen" }} />
      <g transform={`rotate(${rot}) scale(${sx} ${sy})`}>
        <path d="M0,4 C17,-8 18,-38 0,-74 C-18,-38 -17,-8 0,4 Z" fill="url(#llama)" />
        <path d="M0,0 C7,-6 7,-20 0,-34 C-7,-20 -7,-6 0,0 Z" fill="#fffef6" opacity={0.9} />
        <ellipse cx={0} cy={-3} rx={4.5} ry={6} fill="#6fa8ff" opacity={0.55} />
      </g>
    </g>
  );
};

export const Vela: React.FC<{
  x: number;
  y: number;
  color: "morado" | "rosa" | "blanca";
  luz: number;
  aparece: number;
  f: number;
  semilla: number;
  escala?: number;
}> = ({ x, y, color, luz, aparece, f, semilla, escala = 1 }) => {
  if (aparece <= 0) return null;
  const w = 56 * escala;
  const h = ALTO_VELA * escala;
  const caida = Easing.out(Easing.back(1.4))(Math.min(1, aparece));
  const dy = -(1 - caida) * 620;
  const op = Math.min(1, aparece * 3);
  const top = { morado: "#8455bf", rosa: "#eea0c3", blanca: "#f6efe3" }[color];
  return (
    <g transform={`translate(${x} ${y + dy})`} opacity={op}>
      <ellipse cx={0} cy={2} rx={w * 0.7} ry={9} fill="#000" opacity={0.28} />
      <rect x={-w / 2} y={-h} width={w} height={h} rx={6} fill={`url(#vela-${color})`} />
      <ellipse cx={0} cy={-h} rx={w / 2} ry={8} fill={top} />
      <path d={`M${-w / 2 + 8},${-h + 2} q4,30 0,46 q-6,8 -6,-6 z`} fill={top} opacity={0.9} />
      <line x1={0} y1={-h} x2={0} y2={-h - 13} stroke="#2b1d14" strokeWidth={3.2} strokeLinecap="round" />
      {luz > 0 && <circle cx={0} cy={-h - 12} r={2.6} fill="#ffb347" />}
      <Llama x={0} y={-h - 10} luz={luz} f={f} semilla={semilla} escala={escala} />
    </g>
  );
};

const HojaSvg: React.FC<{ h: Hoja; p: number }> = ({ h, p }) => {
  if (p <= 0) return null;
  const s = Easing.out(Easing.back(1.8))(Math.min(1, p));
  return (
    <g transform={`translate(${h.x} ${h.y}) rotate(${h.rot}) scale(${s})`}>
      <path d={`M${-h.l / 2},0 Q0,${-h.w / 2} ${h.l / 2},0 Q0,${h.w / 2} ${-h.l / 2},0 Z`} fill={h.c} />
      <line x1={-h.l / 2 + 4} y1={0} x2={h.l / 2 - 4} y2={0} stroke="#0f3320" strokeWidth={1.2} opacity={0.5} />
    </g>
  );
};

const Pina: React.FC<{ x: number; y: number; rot: number; p: number }> = ({ x, y, rot, p }) => {
  if (p <= 0) return null;
  const s = Easing.out(Easing.back(2))(Math.min(1, p));
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
      <ellipse rx={30} ry={20} fill="#6b4226" />
      {[-16, -5, 6, 17].map((cx) => (
        <path key={cx} d={`M${cx},-16 q6,16 0,32`} stroke="#3d2414" strokeWidth={3} fill="none" />
      ))}
      <ellipse rx={30} ry={20} fill="none" stroke="#3d2414" strokeWidth={2} />
    </g>
  );
};

const Bayas: React.FC<{ x: number; y: number; p: number }> = ({ x, y, p }) => {
  if (p <= 0) return null;
  const s = Easing.out(Easing.back(2.5))(Math.min(1, p));
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      {[
        [0, 0],
        [13, 5],
        [5, 13],
      ].map(([a, b], i) => (
        <g key={i}>
          <circle cx={a} cy={b} r={8.5} fill="#c8202f" />
          <circle cx={a - 2.5} cy={b - 3} r={2.6} fill="#ff8b8b" opacity={0.9} />
        </g>
      ))}
    </g>
  );
};

export type EstadoCorona = {
  /** 0→1: las ramas crecen dando la vuelta al aro. */
  crece: number;
  /** Por vela: 0→1 cae a su sitio. */
  aparece: number[];
  /** Por vela: 0→1 se enciende. */
  luz: number[];
  /** Vela blanca del centro. */
  blanca?: { aparece: number; luz: number };
  /** Cerilla que entra hasta la vela 1 (0→1) o null. */
  cerilla?: number | null;
};

const Cerilla: React.FC<{ p: number; f: number }> = ({ p, f }) => {
  const meta = { x: POS_VELA[0].x + 8, y: POS_VELA[0].y - ALTO_VELA - 26 };
  const fuera = { x: 520, y: -560 };
  const k = p < 0.45 ? Easing.out(Easing.cubic)(p / 0.45) : p < 0.62 ? 1 : 1 - Easing.in(Easing.cubic)((p - 0.62) / 0.38);
  const x = interpolate(k, [0, 1], [fuera.x, meta.x]);
  const y = interpolate(k, [0, 1], [fuera.y, meta.y]);
  return (
    <g transform={`translate(${x} ${y}) rotate(40)`}>
      <rect x={-6} y={0} width={12} height={190} rx={3} fill="#e8c393" />
      <rect x={-6} y={0} width={4} height={190} rx={2} fill="#c79a62" />
      <ellipse cx={0} cy={0} rx={10} ry={14} fill="#7a1f1f" />
      <g transform="rotate(-40)">
        <Llama x={0} y={-4} luz={1} f={f} semilla={7} escala={0.75} />
      </g>
    </g>
  );
};

/** La corona completa en un grupo SVG centrado en (cx, cy). */
export const Corona: React.FC<{ cx: number; cy: number; escala?: number; e: EstadoCorona; f: number; opacidad?: number }> = ({
  cx,
  cy,
  escala = 1,
  e,
  f,
  opacidad = 1,
}) => {
  const pHoja = (o: number) => (e.crece >= 1 ? 1 : interpolate(e.crece, [o * 0.85, o * 0.85 + 0.15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const atras = HOJAS.filter((h) => !h.delante);
  const delante = HOJAS.filter((h) => h.delante);
  const vela = (i: number) => (
    <Vela key={i} x={POS_VELA[i].x} y={POS_VELA[i].y - 8} color={COLOR_VELA[i]} luz={e.luz[i] ?? 0} aparece={e.aparece[i] ?? 0} f={f} semilla={i * 2.7 + 1} />
  );
  return (
    <g transform={`translate(${cx} ${cy}) scale(${escala})`} opacity={opacidad}>
      <ellipse cx={0} cy={40} rx={RX + 80} ry={RY + 40} fill="#000" opacity={0.3 * Math.min(1, e.crece * 2)} />
      <ellipse cx={0} cy={0} rx={RX} ry={RY} fill="none" stroke="#173f27" strokeWidth={64} opacity={Math.min(1, e.crece * 3)} />
      {atras.map((h, i) => (
        <HojaSvg key={"a" + i} h={h} p={pHoja(h.orden)} />
      ))}
      {PINAS.filter((p) => !p.delante).map((p, i) => (
        <Pina key={"pa" + i} {...p} p={pHoja(0.3 + p.orden * 0.6)} />
      ))}
      {BAYAS.filter((b) => !b.delante).map((b, i) => (
        <Bayas key={"ba" + i} {...b} p={pHoja(0.2 + b.orden * 0.7)} />
      ))}
      {vela(1)}
      {vela(2)}
      {e.blanca && (
        <Vela x={0} y={-6} color="blanca" luz={e.blanca.luz} aparece={e.blanca.aparece} f={f} semilla={11} escala={1.15} />
      )}
      {delante.map((h, i) => (
        <HojaSvg key={"d" + i} h={h} p={pHoja(h.orden)} />
      ))}
      {PINAS.filter((p) => p.delante).map((p, i) => (
        <Pina key={"pd" + i} {...p} p={pHoja(0.3 + p.orden * 0.6)} />
      ))}
      {BAYAS.filter((b) => b.delante).map((b, i) => (
        <Bayas key={"bd" + i} {...b} p={pHoja(0.2 + b.orden * 0.7)} />
      ))}
      {vela(0)}
      {vela(3)}
      {e.cerilla != null && e.cerilla > 0 && e.cerilla < 1 && <Cerilla p={e.cerilla} f={f} />}
    </g>
  );
};
