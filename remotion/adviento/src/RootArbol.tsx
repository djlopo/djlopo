import React from 'react';
import {Composition} from 'remotion';
import {Arbol, FIN_ARBOL} from './arbol/Arbol';
export const RootArbol: React.FC = () => (
  <Composition id="arbol" component={Arbol} durationInFrames={Math.round(FIN_ARBOL*30)} fps={30} width={1080} height={1920} />
);
