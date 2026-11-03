// V2 · La lancetta: un indicatore che oscilla mentre scorrono i 21 controlli e si ferma sul verdetto.
import React from 'react';
import {Easing, interpolate, Series, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';
import {Cta, Frame, Kicker, Line, useT} from '../parts';
import {SEM, TUTTI} from '../controlli';

const S1 = 6.2, S2 = 3.2;
export const LANCETTA_S = S1 + S2;

// angolo da -90° (Non ancora) a +90° (Sì): la lancetta cerca e si ferma a metà tra quasi e sì
const ango = (t: number) => {
  const k = [0.6, 1.4, 2.2, 3.0, 3.7, 4.3];
  const v = [-88, 60, -40, 35, -5, 8];
  return interpolate(t, k, v, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
};

const arc = (r: number, a0: number, a1: number) => {
  const p = (a: number) => [250 + r * Math.cos((a - 180) * Math.PI / 180), 250 + r * Math.sin((a - 180) * Math.PI / 180)];
  const [x0, y0] = p(a0), [x1, y1] = p(a1);
  return `M ${x0} ${y0} A ${r} ${r} 0 0 1 ${x1} ${y1}`;
};

const Indicatore: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const story = height > 1500;
  const t = frame / fps;
  const a = ango(t);
  const g = useT(0.3, 0.6);
  const n = Math.max(0, Math.min(21, Math.floor((t - 0.6) / 0.17) + 1));
  const fine = useT(4.5, 0.5);
  const c = TUTTI[Math.max(0, Math.min(20, n - 1))];
  return (
    <Frame bg={C.crema}>
      <Kicker />
      <div style={{marginTop: 30}}>
        <Line at={0} size={story ? 96 : 84}>Quanto è efficace</Line>
        <Line at={0.2} size={story ? 96 : 84} hl>il tuo sito?</Line>
      </div>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
        <svg viewBox="0 0 500 290" style={{width: story ? 860 : 700, opacity: g}}>
          <path d={arc(200, 0, 60)} stroke={SEM.rosso} strokeWidth={56} fill="none" />
          <path d={arc(200, 60, 120)} stroke={SEM.giallo} strokeWidth={56} fill="none" />
          <path d={arc(200, 120, 180)} stroke={SEM.verde} strokeWidth={56} fill="none" />
          <path d={arc(228, 0, 180)} stroke={C.ink} strokeWidth={5} fill="none" />
          <path d={arc(172, 0, 180)} stroke={C.ink} strokeWidth={5} fill="none" />
          <g style={{transformOrigin: '250px 250px', transform: `rotate(${a}deg)`}}>
            <polygon points="244,250 256,250 250,70" fill={C.ink} />
          </g>
          <circle cx={250} cy={250} r={22} fill={C.ink} />
          <text x={58} y={286} fontFamily={display} fontWeight={800} fontSize={22} fill={C.ink}>Non ancora</text>
          <text x={226} y={34} fontFamily={display} fontWeight={800} fontSize={22} fill={C.ink}>Quasi</text>
          <text x={420} y={286} fontFamily={display} fontWeight={800} fontSize={22} fill={C.ink}>Sì</text>
        </svg>
        <div style={{marginTop: story ? 50 : 26, height: story ? 130 : 110, textAlign: 'center'}}>
          <div style={{opacity: 1 - fine, font: `800 ${story ? 44 : 38}px/1.2 ${display}`}}>Controllo {n}/21</div>
          <div style={{opacity: 1 - fine, font: `500 ${story ? 36 : 32}px/1.3 ${text}`, color: C.ink2, marginTop: 6}}>{c.area} · {c.nome}</div>
          <div style={{opacity: fine, translate: `0px ${(fine - 1) * 120 - 0}px`, font: `900 ${story ? 60 : 52}px/1.15 ${display}`}}>
            <span style={{background: SEM.giallo, borderRadius: 12, padding: '0 .15em'}}>Quasi.</span> Qualche modifica prima di investire.
          </div>
        </div>
      </div>
      <p style={{margin: 0, font: `600 26px/1 ${text}`, color: C.ink2}}>Esempio, non un hotel reale</p>
    </Frame>
  );
};

export const LancettaVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <Series>
      <Series.Sequence name="Indicatore" durationInFrames={Math.round(S1 * fps)} premountFor={fps}><Indicatore /></Series.Sequence>
      <Series.Sequence name="CTA" durationInFrames={Math.round(S2 * fps)} premountFor={fps}><Cta line="Il tagliando al tuo sito. Gratis." /></Series.Sequence>
    </Series>
  );
};
