import { Audio } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import SUBS from "./subs.json";
import DATOS from "./datos.json";
import { cargarFuentes, TIT, TXT } from "../corona/fonts";
import { Tree, TreeDefs, type EstadoArbol } from "./Tree";

/* «El árbol de Navidad, ¿es cristiano?» · vertical 1080×1920.
   Mismo estilo que la corona (noche ciruela + oro). Tiempos directos por escena. */

cargarFuentes();

const K = {
  noche: "#160f2b", ciruela: "#2c1c4d", marfil: "#f8eedd", oro: "#f4c46a",
  rosa: "#f2a5c6", rojo: "#e65a6b", verde: "#6fc28a", tenue: "rgba(248,238,221,0.62)",
};

const V = DATOS.V;
const SC = (DATOS.scenes as { a: number; b: number }[]).map((x) => ({ a: V + x.a, b: V + x.b }));
export const FIN_ARBOL = DATOS.fin;

type Palabra = { t: string; a: number; b: number };
const TROZOS = (SUBS as Palabra[][]).map((tr) => tr.map((p) => ({ ...p, a: p.a + V, b: p.b + V })));

const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SAL = Easing.bezier(0.16, 1, 0.3, 1);
const e = (s: number, a: number, d = 0.6) => interpolate(s, [a, a + d], [0, 1], { ...CL, easing: SAL });
const ventana = (s: number, a: number, b: number, f = 0.4) =>
  Math.min(interpolate(s, [a, a + f], [0, 1], CL), interpolate(s, [b - f, b], [1, 0], CL));

// ---------- Texto ----------
const Frase: React.FC<{ s: number; a: number; texto: string; top: number; size?: number; color?: string; oro?: string[]; rojo?: string[]; fuente?: string; peso?: number }> =
({ s, a, texto, top, size = 82, color = K.marfil, oro = [], rojo = [], fuente = TIT, peso = 600 }) => (
  <div style={{ position: "absolute", top, left: 60, right: 60, textAlign: "center", fontFamily: fuente, fontWeight: peso, fontSize: size, lineHeight: 1.08, color, textShadow: "0 6px 30px rgba(0,0,0,0.45)" }}>
    {texto.split(" ").map((w, i) => {
      const p = e(s, a + i * 0.07, 0.55);
      const limpio = w.replace(/[.,:;¿?¡!«»]/g, "");
      const col = oro.includes(limpio) ? K.oro : rojo.includes(limpio) ? K.rojo : undefined;
      return <span key={i} style={{ display: "inline-block", marginRight: "0.24em", opacity: p, transform: `translateY(${(1 - p) * 40}px)`, filter: `blur(${(1 - p) * 8}px)`, color: col }}>{w}</span>;
    })}
  </div>
);

const Chip: React.FC<{ s: number; a: number; children: React.ReactNode; top: number; color?: string }> = ({ s, a, children, top, color = K.oro }) => {
  const p = e(s, a, 0.5);
  const pop = Easing.out(Easing.back(2.4))(Math.min(1, interpolate(s, [a, a + 0.4], [0, 1], CL)));
  return (
    <div style={{ position: "absolute", top, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: p }}>
      <div style={{ transform: `scale(${0.6 + 0.4 * pop})`, border: `3px solid ${color}`, color, background: "rgba(22,15,43,0.55)", borderRadius: 999, padding: "12px 30px", fontFamily: TXT, fontWeight: 900, fontSize: 38, letterSpacing: "0.04em" }}>{children}</div>
    </div>
  );
};

// ---------- Fondo ----------
const MOTAS = Array.from({ length: 30 }, (_, i) => ({ x: random("mx" + i) * 1080, y: random("my" + i) * 1920, r: 2 + random("mr" + i) * 6, v: 7 + random("mv" + i) * 20, fase: random("mf" + i) * 6 }));
const Fondo: React.FC<{ s: number; calor: number }> = ({ s, calor }) => (
  <AbsoluteFill style={{ background: `radial-gradient(120% 80% at 50% 48%, ${K.ciruela} 0%, ${K.noche} 70%)` }}>
    <AbsoluteFill style={{ background: `radial-gradient(60% 40% at 50% 62%, rgba(255,170,80,${0.04 + 0.2 * calor}) 0%, rgba(255,140,60,0) 100%)` }} />
    <svg width={1080} height={1920} style={{ position: "absolute" }}>
      {MOTAS.map((m, i) => {
        const y = (((m.y - s * m.v) % 1920) + 1920) % 1920;
        return <circle key={i} cx={m.x + Math.sin(s * 0.5 + m.fase) * 14} cy={y} r={m.r} fill="#ffd9a0" opacity={0.16 + 0.2 * Math.sin(s * 1.4 + m.fase)} />;
      })}
    </svg>
  </AbsoluteFill>
);

// ---------- Estado del árbol ----------
function arbol(s: number): { e: EstadoArbol; op: number } | null {
  if (s < SC[2].a - 0.1) return null; // escenas 1-2 sin árbol
  const crece = interpolate(s, [SC[2].a, SC[2].a + 1.7], [0, 1], CL);
  const esferas = interpolate(s, [SC[2].a + 3.6, SC[2].b], [0, 1], CL);
  const hostias = interpolate(s, [SC[3].a + 1.6, SC[3].b - 0.4], [0, 1], CL);
  const luces = interpolate(s, [SC[6].a + 0.6, SC[6].a + 5.2], [0, 1], CL);
  const estrella = interpolate(s, [SC[6].a + 5.6, SC[6].b - 0.6], [0, 1], CL);
  const fade = 1 - 0.55 * e(s, FIN_ARBOL - 2.3, 0.5); // atenúa el árbol bajo la tarjeta de marca
  return { op: e(s, SC[2].a - 0.1, 0.5) * fade, e: { crece, esferas, hostias, luces, estrella } };
}

// ---------- Escenas ----------
const Gancho: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[0].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, -1, SC[0].b) }}>
      <Chip s={s} a={a + 0.1} top={260}>EL ÁRBOL DE NAVIDAD</Chip>
      <Frase s={s} a={a + 0.5} top={420} texto="¿Es cristiano?" oro={["cristiano?"]} size={118} />
      <Frase s={s} a={a + 2.6} top={760} texto="Mucha gente cree que es pagano" size={56} color={K.tenue} />
      <Frase s={s} a={a + 4.4} top={1150} texto="Pero su historia es preciosa" oro={["preciosa"]} size={74} />
    </AbsoluteFill>
  );
};

const EdadMedia: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[1].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[1].a, SC[1].b) }}>
      <Frase s={s} a={a + 0.2} top={300} texto="Edad Media" oro={["Media"]} size={96} />
      <Frase s={s} a={a + 2.0} top={520} texto="los autos de Navidad" size={60} color={K.tenue} />
      <Chip s={s} a={a + 4.2} top={1180} color={K.marfil}>24 DIC · ADÁN Y EVA</Chip>
    </AbsoluteFill>
  );
};

const Paraiso: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[2].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[2].a, SC[2].b) }}>
      <Frase s={s} a={a + 0.2} top={250} texto="El árbol del Paraíso" oro={["Paraíso"]} size={82} />
      <Frase s={s} a={a + 4.0} top={1210} texto="manzanas rojas: el fruto del Edén" rojo={["manzanas", "rojas:"]} oro={["Edén"]} size={56} />
    </AbsoluteFill>
  );
};

const Hostias: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[3].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[3].a, SC[3].b) }}>
      <Frase s={s} a={a + 0.2} top={250} texto="Y hostias: Cristo nos redime" oro={["Cristo"]} size={72} />
      <Frase s={s} a={a + 3.6} top={1210} texto="del pecado… a la promesa cumplida" oro={["promesa"]} size={58} color={K.tenue} />
    </AbsoluteFill>
  );
};

const Bonifacio: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[4].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[4].a, SC[4].b) }}>
      <Chip s={s} a={a + 0.1} top={250} color={K.marfil}>CUENTA LA TRADICIÓN</Chip>
      <Frase s={s} a={a + 1.0} top={360} texto="San Bonifacio y el abeto" oro={["abeto"]} size={78} />
      <Frase s={s} a={a + 7.0} top={1180} texto="«Así es Cristo»: el árbol de la vida" oro={["vida"]} size={58} />
    </AbsoluteFill>
  );
};

const Perenne: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[5].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[5].a, SC[5].b) }}>
      <Frase s={s} a={a + 0.2} top={280} texto="Siempre verde" oro={["verde"]} size={92} />
      <Frase s={s} a={a + 2.2} top={1210} texto="como la vida eterna" oro={["eterna"]} size={66} color={K.tenue} />
    </AbsoluteFill>
  );
};

const Luces: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[6].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[6].a, SC[6].b) }}>
      <Frase s={s} a={a + 0.2} top={250} texto="Sus luces: Cristo, la luz del mundo" oro={["luz"]} size={70} />
      <Frase s={s} a={a + 6.2} top={1210} texto="y la estrella de Belén" oro={["estrella", "Belén"]} size={66} />
    </AbsoluteFill>
  );
};

const Vaticano: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[7].a;
  return (
    <AbsoluteFill style={{ opacity: ventana(s, SC[7].a, SC[7].b) }}>
      <Frase s={s} a={a + 0.2} top={260} texto="¿Pagano?" oro={["¿Pagano?"]} size={96} />
      <Frase s={s} a={a + 1.6} top={430} texto="El Vaticano pone el suyo" size={58} color={K.tenue} />
      <Chip s={s} a={a + 3.1} top={1180}>PLAZA DE SAN PEDRO</Chip>
    </AbsoluteFill>
  );
};

const Cierre: React.FC<{ s: number }> = ({ s }) => {
  const a = SC[8].a;
  const guarda = e(s, a + 7.5, 0.5);
  const late = 1 + 0.06 * Math.sin(Math.max(0, s - (a + 8)) * 6) * Math.exp(-Math.max(0, s - (a + 8)) * 0.5);
  const marca = e(s, FIN_ARBOL - 2.3, 0.5);
  return (
    <AbsoluteFill style={{ opacity: e(s, SC[8].a, 0.4) }}>
      <AbsoluteFill style={{ opacity: 1 - marca }}>
        <Frase s={s} a={a + 0.4} top={250} texto="Es un signo de Cristo" oro={["Cristo"]} size={82} />
        <div style={{ position: "absolute", top: 1250, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: guarda }}>
          <div style={{ transform: `scale(${(0.7 + 0.3 * Easing.out(Easing.back(2))(guarda)) * late})`, display: "flex", alignItems: "center", gap: 16, background: K.oro, color: K.noche, borderRadius: 999, padding: "18px 40px", fontFamily: TXT, fontWeight: 900, fontSize: 46 }}>
            <svg width={34} height={42} viewBox="0 0 34 42"><path d="M3 3h28v36L17 29 3 39z" fill={K.noche} /></svg>
            Guárdalo
          </div>
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: marca }}>
        <div style={{ position: "absolute", top: 430, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
          <Img src={staticFile("adviento/logo.png")} style={{ width: 220, height: 220, filter: "drop-shadow(0 10px 40px rgba(244,196,106,0.45))" }} />
        </div>
        <div style={{ position: "absolute", top: 700, left: 40, right: 40, textAlign: "center", fontFamily: TIT, fontWeight: 700, fontSize: 86, color: K.marfil, lineHeight: 1.05 }}>Tu Oración <span style={{ color: K.oro }}>Diaria</span></div>
        <div style={{ position: "absolute", top: 900, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, background: K.oro, color: K.noche, borderRadius: 999, padding: "16px 34px", fontFamily: TXT, fontWeight: 900, fontSize: 42 }}>
            <svg width={44} height={32} viewBox="0 0 44 32"><rect width={44} height={32} rx={9} fill={K.noche} /><path d="M18 9l12 7-12 7z" fill={K.oro} /></svg>
            @tuoraciondiariatv
          </div>
        </div>
        <div style={{ position: "absolute", top: 1008, left: 0, right: 0, textAlign: "center", fontFamily: TXT, fontWeight: 800, fontSize: 32, color: K.tenue }}>reza con nosotros esta Navidad</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- Subtítulos ----------
const Subtitulos: React.FC<{ s: number }> = ({ s }) => {
  const i = TROZOS.findIndex((tr, k) => {
    const fin = k + 1 < TROZOS.length ? Math.min(TROZOS[k + 1][0].a, tr[tr.length - 1].b + 0.6) : tr[tr.length - 1].b + 0.6;
    return s >= tr[0].a - 0.05 && s < fin;
  });
  if (i < 0) return null;
  return (
    <div style={{ position: "absolute", top: 1480, left: 70, right: 70, display: "flex", justifyContent: "center" }}>
      <div style={{ background: "rgba(16,10,32,0.82)", border: "2px solid rgba(244,196,106,0.4)", borderRadius: 24, padding: "16px 30px", fontFamily: TXT, fontWeight: 900, fontSize: 50, lineHeight: 1.12, textAlign: "center", color: K.marfil, boxShadow: "0 12px 40px rgba(0,0,0,0.4)" }}>
        {TROZOS[i].filter((p) => p.t).map((p, k) => (<span key={k} style={{ color: s >= p.a && s < p.b + 0.08 ? K.oro : K.marfil }}>{k ? " " : ""}{p.t}</span>))}
      </div>
    </div>
  );
};

// ---------- Sonido ----------
const Sfx: React.FC<{ n: string; en: number; g: number }> = ({ n, en, g }) => {
  const { fps } = useVideoConfig();
  return (<Sequence from={Math.max(0, Math.round(en * fps))} durationInFrames={3 * fps} layout="none"><Audio src={staticFile(`adviento/${n}.mp3`)} volume={g} /></Sequence>);
};
const EFECTOS: [string, number, number][] = [
  ...SC.map((sc) => ["whoosh", sc.a - 0.25, 0.55] as [string, number, number]),
  ["pop", SC[2].a + 3.8, 0.24], ["pop", SC[2].a + 4.4, 0.24],
  ["pop", SC[3].a + 1.8, 0.22], ["pop", SC[3].a + 2.4, 0.22],
  ["campana", SC[6].a + 5.6, 0.8],
  ["cerilla", SC[6].a + 0.8, 0.5],
  ["campana", SC[8].a + 8.0, 0.7],
];

const Musica: React.FC = () => {
  const { fps } = useVideoConfig();
  const tramos = TROZOS.map((t) => [t[0].a, t[t.length - 1].b] as const);
  return (<Audio src={staticFile("arbol/musica.mp3")} volume={(fr) => {
    const s = fr / fps;
    const lejos = Math.min(...tramos.map(([a, b]) => (s < a ? a - s : s > b ? s - b : 0) / 0.35), 1);
    return (0.15 + 0.12 * lejos) * interpolate(s, [0, 0.5], [0, 1], CL) * interpolate(s, [FIN_ARBOL - 1.8, FIN_ARBOL], [1, 0], CL);
  }} />);
};

// ---------- Composición ----------
export const Arbol: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = f / fps;
  const ar = arbol(s);
  const calor = ar ? (ar.e.luces * 0.7 + ar.e.estrella * 0.3) : 0.1;
  const zoom = 0.95 + 0.06 * e(s, SC[6].a, 10);
  return (
    <AbsoluteFill style={{ background: K.noche }}>
      <Fondo s={s} calor={calor} />
      {ar && (
        <svg width={1080} height={1920} style={{ position: "absolute" }}>
          <TreeDefs />
          <g opacity={ar.op}><Tree cx={540} cy={1180} escala={zoom} e={ar.e} f={f} /></g>
        </svg>
      )}
      {s < SC[0].b + 0.1 && <Gancho s={s} />}
      {s >= SC[1].a - 0.1 && s < SC[1].b + 0.1 && <EdadMedia s={s} />}
      {s >= SC[2].a - 0.1 && s < SC[2].b + 0.1 && <Paraiso s={s} />}
      {s >= SC[3].a - 0.1 && s < SC[3].b + 0.1 && <Hostias s={s} />}
      {s >= SC[4].a - 0.1 && s < SC[4].b + 0.1 && <Bonifacio s={s} />}
      {s >= SC[5].a - 0.1 && s < SC[5].b + 0.1 && <Perenne s={s} />}
      {s >= SC[6].a - 0.1 && s < SC[6].b + 0.1 && <Luces s={s} />}
      {s >= SC[7].a - 0.1 && s < SC[7].b + 0.1 && <Vaticano s={s} />}
      {s >= SC[8].a - 0.1 && <Cierre s={s} />}
      <Subtitulos s={s} />
      <Sequence from={Math.round(V * fps)} layout="none"><Audio src={staticFile("voz-arbol.mp3")} /></Sequence>
      <Musica />
      {EFECTOS.map(([n, t, g], i) => (<Sfx key={i} n={n} en={t} g={g} />))}
    </AbsoluteFill>
  );
};
