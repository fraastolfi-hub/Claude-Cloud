// Reel per gli annunci Meta del libro (9:16, 15 s, senza voce): foto di Francesco con il libro, testo animato, chiusura con prezzo
// e «Il link è qui sotto». Stile del tema editoriale del sito: Newsreader per i titoli, Figtree, giallo solo come sottolineatura.
import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, Series, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/fonts';

loadFont({family: 'Newsreader', url: staticFile('fonts/newsreader.woff2'), weight: '200 800'});
loadFont({family: 'Figtree', url: staticFile('fonts/figtree.woff2'), weight: '300 900'});
const SERIF = 'Newsreader', SANS = 'Figtree';
const CARTA = '#fcfbf8', SABBIA = '#f2efe8', INK = '#15181c', GRAF = '#4a4f57', NEB = '#6f747c', NOTTE = '#121a22', NFG = '#eef0f2', NFG2 = '#b8c0c8', Y = '#ffd22e';
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const useS = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
const useT = (from: number, dur = 0.5) => { const s = useS(); return interpolate(s, [from, from + dur], [0, 1], {...clamp, easing: ease}); };

// testo: *parola* = sottolineatura gialla che si disegna
const Hl: React.FC<{t: string; at: number}> = ({t, at}) => {
  const sw = useT(at + 0.35, 0.5);
  return <>{t.split('*').map((p, i) => i % 2
    ? <span key={i} style={{backgroundImage: `linear-gradient(${Y},${Y})`, backgroundRepeat: 'no-repeat', backgroundSize: `${sw * 100}% .1em`, backgroundPosition: '0 92%'}}>{p}</span>
    : <span key={i}>{p}</span>)}</>;
};
const Title: React.FC<{t: string; at?: number; size?: number; color?: string; top?: number; center?: boolean}> = ({t, at = 0.1, size = 92, color = INK, top = 260, center}) => {
  const a = useT(at, 0.5);
  return <h1 style={{position: 'absolute', left: 72, right: 72, top, margin: 0, font: `500 ${size}px/1.06 ${SERIF}`, letterSpacing: '-.015em', color, opacity: a, translate: `0px ${(1 - a) * 28}px`, textAlign: center ? 'center' : 'left', whiteSpace: 'pre-line'}}><Hl t={t} at={at} /></h1>;
};
const Sub: React.FC<{t: string; at?: number; top: number; color?: string; size?: number}> = ({t, at = 0.5, top, color = GRAF, size = 44}) => {
  const a = useT(at, 0.5);
  return <p style={{position: 'absolute', left: 72, right: 72, top, margin: 0, font: `400 ${size}px/1.4 ${SANS}`, color, opacity: a, translate: `0px ${(1 - a) * 20}px`}}>{t}</p>;
};
const Kicker: React.FC<{dark?: boolean}> = ({dark}) => (
  <span style={{position: 'absolute', left: 72, top: 200, padding: '4px 0 4px 52px', background: `linear-gradient(${dark ? NFG2 : NEB},${dark ? NFG2 : NEB}) 0 50%/38px 2px no-repeat`, color: dark ? NFG2 : NEB, font: `600 26px/1.2 ${SANS}`, letterSpacing: '.14em', textTransform: 'uppercase'}}>Il libro · Hotel Positioning</span>
);

// foto a tutto schermo con leggero zoom; velo in alto per leggere il titolo
const Foto: React.FC<{top?: number}> = ({top = 600}) => {
  const s = useS();
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top, bottom: 0, overflow: 'hidden'}}>
      <Img src={staticFile('francesco-libro.webp')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 86%', scale: String(1.03 + s * 0.012), transformOrigin: '50% 30%'}} />
    </div>
  );
};
const Piano: React.FC<{bg: string; children: React.ReactNode}> = ({bg, children}) => <AbsoluteFill style={{background: bg, fontFamily: SANS, overflow: 'hidden'}}>{children}</AbsoluteFill>;

const Chiusura: React.FC<{titolo: string}> = ({titolo}) => {
  const a = useT(0.6, 0.5); const b = useT(1.3, 0.5); const s = useS();
  const pulse = 1 + 0.03 * Math.max(0, Math.sin((s - 1.8) * Math.PI * 1.4));
  return (
    <Piano bg={CARTA}>
      <Foto top={540} />
      <Kicker />
      <Title t={titolo} top={262} size={84} />
      <div style={{position: 'absolute', right: 64, bottom: 520, opacity: a, translate: `0px ${(1 - a) * 20}px`, background: CARTA, color: INK, padding: '22px 30px', borderRadius: 6, display: 'flex', alignItems: 'baseline', gap: 16, boxShadow: '0 12px 30px rgba(21,24,28,.2)'}}>
        <b style={{font: `500 66px/1 ${SERIF}`}}>19,90 €</b><span style={{font: `600 26px/1.2 ${SANS}`, letterSpacing: '.1em', textTransform: 'uppercase', color: GRAF}}>su Amazon</span>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 400, display: 'flex', justifyContent: 'center', opacity: b}}>
        <span style={{scale: String(pulse), background: INK, color: CARTA, borderRadius: 4, padding: '26px 44px', font: `600 46px/1 ${SANS}`}}>Il link è qui sotto ↓</span>
      </div>
    </Piano>
  );
};

// ---------------------------------------------------------------- R1 · La domanda
const R1a: React.FC = () => (<Piano bg={CARTA}><Foto /><Kicker /><Title t={'Il tuo hotel ha già\n*una risposta.*'} at={0} size={100} /></Piano>);
const R1b: React.FC = () => {
  const st = useT(0.9, 0.4);
  return (<Piano bg={SABBIA}>
    <p style={{position: 'absolute', left: 72, right: 72, top: 560, margin: 0, font: `500 92px/1.1 ${SERIF}`, color: GRAF, opacity: useT(0, 0.4)}}>
      <span style={{position: 'relative'}}>«Posizione, servizio, camere.»<span style={{position: 'absolute', left: 0, top: '55%', height: 6, width: `${st * 100}%`, background: INK}} /></span>
    </p>
    <Title t={'Ce l’ha anche\n*il vicino.*'} at={1.4} size={100} top={900} />
  </Piano>);
};
const R1c: React.FC = () => (<Piano bg={NOTTE}><Title t={'Quando le risposte sono uguali, l’ospite confronta\n*il prezzo.*'} at={0.1} size={92} top={620} color={NFG} /></Piano>);
const R1d: React.FC = () => {
  const a = useT(0, 0.7);
  return (<Piano bg={CARTA}>
    <Title t={'Il libro ti porta\nalla risposta *solo tua.*'} at={0.1} size={90} top={240} />
    <Sub t="Sei passaggi. 120 pagine. Con i casi veri." at={0.7} top={500} />
    <Img src={staticFile('libro.webp')} style={{position: 'absolute', left: 300, top: 700, width: 480, borderRadius: 8, boxShadow: '0 40px 80px rgba(21,24,28,.28)', opacity: a, rotate: `${(1 - a) * 6 - 2}deg`, scale: String(0.9 + 0.1 * a)}} />
  </Piano>);
};
// ---------------------------------------------------------------- R2 · La commissione
const R2a: React.FC = () => (<Piano bg={CARTA}><Foto /><Kicker /><Title t={'Ogni notte su Booking\n*costa una volta e mezza questo libro.*'} at={0} size={84} /></Piano>);
const R2b: React.FC = () => {
  const s = useS(); const n = Math.round(interpolate(s, [0.4, 1.6], [0, 30], {...clamp, easing: Easing.out(Easing.cubic)}));
  return (<Piano bg={NOTTE}>
    <p style={{position: 'absolute', left: 72, top: 520, margin: 0, font: `500 300px/1 ${SERIF}`, color: NFG}}>{n} €</p>
    <Title t={'Commissione su una camera da 180 €.\n*Ogni notte.*'} at={1.2} size={84} top={900} color={NFG} />
    <p style={{position: 'absolute', left: 72, bottom: 400, margin: 0, font: `400 28px/1.3 ${SANS}`, color: NFG2, opacity: useT(1.6, 0.4)}}>Esempio: commissione del 17%.</p>
  </Piano>);
};
const R2c: React.FC = () => {
  const a = useT(0.3, 0.8); const b = useT(1.2, 0.8);
  const bar = (w: number, col: string) => <div style={{height: 70, width: w, background: col, borderRadius: 4}} />;
  return (<Piano bg={CARTA}>
    <Title t={'Il libro: 19,90 €.\n*Una volta.*'} at={0} size={92} top={300} />
    <div style={{position: 'absolute', left: 72, right: 72, top: 760, display: 'grid', gap: 40, font: `600 32px/1.2 ${SANS}`, color: INK}}>
      <div style={{opacity: a}}>Il libro, una volta<div style={{marginTop: 12, display: 'flex', alignItems: 'center', gap: 20}}>{bar(560 * a * 0.66, Y)}<span>19,90 €</span></div></div>
      <div style={{opacity: b}}>La commissione, in un mese di notti<div style={{marginTop: 12, display: 'flex', alignItems: 'center', gap: 20}}>{bar(700 * b, INK)}<span>900 €</span></div></div>
    </div>
    <p style={{position: 'absolute', left: 72, bottom: 400, margin: 0, font: `400 26px/1.3 ${SANS}`, color: NEB, opacity: b}}>Esempio: 30 € a notte per 30 notti, una camera.</p>
  </Piano>);
};
const R2d: React.FC = () => (<Piano bg={SABBIA}><Title t={'Dentro: come farti scegliere\n*senza abbassare il prezzo.*'} at={0.1} size={90} top={640} /></Piano>);
// ---------------------------------------------------------------- R3 · Sei passaggi
const PASSI = ['Il bisogno vero', 'Le alternative', 'Le unicità', 'La persona giusta', 'La categoria', 'Il trend'];
const R3a: React.FC = () => (<Piano bg={CARTA}><Foto /><Kicker /><Title t={'Sei passaggi per trovare\n*perché ti scelgono.*'} at={0} size={92} /></Piano>);
const R3b: React.FC = () => (
  <Piano bg={CARTA}>
    <Title t={'Il metodo, *in ordine.*'} at={0} size={80} top={240} />
    <div style={{position: 'absolute', left: 72, right: 72, top: 420, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 22}}>
      {PASSI.map((p, i) => {
        const a = useT(0.4 + i * 0.45, 0.45);
        return <div key={p} style={{opacity: a, translate: `0px ${(1 - a) * 24}px`, background: i === 4 ? CARTA : '#ffffff', border: `1px solid ${i === 4 ? INK : '#e3e1db'}`, borderRadius: 6, padding: '30px 28px', minHeight: 230}}>
          <span style={{display: 'grid', placeItems: 'center', width: 64, height: 64, borderRadius: '50%', border: `1px solid ${INK}`, font: `500 32px/1 ${SERIF}`}}>{i + 1}</span>
          <p style={{margin: '22px 0 0', font: `500 44px/1.1 ${SERIF}`, color: INK}}>{p}</p>
        </div>;
      })}
    </div>
  </Piano>
);
const R3c: React.FC = () => (<Piano bg={NOTTE}><Title t={'Alla fine stanno\n*su un foglio solo.*'} at={0.1} size={96} top={680} color={NFG} /></Piano>);

type Sc = [React.FC, number];
const montaggio = (sc: Sc[]) => () => {
  const {fps} = useVideoConfig();
  return <Series>{sc.map(([C, d], i) => <Series.Sequence key={i} durationInFrames={Math.round(d * fps)} premountFor={fps}><C /></Series.Sequence>)}</Series>;
};
const fine = (t: string): React.FC => () => <Chiusura titolo={t} />;
export const R1S: Sc[] = [[R1a, 3], [R1b, 3.2], [R1c, 2.6], [R1d, 3], [fine('Tu, oggi,\n*cosa risponderesti?*'), 3.2]];
export const R2S: Sc[] = [[R2a, 2.6], [R2b, 3.2], [R2c, 3.6], [R2d, 2.4], [fine('Lo paghi una volta.\n*Lo usi ogni notte.*'), 3.2]];
export const R3S: Sc[] = [[R3a, 3], [R3b, 5], [R3c, 3], [fine('Il canvas è\n*gratis con il libro.*'), 4]];
export const durata = (sc: Sc[]) => sc.reduce((a, [, d]) => a + d, 0);
export const ReelDomanda = montaggio(R1S);
export const ReelCommissione = montaggio(R2S);
export const ReelPassi = montaggio(R3S);
