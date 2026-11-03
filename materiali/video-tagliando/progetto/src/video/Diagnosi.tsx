// V3 · La centralina: la foto del meccanico e, sotto, la diagnosi che si stampa riga per riga.
import React from 'react';
import {Img, interpolate, Series, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Cta, Frame, Line, useT} from '../parts';
import {SEM} from '../controlli';

const S1 = 7.4, S2 = 3.2;
export const DIAGNOSI_S = S1 + S2;

const RIGHE: [string, string, 'ok' | 'ko' | 'mid'][] = [
  ['Prima schermata', '✗', 'ko'],
  ['Test di sostituzione', '✗', 'ko'],
  ['Recensioni in pagina', '✓', 'ok'],
  ['Pulsante prenota', '✓', 'ok'],
  ['Velocità da telefono', '74/100', 'mid'],
  ['Come ti legge l’AI', 'a metà', 'mid'],
];

const Centralina: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const story = height > 1500;
  const t = frame / fps;
  const ph = useT(0, 0.6);
  const pan = interpolate(frame, [0, 7.4 * fps], [1, 1.08]);
  const perc = Math.round(interpolate(t, [1.6, 5.6], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const fine = useT(5.8, 0.5);
  const col = {ok: SEM.verde, ko: SEM.rosso, mid: SEM.giallo};
  return (
    <Frame bg={C.tealSoft}>
      <Line at={0} size={story ? 88 : 72}>Fai il tagliando</Line>
      <Line at={0.2} size={story ? 88 : 72} hl>al tuo sito.</Line>
      <div style={{marginTop: story ? 36 : 22, height: story ? 520 : 400, borderRadius: 26, overflow: 'hidden', border: `4px solid ${C.ink}`, boxShadow: `10px 10px 0 ${C.ink}`, opacity: ph}}>
        <Img src={staticFile('meccanico.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 4%', scale: String(pan)}} />
      </div>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <div style={{background: C.ink, color: C.crema, borderRadius: 24, padding: story ? '26px 30px' : '14px 24px', border: `4px solid ${C.ink}`}}>
          <div style={{display: 'flex', justifyContent: 'space-between', font: `800 ${story ? 30 : 26}px/1 ${display}`, textTransform: 'uppercase', color: '#c4bdb1'}}>
            <span>Diagnosi · 21 controlli</span><span>{perc}%</span>
          </div>
          <div style={{height: 12, borderRadius: 6, background: '#3a3833', margin: story ? '16px 0 18px' : '12px 0 12px'}}>
            <div style={{height: '100%', width: `${perc}%`, borderRadius: 6, background: C.giallo}} />
          </div>
          {RIGHE.map(([n, v, k], i) => {
            const at = 1.7 + i * 0.62;
            const o = interpolate(t, [at, at + 0.25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
            const chars = Math.round(interpolate(t, [at, at + 0.35], [0, n.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
            return (
              <div key={n} style={{opacity: o, display: 'flex', justifyContent: 'space-between', alignItems: 'center', font: `600 ${story ? 36 : 28}px/${story ? 1.55 : 1.4} ${text}`}}>
                <span>{n.slice(0, chars)}</span>
                <b style={{opacity: interpolate(t, [at + 0.35, at + 0.5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), color: C.ink, background: col[k], borderRadius: 10, padding: '0 14px', font: `800 ${story ? 30 : 26}px/1.4 ${display}`}}>{v}</b>
              </div>
            );
          })}
        </div>
        <div style={{opacity: fine, translate: `0px ${(1 - fine) * 30}px`, marginTop: story ? 28 : 18, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
          <span style={{font: `900 ${story ? 58 : 50}px/1 ${display}`}}>Verdetto: <span style={{background: SEM.giallo, borderRadius: 12, padding: '0 .15em'}}>quasi.</span></span>
          <span style={{font: `600 24px/1 ${text}`, color: C.ink2}}>Esempio</span>
        </div>
      </div>
    </Frame>
  );
};

export const DiagnosiVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <Series>
      <Series.Sequence name="Centralina" durationInFrames={Math.round(S1 * fps)} premountFor={fps}><Centralina /></Series.Sequence>
      <Series.Sequence name="CTA" durationInFrames={Math.round(S2 * fps)} premountFor={fps}><Cta line="Prima della campagna, il tagliando." /></Series.Sequence>
    </Series>
  );
};
