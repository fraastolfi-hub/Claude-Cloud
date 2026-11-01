import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display} from '../theme';
import {Chiusura} from './common';
import {useT} from '../parts';

// story ad muta: l'auto di fine vacanza disegnata, le frasi grandi sopra
const Auto = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const lid = interpolate(t, [3.2, 3.9], [-62, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const go = interpolate(t, [6.3, 8.6], [0, 1300], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (x) => x * x});
  const t1 = useT(0.2, 0.5), t2 = useT(3.4, 0.5), t3 = useT(6.2, 0.5);
  const txt = (o: number, s: React.ReactNode) => <p style={{position: 'absolute', top: 260, left: 96, right: 96, opacity: o, margin: 0, font: `900 92px/1.08 ${display}`, color: C.ink}}>{s}</p>;
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg,#d8d6ff 0 52%,#f1dfb8 52%)'}}>
      {t < 3.3 && txt(t1, <>L'ospite di agosto.<br />È stato benissimo.</>)}
      {t >= 3.3 && t < 6.2 && txt(t2, <>Ti ha lasciato<br />un <span style={{background: C.giallo, borderRadius: 12, padding: '0 .15em'}}>9</span>.</>)}
      {t >= 6.2 && txt(t3, <>L'anno dopo torna<br />in Riviera. <span style={{background: C.giallo, borderRadius: 12, padding: '0 .15em'}}>Dal tuo vicino.</span></>)}
      <div style={{position: 'absolute', left: 140, top: 900, width: 800, height: 360, translate: `${go}px 0px`}}>
        {/* ombrellone e valigie nel bagagliaio */}
        <div style={{position: 'absolute', left: -10, top: -40, width: 26, height: 220, background: C.ink, borderRadius: 10, rotate: '-18deg', transformOrigin: 'bottom'}} />
        <div style={{position: 'absolute', left: -120, top: -120, width: 240, height: 110, background: C.rosa, border: `5px solid ${C.ink}`, borderRadius: '120px 120px 10px 10px', rotate: '-18deg'}} />
        <div style={{position: 'absolute', left: 40, top: 40, width: 150, height: 120, background: C.lilla, border: `5px solid ${C.ink}`, borderRadius: 14}} />
        <div style={{position: 'absolute', left: 170, top: 70, width: 120, height: 90, background: C.teal, border: `5px solid ${C.ink}`, borderRadius: 14}} />
        {/* carrozzeria */}
        <div style={{position: 'absolute', left: 0, top: 150, width: 800, height: 150, background: '#fff', border: `6px solid ${C.ink}`, borderRadius: 40}} />
        <div style={{position: 'absolute', left: 300, top: 40, width: 380, height: 130, background: '#bfe3f2', border: `6px solid ${C.ink}`, borderRadius: '60px 80px 0 0'}} />
        <div style={{position: 'absolute', left: 0, top: 150, width: 300, height: 26, background: C.giallo, border: `6px solid ${C.ink}`, borderRadius: 12, rotate: `${lid}deg`, transformOrigin: 'right center'}} />
        <div style={{position: 'absolute', left: 90, top: 260, width: 120, height: 120, borderRadius: '50%', background: C.ink, border: '18px solid #57534c'}} />
        <div style={{position: 'absolute', left: 580, top: 260, width: 120, height: 120, borderRadius: '50%', background: C.ink, border: '18px solid #57534c'}} />
      </div>
    </AbsoluteFill>
  );
};

const Giallo = () => {
  const a = useT(0.1, 0.4), b = useT(0.9, 0.4);
  return (
    <AbsoluteFill style={{background: C.giallo, justifyContent: 'center', padding: '0 96px'}}>
      <p style={{opacity: a, margin: 0, font: `900 120px/1.05 ${display}`, color: C.ink}}>Si ricordava il mare.</p>
      <p style={{opacity: b, margin: '30px 0 0', font: `900 150px/1 ${display}`, color: C.ink}}><span style={{background: '#fff', borderRadius: 14, padding: '0 .12em'}}>Non te.</span></p>
    </AbsoluteFill>
  );
};

export const Reel6: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence name="Auto" durationInFrames={9 * fps}><Auto /></Sequence>
      <Sequence name="Giallo" from={9 * fps} durationInFrames={3 * fps}><Giallo /></Sequence>
      <Sequence name="Chiusura" from={12 * fps} durationInFrames={3 * fps} premountFor={fps}><Chiusura /></Sequence>
    </AbsoluteFill>
  );
};
