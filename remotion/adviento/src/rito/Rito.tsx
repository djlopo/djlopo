import { Audio } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import SUBS from "./subs.json";
import DATOS from "./datos.json";
import { cargarFuentes, TIT, TXT } from "../corona/fonts";
import { Corona, Defs, type EstadoCorona } from "../corona/Corona";

/* «Encendido de la 1ª vela de la Corona de Adviento — en familia» · 1920×1080.
   Rito guiado: oración a la izquierda (para rezar siguiendo), corona a la derecha. */
cargarFuentes();

const K = { noche: "#160f2b", ciruela: "#2c1c4d", marfil: "#f8eedd", oro: "#f4c46a", tenue: "rgba(248,238,221,0.6)" };
const V = DATOS.V;
const SC = (DATOS.scenes as { a: number; b: number }[]).map((x) => ({ a: V + x.a, b: V + x.b }));
export const FIN_RITO = DATOS.fin;
const LABELS = ["Bienvenida", "Señal de la cruz", "Palabra de Dios · Isaías 9", "Bendición de la corona", "Primera vela · la Esperanza", "Padrenuestro", "Oración y bendición", "Hasta el próximo domingo"];

type Palabra = { t: string; a: number; b: number };
const TROZOS = (SUBS as Palabra[][]).map((tr) => tr.map((p) => ({ ...p, a: p.a + V, b: p.b + V })));
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const MOTAS = Array.from({ length: 30 }, (_, i) => ({ x: random("mx" + i) * 1920, y: random("my" + i) * 1080, r: 2 + random("mr" + i) * 6, v: 6 + random("mv" + i) * 16, fase: random("mf" + i) * 6 }));
const Fondo: React.FC<{ s: number; calor: number }> = ({ s, calor }) => (
  <AbsoluteFill style={{ background: `radial-gradient(90% 120% at 74% 55%, ${K.ciruela} 0%, ${K.noche} 72%)` }}>
    <AbsoluteFill style={{ background: `radial-gradient(28% 40% at 74% 55%, rgba(255,170,80,${0.05 + 0.22 * calor}) 0%, rgba(255,140,60,0) 100%)` }} />
    <svg width={1920} height={1080} style={{ position: "absolute" }}>
      {MOTAS.map((m, i) => { const y = (((m.y - s * m.v) % 1080) + 1080) % 1080; return <circle key={i} cx={m.x + Math.sin(s * 0.5 + m.fase) * 12} cy={y} r={m.r} fill="#ffd9a0" opacity={0.14 + 0.18 * Math.sin(s * 1.2 + m.fase)} />; })}
    </svg>
  </AbsoluteFill>
);

function corona(s: number): EstadoCorona {
  const s5 = SC[4].a;
  const cerilla = s >= s5 + 1.4 && s < s5 + 4.2 ? interpolate(s, [s5 + 1.4, s5 + 3.4], [0, 1], CL) : s >= s5 + 4.2 ? 1 : 0;
  const luz0 = s >= s5 + 3.0 ? Math.min(1, (s - (s5 + 3.0)) / 0.6) : 0;
  return { crece: 1, aparece: [1, 1, 1, 1], luz: [luz0, 0, 0, 0], cerilla: cerilla > 0 && cerilla < 1 ? cerilla : null };
}

const Oracion: React.FC<{ s: number }> = ({ s }) => {
  const i = TROZOS.findIndex((tr, k) => {
    const fin = k + 1 < TROZOS.length ? Math.min(TROZOS[k + 1][0].a, tr[tr.length - 1].b + 0.8) : tr[tr.length - 1].b + 0.8;
    return s >= tr[0].a - 0.1 && s < fin;
  });
  if (i < 0) return null;
  const op = Math.min(interpolate(s, [TROZOS[i][0].a - 0.1, TROZOS[i][0].a + 0.3], [0, 1], CL), 1);
  return (
    <div style={{ position: "absolute", left: 110, top: 300, width: 1020, minHeight: 480, display: "flex", alignItems: "center", opacity: op }}>
      <div style={{ fontFamily: TIT, fontWeight: 600, fontSize: 64, lineHeight: 1.3, color: K.marfil, textShadow: "0 6px 30px rgba(0,0,0,0.5)" }}>
        {TROZOS[i].filter((p) => p.t).map((p, k) => (
          <span key={k} style={{ color: s >= p.a && s < p.b + 0.12 ? K.oro : K.marfil }}>{k ? " " : ""}{p.t}</span>
        ))}
      </div>
    </div>
  );
};

const Sfx: React.FC<{ n: string; en: number; g: number }> = ({ n, en, g }) => {
  const { fps } = useVideoConfig();
  return (<Sequence from={Math.max(0, Math.round(en * fps))} durationInFrames={3 * fps} layout="none"><Audio src={staticFile(`adviento/${n}.mp3`)} volume={g} /></Sequence>);
};
const Musica: React.FC = () => {
  const { fps } = useVideoConfig();
  return (<Audio src={staticFile("rito/musica.mp3")} volume={(fr) => {
    const s = fr / fps;
    return 0.12 * interpolate(s, [0, 1], [0, 1], CL) * interpolate(s, [FIN_RITO - 2, FIN_RITO], [1, 0], CL);
  }} />);
};

export const Rito: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = f / fps;
  const e = corona(s);
  const calor = e.luz[0] * 0.8;
  const ki = SC.reduce((acc, sc, k) => (s >= sc.a - 0.1 ? k : acc), 0);
  return (
    <AbsoluteFill style={{ background: K.noche }}>
      <Fondo s={s} calor={calor} />
      {/* cabecera */}
      <div style={{ position: "absolute", top: 70, left: 0, right: 0, textAlign: "center" }}>
        <div style={{ fontFamily: TXT, fontWeight: 900, fontSize: 30, letterSpacing: "0.12em", color: K.tenue }}>I DOMINGO DE ADVIENTO · ENCENDIDO DE LA 1ª VELA</div>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 48, color: K.oro, marginTop: 10 }}>{LABELS[ki]}</div>
      </div>
      {/* corona a la derecha */}
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <Defs />
        <Corona cx={1480} cy={640} escala={0.72} e={e} f={f} />
      </svg>
      {/* oración a la izquierda */}
      <Oracion s={s} />
      {/* marca */}
      <div style={{ position: "absolute", bottom: 46, left: 0, right: 0, display: "flex", alignItems: "center", justifyContent: "center", gap: 16 }}>
        <Img src={staticFile("adviento/logo.png")} style={{ width: 54, height: 54 }} />
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 32, color: K.marfil }}>Tu Oración <span style={{ color: K.oro }}>Diaria</span></div>
        <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 26, color: K.tenue, marginLeft: 10 }}>· youtube.com/@OracionDiariaHoyES</div>
      </div>
      <Sequence from={Math.round(V * fps)} layout="none"><Audio src={staticFile("voz-rito.mp3")} /></Sequence>
      <Musica />
      <Sfx n="cerilla" en={SC[4].a + 2.4} g={0.7} />
      <Sfx n="campana" en={SC[4].a + 3.2} g={0.5} />
      <Sfx n="campana" en={0.2} g={0.4} />
    </AbsoluteFill>
  );
};
