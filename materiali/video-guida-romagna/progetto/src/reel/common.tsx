import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text, GIALLO_SUB} from '../theme';
import {Logo, useT} from '../parts';

// sottotitoli: una frase per schermata; tra *asterischi* la parola chiave in giallo
export type Sub = [number, number, string];
const parse = (s: string) => s.split(/(\*[^*]+\*)/).map((p, i) => p.startsWith('*') ? <span key={i} style={{color: GIALLO_SUB}}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>);

export const Subs: React.FC<{subs: Sub[]}> = ({subs}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cur = subs.find(([a, b]) => t >= a && t < b);
  if (!cur) return null;
  const k = interpolate(t, [cur[0], cur[0] + 0.15], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', padding: '0 80px 420px'}}>
      <div style={{opacity: k, scale: String(0.94 + 0.06 * k), background: 'rgba(38,37,33,.92)', color: '#fff', borderRadius: 22, padding: '20px 34px', font: `800 58px/1.2 ${display}`, textAlign: 'center', maxWidth: 920}}>{parse(cur[2])}</div>
    </AbsoluteFill>
  );
};

// chiusura comune (ultimi 3 secondi): la guida, la promessa, il pulsante Scarica
export const Chiusura: React.FC<{titolo?: string; pulsante?: string}> = ({titolo = 'Guida gratuita per gli hotel della Romagna', pulsante = 'Scarica'}) => {
  const cov = useT(0, 0.6);
  const t1 = useT(0.35, 0.5);
  const t2 = useT(0.7, 0.5);
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const bob = Math.sin(frame / fps * Math.PI * 2) * 10;
  return (
    <AbsoluteFill style={{background: C.crema, fontFamily: text, color: C.ink, alignItems: 'center', padding: '200px 96px 380px', textAlign: 'center'}}>
      <Img src={staticFile('copertina.webp')} style={{width: 460, border: `4px solid ${C.ink}`, borderRadius: 18, boxShadow: `14px 14px 0 ${C.ink}`, opacity: cov, rotate: `${4 + (1 - cov) * 12}deg`, translate: `0px ${(1 - cov) * 160}px`}} />
      <p style={{opacity: t1, margin: '70px 0 0', font: `900 68px/1.1 ${display}`}}>{titolo}</p>
      <div style={{opacity: t2, marginTop: 40, background: C.giallo, border: `4px solid ${C.ink}`, borderRadius: 18, boxShadow: `8px 8px 0 ${C.ink}`, padding: '24px 60px', font: `900 56px/1 ${display}`}}>{pulsante} ↓</div>
      <p style={{opacity: t2, margin: '26px 0 0', font: `600 36px ${text}`, color: C.ink2, translate: `0px ${bob}px`}}>Il link è qui sotto</p>
      <div style={{marginTop: 'auto', opacity: t2}}><Logo /></div>
    </AbsoluteFill>
  );
};

// segnaposto per le riprese da girare
export const DaGirare: React.FC<{label: string; bg?: string}> = ({label, bg = '#3a3833'}) => (
  <AbsoluteFill style={{background: `repeating-linear-gradient(45deg, ${bg} 0 40px, #45433d 40px 80px)`, alignItems: 'center', justifyContent: 'center', padding: 120}}>
    <div style={{border: '4px dashed #faf7f4', borderRadius: 24, padding: '30px 36px', color: '#faf7f4', font: `700 40px/1.35 ${display}`, textAlign: 'center'}}>RIPRESA DA GIRARE<br /><span style={{font: `500 34px/1.35 ${text}`}}>{label}</span></div>
  </AbsoluteFill>
);
