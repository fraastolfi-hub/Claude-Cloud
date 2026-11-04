// I due reel dello script reel-libro-v1.md (Le pesche di mio nonno · La prima pagina), versione senza riprese:
// grafica animata + sottotitoli. Il "testo a schermo" dello script è il titolo grande; la "voce" diventa il sottotitolo.
// Regola dello script: il primo fotogramma è la copertina e deve funzionare muto e fermo (il primo titolo è già visibile).
import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, Series, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const useS = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
const useT = (from: number, dur = 0.5) => { const s = useS(); return from < 0 ? 1 : interpolate(s, [from, from + dur], [0, 1], {...clamp, easing: ease}); };
const INK = C.ink, Y = '#FFE600', CR = '#f6f1ea', ROSSO = '#e0452b';

const Fondo: React.FC<{children: React.ReactNode; scuro?: boolean}> = ({children, scuro}) => {
  const s = useS();
  return (
    <AbsoluteFill style={{background: scuro ? INK : CR, fontFamily: text, color: scuro ? '#fff' : INK, overflow: 'hidden'}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: '50%', left: -320, top: 380 + Math.sin(s * 0.6) * 30, background: `radial-gradient(circle, ${scuro ? 'rgba(255,230,0,.10)' : 'rgba(255,230,0,.20)'}, rgba(255,230,0,0) 65%)`}} />
      {children}
    </AbsoluteFill>
  );
};

const hl = (p: string, i: number, sw = 1) => i % 2
  ? <span key={i} style={{backgroundImage: `linear-gradient(${Y},${Y})`, backgroundRepeat: 'no-repeat', backgroundSize: `${sw * 100}% 45%`, backgroundPosition: '0 88%', padding: '0 .05em'}}>{p}</span>
  : <span key={i}>{p}</span>;

// titolo grande (testo a schermo); *parola* = evidenziatore giallo
const Titolo: React.FC<{t: string; at?: number; top?: number; size?: number; scuro?: boolean}> = ({t, at = 0, top = 280, size = 96}) => {
  const a = useT(at, 0.45); const sw = useT(at < 0 ? -1 : at + 0.25, 0.45);
  return (
    <h1 style={{position: 'absolute', left: 80, right: 80, top, margin: 0, textAlign: 'center', font: `900 ${size}px/1.06 ${display}`, letterSpacing: '-.02em', opacity: a, translate: `0px ${(1 - a) * 26}px`, whiteSpace: 'pre-line'}}>
      {t.split('*').map((p, i) => hl(p, i, sw))}
    </h1>
  );
};

// sottotitolo (la voce): le frasi si alternano nel tempo della scena
const Voce: React.FC<{frasi: string[]; dur: number; scuro?: boolean}> = ({frasi, dur, scuro}) => {
  const s = useS();
  const k = Math.min(frasi.length - 1, Math.floor((s / dur) * frasi.length));
  const t0 = (k * dur) / frasi.length;
  const a = interpolate(s, [t0, t0 + 0.2], [0, 1], clamp);
  return (
    <div style={{position: 'absolute', left: 90, right: 90, top: 1420, display: 'flex', justifyContent: 'center'}}>
      <p style={{margin: 0, textAlign: 'center', font: `700 46px/1.3 ${text}`, color: scuro ? '#fff' : INK, background: scuro ? 'rgba(255,255,255,.08)' : 'rgba(255,255,255,.75)', borderRadius: 20, padding: '18px 28px', opacity: a}}>{frasi[k]}</p>
    </div>
  );
};

const Bio: React.FC<{at: number; top?: number; label?: string}> = ({at, top = 1250, label = 'Il link è in bio'}) => {
  const s = useS(); const a = useT(at, 0.4);
  const pulse = 1 + 0.04 * Math.max(0, Math.sin((s - at - 0.4) * Math.PI * 1.5));
  return <div style={{position: 'absolute', left: 0, right: 0, top, display: 'flex', justifyContent: 'center', opacity: a}}><span style={{scale: String(pulse), background: INK, color: '#fff', borderRadius: 999, padding: '28px 60px', font: `900 60px/1 ${display}`}}>{label}</span></div>;
};

// ---------------------------------------------------------------- disegni

const Pesca: React.FC<{size?: number; x: number; y: number; rot?: number; o?: number}> = ({size = 200, x, y, rot = 0, o = 1}) => (
  <svg viewBox="0 0 100 100" style={{position: 'absolute', left: x, top: y, width: size, height: size, rotate: `${rot}deg`, opacity: o}}>
    <path d="M50 22 C20 18 8 45 14 66 C20 88 44 96 54 92 C76 88 94 70 88 46 C82 24 64 20 50 22Z" fill="#ffab6b" stroke={INK} strokeWidth={3} />
    <path d="M50 22 C46 40 48 70 54 92" fill="none" stroke={INK} strokeWidth={2.5} opacity={0.5} />
    <path d="M52 22 C56 10 70 6 80 10 C72 20 62 22 52 22Z" fill="#5fb86a" stroke={INK} strokeWidth={3} />
  </svg>
);

const Cassetta: React.FC<{x: number; y: number; w?: number; children?: React.ReactNode; o?: number; scale?: number}> = ({x, y, w = 620, children, o = 1, scale = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: w * 0.55, opacity: o, scale: String(scale)}}>
    <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'flex-end', justifyContent: 'center'}}>{children}</div>
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: '62%', background: '#c99459', border: `5px solid ${INK}`, borderRadius: 14, display: 'grid', gridTemplateRows: '1fr 1fr', gap: 10, padding: 14}}>
      <div style={{background: '#b07c45', borderRadius: 6, border: `3px solid ${INK}`}} />
      <div style={{background: '#b07c45', borderRadius: 6, border: `3px solid ${INK}`}} />
    </div>
  </div>
);

const Albero: React.FC<{x: number; s?: number}> = ({x, s = 1}) => (
  <svg viewBox="0 0 120 200" style={{position: 'absolute', left: x, top: 1060, width: 120 * s, height: 200 * s, opacity: 0.35}}>
    <path d="M60 200 L60 110 M60 130 L30 80 M60 120 L92 70 M30 80 L18 50 M30 80 L44 46 M92 70 L104 40 M92 70 L78 38 M60 110 L60 60" stroke={INK} strokeWidth={6} strokeLinecap="round" fill="none" />
  </svg>
);

const Scheda: React.FC<{x: number; y: number; w: number; titolo: string; sotto: string; badge?: React.ReactNode; o?: number; tu?: boolean}> = ({x, y, w, titolo, sotto, badge, o = 1, tu}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, opacity: o, background: '#fff', borderRadius: 26, boxShadow: '0 18px 50px rgba(38,37,33,.12)', border: tu ? `4px solid ${INK}` : '4px solid transparent', overflow: 'hidden'}}>
    <div style={{height: 190, background: 'linear-gradient(180deg,#bfe3f2 0 50%,#4fb3d9 50% 72%,#f1dfb8 72%)', position: 'relative'}}>{badge}</div>
    <div style={{padding: '20px 24px'}}><b style={{font: `800 38px/1.15 ${display}`}}>{titolo}</b><div style={{font: `600 28px/1.3 ${text}`, color: C.ink2}}>{sotto}</div></div>
  </div>
);

const Libro: React.FC<{x: number; y: number; w: number; rot?: number; o?: number; sc?: number}> = ({x, y, w, rot = 0, o = 1, sc = 1}) => (
  <Img src={staticFile('libro.webp')} style={{position: 'absolute', left: x, top: y, width: w, borderRadius: 8, boxShadow: '0 36px 70px rgba(38,37,33,.3)', rotate: `${rot}deg`, opacity: o, scale: String(sc)}} />
);

// ---------------------------------------------------------------- REEL 1 · Le pesche di mio nonno

type Beat = {d: number; voce: string[]; C: React.FC<{d: number}>; scuro?: boolean};

const P1: React.FC<{d: number}> = () => {
  const s = useS();
  return (<>
    <Titolo t={'Mio nonno aveva le pesche\n*migliori della zona*…'} at={-1} top={300} size={92} />
    <Albero x={90} s={1.4} /><Albero x={800} s={1.2} />
    {[[260, 720, -12], [420, 690, 8], [580, 730, -4], [340, 860, 14], [500, 850, -10]].map(([x, y, r], i) =>
      <Pesca key={i} x={x} y={y + Math.sin(s * 2 + i) * 6} rot={r} size={190} />)}
  </>);
};
const P2: React.FC<{d: number}> = () => {
  const c = useT(0.2, 0.6);
  return (<>
    <Titolo t={'…e il potere\ndi un *mendicante*.'} />
    <Cassetta x={230} y={760 + (1 - c) * 120} o={c} />
    <p style={{position: 'absolute', left: 0, right: 0, top: 1170, textAlign: 'center', margin: 0, font: `700 40px/1 ${display}`, color: '#a39d93', opacity: useT(0.9, 0.4)}}>cassetta vuota</p>
  </>);
};
const P3: React.FC<{d: number}> = () => {
  const st = useT(2.6, 0.35);
  return (<>
    <Titolo t={'Il prezzo lo faceva\n*un altro*.'} />
    <Cassetta x={230} y={800}>
      <div style={{display: 'flex', marginBottom: 160}}>{[0, 1, 2].map((i) => <div key={i} style={{width: 150, height: 150, position: 'relative'}}><Pesca x={0} y={0} size={150} rot={i * 9 - 9} /></div>)}</div>
    </Cassetta>
    <div style={{position: 'absolute', left: 620, top: 690, rotate: `${-14 + (1 - st) * 20}deg`, scale: String(1.6 - 0.6 * st), opacity: st, border: `7px solid ${ROSSO}`, color: ROSSO, borderRadius: 16, padding: '12px 24px', font: `900 56px/1 ${display}`, background: 'rgba(255,255,255,.85)'}}>0,30 €/kg</div>
  </>);
};
const P4: React.FC<{d: number}> = () => {
  const s = useS();
  const n = Math.round(interpolate(s, [0.4, 3.2], [1, 40], {...clamp, easing: Easing.out(Easing.cubic)}));
  return (<>
    <Titolo t={'*Quarant’anni*\na lamentarsi.'} />
    <p style={{position: 'absolute', left: 0, right: 0, top: 720, margin: 0, textAlign: 'center', font: `900 300px/1 ${display}`, letterSpacing: '-.04em'}}>{n}</p>
    <p style={{position: 'absolute', left: 0, right: 0, top: 1040, margin: 0, textAlign: 'center', font: `700 54px/1 ${display}`, color: C.ink2}}>raccolti</p>
  </>);
};
const P5: React.FC<{d: number}> = () => {
  const a = useT(0.1, 0.5);
  return <h1 style={{position: 'absolute', left: 80, right: 80, top: 720, margin: 0, textAlign: 'center', font: `900 110px/1.08 ${display}`, color: Y, opacity: a, scale: String(0.94 + 0.06 * a), whiteSpace: 'pre-line'}}>{'«Vendere non è\nil mio mestiere.»'}</h1>;
};
const P6: React.FC<{d: number}> = () => {
  const a = useT(0.3, 0.5); const b = useT(1.2, 0.5);
  return (<>
    <Titolo t={'Vedo *mio nonno*.'} />
    <div style={{position: 'absolute', left: 100, top: 700, width: 380, height: 300, opacity: a}}><Pesca x={60} y={20} size={130} rot={-10} /><Pesca x={180} y={30} size={130} rot={8} /><Cassetta x={0} y={110} w={380} /></div>
    <p style={{position: 'absolute', left: 500, top: 800, margin: 0, font: `900 120px/1 ${display}`, opacity: b}}>=</p>
    <svg viewBox="0 0 100 110" style={{position: 'absolute', left: 640, top: 680, width: 300, opacity: b}}>
      <rect x={14} y={20} width={72} height={88} rx={6} fill="#fff" stroke={INK} strokeWidth={4} />
      {[0, 1, 2, 3].map((r) => [0, 1, 2].map((c) => <rect key={`${r}${c}`} x={24 + c * 20} y={30 + r * 18} width={12} height={10} rx={2} fill={r === 1 && c === 1 ? Y : '#bfe3f2'} stroke={INK} strokeWidth={2} />))}
      <rect x={42} y={92} width={16} height={16} fill={INK} />
    </svg>
  </>);
};
const P7: React.FC<{d: number}> = () => {
  const a = useT(0.3, 0.5); const b = useT(2.2, 0.5);
  return (<>
    <Titolo t={'La vendita\nla regala a *Booking*.'} />
    <Scheda x={150} y={640} w={780} titolo="Camera curata come un gioiello" sotto="Lenzuola stirate · fiori freschi · vista mare" o={a} />
    <div style={{position: 'absolute', left: 150, right: 150, top: 1070, opacity: b, translate: `0px ${(1 - b) * 40}px`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: '#003b95', color: '#fff', borderRadius: 22, padding: '26px 34px', font: `800 46px/1 ${display}`}}>
      <span>Prenota</span><span style={{background: '#fff', color: '#003b95', borderRadius: 12, padding: '10px 16px', fontSize: 38}}>−18%</span>
    </div>
  </>);
};
const P8: React.FC<{d: number}> = () => {
  const l = useT(0.2, 0.7); const t = useT(1.4, 0.4);
  return (<>
    <Cassetta x={190} y={590} w={700}><div style={{marginBottom: 40}} /></Cassetta>
    <Libro x={375} y={180 + l * 120} w={330} rot={-6 + l * 4} o={l} />
    <p style={{position: 'absolute', left: 60, right: 60, top: 1040, margin: 0, textAlign: 'center', font: `900 84px/1.05 ${display}`, opacity: t}}>{hl('Hotel Positioning', 1, t)}</p>
    <p style={{position: 'absolute', left: 0, right: 0, top: 1150, margin: 0, textAlign: 'center', font: `700 46px/1 ${text}`, color: C.ink2, opacity: t}}>19,90 € su Amazon</p>
    <Bio at={2.4} top={1260} />
  </>);
};

const REEL1: Beat[] = [
  {d: 3, voce: ['Mio nonno aveva le pesche migliori della zona…'], C: P1},
  {d: 3, voce: ['…e il potere contrattuale di un mendicante.'], C: P2},
  {d: 6, voce: ['A fine raccolto arrivava il rappresentante della cooperativa.', 'Apriva due casse a caso.', 'E il prezzo lo faceva lui.'], C: P3},
  {d: 5, voce: ['Nonno si è lamentato per quarant’anni.', 'Poteva vendere da solo, e guadagnare il triplo.'], C: P4},
  {d: 3, voce: ['Una frase, sempre quella.'], C: P5, scuro: true},
  {d: 4, voce: ['Quando guardo un albergatore…', '…vedo mio nonno.'], C: P6},
  {d: 6, voce: ['Cura le camere come un orafo.', 'Poi la vendita la regala a Booking.'], C: P7},
  {d: 5, voce: ['L’ho scritto per chi il prezzo vuole farselo da solo.'], C: P8},
];

// ---------------------------------------------------------------- REEL 2 · La prima pagina

const Q1: React.FC<{d: number}> = () => (<>
  <Libro x={330} y={560} w={420} rot={-3} />
  <Titolo t={'Questo *non* è un libro\nsul marketing alberghiero.'} at={-1} top={250} size={86} />
</>);
const Post: React.FC<{t: string; x: number; y: number; rot: number; at: number; giu?: number}> = ({t, x, y, rot, at, giu = 99}) => {
  const a = useT(at, 0.4); const f = useT(giu, 0.6); const st = useT(giu - 0.4, 0.3);
  return (
    <div style={{position: 'absolute', left: x, top: y + f * 900, rotate: `${rot + f * 30}deg`, opacity: a * (1 - f), scale: String(0.8 + 0.2 * a), width: 420, padding: '40px 34px', background: '#fff6a8', boxShadow: '0 16px 40px rgba(38,37,33,.15)', font: `800 54px/1.15 ${display}`}}>
      <span style={{position: 'relative'}}>{t}<span style={{position: 'absolute', left: 0, top: '52%', height: 7, width: `${st * 100}%`, background: ROSSO, borderRadius: 4}} /></span>
    </div>
  );
};
const Q2: React.FC<{d: number}> = () => (<>
  <Titolo t={'Di quelli ne trovi *a chili*.'} />
  <Post t="«Cura le foto.»" x={110} y={620} rot={-6} at={0.4} />
  <Post t="«Spingi il diretto.»" x={540} y={820} rot={5} at={1.4} />
</>);
const Q3: React.FC<{d: number}> = () => (<>
  <Post t="«Cura le foto.»" x={110} y={620} rot={-6} at={-1} giu={0.6} />
  <Post t="«Spingi il diretto.»" x={540} y={820} rot={5} at={-1} giu={0.8} />
  <Titolo t={'*E inutili.*'} top={760} size={150} at={0.2} />
</>);
const Q4: React.FC<{d: number}> = () => {
  const s = useS(); const a = useT(0.3, 0.6);
  return (<>
    <Titolo t={'Arrivano tutti\n*dopo una domanda*.'} />
    <p style={{position: 'absolute', left: 0, right: 0, top: 640, margin: 0, textAlign: 'center', font: `900 520px/1 ${display}`, opacity: a, scale: String(0.7 + 0.3 * a), rotate: `${Math.sin(s * 3) * 3}deg`}}><span style={{color: Y, WebkitTextStroke: `10px ${INK}`}}>?</span></p>
  </>);
};
const Q5: React.FC<{d: number}> = () => {
  const a = useT(0.3, 0.5); const b = useT(0.9, 0.5); const m = useT(1.8, 0.5); const q = useT(4.5, 0.5);
  return (<>
    <Titolo t={'Perché dovrebbe\nscegliere *te*?'} at={q > 0 ? 4.5 : 99} />
    <Scheda x={80} y={660} w={430} titolo="Il tuo hotel" sotto="Piscina · Colazione" o={a} tu />
    <Scheda x={570} y={660} w={430} titolo="L’hotel vicino" sotto="Piscina · Colazione" o={b} />
    <div style={{position: 'absolute', left: 0, right: 0, top: 1110, display: 'flex', justifyContent: 'center', opacity: m}}>
      <span style={{font: `800 46px/1 ${display}`, background: '#fff', borderRadius: 999, padding: '16px 30px', boxShadow: '0 8px 24px rgba(38,37,33,.1)'}}>⟷ 300 metri</span>
    </div>
  </>);
};
const Q6: React.FC<{d: number}> = () => {
  const s = useS();
  const p = Math.round(interpolate(s, [0.6, 3.4], [120, 79], {...clamp, easing: Easing.in(Easing.quad)}));
  return (<>
    <Titolo t={'Resta il prezzo.\n*Il tuo.*'} />
    <div style={{position: 'absolute', left: 290, top: 700, width: 500, height: 330, rotate: '-6deg', background: '#fff', border: `6px solid ${INK}`, borderRadius: '24px 90px 90px 24px', display: 'grid', placeItems: 'center', font: `900 160px/1 ${display}`, color: p < 100 ? ROSSO : INK}}>
      {p} €
      <i style={{position: 'absolute', right: 50, top: '50%', marginTop: -22, width: 44, height: 44, borderRadius: '50%', border: `6px solid ${INK}`, background: CR}} />
    </div>
  </>);
};
const Q7: React.FC<{d: number}> = () => {
  const a = useT(0.3, 0.6); const b = useT(1.4, 0.8);
  const bar = (w: number, col: string) => ({height: 90, width: w, background: col, border: `4px solid ${INK}`, borderRadius: 16});
  return (<>
    <Titolo t={'*19,90 €*'} size={170} top={260} />
    <div style={{position: 'absolute', left: 110, right: 110, top: 720, display: 'grid', gap: 40, font: `800 42px/1.2 ${display}`}}>
      <div style={{opacity: a}}>Il libro<div style={{marginTop: 14, display: 'flex', alignItems: 'center', gap: 22}}><div style={bar(560 * a, Y)} /><span>19,90 €</span></div></div>
      <div style={{opacity: b}}>Commissione su una camera da 180 €<div style={{marginTop: 14, display: 'flex', alignItems: 'center', gap: 22}}><div style={bar(845 * 0.86 * b, ROSSO)} /><span>30 €</span></div></div>
    </div>
  </>);
};
const Q8: React.FC<{d: number}> = () => {
  const l = useT(0, 0.6);
  return (<>
    <Titolo t={'Lo paghi *una volta*.'} />
    <Libro x={385} y={480} w={310} rot={(1 - l) * -10} o={l} sc={0.9 + 0.1 * l} />
    <Bio at={1.6} top={1040} />
    <p style={{position: 'absolute', left: 0, right: 0, top: 1800, margin: 0, textAlign: 'center', font: `600 28px/1 ${text}`, color: '#8a847a'}}>Esempio: 30 € di commissione su una camera da 180 €.</p>
  </>);
};

const REEL2: Beat[] = [
  {d: 3, voce: ['«Questo non è un libro sul marketing alberghiero.»'], C: Q1},
  {d: 5, voce: ['Di quelli ne trovi a chili.', 'Cura le foto, spingi il diretto. Consigli giusti…'], C: Q2},
  {d: 2, voce: ['…e inutili.'], C: Q3},
  {d: 3, voce: ['Perché arrivano tutti dopo una domanda.'], C: Q4},
  {d: 7, voce: ['Perché un ospite dovrebbe scegliere te…', '…e non l’hotel a trecento metri, con la tua stessa piscina?'], C: Q5},
  {d: 5, voce: ['Se non sai rispondere in una frase, resta il prezzo.', 'Il tuo.'], C: Q6},
  {d: 5, voce: ['Costa diciannove e novanta.', 'Meno della commissione su una camera da centottanta euro.'], C: Q7},
  {d: 4, voce: ['Il libro lo paghi una volta. La commissione, ogni notte.'], C: Q8},
];

// ---------------------------------------------------------------- montaggio

const Scena: React.FC<{b: Beat}> = ({b}) => (
  <Fondo scuro={b.scuro}><b.C d={b.d} /><Voce frasi={b.voce} dur={b.d} scuro={b.scuro} /></Fondo>
);
const Reel: React.FC<{beats: Beat[]}> = ({beats}) => {
  const {fps} = useVideoConfig();
  return <Series>{beats.map((b, i) => <Series.Sequence key={i} durationInFrames={Math.round(b.d * fps)} premountFor={fps}><Scena b={b} /></Series.Sequence>)}</Series>;
};
export const REEL1_S = REEL1.reduce((a, b) => a + b.d, 0);
export const REEL2_S = REEL2.reduce((a, b) => a + b.d, 0);
export const ReelPesche: React.FC = () => <Reel beats={REEL1} />;
export const ReelPrimaPagina: React.FC = () => <Reel beats={REEL2} />;
