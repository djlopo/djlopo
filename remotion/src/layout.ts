import timings from './timings.json';

export const FPS = 30;
export const SELLO = 120;   // 4 s portada
export const HEAD = 15;     // 0.5 s antes de la voz
export const TAIL = 24;     // 0.8 s de respiro tras la voz
export const CLOSE = 90;    // 3 s cierre

export type Section = {id: string; img: string; audio: string; dur: number};
export const SECTIONS: Section[] = (timings as any).sections;

export const sceneFrames = (dur: number) => Math.round(dur * FPS) + HEAD + TAIL;
export const TOTAL = SELLO + SECTIONS.reduce((a, s) => a + sceneFrames(s.dur), 0) + CLOSE;
