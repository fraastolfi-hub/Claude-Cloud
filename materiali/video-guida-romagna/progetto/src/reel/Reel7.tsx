import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Chiusura} from './common';
import {useT} from '../parts';

const Box: React.FC<{i: number}> = ({i}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const appear = interpolate(t, [4 + i * 0.25, 4.4 + i * 0.25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const flip = i === 0 ? interpolate(t, [8, 8.7], [0, 180], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const shake = (i === 1 || i === 2) && t > 11 && t < 15 ? Math.sin(t * 40 + i) * 6 : 0;
  const blink = i === 3 && t > 12 ? 0.5 + 0.5 * Math.abs(Math.sin((t - 12) * Math.PI * 1.6)) : 1;
  const shown = flip > 90;
  return (
    <div style={{width: 380, height: 220, opacity: appear * blink, scale: String(0.6 + 0.4 * appear), rotate: `${shake / 3}deg`, translate: `${shake}px 0px`, perspective: 800}}>
      <div style={{width: '100%', height: '100%', borderRadius: 30, border: `5px solid ${C.ink}`, boxShadow: `8px 8px 0 ${C.ink}`, background: shown ? C.lillaSoft : C.giallo, display: 'grid', placeItems: 'center', rotate: `y ${shown ? flip - 180 : flip}deg`, font: `900 ${shown ? 62 : 110}px ${display}`, color: C.ink, position: 'relative', overflow: 'hidden'}}>
        {shown ? <>Location<svg viewBox="0 0 380 60" style={{position: 'absolute', bottom: 14, left: 0, width: '100%'}}><path d="M0 30 Q 32 10 64 30 T 128 30 T 192 30 T 256 30 T 320 30 T 384 30" fill="none" stroke={C.lilla} strokeWidth="7" /></svg></> : '?'}
      </div>
    </div>
  );
};

const Formula = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const a = useT(0.1, 0.5), b = useT(2, 0.5), r = useT(5.2, 0.5), c1 = useT(8.6, 0.5), c2 = useT(11.2, 0.5);
  const titleUp = interpolate(t, [3.6, 4.2], [0, -1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: C.crema, fontFamily: text, padding: '220px 96px 380px'}}>
      <div style={{scale: String(1 + titleUp * 0.32), transformOrigin: 'top left'}}>
        <p style={{opacity: a, margin: 0, font: `900 110px/1.05 ${display}`, color: C.ink}}>Il prezzo lo decidi <span style={{background: C.giallo, borderRadius: 12, padding: '0 .12em'}}>tu</span>.</p>
        <p style={{opacity: b, margin: '20px 0 0', font: `900 110px/1.05 ${display}`, color: C.ink}}>Il valore <span style={{background: C.giallo, borderRadius: 12, padding: '0 .12em'}}>no</span>.</p>
      </div>
      <div style={{marginTop: 30, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px 48px', justifyItems: 'center'}}>
        <Box i={0} /><Box i={1} /><Box i={2} /><Box i={3} />
      </div>
      <p style={{opacity: r, margin: '40px 0 0', textAlign: 'center', font: `900 72px ${display}`, color: C.ink}}>= il valore del tuo hotel</p>
      <div style={{position: 'relative', marginTop: 30, height: 140, textAlign: 'center', font: `700 52px/1.3 ${text}`, color: C.ink2}}>
        <p style={{position: 'absolute', inset: 0, margin: 0, opacity: c1 * (1 - c2)}}><b style={{color: C.ink}}>Location</b>: il mare. Ce l'hanno tutti.</p>
        <p style={{position: 'absolute', inset: 0, margin: 0, opacity: c2}}>Due costano anni.<br /><b style={{color: C.ink}}>Una si cambia da lunedì.</b></p>
      </div>
    </AbsoluteFill>
  );
};

export const Reel7: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence name="Formula" durationInFrames={15 * fps}><Formula /></Sequence>
      <Sequence name="Chiusura" from={15 * fps} durationInFrames={3 * fps} premountFor={fps}><Chiusura titolo="La formula è nella guida. Gratis." /></Sequence>
    </AbsoluteFill>
  );
};
