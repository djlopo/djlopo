import React from 'react';
import {Composition} from 'remotion';
import {Adviento, FIN_ADVIENTO} from './corona/Adviento';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="adviento"
      component={Adviento}
      durationInFrames={Math.round(FIN_ADVIENTO * 30)}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
