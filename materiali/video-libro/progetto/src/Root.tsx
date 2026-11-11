import React from 'react';
import {Composition} from 'remotion';
import './theme';
import {LibroVideo, LIBRO_S} from './video/Libro';
import {ReelPesche, ReelPrimaPagina, REEL1_S, REEL2_S} from './video/Reels';
import {ReelDomanda, ReelCommissione, ReelPassi, R1S, R2S, R3S, durata} from './video/AdsLibro';

const FPS = 30;
export const RemotionRoot: React.FC = () => (
  <>
  <Composition id="Libro-6Passaggi-916" component={LibroVideo} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(LIBRO_S * FPS)} defaultProps={{musica: undefined as string | undefined}} />
  <Composition id="Reel1-Pesche-916" component={ReelPesche} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(REEL1_S * FPS)} />
  <Composition id="Reel2-PrimaPagina-916" component={ReelPrimaPagina} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(REEL2_S * FPS)} />
  <Composition id="Ad-Libro-Domanda-916" component={ReelDomanda} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(durata(R1S) * FPS)} />
  <Composition id="Ad-Libro-Commissione-916" component={ReelCommissione} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(durata(R2S) * FPS)} />
  <Composition id="Ad-Libro-Passi-916" component={ReelPassi} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(durata(R3S) * FPS)} />
  </>
);
