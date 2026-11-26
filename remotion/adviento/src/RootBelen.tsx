import React from 'react';
import {Composition} from 'remotion';
import {Belen, FIN_BELEN} from './belen/Belen';
export const RootBelen: React.FC = () => (
  <Composition id="belen" component={Belen} durationInFrames={Math.round(FIN_BELEN*30)} fps={30} width={1080} height={1920} />
);
