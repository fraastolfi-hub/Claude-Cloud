// Reel 1 e Reel 5: girati da Francesco. Senza file mostrano i segnaposto con le indicazioni di ripresa;
// con la prop `clip` (file in public/) usano il girato, con sottotitoli e chiusura già a tempo.
import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig} from 'remotion';
import {Chiusura, DaGirare, Sub, Subs} from './common';

type Shot = [number, number, string];
const Girato: React.FC<{clip?: string; shots: Shot[]; subs: Sub[]; fine: number; dur: number}> = ({clip, shots, subs, fine, dur}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      {clip ? (
        <Sequence name="Girato" durationInFrames={Math.round(fine * fps)}><OffthreadVideo src={staticFile(clip)} style={{width: '100%', height: '100%', objectFit: 'cover'}} muted={false} /></Sequence>
      ) : shots.map(([a, b, l], i) => (
        <Sequence key={i} name={`Ripresa ${i + 1}`} from={Math.round(a * fps)} durationInFrames={Math.round((b - a) * fps)}><DaGirare label={l} /></Sequence>
      ))}
      <Subs subs={subs} />
      <Sequence name="Chiusura" from={Math.round(fine * fps)} durationInFrames={Math.round((dur - fine) * fps)} premountFor={fps}><Chiusura /></Sequence>
    </AbsoluteFill>
  );
};

export const Reel1: React.FC<{clip?: string}> = ({clip}) => (
  <Girato clip={clip} dur={30} fine={25} shots={[
    [0, 2, 'Francesco di spalle sulla spiaggia vuota. Si gira.'],
    [2, 6, 'Primo piano.'],
    [6, 10, 'Indica la spiaggia, la camera allarga sulle cabine.'],
    [10, 15, 'Cammina lungo le cabine.'],
    [15, 21, 'Si ferma, guarda in camera.'],
    [21, 25, 'Pausa. Mezzo sorriso. Tira fuori la guida stampata.'],
  ]} subs={[
    [0, 2, '*E tu, albergatore della Romagna…*'],
    [2, 6, '"A due passi dal *mare*"?'],
    [6, 10, 'Lo scrive anche il *vicino*.'],
    [10, 15, '"Abbiamo il *caffè*."'],
    [15, 21, 'Il mare *non è tuo*.'],
    [21, 25, 'Il mare ce l\'hai. *Ti manca il resto.*'],
  ]} />
);

export const Reel5: React.FC<{clip?: string}> = ({clip}) => (
  <Girato clip={clip} dur={25} fine={21} shots={[
    [0, 3, 'Lungomare di sera, luci, menù plastificati esposti.'],
    [3, 6, 'Una vetrina, poi un\'altra uguale.'],
    [6, 11, 'Un cameriere di spalle porge un menù a dei passanti.'],
    [11, 16, 'Primo piano su due menù uguali, uno accanto all\'altro.'],
    [16, 21, 'Stacco su Francesco, sul lungomare.'],
  ]} subs={[
    [0, 3, 'Quante *agenzie* hai cambiato?'],
    [3, 6, 'Quella del *nipote del cugino*?'],
    [6, 11, 'L\'agenzia fa il *buttadentro*.'],
    [11, 16, 'Il menù è *uguale a quello accanto*.'],
    [16, 21, 'Il traffico si compra. *Il motivo no.*'],
  ]} />
);
