import React from 'react';
import {Composition, Folder} from 'remotion';
import './theme';
import {Mare, MARE_S} from './video/Mare';
import {TreSecondi, TRE_S} from './video/TreSecondi';
import {Regalato, REG_S} from './video/Regalato';
import {Rimini, RIM_S} from './video/Rimini';

const FPS = 30;
const V = [
  {id: 'R1-Mare', c: Mare, s: MARE_S},
  {id: 'R2-TreSecondi', c: TreSecondi, s: TRE_S},
  {id: 'R3-Regalato', c: Regalato, s: REG_S},
  {id: 'R8-Rimini', c: Rimini, s: RIM_S},
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
