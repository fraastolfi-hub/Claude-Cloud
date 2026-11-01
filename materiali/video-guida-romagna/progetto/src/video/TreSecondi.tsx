import React from 'react';
import {Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Cta, Frame, Kicker, Line, Sub, useT} from '../parts';

const Apertura = () => (
  <Frame bg={C.lillaSoft}>
    <Kicker />
    <div style={{marginTop: 'auto', marginBottom: 'auto'}}>
      <Line at={0.2} size={128}>Sabato del cambio.</Line>
      <Line at={0.6} size={128} hl>Coda sull'A14.</Line>
      <Sub at={1.3}>Cinquanta hotel a Riccione. <b style={{color: C.ink}}>Tre secondi a testa.</b></Sub>
    </div>
  </Frame>
);

const PREZZI = ['92 €', '89 €', '91 €', '86 €', '94 €', '90 €', '88 €'];

// elenco di hotel tutti uguali che scorre; in tre secondi l'ospite tocca il più economico
const Telefono = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scroll = interpolate(frame, [0.3 * fps, 2.3 * fps], [0, -330], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const pick = useT(2.4, 0.4);
  const secs = Math.max(1, 3 - Math.floor(frame / fps));
  return (
    <div style={{position: 'relative', alignSelf: 'center', width: 720, height: 820, background: '#fff', border: `5px solid ${C.ink}`, borderRadius: 56, boxShadow: `12px 12px 0 ${C.ink}`, overflow: 'hidden'}}>
      <div style={{position: 'absolute', top: 0, left: 0, right: 0, zIndex: 2, background: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '30px 34px 20px', borderBottom: '3px solid #e8e2d8'}}>
        <span style={{font: `800 40px ${display}`}}>Riccione</span>
        <span style={{width: 74, height: 74, borderRadius: '50%', background: C.giallo, border: `4px solid ${C.ink}`, display: 'grid', placeItems: 'center', font: `900 40px ${display}`}}>{secs}</span>
      </div>
      <div style={{position: 'absolute', top: 130, left: 24, right: 24, translate: `0px ${scroll}px`}}>
        {PREZZI.map((p, i) => {
          const on = i === 3 && pick > 0;
          return (
            <div key={i} style={{display: 'grid', gridTemplateColumns: '150px 1fr auto', gap: 20, alignItems: 'center', padding: '18px 14px', borderBottom: '3px solid #f0ebe3', borderRadius: 18, background: on ? `rgba(255,210,46,${pick})` : 'transparent', outline: on ? `4px solid rgba(38,37,33,${pick})` : 'none'}}>
              <div style={{height: 104, borderRadius: 16, background: 'linear-gradient(180deg,#bfe3f2 0 50%,#7cc4d8 50% 66%,#f1dfb8 66%)'}} />
              <div><b style={{display: 'block', font: `800 32px/1.2 ${display}`}}>Hotel <span style={{filter: 'blur(7px)'}}>xxxxxxx</span></b><span style={{display: 'inline-block', marginTop: 8, font: `700 25px ${text}`, background: C.gialloSoft, borderRadius: 8, padding: '3px 10px'}}>A due passi dal mare</span></div>
              <b style={{font: `900 40px ${display}`}}>{p}</b>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const Scelta = () => (
  <Frame bg={C.lillaSoft}>
    <Line at={0} size={112}>Hai tre secondi.</Line>
    <Line at={0.2} size={112} hl>Cosa dici?</Line>
    <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', paddingTop: 40}}><Telefono /></div>
  </Frame>
);

export const TreSecondi: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <>
      <Sequence name="Apertura" durationInFrames={Math.round(2.8 * fps)} premountFor={fps}><Apertura /></Sequence>
      <Sequence name="Telefono" from={Math.round(2.8 * fps)} durationInFrames={Math.round(3.4 * fps)} premountFor={fps}><Scelta /></Sequence>
      <Sequence name="CTA" from={Math.round(6.2 * fps)} premountFor={fps}><Cta line="In tre secondi vince il più chiaro." /></Sequence>
    </>
  );
};
export const TRE_S = 9.2;
