import React from 'react';
import {Composition} from 'remotion';
import {Logo, LogoHoriz, PostA, PostB} from './marca/Slides';

const LogoTrans: React.FC = () => <Logo plain />;

export const RootMarca: React.FC = () => (
  <>
    <Composition id="logo" component={Logo} durationInFrames={1} fps={1} width={1080} height={1080} />
    <Composition id="logoTrans" component={LogoTrans} durationInFrames={1} fps={1} width={1080} height={1080} />
    <Composition id="logoHoriz" component={LogoHoriz} durationInFrames={1} fps={1} width={1600} height={620} />
    <Composition id="postA" component={PostA} durationInFrames={6} fps={1} width={1080} height={1350} />
    <Composition id="postB" component={PostB} durationInFrames={6} fps={1} width={1080} height={1350} />
  </>
);
