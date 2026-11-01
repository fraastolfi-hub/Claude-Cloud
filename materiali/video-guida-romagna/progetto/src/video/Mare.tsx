import React from 'react';
import {Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C} from '../theme';
import {Cta, Frame, Kicker, Line, Sub, useT} from '../parts';

const Apertura = () => (
  <Frame bg={C.crema}>
    <Kicker />
    <div style={{marginTop: 'auto', marginBottom: 'auto'}}>
      <Line at={0.2} size={150}>Il mare</Line>
      <Line at={0.6} size={150} hl>non è tuo.</Line>
      <Sub at={1.4}>Lo scrivono tutti: «a due passi dal mare».</Sub>
    </div>
  </Frame>
);

// file di ombrelloni che si riempiono; uno solo è giallo, ed è il tuo
const Ombrelloni = () => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const rows = 7, cols = 7;
  const me = useT(1.5, 0.5);
  return (
    <div style={{alignSelf: 'center', width: height > 1500 ? '100%' : 640, display: 'grid', gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: height > 1500 ? 22 : 16, background: '#f6e7c8', border: `4px solid ${C.ink}`, borderRadius: 32, padding: 34, boxShadow: `10px 10px 0 ${C.ink}`}}>
      {Array.from({length: rows * cols}).map((_, i) => {
        const r = Math.floor(i / cols);
        const t = interpolate(frame, [(0.15 + r * 0.12) * fps, (0.45 + r * 0.12) * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const isMe = i === 24;
        return <div key={i} style={{aspectRatio: '1', borderRadius: '50%', background: isMe && me > 0 ? C.giallo : C.rosa, border: `${isMe ? 5 : 3}px solid ${C.ink}`, scale: String(t * (isMe ? 1 + 0.25 * me : 1)), opacity: t}} />;
      })}
    </div>
  );
};

const Mille = () => (
  <Frame bg={C.crema}>
    <Line at={0} size={112}>È di</Line>
    <Line at={0.2} size={112} hl>mille hotel.</Line>
    <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '40px 0'}}><Ombrelloni /></div>
    <Sub at={1.8}>Quindi, per l'ospite, <b style={{color: C.ink}}>non è un motivo.</b></Sub>
  </Frame>
);

export const Mare: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <>
      <Sequence name="Apertura" durationInFrames={Math.round(2.8 * fps)} premountFor={fps}><Apertura /></Sequence>
      <Sequence name="Ombrelloni" from={Math.round(2.8 * fps)} durationInFrames={Math.round(3.2 * fps)} premountFor={fps}><Mille /></Sequence>
      <Sequence name="CTA" from={Math.round(6 * fps)} premountFor={fps}><Cta line="Il mare ce l'hai. Ti manca il resto." /></Sequence>
    </>
  );
};
export const MARE_S = 9;
