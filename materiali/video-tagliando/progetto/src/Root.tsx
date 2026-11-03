import React from 'react';
import {Composition, Folder} from 'remotion';
import './theme';
import {CalcoloVideo, CALCOLO_S} from './video/Calcolo';
import {LancettaVideo, LANCETTA_S} from './video/Lancetta';
import {DiagnosiVideo, DIAGNOSI_S} from './video/Diagnosi';

const FPS = 30;
const V = [
  {id: 'V1-Calcolo', c: CalcoloVideo, s: CALCOLO_S},
  {id: 'V2-Lancetta', c: LancettaVideo, s: LANCETTA_S},
  {id: 'V3-Diagnosi', c: DiagnosiVideo, s: DIAGNOSI_S},
];

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Reel-9x16">
      {V.map((v) => <Composition key={v.id} id={`${v.id}-916`} component={v.c} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(v.s * FPS)} />)}
    </Folder>
    <Folder name="Feed-4x5">
      {V.map((v) => <Composition key={v.id} id={`${v.id}-45`} component={v.c} width={1080} height={1350} fps={FPS} durationInFrames={Math.round(v.s * FPS)} />)}
    </Folder>
  </>
);
