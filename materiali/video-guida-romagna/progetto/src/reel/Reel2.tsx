import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Chiusura, Subs} from './common';
import {useT} from '../parts';

const CARDS = [
  ['Accogliente', '92 €'], ['Confortevole', '89 €'], ['A due passi dal mare', '91 €'], ['Accogliente', '86 €'], ['A due passi dal mare', '94 €'],
  ['Confortevole', '90 €'], ['Accogliente', '88 €'], ['A due passi dal mare', '93 €'], ['Confortevole', '79 €'], ['Accogliente', '95 €'], ['A due passi dal mare', '87 €'], ['Confortevole', '92 €'],
];

// la griglia di una app di prenotazione, generica: nomi sfocati, nessun marchio
const Schermo = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const scroll = interpolate(t, [0, 6, 6.5], [0, -1500, -1530], {extrapolateRight: 'clamp', easing: (x) => x});
  const zoom = interpolate(t, [6, 7], [1, 1.45], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const tap = useT(12, 0.4);
  const secs = Math.max(1, 3 - Math.floor(t / 0.7));
  return (
    <AbsoluteFill style={{background: '#f2efe9', fontFamily: text}}>
      <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 210, zIndex: 3, background: '#fff', borderBottom: '3px solid #e8e2d8', display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', padding: '0 60px 30px'}}>
        <div><b style={{display: 'block', font: `800 54px ${display}`, color: C.ink}}>Riccione</b><span style={{font: `500 30px ${text}`, color: C.ink2}}>Agosto · 50 strutture</span></div>
        <span style={{opacity: t < 2.2 ? 1 : 0, width: 120, height: 120, borderRadius: '50%', background: C.giallo, border: `5px solid ${C.ink}`, display: 'grid', placeItems: 'center', font: `900 70px ${display}`, color: C.ink}}>{secs}</span>
      </div>
      <div style={{position: 'absolute', top: 230, left: 40, right: 40, translate: `0px ${scroll}px`, scale: String(zoom), transformOrigin: '96% 1700px'}}>
        {CARDS.map(([tag, p], i) => {
          const cheap = i === 8;
          return (
            <div key={i} style={{display: 'grid', gridTemplateColumns: '260px 1fr auto', gap: 26, alignItems: 'center', padding: 22, marginBottom: 20, background: cheap && tap > 0 ? `rgba(255,210,46,${tap})` : '#fff', border: '3px solid #e8e2d8', borderRadius: 26, position: 'relative'}}>
              <div style={{height: 180, borderRadius: 18, background: 'linear-gradient(180deg,#bfe3f2 0 50%,#7cc4d8 50% 66%,#f1dfb8 66%)'}} />
              <div><b style={{display: 'block', font: `800 40px/1.2 ${display}`, color: C.ink}}>Hotel <span style={{filter: 'blur(9px)'}}>xxxxxx</span></b><span style={{display: 'block', marginTop: 6, font: `500 28px ${text}`, color: C.ink2}}>★★★ · 8,4</span><span style={{display: 'inline-block', marginTop: 10, font: `700 30px ${text}`, background: C.gialloSoft, borderRadius: 10, padding: '4px 12px'}}>{tag}</span></div>
              <b style={{font: `900 52px ${display}`, color: C.ink}}>{p}</b>
              {cheap && tap > 0 && <span style={{position: 'absolute', right: 70, top: 90, width: 120 + tap * 120, height: 120 + tap * 120, translate: '50% -50%', borderRadius: '50%', border: `6px solid rgba(38,37,33,${1 - tap})`}} />}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Nero = () => {
  const a = useT(0.1, 0.4), b = useT(0.9, 0.5);
  return (
    <AbsoluteFill style={{background: C.ink, justifyContent: 'center', padding: '0 96px', textAlign: 'center'}}>
      <p style={{opacity: a, font: `900 92px/1.1 ${display}`, color: C.crema, margin: 0}}>Non vince il migliore.</p>
      <p style={{opacity: b, font: `900 92px/1.1 ${display}`, color: C.giallo, margin: '30px 0 0'}}>Vince il più chiaro.</p>
    </AbsoluteFill>
  );
};

export const Reel2: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence name="Schermo" durationInFrames={14 * fps}><Schermo /></Sequence>
      <Sequence name="Nero" from={14 * fps} durationInFrames={3 * fps}><Nero /></Sequence>
      <Subs subs={[[0, 2, '*3 secondi.*'], [2, 6, 'In coda sull\'*A14*. Il sabato del cambio.'], [6, 11, '"Accogliente." "Confortevole." "A due passi dal *mare*."'], [11, 14, 'Tocca quello che *costa meno*.']]} />
      <Sequence name="Chiusura" from={17 * fps} durationInFrames={3 * fps} premountFor={fps}><Chiusura /></Sequence>
    </AbsoluteFill>
  );
};
