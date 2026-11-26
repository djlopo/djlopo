import { Audio } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import SUBS from "../subs/adviento.json";
import DATOS from "../datos.json";
import { cargarFuentes, TIT, TXT } from "./fonts";
import { ALTO_VELA, Corona, Defs, Llama, RX, RY, Vela, type EstadoCorona } from "./Corona";

/*
 * «La corona de Adviento» · vertical 1080×1920, ~64 s.
 * Estilo propio: noche ciruela, luz de vela y verde abeto.
 * Tipografia del canal (Fraunces + Nunito) alojada en /public.
 * Incluye el detalle de las bayas rojas y un cierre de marca «Tu Oracion Diaria».
 */

cargarFuentes();

const K = {
  noche: "#160f2b",
  ciruela: "#2c1c4d",
  marfil: "#f8eedd",
  oro: "#f4c46a",
  rosa: "#f2a5c6",
  morado: "#a77be0",
  verde: "#6fc28a",
  rojo: "#e65a6b",
  tenue: "rgba(248,238,221,0.62)",
};

type Escena = { rs: number; re: number; ns: number; ne: number };
const SC = DATOS.scenes as Escena[];
const V = DATOS.V; // la voz entra a los 0,3 s
// remapea un segundo de la narración de referencia al timeline real de las voces
function remap(x: number): number {
  const seg = (s: Escena) => s.ns + ((x - s.rs) * (s.ne - s.ns)) / (s.re - s.rs);
  if (x <= SC[0].rs) return seg(SC[0]);
  for (const s of SC) if (x <= s.re) return seg(s);
  return seg(SC[SC.length - 1]);
}
const T = (x: number) => V + remap(x);
export const FIN_ADVIENTO = DATOS.fin;

type Palabra = { t: string; a: number; b: number };
const TROZOS = (SUBS as Palabra[][]).map((tr) => tr.map((p) => ({ ...p, a: p.a + V, b: p.b + V })));

const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SALIDA = Easing.bezier(0.16, 1, 0.3, 1);
const e = (s: number, a: number, d = 0.6) => interpolate(s, [a, a + d], [0, 1], { ...CL, easing: SALIDA });
const ventana = (s: number, a: number, b: number, f = 0.35) =>
  Math.min(interpolate(s, [a, a + f], [0, 1], CL), interpolate(s, [b - f, b], [1, 0], CL));

// ---------- Escenas (inicio de cada una) ----------
const E = {
  gancho: 0,
  que: T(3.7),
  origen: T(11.5),
  circulo: T(21.45),
  velas: T(28.3),
  encender: T(33.25),
  blanca: T(45.8),
  hacer: T(49.85),
  cierre: T(57.65),
};

// ---------- Piezas de texto ----------

/** Frase que entra palabra a palabra (sube y se enfoca). */
const Frase: React.FC<{
  s: number;
  a: number;
  texto: string;
  top: number;
  size?: number;
  color?: string;
  oro?: string[];
  rojo?: string[];
  fuente?: string;
  peso?: number;
}> = ({ s, a, texto, top, size = 82, color = K.marfil, oro = [], rojo = [], fuente = TIT, peso = 600 }) => (
  <div
    style={{
      position: "absolute",
      top,
      left: 60,
      right: 60,
      textAlign: "center",
      fontFamily: fuente,
      fontWeight: peso,
      fontSize: size,
      lineHeight: 1.08,
      color,
      textShadow: "0 6px 30px rgba(0,0,0,0.45)",
    }}
  >
    {texto.split(" ").map((w, i) => {
      const p = e(s, a + i * 0.07, 0.55);
      const limpio = w.replace(/[.,:;¿?¡!«»]/g, "");
      const col = oro.includes(limpio) ? K.oro : rojo.includes(limpio) ? K.rojo : undefined;
      return (
        <span
          key={i}
          style={{
            display: "inline-block",
            marginRight: "0.24em",
            opacity: p,
            transform: `translateY(${(1 - p) * 40}px)`,
            filter: `blur(${(1 - p) * 8}px)`,
            color: col,
          }}
        >
          {w}
        </span>
      );
    })}
  </div>
);

/** Pildora pequeña (fecha, etiqueta). */
const Chip: React.FC<{ s: number; a: number; children: React.ReactNode; top: number; color?: string }> = ({
  s,
  a,
  children,
  top,
  color = K.oro,
}) => {
  const p = e(s, a, 0.5);
  const pop = Easing.out(Easing.back(2.4))(Math.min(1, interpolate(s, [a, a + 0.4], [0, 1], CL)));
  return (
    <div style={{ position: "absolute", top, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: p }}>
      <div
        style={{
          transform: `scale(${0.6 + 0.4 * pop})`,
          border: `3px solid ${color}`,
          color,
          background: "rgba(22,15,43,0.55)",
          borderRadius: 999,
          padding: "12px 30px",
          fontFamily: TXT,
          fontWeight: 900,
          fontSize: 40,
          letterSpacing: "0.04em",
          display: "flex",
          alignItems: "center",
          gap: 14,
        }}
      >
        {children}
      </div>
    </div>
  );
};

// ---------- Fondo ----------

const MOTAS = Array.from({ length: 34 }, (_, i) => ({
  x: random("mx" + i) * 1080,
  y: random("my" + i) * 1920,
  r: 2 + random("mr" + i) * 7,
  v: 8 + random("mv" + i) * 22,
  fase: random("mf" + i) * 6,
}));

const Fondo: React.FC<{ s: number; calor: number }> = ({ s, calor }) => (
  <AbsoluteFill style={{ background: `radial-gradient(120% 80% at 50% 45%, ${K.ciruela} 0%, ${K.noche} 70%)` }}>
    <AbsoluteFill
      style={{
        background: `radial-gradient(55% 34% at 50% 52%, rgba(255,170,80,${0.05 + 0.22 * calor}) 0%, rgba(255,140,60,0) 100%)`,
      }}
    />
    <svg width={1080} height={1920} style={{ position: "absolute" }}>
      {MOTAS.map((m, i) => {
        const y = (((m.y - s * m.v) % 1920) + 1920) % 1920;
        const o = 0.18 + 0.22 * Math.sin(s * 1.4 + m.fase);
        return <circle key={i} cx={m.x + Math.sin(s * 0.5 + m.fase) * 14} cy={y} r={m.r} fill="#ffd9a0" opacity={o} />;
      })}
    </svg>
  </AbsoluteFill>
);

// ---------- Estado de la corona según el segundo ----------

const lit = (s: number, a: number) => (s >= a ? Math.min(1, (s - a) / 0.45) : 0);

function corona(s: number): { e: EstadoCorona; op: number } | null {
  const visible = s < E.que + 0.1 || (s >= E.circulo + 4.2 && s < E.hacer + 0.35) || s >= E.cierre - 0.1;
  if (!visible) return null;
  if (s < E.que + 0.1) {
    return {
      op: ventana(s, -1, E.que + 0.1),
      e: { crece: 1, aparece: [1, 1, 1, 1], luz: [lit(s, T(1.55)), 0, 0, 0], cerilla: interpolate(s, [T(0.45), T(2.6)], [0, 1], CL) },
    };
  }
  if (s >= E.cierre - 0.1) {
    return { op: e(s, E.cierre - 0.1, 0.5) * 0.5, e: { crece: 1, aparece: [1, 1, 1, 1], luz: [lit(s, T(59.75)), 0, 0, 0] } };
  }
  const crece = interpolate(s, [T(25.5), T(27.6)], [0, 1], CL);
  const cae = (a: number) => interpolate(s, [a, a + 0.55], [0, 1], CL);
  return {
    op: Math.min(interpolate(s, [E.circulo + 4.2, E.circulo + 4.5], [0, 1], CL), interpolate(s, [E.hacer, E.hacer + 0.35], [1, 0], CL)),
    e: {
      crece,
      aparece: [cae(T(30.05)), cae(T(30.35)), cae(T(31.35)), cae(T(30.65))],
      luz: [lit(s, T(34.45)), lit(s, T(36.4)), lit(s, T(39.6)), lit(s, T(43.6))],
      blanca: { aparece: interpolate(s, [T(46.0), T(46.7)], [0, 1], CL), luz: lit(s, T(48.85)) },
    },
  };
}

// ---------- Escenas ----------

const Gancho: React.FC<{ s: number }> = ({ s }) => (
  <AbsoluteFill style={{ opacity: ventana(s, -1, E.que) }}>
    <Chip s={s} a={T(0.0)} top={250}>
      DOMINGO 29 NOV
    </Chip>
    <Frase s={s} a={T(0.15)} top={360} texto="Este domingo se enciende la primera vela" oro={["primera", "vela"]} size={84} />
    <Frase s={s} a={T(2.6)} top={1200} texto="¿Sabes por qué?" size={92} color={K.oro} />
  </AbsoluteFill>
);

const FECHAS = ["29 nov", "6 dic", "13 dic", "20 dic"];

const QueEs: React.FC<{ s: number; f: number }> = ({ s, f }) => {
  const op = ventana(s, E.que, E.origen);
  const venida = e(s, T(7.9), 0.7);
  return (
    <AbsoluteFill style={{ opacity: op, transform: `scale(${1.04 - 0.04 * e(s, E.que, 0.8)})` }}>
      <Frase s={s} a={T(3.84)} top={240} texto="La corona de Adviento" oro={["Adviento"]} size={92} />
      <svg width={1080} height={420} style={{ position: "absolute", top: 500 }}>
        <line x1={110} y1={150} x2={970} y2={150} stroke={K.tenue} strokeWidth={4} strokeDasharray="4 14" strokeLinecap="round" opacity={e(s, T(4.6))} />
        {FECHAS.map((d, i) => {
          const a = T(4.95) + i * 0.33;
          const p = e(s, a, 0.45);
          const x = 140 + i * 190;
          return (
            <g key={i} opacity={p} transform={`translate(${x} ${150}) scale(${0.5 + 0.5 * Easing.out(Easing.back(2))(p)})`}>
              <circle r={58} fill={i === 2 ? "#5a2a48" : "#3a2466"} stroke={i === 2 ? K.rosa : K.morado} strokeWidth={5} />
              <text y={18} textAnchor="middle" fontFamily={TIT} fontWeight={700} fontSize={54} fill={K.marfil}>
                {i + 1}
              </text>
              <text y={118} textAnchor="middle" fontFamily={TXT} fontWeight={800} fontSize={32} fill={K.tenue}>
                {d}
              </text>
            </g>
          );
        })}
        {(() => {
          const p = e(s, T(7.1), 0.6);
          const pop = Easing.out(Easing.back(2.5))(Math.min(1, interpolate(s, [T(7.1), T(7.5)], [0, 1], CL)));
          const pts = Array.from({ length: 10 }, (_, k) => {
            const r = k % 2 ? 30 : 70;
            const a = (k * Math.PI) / 5 - Math.PI / 2;
            return `${r * Math.cos(a)},${r * Math.sin(a)}`;
          }).join(" ");
          return (
            <g opacity={p} transform={`translate(930 150) scale(${pop}) rotate(${(1 - p) * -90 + Math.sin(f * 0.08) * 4})`}>
              <circle r={110} fill="url(#brilloHtml)" />
              <polygon points={pts} fill={K.oro} />
              <text y={128} textAnchor="middle" fontFamily={TXT} fontWeight={900} fontSize={34} fill={K.oro} transform={`rotate(${-((1 - p) * -90 + Math.sin(f * 0.08) * 4)})`}>
                25 dic
              </text>
            </g>
          );
        })()}
        <defs>
          <radialGradient id="brilloHtml">
            <stop offset="0" stopColor="#ffd37a" stopOpacity="0.55" />
            <stop offset="1" stopColor="#ffd37a" stopOpacity="0" />
          </radialGradient>
        </defs>
      </svg>
      <div style={{ position: "absolute", top: 1010, left: 0, right: 0, textAlign: "center", opacity: venida, transform: `translateY(${(1 - venida) * 50}px)` }}>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 118, color: K.marfil }}>Adviento</div>
        <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 40, color: K.tenue, marginTop: 6 }}>del latín adventus</div>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 96, color: K.oro, marginTop: 10, opacity: e(s, T(8.9), 0.5) }}>= «venida»</div>
      </div>
      <Chip s={s} a={T(10.1)} top={880}>
        TIEMPO DE ESPERAR
      </Chip>
    </AbsoluteFill>
  );
};

const Origen: React.FC<{ s: number; f: number }> = ({ s, f }) => {
  const op = ventana(s, E.origen, E.circulo);
  const anio = Math.round(interpolate(s, [T(12.75), T(14.4)], [1800, 1839], { ...CL, easing: Easing.out(Easing.cubic) }));
  const rueda = e(s, T(11.8), 0.9);
  const giro = interpolate(s, [T(11.8), T(16.5)], [-120, 0], { ...CL, easing: SALIDA });
  const R = 290;
  const dia = Math.max(0, Math.min(24, Math.floor(interpolate(s, [T(19.3), T(21.3)], [0, 24.99], CL))));
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Frase s={s} a={T(11.6)} top={230} texto="Hamburgo," size={84} />
      <div style={{ position: "absolute", top: 320, left: 0, right: 0, textAlign: "center", fontFamily: TIT, fontWeight: 700, fontSize: 150, color: K.oro, opacity: e(s, T(12.7), 0.4) }}>
        {anio}
      </div>
      <Chip s={s} a={T(14.75)} top={525} color={K.marfil}>
        JOHANN H. WICHERN · PASTOR
      </Chip>
      <svg width={1080} height={1920} style={{ position: "absolute", top: 0 }}>
        <Defs />
        <g transform={`translate(540 1010) rotate(${giro}) scale(${0.6 + 0.4 * rueda})`} opacity={rueda}>
          <circle r={R} fill="none" stroke="#7a4b2a" strokeWidth={36} />
          <circle r={R} fill="none" stroke="#a46b3d" strokeWidth={10} />
          {Array.from({ length: 10 }, (_, k) => (
            <line key={k} x1={0} y1={0} x2={(R - 10) * Math.cos((k * Math.PI) / 5)} y2={(R - 10) * Math.sin((k * Math.PI) / 5)} stroke="#8a5a34" strokeWidth={14} />
          ))}
          <circle r={46} fill="#6b3f22" stroke="#a46b3d" strokeWidth={8} />
        </g>
        {Array.from({ length: 28 }, (_, k) => {
          const grande = k % 7 === 0;
          const n = Math.floor(k - Math.floor(k / 7) - (grande ? 0 : 1));
          const a = (k / 28) * Math.PI * 2 - Math.PI / 2;
          const x = 540 + R * Math.cos(a);
          const y = 1010 + R * Math.sin(a);
          const ap = e(s, T(16.6) + k * 0.05, 0.4);
          const luz = grande ? 0 : dia > n ? 1 : 0;
          return (
            <g key={k} opacity={ap * rueda}>
              <Vela x={x} y={y + 14} color={grande ? "blanca" : "morado"} luz={0} aparece={1} f={f} semilla={k} escala={grande ? 0.42 : 0.26} />
              {!grande && <rect x={x - 7.3} y={y + 14 - ALTO_VELA * 0.26} width={14.6} height={ALTO_VELA * 0.26} rx={3} fill="#c62b35" />}
              <Llama x={x} y={y + 14 - ALTO_VELA * (grande ? 0.42 : 0.26) - 4} luz={luz} f={f} semilla={k * 1.7} escala={0.4} />
            </g>
          );
        })}
      </svg>
      <div style={{ position: "absolute", top: 1320, left: 0, right: 0, textAlign: "center", opacity: e(s, T(19.2), 0.4), fontFamily: TXT, fontWeight: 900, fontSize: 46, color: K.marfil }}>
        Día <span style={{ color: K.oro, fontSize: 64 }}>{Math.max(1, dia)}</span> de 24
      </div>
    </AbsoluteFill>
  );
};

const Circulo: React.FC<{ s: number }> = ({ s }) => {
  const op = ventana(s, E.circulo, E.velas, 0.4);
  const traza = e(s, T(21.6), 1.6);
  const aplasta = e(s, T(25.4), 1.1);
  const L = 2 * Math.PI * RX;
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <g transform={`translate(540 1080) scale(1 ${1 - (1 - RY / RX) * aplasta})`} opacity={1 - 0.85 * e(s, T(26.4), 0.8)}>
          <circle r={RX} fill="none" stroke={K.oro} strokeWidth={10} strokeDasharray={L} strokeDashoffset={L * (1 - traza)} strokeLinecap="round" transform="rotate(-90)" />
          {traza > 0 && traza < 1 && (
            <circle cx={RX * Math.cos(traza * Math.PI * 2 - Math.PI / 2)} cy={RX * Math.sin(traza * Math.PI * 2 - Math.PI / 2)} r={16} fill="#fff4d6" />
          )}
        </g>
      </svg>
      <div style={{ opacity: 1 - e(s, T(25.2), 0.4) }}>
        <Frase s={s} a={T(22.6)} top={280} texto="Sin principio ni fin" oro={["fin"]} size={88} />
        <Frase s={s} a={T(24.0)} top={1320} texto="como el amor de Dios" size={62} color={K.tenue} />
      </div>
      <Frase s={s} a={T(26.4)} top={270} texto="Verde: vida y esperanza" oro={["Verde:"]} size={82} />
      <Frase s={s} a={T(27.1)} top={1230} texto="y los frutos rojos, los del Edén" rojo={["frutos", "rojos,"]} oro={["Edén"]} size={60} />
    </AbsoluteFill>
  );
};

const Velas: React.FC<{ s: number }> = ({ s }) => {
  const op = ventana(s, E.velas, E.encender);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Frase s={s} a={T(28.56)} top={240} texto="Cuatro velas" oro={["Cuatro"]} size={96} />
      <div style={{ position: "absolute", top: 400, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 24 }}>
        {[
          ["3 moradas", K.morado, T(30.05)],
          ["1 rosa", K.rosa, T(31.3)],
        ].map(([t, c, a]) => {
          const p = e(s, a as number, 0.45);
          return (
            <div
              key={t as string}
              style={{
                opacity: p,
                transform: `scale(${0.6 + 0.4 * Easing.out(Easing.back(2.4))(p)})`,
                border: `3px solid ${c}`,
                color: c as string,
                borderRadius: 999,
                padding: "12px 30px",
                fontFamily: TXT,
                fontWeight: 900,
                fontSize: 44,
                background: "rgba(22,15,43,0.55)",
              }}
            >
              {t}
            </div>
          );
        })}
      </div>
      <Frase s={s} a={T(31.9)} top={1230} texto="Una por cada domingo" size={64} color={K.oro} />
    </AbsoluteFill>
  );
};

const DOMINGOS = [
  { a: T(33.36), n: "Domingo 1", d: "29 nov", w: "Esperanza", c: K.oro },
  { a: T(35.6), n: "Domingo 2", d: "6 dic", w: "Paz", c: K.oro },
  { a: T(38.88), n: "Domingo 3", d: "13 dic", w: "Alegría", c: K.rosa },
  { a: T(42.68), n: "Domingo 4", d: "20 dic", w: "Amor", c: K.oro },
];

const Encender: React.FC<{ s: number }> = ({ s }) => {
  const op = ventana(s, E.encender, E.blanca);
  const k = DOMINGOS.reduce((acc, d, i) => (s >= d.a ? i : acc), 0);
  const juntas = e(s, T(44.4), 0.5);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      {DOMINGOS.map((d, i) => {
        const dentro = e(s, d.a, 0.5);
        const sale = i < 3 ? e(s, DOMINGOS[i + 1].a - 0.25, 0.3) : 0;
        const o = Math.max(0, dentro - sale) * (1 - juntas);
        return (
          <div key={i} style={{ position: "absolute", top: 230, left: 0, right: 0, textAlign: "center", opacity: o, transform: `translateY(${(1 - dentro) * 50 - sale * 50}px)` }}>
            <div style={{ fontFamily: TXT, fontWeight: 900, fontSize: 42, color: K.tenue, letterSpacing: "0.05em" }}>
              {d.n.toUpperCase()} · {d.d.toUpperCase()}
            </div>
            <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 140, color: d.c, lineHeight: 1.1 }}>{d.w}</div>
            {i === 2 && <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 36, color: K.rosa, opacity: 0.85 }}>«ya queda poco»</div>}
          </div>
        );
      })}
      <div style={{ position: "absolute", top: 250, left: 0, right: 0, textAlign: "center", opacity: juntas }}>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 120, color: K.oro, lineHeight: 1.05 }}>Las cuatro,</div>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 120, color: K.marfil, lineHeight: 1.05 }}>juntas</div>
      </div>
      <div style={{ position: "absolute", top: 510, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 22, opacity: 1 - juntas }}>
        {DOMINGOS.map((d, i) => (
          <div key={i} style={{ width: 22, height: 22, borderRadius: 99, background: i <= k ? (i === 2 ? K.rosa : K.oro) : "rgba(248,238,221,0.2)" }} />
        ))}
      </div>
      <div style={{ opacity: 1 - e(s, T(42.4), 0.3) }}>
        <Chip s={s} a={T(37.15)} top={1180} color={K.marfil}>
          ↺ y vuelves a encender las anteriores
        </Chip>
      </div>
      <div
        style={{
          position: "absolute",
          top: 1395,
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: TXT,
          fontWeight: 700,
          fontSize: 28,
          color: K.tenue,
          opacity: e(s, T(34.5), 0.6) * 0.8,
        }}
      >
        Los nombres de las velas cambian según la tradición
      </div>
    </AbsoluteFill>
  );
};

const Blanca: React.FC<{ s: number }> = ({ s }) => (
  <AbsoluteFill style={{ opacity: ventana(s, E.blanca, E.hacer) }}>
    <Frase s={s} a={T(45.95)} top={250} texto="Y una vela blanca" oro={["blanca"]} size={92} />
    <Chip s={s} a={T(48.85)} top={420} color={K.marfil}>
      NOCHEBUENA · 24 DIC
    </Chip>
  </AbsoluteFill>
);

const ICONOS: Record<string, React.ReactNode> = {
  aro: <ellipse cx={0} cy={0} rx={86} ry={86} fill="none" stroke="#b98a55" strokeWidth={18} />,
  abeto: (
    <g>
      <line x1={-80} y1={60} x2={80} y2={-60} stroke="#5b3a22" strokeWidth={8} strokeLinecap="round" />
      {Array.from({ length: 9 }, (_, i) => {
        const t = -0.8 + i * 0.2;
        const x = t * 100;
        const y = -t * 75;
        return (
          <g key={i}>
            <line x1={x} y1={y} x2={x - 24} y2={y - 34} stroke="#3b8a52" strokeWidth={7} strokeLinecap="round" />
            <line x1={x} y1={y} x2={x + 30} y2={y + 22} stroke="#2b7244" strokeWidth={7} strokeLinecap="round" />
          </g>
        );
      })}
    </g>
  ),
  pinas: (
    <g>
      {[-45, 45].map((x) => (
        <g key={x} transform={`translate(${x} 0) rotate(${x > 0 ? 18 : -18})`}>
          <ellipse rx={36} ry={58} fill="#6b4226" />
          {[-36, -14, 8, 30].map((y) => (
            <path key={y} d={`M-30,${y} q30,14 60,0`} stroke="#3d2414" strokeWidth={4} fill="none" />
          ))}
        </g>
      ))}
    </g>
  ),
  velas: (
    <g>
      {[-66, -22, 22, 66].map((x, i) => (
        <rect key={x} x={x - 15} y={-60} width={30} height={120} rx={5} fill={i === 2 ? "#ec9cc0" : "#8455bf"} />
      ))}
    </g>
  ),
};

const MATERIALES = [
  { k: "aro", t: "Un aro", a: T(51.15) },
  { k: "abeto", t: "Ramas de abeto", a: T(51.75) },
  { k: "pinas", t: "Piñas", a: T(52.8) },
  { k: "velas", t: "4 velas", a: T(53.75) },
];

const Hacer: React.FC<{ s: number; f: number }> = ({ s, f }) => {
  const op = ventana(s, E.hacer, E.cierre);
  const aviso = e(s, T(54.7), 0.5);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Frase s={s} a={T(49.92)} top={240} texto="Cómo hacerla" oro={["hacerla"]} size={96} />
      <div style={{ position: "absolute", top: 420, left: 90, right: 90, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 30, opacity: 1 - 0.75 * aviso }}>
        {MATERIALES.map((m) => {
          const p = e(s, m.a, 0.45);
          const pop = Easing.out(Easing.back(2))(Math.min(1, interpolate(s, [m.a, m.a + 0.4], [0, 1], CL)));
          return (
            <div
              key={m.k}
              style={{
                height: 400,
                borderRadius: 36,
                background: "rgba(248,238,221,0.07)",
                border: "2px solid rgba(248,238,221,0.16)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 26,
                opacity: p,
                transform: `scale(${0.7 + 0.3 * pop})`,
              }}
            >
              <svg width={240} height={220} viewBox="-120 -110 240 220">
                {ICONOS[m.k]}
              </svg>
              <div style={{ fontFamily: TXT, fontWeight: 900, fontSize: 44, color: K.marfil }}>{m.t}</div>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", top: 700, left: 110, right: 110, opacity: aviso, transform: `translateY(${(1 - aviso) * 80}px) scale(${0.9 + 0.1 * aviso})` }}>
        <div
          style={{
            borderRadius: 40,
            background: "#2a1a1a",
            border: `4px solid ${K.oro}`,
            padding: "40px 40px 46px",
            textAlign: "center",
            boxShadow: "0 30px 80px rgba(0,0,0,0.5)",
          }}
        >
          <svg width={200} height={190} viewBox="-100 -150 200 190" style={{ overflow: "visible" }}>
            <Defs />
            <Llama x={0} y={0} luz={1} f={f} semilla={4} escala={1.2} />
          </svg>
          <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 70, color: K.oro, lineHeight: 1.1 }}>Nunca la dejes sola</div>
          <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 40, color: K.marfil, marginTop: 12 }}>encendida y sin nadie delante</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Cierre de marca «Tu Oración Diaria» ----------

const Cierre: React.FC<{ s: number }> = ({ s }) => {
  const base = e(s, E.cierre, 0.4);
  const guarda = e(s, T(58.9), 0.5);
  const late = 1 + 0.06 * Math.sin(Math.max(0, s - T(59.4)) * 6) * Math.exp(-Math.max(0, s - T(59.4)) * 0.5);
  // tarjeta de marca en los ~2,3 s finales (tras la narración de cierre)
  const marca = e(s, FIN_ADVIENTO - 2.3, 0.5);
  return (
    <AbsoluteFill style={{ opacity: base }}>
      {/* Cierre «Guárdalo» sobre la corona (formato original) */}
      <AbsoluteFill style={{ opacity: 1 - marca }}>
        <Frase s={s} a={T(58.4)} top={250} texto="Este domingo, enciende la primera" oro={["primera"]} size={82} />
        <div style={{ position: "absolute", top: 1290, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: guarda }}>
          <div
            style={{
              transform: `scale(${(0.7 + 0.3 * Easing.out(Easing.back(2))(guarda)) * late})`,
              display: "flex",
              alignItems: "center",
              gap: 16,
              background: K.oro,
              color: K.noche,
              borderRadius: 999,
              padding: "18px 40px",
              fontFamily: TXT,
              fontWeight: 900,
              fontSize: 46,
            }}
          >
            <svg width={34} height={42} viewBox="0 0 34 42">
              <path d="M3 3h28v36L17 29 3 39z" fill={K.noche} />
            </svg>
            Guárdalo
          </div>
        </div>
      </AbsoluteFill>
      {/* Tarjeta de marca (2 s finales): isotipo + handle */}
      <AbsoluteFill style={{ opacity: marca }}>
        <div style={{ position: "absolute", top: 430, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
          <Img src={staticFile("adviento/logo.png")} style={{ width: 220, height: 220, filter: "drop-shadow(0 10px 40px rgba(244,196,106,0.45))" }} />
        </div>
        <div style={{ position: "absolute", top: 700, left: 40, right: 40, textAlign: "center" }}>
          <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 86, color: K.marfil, lineHeight: 1.05 }}>
            Tu Oración <span style={{ color: K.oro }}>Diaria</span>
          </div>
        </div>
        <div style={{ position: "absolute", top: 900, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, background: K.oro, color: K.noche, borderRadius: 999, padding: "16px 34px", fontFamily: TXT, fontWeight: 900, fontSize: 42 }}>
            <svg width={44} height={32} viewBox="0 0 44 32">
              <rect width={44} height={32} rx={9} fill={K.noche} />
              <path d="M18 9l12 7-12 7z" fill={K.oro} />
            </svg>
            @tuoraciondiariatv
          </div>
        </div>
        <div style={{ position: "absolute", top: 1008, left: 0, right: 0, textAlign: "center", fontFamily: TXT, fontWeight: 800, fontSize: 32, color: K.tenue }}>
          vídeos completos en YouTube
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- Subtítulos (palabra a palabra, sobre la banda de IG) ----------

const Subtitulos: React.FC<{ s: number }> = ({ s }) => {
  const i = TROZOS.findIndex((tr, k) => {
    const fin = k + 1 < TROZOS.length ? Math.min(TROZOS[k + 1][0].a, tr[tr.length - 1].b + 0.6) : tr[tr.length - 1].b + 0.6;
    return s >= tr[0].a - 0.05 && s < fin;
  });
  if (i < 0) return null;
  return (
    <div style={{ position: "absolute", top: 1480, left: 70, right: 70, display: "flex", justifyContent: "center" }}>
      <div
        style={{
          background: "rgba(16,10,32,0.82)",
          border: "2px solid rgba(244,196,106,0.4)",
          borderRadius: 24,
          padding: "16px 30px",
          fontFamily: TXT,
          fontWeight: 900,
          fontSize: 50,
          lineHeight: 1.12,
          textAlign: "center",
          color: K.marfil,
          boxShadow: "0 12px 40px rgba(0,0,0,0.4)",
        }}
      >
        {TROZOS[i]
          .filter((p) => p.t)
          .map((p, k) => (
            <span key={k} style={{ color: s >= p.a && s < p.b + 0.08 ? K.oro : K.marfil }}>
              {k ? " " : ""}
              {p.t}
            </span>
          ))}
      </div>
    </div>
  );
};

// ---------- Sonido ----------

const Sfx: React.FC<{ n: string; en: number; g: number }> = ({ n, en, g }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.max(0, Math.round(en * fps))} durationInFrames={3 * fps} layout="none">
      <Audio src={staticFile(`adviento/${n}.mp3`)} volume={g} />
    </Sequence>
  );
};

const EFECTOS: [string, number, number][] = [
  ["cerilla", T(1.2), 0.9],
  ...[E.que, E.origen, E.circulo, E.velas, E.hacer, E.cierre].map((t) => ["whoosh", t - 0.25, 0.6] as [string, number, number]),
  ...[0, 1, 2, 3].map((i) => ["pop", T(4.95) + i * 0.33, 0.22] as [string, number, number]),
  ["campana", T(7.1), 0.7],
  ["pop", T(7.9), 0.22],
  ["pop", T(14.75), 0.22],
  ["pop", T(30.05), 0.2],
  ["pop", T(30.35), 0.2],
  ["pop", T(30.65), 0.2],
  ["pop", T(31.35), 0.24],
  ["cerilla", T(34.25), 0.8],
  ["cerilla", T(36.2), 0.8],
  ["cerilla", T(39.4), 0.8],
  ["cerilla", T(43.4), 0.8],
  ["campana", T(44.4), 0.9],
  ["cerilla", T(48.65), 0.8],
  ...MATERIALES.map((m) => ["pop", m.a, 0.24] as [string, number, number]),
  ["pop", T(54.7), 0.26],
  ["cerilla", T(59.55), 0.8],
  ["campana", T(61.2), 0.8],
];

const Musica: React.FC = () => {
  const { fps } = useVideoConfig();
  const tramos = TROZOS.map((t) => [t[0].a, t[t.length - 1].b] as const);
  return (
    <Audio
      src={staticFile("adviento/musica.mp3")}
      volume={(fr) => {
        const s = fr / fps;
        const lejos = Math.min(...tramos.map(([a, b]) => (s < a ? a - s : s > b ? s - b : 0) / 0.35), 1);
        const base = 0.15 + 0.12 * lejos;
        return base * interpolate(s, [0, 0.5], [0, 1], CL) * interpolate(s, [FIN_ADVIENTO - 1.8, FIN_ADVIENTO], [1, 0], CL);
      }}
    />
  );
};

// ---------- Composición ----------

export const Adviento: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = f / fps;
  const c = corona(s);
  const calor = c ? (c.e.luz.reduce((a, b) => a + b, 0) + (c.e.blanca?.luz ?? 0)) / 4 : 0.15;
  const zoom = 1 + 0.06 * e(s, E.encender, 12) - 0.06 * e(s, E.blanca, 1);
  return (
    <AbsoluteFill style={{ background: K.noche }}>
      <Fondo s={s} calor={calor} />
      {c && (
        <svg width={1080} height={1920} style={{ position: "absolute" }}>
          <Defs />
          <Corona cx={540} cy={1090} escala={zoom} e={c.e} f={f} opacidad={c.op} />
        </svg>
      )}
      {s < E.que + 0.1 && <Gancho s={s} />}
      {s >= E.que - 0.1 && s < E.origen + 0.1 && <QueEs s={s} f={f} />}
      {s >= E.origen - 0.1 && s < E.circulo + 0.1 && <Origen s={s} f={f} />}
      {s >= E.circulo - 0.1 && s < E.velas + 0.1 && <Circulo s={s} />}
      {s >= E.velas - 0.1 && s < E.encender + 0.1 && <Velas s={s} />}
      {s >= E.encender - 0.1 && s < E.blanca + 0.1 && <Encender s={s} />}
      {s >= E.blanca - 0.1 && s < E.hacer + 0.1 && <Blanca s={s} />}
      {s >= E.hacer - 0.1 && s < E.cierre + 0.1 && <Hacer s={s} f={f} />}
      {s >= E.cierre - 0.1 && <Cierre s={s} />}
      <Subtitulos s={s} />
      <Sequence from={Math.round(V * fps)} layout="none">
        <Audio src={staticFile("voz-adviento.mp3")} />
      </Sequence>
      <Musica />
      {EFECTOS.map(([n, t, g], i) => (
        <Sfx key={i} n={n} en={t} g={g} />
      ))}
    </AbsoluteFill>
  );
};
