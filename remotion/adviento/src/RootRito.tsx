import React from 'react';
import {Composition} from 'remotion';
import {Rito, FIN_RITO} from './rito/Rito';
export const RootRito: React.FC = () => (
  <Composition id="rito" component={Rito} durationInFrames={Math.round(FIN_RITO*30)} fps={30} width={1920} height={1080} />
);
