import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {hand, text} from '../theme';
import {Chiusura, Subs} from './common';

// una riga scritta a mano che compare da sinistra a destra, come se la penna la tracciasse
const Scritta: React.FC<{at: number; dur?: number; size: number; color?: string; children: React.ReactNode}> = ({at, dur = 1.2, size, color = '#1f3b8f', children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = interpolate(frame, [at * fps, (at + dur) * fps], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{font: `700 ${size}px/1.05 ${hand}`, color, clipPath: `inset(-20% ${100 - p}% -20% 0)`}}>{children}</div>;
};

const Tovagliolo = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const turn = interpolate(t, [14, 15], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const crumple = interpolate(t, [18, 19.6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const line = interpolate(t, [10, 10.6], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 40%, #a7744a, #6e4529)', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{width: 820, height: 820, marginTop: -260, background: '#fffdf8', borderRadius: 10, boxShadow: '0 30px 60px rgba(0,0,0,.35)', backgroundImage: 'radial-gradient(#ece6da 1.5px, transparent 1.6px)', backgroundSize: '22px 22px', padding: '90px 90px', rotate: `${-4 + turn * 4 + crumple * 40}deg`, scale: String((1 + turn * 0.12) * (1 - crumple * 0.85)), opacity: 1 - crumple * 0.9, filter: `blur(${crumple * 3}px)`}}>
        <Scritta at={0.2} size={150}>10 €</Scritta>
        <Scritta at={2.2} size={110}>× 40 camere</Scritta>
        <Scritta at={6.2} size={110}>× 100 notti</Scritta>
        <div style={{height: 8, width: `${line}%`, background: '#1f3b8f', borderRadius: 4, margin: '24px 0 10px'}} />
        <Scritta at={10.6} dur={1.4} size={170} color="#c0392b">40.000 €</Scritta>
      </div>
      <p style={{position: 'absolute', bottom: 330, font: `600 30px ${text}`, color: '#f3e7d8'}}>Esempio con numeri tondi.</p>
    </AbsoluteFill>
  );
};

export const Reel3: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence name="Tovagliolo" durationInFrames={20 * fps}><Tovagliolo /></Sequence>
      <Subs subs={[[0, 2, 'Quanto hai *regalato* quest\'anno?'], [2, 6, 'Il vicino abbassa. *Tu dietro.*'], [6, 10, 'Per *cento notti*.'], [10, 14, '*40.000 €*'], [14, 18, 'Il bagno nuovo. *Regalato.*'], [18, 20, 'Lo sconto è il prezzo di un *motivo che non hai*.']]} />
      <Sequence name="Chiusura" from={20 * fps} durationInFrames={2 * fps} premountFor={fps}><Chiusura /></Sequence>
    </AbsoluteFill>
  );
};
