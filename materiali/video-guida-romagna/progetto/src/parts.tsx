import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from './theme';

const ease = Easing.bezier(0.16, 1, 0.3, 1);
// 0 → 1 tra due istanti (in secondi), con entrata morbida
export const useT = (fromS: number, durS = 0.6) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return interpolate(frame, [fromS * fps, (fromS + durS) * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
};

// margini sicuri: nelle Stories/Reels testi lontani dall'interfaccia di Instagram
export const useSafe = () => {
  const {height} = useVideoConfig();
  return height > 1500 ? {top: 220, bottom: 380, side: 96} : {top: 90, bottom: 90, side: 80};
};

export const Frame: React.FC<{bg: string; children: React.ReactNode}> = ({bg, children}) => {
  const s = useSafe();
  return (
    <AbsoluteFill style={{background: bg, fontFamily: text, color: C.ink}}>
      <div style={{position: 'absolute', left: s.side, right: s.side, top: s.top, bottom: s.bottom, display: 'flex', flexDirection: 'column'}}>{children}</div>
    </AbsoluteFill>
  );
};

export const Kicker: React.FC<{dark?: boolean}> = ({dark}) => {
  const t = useT(0, 0.5);
  return (
    <div style={{alignSelf: 'flex-start', opacity: t, translate: `0px ${(1 - t) * 20}px`, display: 'inline-flex', alignItems: 'center', gap: 12, border: `3px solid ${dark ? C.crema : C.ink}`, borderRadius: 999, background: dark ? C.ink : '#fff', color: dark ? C.crema : C.ink, padding: '12px 22px', font: `800 30px/1 ${display}`, textTransform: 'uppercase'}}>
      <i style={{width: 16, height: 16, borderRadius: '50%', background: C.giallo, border: `2.5px solid ${dark ? C.crema : C.ink}`}} />
      E tu, albergatore della Romagna?
    </div>
  );
};

// riga di titolo che entra dal basso; con hl l'evidenziatore giallo si stende da sinistra
// instant: evidenziatore già steso (su fondo scuro il testo nero sarebbe invisibile durante la stesura)
export const Line: React.FC<{at: number; hl?: boolean; instant?: boolean; size?: number; color?: string; hlColor?: string; children: React.ReactNode}> = ({at, hl, instant, size = 112, color = C.ink, hlColor = C.giallo, children}) => {
  const t = useT(at, 0.6);
  const sw = useT(at + 0.25, 0.5);
  const sweep = instant ? 1 : sw;
  return (
    <div style={{opacity: t, translate: `0px ${(1 - t) * 40}px`, font: `900 ${size}px/1.04 ${display}`, color: hl ? C.ink : color}}>
      <span style={hl ? {backgroundImage: `linear-gradient(${hlColor},${hlColor})`, backgroundRepeat: 'no-repeat', backgroundSize: `${sweep * 100}% 100%`, borderRadius: 14, padding: '0 .12em', boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone'} : {}}>{children}</span>
    </div>
  );
};

export const Sub: React.FC<{at: number; dark?: boolean; size?: number; children: React.ReactNode}> = ({at, dark, size = 46, children}) => {
  const t = useT(at, 0.6);
  return <p style={{opacity: t, translate: `0px ${(1 - t) * 24}px`, margin: '30px 0 0', font: `500 ${size}px/1.3 ${text}`, color: dark ? '#c4bdb1' : C.ink2}}>{children}</p>;
};

export const Logo: React.FC<{dark?: boolean}> = ({dark}) => {
  const ink = dark ? C.crema : C.ink;
  return (
    <span style={{display: 'inline-flex', alignItems: 'center', gap: 16, font: `800 38px/1 ${display}`, color: ink}}>
      <span style={{width: 52, height: 42, background: `linear-gradient(${ink},${ink}) 0 16px/12px 26px no-repeat, linear-gradient(${ink},${ink}) 14px 7px/12px 35px no-repeat, linear-gradient(${C.giallo},${C.giallo}) 28px 2px/12px 40px no-repeat, linear-gradient(${ink},${ink}) 42px 14px/10px 28px no-repeat`}} />
      Hotel Positioning
    </span>
  );
};

// scena finale comune: copertina della guida, promessa, pulsante
export const Cta: React.FC<{line: string; dark?: boolean}> = ({line, dark}) => {
  const cov = useT(0.1, 0.7);
  const t1 = useT(0.4, 0.6);
  const t2 = useT(0.8, 0.6);
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pulse = 1 + 0.04 * Math.max(0, Math.sin((frame / fps - 1.4) * Math.PI * 1.6));
  return (
    <Frame bg={dark ? C.ink : C.crema}>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
        <Img src={staticFile('copertina.webp')} style={{width: 380, border: `4px solid ${C.ink}`, borderRadius: 16, boxShadow: `12px 12px 0 ${dark ? C.giallo : C.ink}`, opacity: cov, rotate: `${(1 - cov) * 10 + 4}deg`, scale: String(0.85 + 0.15 * cov)}} />
        <p style={{opacity: t1, translate: `0px ${(1 - t1) * 24}px`, margin: '70px 0 0', font: `900 74px/1.08 ${display}`, color: dark ? C.crema : C.ink}}>{line}</p>
        <div style={{opacity: t2, scale: String(pulse), marginTop: 46, background: C.giallo, border: `4px solid ${C.ink}`, borderRadius: 18, boxShadow: `8px 8px 0 ${dark ? C.crema : C.ink}`, padding: '26px 44px', font: `900 50px/1 ${display}`, color: C.ink}}>Scarica la guida gratis →</div>
        <p style={{opacity: t2, margin: '34px 0 0', font: `600 34px/1.3 ${text}`, color: dark ? '#c4bdb1' : C.ink2}}>18 pagine · arriva nella tua email</p>
      </div>
      <div style={{display: 'flex', justifyContent: 'center', opacity: t2}}><Logo dark={dark} /></div>
    </Frame>
  );
};
