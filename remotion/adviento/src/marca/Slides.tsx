import React from "react";
import { AbsoluteFill, Img, random, staticFile, useCurrentFrame } from "remotion";
import { cargarFuentes, TIT, TXT } from "../corona/fonts";

cargarFuentes();

export const K = {
  noche: "#160f2b", ciruela: "#2c1c4d", marfil: "#f8eedd", oro: "#f4c46a",
  rosa: "#f2a5c6", morado: "#a77be0", verde: "#6fc28a", tenue: "rgba(248,238,221,0.62)",
};

const Motas: React.FC = () => (
  <svg width="100%" height="100%" style={{ position: "absolute", inset: 0 }} viewBox="0 0 1080 1350" preserveAspectRatio="none">
    {Array.from({ length: 26 }, (_, i) => (
      <circle key={i} cx={random("x" + i) * 1080} cy={random("y" + i) * 1350}
        r={1.5 + random("r" + i) * 5} fill="#ffd9a0" opacity={0.1 + random("o" + i) * 0.22} />
    ))}
  </svg>
);

export const Fondo: React.FC<{ plain?: boolean; children?: React.ReactNode }> = ({ plain, children }) => (
  <AbsoluteFill style={{
    background: plain ? "transparent" : `radial-gradient(125% 85% at 50% 40%, ${K.ciruela} 0%, ${K.noche} 72%)`,
    fontFamily: TXT, color: K.marfil,
  }}>
    {!plain && <Motas />}
    {children}
  </AbsoluteFill>
);

// ---------- Iconos (oro, trazo) ----------
const G = K.oro;
const Sunrise: React.FC = () => (
  <svg width={190} height={190} viewBox="-100 -100 200 200" fill="none" stroke={G} strokeWidth={9} strokeLinecap="round">
    <line x1={-92} y1={55} x2={92} y2={55} /><path d="M-55 55 a55 55 0 0 1 110 0" fill={G} stroke="none" />
    {[-90, -55, 0, 55, 90].map((a, i) => { const r = (a * Math.PI) / 180; return <line key={i} x1={75 * Math.cos(r)} y1={-75 * Math.sin(r) + 55 - 110} x2={95 * Math.cos(r)} y2={-95 * Math.sin(r) + 55 - 110} transform="translate(0 110)" />; })}
  </svg>
);
const Book: React.FC = () => (
  <svg width={190} height={190} viewBox="-100 -100 200 200" fill="none" stroke={G} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round">
    <path d="M0 -58 C-28 -72 -70 -70 -86 -62 L-86 60 C-70 52 -28 54 0 66 C28 54 70 52 86 60 L86 -62 C70 -70 28 -72 0 -58 Z" />
    <line x1={0} y1={-58} x2={0} y2={66} />
    {[-30, -6, 18].map((y) => (<React.Fragment key={y}><line x1={-70} y1={y} x2={-18} y2={y + 4} strokeWidth={5} /><line x1={18} y1={y + 4} x2={70} y2={y} strokeWidth={5} /></React.Fragment>))}
  </svg>
);
const Rosary: React.FC = () => (
  <svg width={190} height={190} viewBox="-100 -100 200 200" fill={G} stroke="none">
    {Array.from({ length: 14 }, (_, k) => { const a = (k / 14) * Math.PI * 2; const x = 66 * Math.cos(a), y = 66 * Math.sin(a) - 16; return <circle key={k} cx={x} cy={y} r={k % 4 ? 7 : 11} />; })}
    <rect x={-6} y={54} width={12} height={46} rx={4} /><rect x={-24} y={70} width={48} height={12} rx={4} />
  </svg>
);
const Candle: React.FC = () => (
  <svg width={190} height={190} viewBox="-100 -100 200 200" fill={G} stroke="none">
    <rect x={-26} y={-26} width={52} height={110} rx={10} />
    <rect x={-3} y={-44} width={6} height={20} rx={3} />
    <path d="M0 -92 C24 -58 24 -44 0 -34 C-24 -44 -24 -58 0 -92 Z" />
  </svg>
);
const Halo: React.FC = () => (
  <svg width={190} height={190} viewBox="-100 -100 200 200" fill="none" stroke={G} strokeWidth={9} strokeLinecap="round">
    <ellipse cx={0} cy={-58} rx={62} ry={22} /><circle cx={0} cy={2} r={34} /><path d="M-66 92 a66 72 0 0 1 132 0" />
  </svg>
);
const Bell: React.FC<{ s?: number }> = ({ s = 38 }) => (
  <svg width={s} height={s} viewBox="-50 -50 100 100" fill={K.noche} stroke="none" style={{ marginRight: 6 }}>
    <path d="M0 -42 C26 -42 34 -20 34 4 C34 22 44 30 44 30 L-44 30 C-44 30 -34 22 -34 4 C-34 -20 -26 -42 0 -42 Z" />
    <circle cx={0} cy={42} r={9} />
  </svg>
);
const ICONS: Record<string, React.FC> = { sunrise: Sunrise, book: Book, rosary: Rosary, candle: Candle, halo: Halo };

// ---------- Logo ----------
export const Logo: React.FC<{ plain?: boolean }> = ({ plain }) => (
  <Fondo plain={plain}>
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ textAlign: "center" }}>
        <Img src={staticFile("adviento/logo.png")} style={{ width: 300, height: 300, filter: "drop-shadow(0 12px 46px rgba(244,196,106,0.4))" }} />
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 118, color: K.marfil, lineHeight: 1.0, marginTop: 10 }}>Tu Oración</div>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 118, color: K.oro, lineHeight: 1.05 }}>Diaria</div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 20, marginTop: 26 }}>
          <span style={{ width: 70, height: 2, background: K.tenue }} />
          <span style={{ fontFamily: TXT, fontWeight: 800, fontSize: 30, letterSpacing: "0.18em", color: K.tenue }}>CADA DÍA</span>
          <span style={{ width: 70, height: 2, background: K.tenue }} />
        </div>
      </div>
    </AbsoluteFill>
  </Fondo>
);

export const LogoHoriz: React.FC = () => (
  <Fondo plain>
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "row", gap: 40 }}>
      <Img src={staticFile("adviento/logo.png")} style={{ width: 260, height: 260 }} />
      <div>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 104, color: K.marfil, lineHeight: 1.0 }}>Tu Oración</div>
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 104, color: K.oro, lineHeight: 1.05 }}>Diaria</div>
        <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 28, letterSpacing: "0.16em", color: K.tenue, marginTop: 14 }}>EVANGELIO · ROSARIO · ORACIÓN</div>
      </div>
    </AbsoluteFill>
  </Fondo>
);

// ---------- Slides de carrusel ----------
type Slide = {
  kicker?: string; icon?: string; step?: number; title: string; titleOro?: string;
  body?: string; foot?: boolean; big?: boolean; date?: string;
};

const Pill: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ display: "inline-flex", alignItems: "center", gap: 10, border: `3px solid ${K.oro}`, color: K.oro, borderRadius: 999, padding: "10px 26px", fontFamily: TXT, fontWeight: 900, fontSize: 32, letterSpacing: "0.05em", background: "rgba(22,15,43,0.4)" }}>{children}</div>
);

const SlideView: React.FC<{ s: Slide }> = ({ s }) => {
  const Icon = s.icon ? ICONS[s.icon] : null;
  return (
    <Fondo>
      <AbsoluteFill style={{ padding: 96, alignItems: "center", justifyContent: "center", textAlign: "center" }}>
        {s.kicker && <div style={{ marginBottom: 34 }}><Pill>{s.kicker}</Pill></div>}
        {s.step != null && (
          <div style={{ width: 128, height: 128, borderRadius: 999, border: `4px solid ${K.oro}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: TIT, fontWeight: 700, fontSize: 78, color: K.oro, marginBottom: 30 }}>{s.step}</div>
        )}
        {Icon && <div style={{ marginBottom: 30 }}><Icon /></div>}
        <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: s.big ? 104 : 86, color: K.marfil, lineHeight: 1.08 }}>
          {s.title} {s.titleOro && <span style={{ color: K.oro }}>{s.titleOro}</span>}
        </div>
        {s.date && <div style={{ fontFamily: TXT, fontWeight: 900, fontSize: 46, color: K.oro, marginTop: 24 }}>{s.date}</div>}
        {s.body && <div style={{ fontFamily: TXT, fontWeight: 700, fontSize: 44, color: K.tenue, lineHeight: 1.35, marginTop: 28, maxWidth: 820 }}>{s.body}</div>}
        {s.foot && (
          <div style={{ position: "absolute", bottom: 90, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
            <Img src={staticFile("adviento/logo.png")} style={{ width: 92, height: 92 }} />
            <div style={{ display: "flex", alignItems: "center", background: K.oro, color: K.noche, borderRadius: 999, padding: "14px 32px", fontFamily: TXT, fontWeight: 900, fontSize: 40 }}>
              <Bell /> @tuoraciondiariatv
            </div>
            <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 30, color: K.tenue }}>vídeos completos en YouTube</div>
          </div>
        )}
      </AbsoluteFill>
    </Fondo>
  );
};

export const POST_A: Slide[] = [
  { kicker: "BIENVENIDA", title: "Reza con nosotros,", titleOro: "cada día", body: "Tu día con Dios, en tres momentos →", big: true },
  { icon: "sunrise", title: "Laudes", body: "La oración de la mañana de la Iglesia, en vídeo." },
  { icon: "book", title: "Evangelio", titleOro: "del día", body: "Las lecturas de la Misa y una breve reflexión." },
  { icon: "rosary", title: "Santo Rosario", body: "Cada noche, con la Palabra en cada misterio." },
  { icon: "halo", title: "Santos y", titleOro: "Adviento", body: "Vidas de santos y especiales del tiempo litúrgico." },
  { title: "Empezamos", titleOro: "este domingo", date: "I Domingo de Adviento · 29 nov", foot: true, big: true },
];

export const POST_B: Slide[] = [
  { kicker: "GUÁRDALO", title: "Cómo rezar", titleOro: "cada día", body: "Tu rutina con nosotros, en 3 pasos →", big: true },
  { step: 1, icon: "sunrise", title: "Mañana", body: "Laudes — la oración con la que amanece la Iglesia." },
  { step: 2, icon: "book", title: "Mediodía", body: "Evangelio del día y una breve reflexión." },
  { step: 3, icon: "rosary", title: "Noche", body: "Santo Rosario para cerrar el día." },
  { icon: "candle", title: "Y este domingo,", titleOro: "el Adviento", body: "Un rito de encendido cada domingo hasta Navidad." },
  { title: "Reza con", titleOro: "nosotros", body: "1 · Laudes   2 · Evangelio   3 · Rosario", foot: true, big: true },
];

export const PostA: React.FC = () => <SlideView s={POST_A[useCurrentFrame()]} />;
export const PostB: React.FC = () => <SlideView s={POST_B[useCurrentFrame()]} />;

// ---------- Tarjeta de versículo (post de feed) ----------
export const Verso: React.FC = () => (
  <Fondo>
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", padding: 90, textAlign: "center" }}>
      <div style={{ position: "absolute", top: 150 }}><Pill>I DOMINGO DE ADVIENTO</Pill></div>
      <div style={{ fontFamily: TIT, fontWeight: 700, fontSize: 210, color: K.oro, lineHeight: 1, textShadow: "0 8px 40px rgba(0,0,0,0.5)" }}>«Velad»</div>
      <div style={{ fontFamily: TIT, fontWeight: 600, fontSize: 60, color: K.marfil, lineHeight: 1.25, marginTop: 36, maxWidth: 860 }}>
        porque no sabéis qué día vendrá vuestro Señor
      </div>
      <div style={{ fontFamily: TXT, fontWeight: 800, fontSize: 40, color: K.tenue, letterSpacing: "0.06em", marginTop: 40 }}>MATEO 24, 42</div>
      <div style={{ position: "absolute", bottom: 110, display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
        <Img src={staticFile("adviento/logo.png")} style={{ width: 78, height: 78 }} />
        <div style={{ fontFamily: TXT, fontWeight: 900, fontSize: 34, color: K.marfil }}>@tuoraciondiariatv</div>
      </div>
    </AbsoluteFill>
  </Fondo>
);
