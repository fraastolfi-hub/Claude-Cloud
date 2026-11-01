import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Chiusura, Subs} from './common';
import {useT} from '../parts';

// homepage finta, senza città né nome reale; il «logo» è un segno grafico diverso per ciascuna
const Sito: React.FC<{img: string; mark: React.ReactNode; price: string; at: number}> = ({img, mark, price, at}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const postIn = interpolate(t, [0.2 + at, 0.8 + at], [-300, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const postOut = interpolate(t, [13.2, 14], [0, 340], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const pr = useT(6.2 + at, 0.5);
  return (
    <div style={{width: 440}}>
      <div style={{background: '#fff', border: `4px solid ${C.ink}`, borderRadius: 26, overflow: 'hidden', boxShadow: `8px 8px 0 ${C.ink}`}}>
        <div style={{position: 'relative', height: 96, display: 'flex', alignItems: 'center', padding: '0 24px', borderBottom: '2px solid #eee'}}>
          {mark}
          <div style={{position: 'absolute', left: 14, top: 10, width: 230, height: 76, background: C.giallo, borderRadius: 4, boxShadow: '0 6px 12px rgba(0,0,0,.18)', rotate: `${-4 + postOut / 60}deg`, translate: `${postIn + postOut}px ${postOut / 4}px`}} />
        </div>
        <Img src={staticFile(img)} style={{display: 'block', width: '100%', height: 260, objectFit: 'cover'}} />
        <div style={{padding: 24}}>
          <p style={{margin: 0, font: `800 36px/1.15 ${display}`, color: C.ink}}>Accogliente, a due passi dal mare.</p>
          <p style={{margin: '10px 0 0', font: `500 24px/1.3 ${text}`, color: C.ink2}}>Camere confortevoli, colazione inclusa.</p>
        </div>
      </div>
      <p style={{opacity: pr, margin: '26px 0 0', textAlign: 'center', font: `900 72px ${display}`, color: C.ink}}>{price}</p>
    </div>
  );
};

const Tavolo = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const focus = t < 2 ? 0 : t < 4 ? -1 : t < 6 ? 1 : 0;
  const tap = useT(10, 0.5);
  const ov = useT(10.2, 0.4);
  return (
    <AbsoluteFill style={{background: '#e9dfcf', alignItems: 'center', justifyContent: 'flex-start', paddingTop: 300}}>
      <div style={{scale: '1.12'}}>
      <div style={{display: 'flex', gap: 40, translate: `${focus * -120}px 0px`}}>
        <Sito at={0} img="uguale-1.webp" price="92 €" mark={<span style={{font: `900 34px ${display}`, color: C.lilla}}>◆ HOTEL</span>} />
        <div style={{position: 'relative'}}>
          <Sito at={0.3} img="uguale-2.webp" price="84 €" mark={<span style={{font: `900 34px ${display}`, color: C.teal}}>≈ HOTEL</span>} />
          {tap > 0 && <span style={{position: 'absolute', left: '50%', bottom: 40, width: 80 + tap * 180, height: 80 + tap * 180, translate: '-50% 50%', borderRadius: '50%', border: `8px solid rgba(38,37,33,${1 - tap})`}} />}
          <span style={{position: 'absolute', left: '50%', bottom: -150, translate: '-50% 0px', opacity: ov, scale: String(0.8 + 0.2 * ov), background: C.giallo, border: `4px solid ${C.ink}`, borderRadius: 16, padding: '10px 30px', font: `900 64px ${display}`, color: C.ink}}>Ovvio.</span>
        </div>
      </div>
      </div>
    </AbsoluteFill>
  );
};

export const Reel4: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence name="Tavolo" durationInFrames={17 * fps}><Tavolo /></Sequence>
      <Subs subs={[[0, 2, '*Copri il logo.*'], [2, 6, 'Stessa frase. *Stessa piscina.*'], [6, 10, '92 € · *84 €*'], [13, 17, 'Se sembri uguale, il prezzo lo fanno *i tuoi concorrenti*.']]} />
      <Sequence name="Chiusura" from={17 * fps} durationInFrames={3 * fps} premountFor={fps}><Chiusura titolo="Fai la prova stasera, con il tuo sito." pulsante="Scarica la guida" /></Sequence>
    </AbsoluteFill>
  );
};
