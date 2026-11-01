import React from 'react';
import {Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display} from '../theme';
import {Cta, Frame, Kicker, Line, Sub, useT} from '../parts';

const Apertura = () => (
  <Frame bg={C.crema}>
    <Kicker />
    <div style={{marginTop: 'auto', marginBottom: 'auto'}}>
      <Line at={0.2} size={128}>Quanto hai regalato</Line>
      <Line at={0.6} size={128} hl>quest'anno?</Line>
    </div>
  </Frame>
);

// il cartellino del prezzo che scende di dieci euro alla volta
const Cartellino = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const step = Math.min(3, Math.floor(Math.max(0, frame - 0.4 * fps) / (0.55 * fps)));
  const prezzi = ['120 €', '110 €', '100 €', '90 €'];
  const local = (frame - 0.4 * fps) % (0.55 * fps);
  const bump = step < 3 ? interpolate(local, [0, 6], [1.12, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
  return (
    <div style={{alignSelf: 'center', display: 'flex', alignItems: 'center', gap: 34}}>
      <div style={{rotate: '-6deg', scale: String(bump), background: step % 2 ? C.rosaSoft : '#fff', border: `5px solid ${C.ink}`, borderRadius: 30, boxShadow: `10px 10px 0 ${C.ink}`, padding: '46px 64px', font: `900 150px/1 ${display}`}}>{prezzi[step]}</div>
      <div style={{font: `900 120px/1 ${display}`, color: '#ff5a3c'}}>↓</div>
    </div>
  );
};

const Vicino = () => (
  <Frame bg={C.crema}>
    <Line at={0} size={100}>Il vicino abbassa.</Line>
    <Line at={0.3} size={100} hl>Tu dietro.</Line>
    <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}><Cartellino /></div>
    <Sub at={1.2}>È come svendere le sdraio a fine stagione. <b style={{color: C.ink}}>Solo che tu lo fai a luglio.</b></Sub>
  </Frame>
);

// il conto: 10 € × 40 camere × 100 notti, il contatore sale a 40.000 €
const Conto = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = Math.round(interpolate(frame, [0.9 * fps, 2.2 * fps], [0, 40000], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) / 100) * 100;
  const a = useT(0, 0.5), b = useT(0.3, 0.5), c = useT(0.6, 0.5), d = useT(2.3, 0.5);
  const chip = (t: number, s: string) => <span style={{opacity: t, translate: `0px ${(1 - t) * 20}px`, display: 'inline-block', background: '#fff', border: `4px solid ${C.ink}`, borderRadius: 999, padding: '14px 30px', font: `800 54px/1 ${display}`}}>{s}</span>;
  return (
    <Frame bg={C.crema}>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 26, textAlign: 'center'}}>
        {chip(a, '10 € di sconto')}{chip(b, '× 40 camere')}{chip(c, '× 100 notti')}
        <div style={{marginTop: 30, background: C.giallo, border: `5px solid ${C.ink}`, borderRadius: 26, boxShadow: `10px 10px 0 ${C.ink}`, padding: '24px 46px', font: `900 150px/1 ${display}`}}>{n.toLocaleString('it-IT')} €</div>
        <p style={{opacity: d, margin: '30px 0 0', font: `900 70px/1.1 ${display}`}}>Il bagno nuovo. Regalato.</p>
      </div>
    </Frame>
  );
};

export const Regalato: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <>
      <Sequence name="Apertura" durationInFrames={Math.round(2.4 * fps)} premountFor={fps}><Apertura /></Sequence>
      <Sequence name="Vicino" from={Math.round(2.4 * fps)} durationInFrames={Math.round(2.9 * fps)} premountFor={fps}><Vicino /></Sequence>
      <Sequence name="Conto" from={Math.round(5.3 * fps)} durationInFrames={Math.round(3.3 * fps)} premountFor={fps}><Conto /></Sequence>
      <Sequence name="CTA" from={Math.round(8.6 * fps)} premountFor={fps}><Cta line="Lo sconto è il prezzo di un motivo che non hai." /></Sequence>
    </>
  );
};
export const REG_S = 11.6;
