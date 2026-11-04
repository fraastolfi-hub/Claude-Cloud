import React from 'react';
import {Composition} from 'remotion';
import './theme';
import {LibroVideo, LIBRO_S} from './video/Libro';

const FPS = 30;
export const RemotionRoot: React.FC = () => (
  <Composition id="Libro-6Passaggi-916" component={LibroVideo} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(LIBRO_S * FPS)} defaultProps={{musica: undefined as string | undefined}} />
);
