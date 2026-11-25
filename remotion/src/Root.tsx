import React from 'react';
import {Composition} from 'remotion';
import {Especial} from './Especial';
import {FPS, TOTAL} from './layout';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="especial"
      component={Especial}
      durationInFrames={TOTAL}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
