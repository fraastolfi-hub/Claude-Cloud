import React from 'react';
import {Img, Sequence, staticFile, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Cta, Frame, Kicker, Line, useT} from '../parts';

const Stat: React.FC<{at: number; bg: string; big: string; small: string}> = ({at, bg, big, small}) => {
  const t = useT(at, 0.5);
  return (
    <div style={{opacity: t, translate: `${(1 - t) * 60}px 0px`, background: bg, border: `4px solid ${C.ink}`, borderRadius: 24, boxShadow: `6px 6px 0 ${C.ink}`, padding: '22px 26px'}}>
      <b style={{display: 'block', font: `900 54px/1 ${display}`}}>{big}</b>
      <span style={{display: 'block', marginTop: 8, font: `600 28px ${text}`, color: C.ink2}}>{small}</span>
    </div>
  );
};

const Chi = () => {
  const ph = useT(0.5, 0.8);
  return (
    <Frame bg={C.lillaSoft}>
      <Kicker />
      <div style={{marginTop: 40}}>
        <Line at={0.2} size={112}>Una guida</Line>
        <Line at={0.5} size={112} hl>scritta da Rimini.</Line>
      </div>
      <div style={{flex: 1, display: 'grid', gridTemplateColumns: '440px 1fr', gap: 30, alignItems: 'end', paddingTop: 40}}>
        <div style={{position: 'relative', height: 600, border: `4px solid ${C.ink}`, borderRadius: '220px 220px 30px 30px', background: C.lilla, overflow: 'hidden', boxShadow: `10px 10px 0 ${C.ink}`, opacity: ph, translate: `0px ${(1 - ph) * 80}px`}}>
          <Img src={staticFile('francesco.png')} style={{position: 'absolute', bottom: 0, left: '50%', width: '88%', translate: '-50% 0px'}} />
        </div>
        <div style={{display: 'grid', gap: 18, paddingBottom: 10}}>
          <Stat at={1.2} bg={C.gialloSoft} big="0 → 30 M€" small="TUI.it" />
          <Stat at={1.6} bg={C.lillaSoft} big="20 strutture" small="marketing Atahotels" />
          <Stat at={2.0} bg={C.tealSoft} big="10 locali" small="aperti con i miei soldi" />
        </div>
      </div>
    </Frame>
  );
};

const Cicatrici = () => (
  <Frame bg={C.ink}>
    <div style={{marginTop: 'auto', marginBottom: 'auto'}}>
      <Line at={0.1} size={104} color={C.crema}>I consulenti vendono consigli.</Line>
      <div style={{height: 30}} />
      <Line at={0.9} size={104} hl instant>Gli operatori vendono cicatrici.</Line>
    </div>
  </Frame>
);

export const Rimini: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <>
      <Sequence name="Chi" durationInFrames={Math.round(3.6 * fps)} premountFor={fps}><Chi /></Sequence>
      <Sequence name="Cicatrici" from={Math.round(3.6 * fps)} durationInFrames={Math.round(2.8 * fps)} premountFor={fps}><Cicatrici /></Sequence>
      <Sequence name="CTA" from={Math.round(6.4 * fps)} premountFor={fps}><Cta line="Ho messo le cicatrici in una guida gratuita." /></Sequence>
    </>
  );
};
export const RIM_S = 9.4;
