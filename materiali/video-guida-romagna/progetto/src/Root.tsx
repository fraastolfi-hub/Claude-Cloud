import React from 'react';
import {Composition, Folder} from 'remotion';
import './theme';
import {Mare, MARE_S} from './video/Mare';
import {TreSecondi, TRE_S} from './video/TreSecondi';
import {Regalato, REG_S} from './video/Regalato';
import {Rimini, RIM_S} from './video/Rimini';
import {Reel1, Reel5} from './reel/Girato';
import {Reel2} from './reel/Reel2';
import {Reel3} from './reel/Reel3';
import {Reel4} from './reel/Reel4';
import {Reel6} from './reel/Reel6';
import {Reel7} from './reel/Reel7';
import {Reel2Voce, Reel3Voce, Reel4Voce, Reel7Voce, VOCE} from './reel/Voce';

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
    <Folder name="Reel-script">
      <Composition id="Reel1-MareNonTuo" component={Reel1} width={1080} height={1920} fps={FPS} durationInFrames={30 * FPS} defaultProps={{clip: undefined as string | undefined}} />
      <Composition id="Reel2-TreSecondi" component={Reel2} width={1080} height={1920} fps={FPS} durationInFrames={20 * FPS} />
      <Composition id="Reel3-Tovagliolo" component={Reel3} width={1080} height={1920} fps={FPS} durationInFrames={22 * FPS} />
      <Composition id="Reel4-CopriIlLogo" component={Reel4} width={1080} height={1920} fps={FPS} durationInFrames={20 * FPS} />
      <Composition id="Reel5-Buttadentro" component={Reel5} width={1080} height={1920} fps={FPS} durationInFrames={25 * FPS} defaultProps={{clip: undefined as string | undefined}} />
      <Composition id="Reel6-SiRicordavaIlMare" component={Reel6} width={1080} height={1920} fps={FPS} durationInFrames={15 * FPS} />
      <Composition id="Reel7-FormulaCoperta" component={Reel7} width={1080} height={1920} fps={FPS} durationInFrames={18 * FPS} />
    </Folder>
    <Folder name="Reel-voce">
      <Composition id="Reel2-TreSecondi-voce" component={Reel2Voce} width={1080} height={1920} fps={FPS} durationInFrames={Math.ceil(VOCE.reel2.dur * FPS)} />
      <Composition id="Reel3-Tovagliolo-voce" component={Reel3Voce} width={1080} height={1920} fps={FPS} durationInFrames={Math.ceil(VOCE.reel3.dur * FPS)} />
      <Composition id="Reel4-CopriIlLogo-voce" component={Reel4Voce} width={1080} height={1920} fps={FPS} durationInFrames={Math.ceil(VOCE.reel4.dur * FPS)} />
      <Composition id="Reel7-FormulaCoperta-voce" component={Reel7Voce} width={1080} height={1920} fps={FPS} durationInFrames={Math.ceil(VOCE.reel7.dur * FPS)} />
    </Folder>
    <Folder name="Feed-4x5">
      {V.map((v) => <Composition key={v.id} id={`${v.id}-45`} component={v.c} width={1080} height={1350} fps={FPS} durationInFrames={Math.round(v.s * FPS)} />)}
    </Folder>
  </>
);
