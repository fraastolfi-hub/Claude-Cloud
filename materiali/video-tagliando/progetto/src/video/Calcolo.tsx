// V1 · Il calcolo: 21 controlli che si spuntano, quattro semafori che si accendono, il verdetto.
import React from 'react';
import {Easing, interpolate, Series, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Cta, Frame, Kicker, Line, Sub, useSafe, useT} from '../parts';
import {AREE, SEM, TUTTI} from '../controlli';

const S1 = 3, S2 = 5.6, S3 = 2.6, S4 = 3.2;
export const CALCOLO_S = S1 + S2 + S3 + S4;

const Gancio: React.FC = () => (
  <Frame bg={C.crema}>
    <Kicker />
    <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
      <Line at={0.2}>Il tuo sito</Line>
      <Line at={0.5} hl>merita un budget?</Line>
      <Sub at={1.2}>21 controlli. Un verdetto. <b>Ecco come si calcola.</b></Sub>
    </div>
  </Frame>
);

// ogni controllo si spunta in 0,18 s, area dopo area
const STEP = 0.18;
const Calcolo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const story = height > 1500;
  const t = frame / fps - 0.4;
  const fatti = Math.max(0, Math.min(21, Math.floor(t / STEP) + 1));
  const head = useT(0, 0.4);
  let idx = 0;
  return (
    <Frame bg={C.lillaSoft}>
      <div style={{opacity: head, display: 'flex', alignItems: 'baseline', justifyContent: 'space-between'}}>
        <span style={{font: `900 ${story ? 64 : 56}px/1 ${display}`}}>Il calcolo</span>
        <span style={{font: `900 ${story ? 120 : 96}px/1 ${display}`}}>{t < 0 ? 0 : fatti}<span style={{fontSize: story ? 56 : 46, color: C.ink2}}>/21</span></span>
      </div>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: story ? 30 : 18}}>
        {AREE.map((a) => {
          const start = idx; idx += a.controlli.length;
          const done = fatti >= idx;
          const cur = TUTTI[Math.min(fatti, 21) - 1];
          const lit = interpolate(t, [idx * STEP, idx * STEP + 0.25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <div key={a.nome} style={{background: '#fff', border: `4px solid ${C.ink}`, borderRadius: 24, boxShadow: `8px 8px 0 ${C.ink}`, padding: story ? '22px 26px' : '14px 22px', display: 'grid', gridTemplateColumns: '1fr auto', alignItems: 'center', gap: 18}}>
              <div>
                <div style={{font: `800 ${story ? 40 : 34}px/1.1 ${display}`}}>{a.nome}</div>
                <div style={{display: 'flex', gap: 10, marginTop: 12}}>
                  {a.controlli.map((c, i) => {
                    const on = fatti > start + i;
                    return <i key={i} style={{width: story ? 34 : 28, height: story ? 34 : 28, borderRadius: 9, border: `3px solid ${C.ink}`, background: on ? (c.ok ? SEM.verde : SEM.rosso) : '#f3efe9', display: 'grid', placeItems: 'center', font: `900 ${story ? 22 : 18}px/1 ${display}`, fontStyle: 'normal'}}>{on ? (c.ok ? '✓' : '✗') : ''}</i>;
                  })}
                </div>
                <div style={{marginTop: 10, height: story ? 34 : 28, font: `500 ${story ? 28 : 24}px/1.2 ${text}`, color: C.ink2}}>{cur && cur.area === a.nome && !done ? cur.nome : done ? `${a.controlli.length} controlli` : ''}</div>
              </div>
              <div style={{width: story ? 92 : 76, height: story ? 92 : 76, borderRadius: '50%', border: `4px solid ${C.ink}`, background: lit > 0 ? SEM[a.colore] : SEM.spento, scale: String(1 + 0.18 * Math.sin(lit * Math.PI))}} />
            </div>
          );
        })}
      </div>
      <p style={{margin: '18px 0 0', font: `600 26px/1 ${text}`, color: C.ink2}}>Esempio, non un hotel reale</p>
    </Frame>
  );
};

const Verdetto: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const story = height > 1500;
  const q = useT(0, 0.5);
  const st = interpolate(frame, [0.5 * fps, 0.85 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.3, 1.6, 0.5, 1)});
  const s = useT(1.1, 0.5);
  return (
    <Frame bg={C.ink}>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
        <p style={{opacity: q, font: `800 ${story ? 56 : 50}px/1.15 ${display}`, color: C.crema}}>Il tuo sito merita un budget?</p>
        <div style={{opacity: st, scale: String(2 - st), rotate: '-4deg', marginTop: story ? 80 : 50, background: SEM.rosso, color: C.ink, border: `5px solid ${C.crema}`, borderRadius: 26, padding: '26px 50px', font: `900 ${story ? 120 : 104}px/1 ${display}`}}>Non ancora.</div>
        <p style={{opacity: s, marginTop: story ? 70 : 44, font: `600 ${story ? 48 : 42}px/1.25 ${text}`, color: '#c4bdb1'}}>Prima va sistemato <b style={{color: C.crema}}>il messaggio.</b></p>
      </div>
    </Frame>
  );
};

export const Calcolo_: React.FC = () => {
  const {fps} = useVideoConfig();
  useSafe();
  return (
    <Series>
      <Series.Sequence name="Gancio" durationInFrames={Math.round(S1 * fps)} premountFor={fps}><Gancio /></Series.Sequence>
      <Series.Sequence name="Calcolo" durationInFrames={Math.round(S2 * fps)} premountFor={fps}><Calcolo /></Series.Sequence>
      <Series.Sequence name="Verdetto" durationInFrames={Math.round(S3 * fps)} premountFor={fps}><Verdetto /></Series.Sequence>
      <Series.Sequence name="CTA" durationInFrames={Math.round(S4 * fps)} premountFor={fps}><Cta /></Series.Sequence>
    </Series>
  );
};
export {Calcolo_ as CalcoloVideo};
