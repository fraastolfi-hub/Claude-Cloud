// Reel del libro: «Come far scegliere il tuo hotel in 6 passaggi». Stile tutorial (riferimento: video "How to edit a
// video with Claude"): etichetta PASSO 0X / 06 con i pallini, titolo con una parola evidenziata, un'interfaccia animata al
// centro, il sottotitolo in basso. Senza voce: musica (facoltativa, prop `musica`) e sottotitoli. Chiusura: Link in bio.
import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, interpolate, Series, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, text} from '../theme';

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const useT = (from: number, dur = 0.5) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return interpolate(f, [from * fps, (from + dur) * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
};
const useS = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
const INK = C.ink, Y = C.giallo, CR = '#f6f1ea', GRIGIO = '#c9c3b8';

// fondo crema con due macchie morbide, come nel riferimento
const Fondo: React.FC<{children: React.ReactNode}> = ({children}) => {
  const s = useS();
  return (
    <AbsoluteFill style={{background: CR, fontFamily: text, color: INK, overflow: 'hidden'}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: '50%', left: -300, top: 300 + Math.sin(s * 0.6) * 30, background: 'radial-gradient(circle, rgba(255,210,46,.22), rgba(255,210,46,0) 65%)'}} />
      <div style={{position: 'absolute', width: 1000, height: 1000, borderRadius: '50%', right: -420, bottom: 120 + Math.cos(s * 0.5) * 30, background: 'radial-gradient(circle, rgba(255,255,255,.9), rgba(255,255,255,0) 65%)'}} />
      {children}
    </AbsoluteFill>
  );
};

const Pill: React.FC<{label: string; step?: number}> = ({label, step}) => {
  const t = useT(0, 0.4);
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: 230, display: 'flex', justifyContent: 'space-between', alignItems: 'center', opacity: t, translate: `0px ${(1 - t) * -16}px`}}>
      <span style={{display: 'inline-flex', alignItems: 'center', gap: 14, background: '#fff', borderRadius: 999, padding: '16px 28px', boxShadow: '0 6px 24px rgba(38,37,33,.08)', font: `800 30px/1 ${display}`, letterSpacing: '.12em', textTransform: 'uppercase', color: C.ink2}}>
        <i style={{width: 14, height: 14, borderRadius: '50%', background: Y, border: `2.5px solid ${INK}`}} />
        {step ? <>Passo <b style={{color: INK}}>{String(step).padStart(2, '0')}</b> <span style={{color: GRIGIO}}>/ 06</span></> : label}
      </span>
      {step !== undefined || label === 'Bonus' ? (
        <span style={{display: 'flex', gap: 10}}>
          {[1, 2, 3, 4, 5, 6].map((i) => <i key={i} style={{width: 16, height: 16, borderRadius: '50%', background: (step ?? 7) >= i ? INK : '#e3ddd4'}} />)}
        </span>
      ) : null}
    </div>
  );
};

// titolo: la parola tra * viene evidenziata in giallo
const Titolo: React.FC<{t: string; top?: number; size?: number; at?: number}> = ({t, top = 330, size = 92, at = 0.1}) => {
  const a = useT(at, 0.5); const sw = useT(at + 0.3, 0.5);
  const parti = t.split('*');
  return (
    <h1 style={{position: 'absolute', left: 80, right: 80, top, margin: 0, font: `900 ${size}px/1.05 ${display}`, letterSpacing: '-.02em', opacity: a, translate: `0px ${(1 - a) * 30}px`}}>
      {parti.map((p, i) => i % 2 ? <span key={i} style={{backgroundImage: `linear-gradient(${Y},${Y})`, backgroundRepeat: 'no-repeat', backgroundSize: `${sw * 100}% 42%`, backgroundPosition: '0 88%', padding: '0 .06em'}}>{p}</span> : <span key={i}>{p}</span>)}
    </h1>
  );
};

// sottotitolo in basso: la parola tra * è colorata
const Sotto: React.FC<{t: string; at?: number}> = ({t, at = 0.35}) => {
  const a = useT(at, 0.4);
  return (
    <p style={{position: 'absolute', left: 90, right: 90, top: 1440, margin: 0, textAlign: 'center', font: `800 54px/1.25 ${display}`, opacity: a, translate: `0px ${(1 - a) * 20}px`}}>
      {t.split('*').map((p, i) => i % 2 ? <span key={i} style={{color: '#c98a00'}}>{p}</span> : <span key={i}>{p}</span>)}
    </p>
  );
};

const Finestra: React.FC<{titolo?: string; top?: number; h?: number | 'auto'; children: React.ReactNode; at?: number}> = ({titolo = 'Hotel Positioning', top = 560, h, children, at = 0.2}) => {
  const a = useT(at, 0.55);
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top, height: h ?? 'auto', paddingBottom: h ? 0 : 10, background: '#fff', borderRadius: 34, boxShadow: '0 30px 80px rgba(38,37,33,.12)', opacity: a, translate: `0px ${(1 - a) * 60}px`, scale: String(0.96 + 0.04 * a), overflow: 'hidden'}}>
      <div style={{height: 74, display: 'flex', alignItems: 'center', gap: 12, padding: '0 28px', borderBottom: '2px solid #f0ebe3'}}>
        {['#ff5f57', '#febc2e', '#28c840'].map((c) => <i key={c} style={{width: 16, height: 16, borderRadius: '50%', background: c}} />)}
        <span style={{flex: 1, textAlign: 'center', font: `700 26px/1 ${display}`, color: C.ink2, marginRight: 60}}>{titolo}</span>
      </div>
      <div style={{padding: 44}}>{children}</div>
    </div>
  );
};

// ---------------------------------------------------------------- scene

const Gancio: React.FC = () => {
  const s = useS();
  const prezzi = [[92, 89, 84], [91, 88, 85], [93, 87, 83], [90, 86, 82]];
  const k = s < 1.6 ? 0 : s < 2.6 ? 1 : 2;
  return (
    <Fondo>
      <Titolo t={'Perché l’ospite\nsceglie *te*?'} top={260} size={112} at={0} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 600, display: 'grid', gap: 18}}>
        {prezzi.map((p, i) => {
          const a = useT(0.4 + i * 0.12, 0.4);
          return (
            <div key={i} style={{opacity: a, translate: `${(1 - a) * 80}px 0px`, background: '#fff', borderRadius: 24, boxShadow: '0 10px 30px rgba(38,37,33,.08)', padding: '22px 28px', display: 'grid', gridTemplateColumns: '120px 1fr auto', gap: 24, alignItems: 'center'}}>
              <div style={{height: 90, borderRadius: 16, background: 'linear-gradient(180deg,#bfe3f2 0 52%,#7cc4d8 52% 68%,#f1dfb8 68%)'}} />
              <div><b style={{font: `800 32px/1.2 ${display}`}}>Hotel <i style={{fontStyle: 'normal', filter: 'blur(7px)'}}>xxxxxx</i></b><div style={{marginTop: 6, font: `600 26px/1.2 ${text}`, background: C.gialloSoft, display: 'inline-block', padding: '2px 10px', borderRadius: 8}}>A due passi dal mare</div></div>
              <b style={{font: `900 46px/1 ${display}`, color: k ? '#c8361c' : INK}}>{p[k]} €</b>
            </div>
          );
        })}
      </div>
      <Sotto t={'Su Booking sembrate *tutti uguali.*'} at={0.9} />
    </Fondo>
  );
};

const Promessa: React.FC = () => {
  const s = useS();
  return (
    <Fondo>
      <p style={{position: 'absolute', left: 0, right: 0, top: 380, textAlign: 'center', margin: 0, font: `700 56px/1 ${display}`, color: C.ink2, opacity: useT(0, 0.4)}}>È più semplice di quanto pensi.</p>
      <h1 style={{position: 'absolute', left: 0, right: 0, top: 470, textAlign: 'center', margin: 0, font: `900 150px/1 ${display}`, letterSpacing: '-.03em', opacity: useT(0.25, 0.5), scale: String(0.9 + 0.1 * useT(0.25, 0.5))}}>6 passaggi<span style={{color: Y}}>.</span></h1>
      <div style={{position: 'absolute', left: 540, top: 1000}}>
        {[1, 2, 3, 4, 5, 6].map((n) => {
          const a = interpolate(s, [0.6 + n * 0.08, 1.2 + n * 0.08], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
          const ang = (n - 3.5) * 13 * a;
          return <div key={n} style={{position: 'absolute', left: -95, top: -130, width: 190, height: 250, background: n === 6 ? Y : '#fff', borderRadius: 22, boxShadow: '0 12px 30px rgba(38,37,33,.12)', border: `3px solid ${INK}`, transformOrigin: '50% 160%', rotate: `${ang}deg`, opacity: Math.min(1, a * 2), display: 'grid', placeItems: 'center', font: `900 64px/1 ${display}`}}>{String(n).padStart(2, '0')}</div>;
        })}
      </div>
      <Sotto t={'Li trovi in ordine *nel libro.*'} at={1.2} />
    </Fondo>
  );
};

const Bisogno: React.FC = () => {
  const s = useS();
  const frase = 'Cercavo un posto dove staccare davvero, senza dover organizzare niente.';
  const n = Math.round(interpolate(s, [0.8, 2.6], [0, frase.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const hl = useT(2.7, 0.5);
  const i0 = frase.indexOf('staccare davvero'), i1 = i0 + 'staccare davvero'.length;
  const vis = frase.slice(0, n);
  return (
    <Fondo>
      <Pill label="" step={1} />
      <Titolo t={'Il bisogno *vero*'} />
      <Finestra titolo="Recensioni · Booking">
        <div style={{display: 'flex', gap: 18, alignItems: 'center'}}>
          <i style={{width: 70, height: 70, borderRadius: '50%', background: C.lillaSoft, display: 'grid', placeItems: 'center', fontStyle: 'normal', font: `800 30px/1 ${display}`}}>G</i>
          <div><b style={{font: `800 32px/1.2 ${display}`}}>Giulia</b><div style={{font: `600 26px/1.2 ${text}`, color: C.ink2}}>Coppia · 2 notti</div></div>
          <b style={{marginLeft: 'auto', background: '#003b95', color: '#fff', borderRadius: 12, padding: '10px 14px', font: `800 30px/1 ${display}`}}>9,4</b>
        </div>
        <p style={{margin: '40px 0 0', font: `500 46px/1.4 ${text}`}}>
          «{vis.slice(0, Math.min(n, i0))}
          {n > i0 ? <span style={{backgroundImage: `linear-gradient(${Y},${Y})`, backgroundRepeat: 'no-repeat', backgroundSize: `${hl * 100}% 100%`, borderRadius: 8, fontWeight: 700}}>{vis.slice(i0, Math.min(n, i1))}</span> : null}
          {n > i1 ? vis.slice(i1) : null}{n >= frase.length ? '»' : <span style={{opacity: Math.round(s * 2) % 2}}>|</span>}
        </p>
      </Finestra>
      <Sotto t={'Cosa chiede *davvero* l’ospite al tuo hotel?'} at={0.6} />
    </Fondo>
  );
};

const Alternative: React.FC = () => {
  const items = [['L’hotel del vicino', '89 €'], ['Una casa vacanze', '75 €'], ['Un weekend a casa', '0 €']];
  return (
    <Fondo>
      <Pill label="" step={2} />
      <Titolo t={'Le *alternative*'} />
      <Finestra titolo="L’ospite confronta">
        <div style={{display: 'grid', gap: 22}}>
          {items.map(([a, b], i) => {
            const t = useT(0.6 + i * 0.35, 0.45);
            return (
              <div key={a} style={{opacity: t, translate: `0px ${(1 - t) * 30}px`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', border: `3px solid ${i === 2 ? INK : '#e3ddd4'}`, background: i === 2 ? C.gialloSoft : '#fff', borderRadius: 22, padding: '30px 32px', font: `800 44px/1.2 ${display}`}}>
                <span>{a}</span><span style={{color: C.ink2, fontSize: 38}}>{b}</span>
              </div>
            );
          })}
        </div>
      </Finestra>
      <Sotto t={'Quelle che ha davvero. *Anche se non sono hotel.*'} at={0.5} />
    </Fondo>
  );
};

const Unicita: React.FC = () => {
  const righe: [string, boolean][] = [['accogliente', false], ['elegante', false], ['Colazione fino all’una', true], ['Navetta dalla stazione', true], ['Check-out alle 18', true]];
  return (
    <Fondo>
      <Pill label="" step={3} />
      <Titolo t={'Le *unicità*'} />
      <Finestra titolo="Lette nelle recensioni">
        <div style={{display: 'grid', gap: 18}}>
          {righe.map(([r, ok], i) => {
            const t = useT(0.6 + i * 0.32, 0.4);
            const strike = useT(0.9 + i * 0.32, 0.35);
            return (
              <div key={r} style={{opacity: t, display: 'flex', alignItems: 'center', gap: 22, font: `${ok ? 800 : 500} 46px/1.3 ${ok ? display : text}`, color: ok ? INK : '#a39d93'}}>
                <i style={{width: 50, height: 50, flex: 'none', borderRadius: 14, border: `3px solid ${INK}`, background: ok ? '#5fd08a' : '#ff5a3c', display: 'grid', placeItems: 'center', fontStyle: 'normal', font: `900 28px/1 ${display}`, color: INK, scale: String(t)}}>{ok ? '✓' : '✗'}</i>
                <span style={{position: 'relative'}}>{r}{ok ? null : <span style={{position: 'absolute', left: 0, top: '55%', height: 5, width: `${strike * 100}%`, background: '#ff5a3c', borderRadius: 3}} />}</span>
              </div>
            );
          })}
        </div>
      </Finestra>
      <Sotto t={'*Fatti*, non aggettivi.'} at={0.5} />
    </Fondo>
  );
};

const Persona: React.FC = () => {
  const s = useS();
  const sel = new Set([3, 7, 8, 12, 16, 19, 23, 24, 28, 31, 33, 36, 38, 41]);
  const n = Math.round(interpolate(s, [1.2, 2.6], [0, sel.size], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const ordine = [...sel];
  const ok = useT(2.8, 0.4);
  return (
    <Fondo>
      <Pill label="" step={4} />
      <Titolo t={'La persona *giusta*'} />
      <Finestra titolo="Chi apprezza quel valore">
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: 22, justifyItems: 'center'}}>
          {Array.from({length: 48}, (_, i) => {
            const on = ordine.indexOf(i) > -1 && ordine.indexOf(i) < n;
            return <i key={i} style={{width: 58, height: 58, borderRadius: '50%', background: on ? Y : '#ebe5dc', border: on ? `3px solid ${INK}` : '3px solid transparent', scale: on ? '1.1' : '1'}} />;
          })}
        </div>
        <div style={{marginTop: 40, opacity: ok, display: 'flex', alignItems: 'center', gap: 16, font: `800 40px/1.2 ${display}`}}>
          <i style={{width: 50, height: 50, borderRadius: 14, border: `3px solid ${INK}`, background: '#5fd08a', display: 'grid', placeItems: 'center', fontStyle: 'normal'}}>✓</i>
          Abbastanza numerosi
        </div>
      </Finestra>
      <Sotto t={'Chi apprezza quel valore. *Ed è abbastanza numeroso.*'} at={0.5} />
    </Fondo>
  );
};

const Categoria: React.FC = () => {
  const s = useS();
  const mv = interpolate(s, [1.4, 2.6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const altri = [[130, 470], [190, 520], [150, 560], [230, 470], [100, 540], [210, 590]];
  const x = interpolate(mv, [0, 1], [170, 600]), y = interpolate(mv, [0, 1], [500, 160]);
  const lab = useT(2.7, 0.4);
  return (
    <Fondo>
      <Pill label="" step={5} />
      <Titolo t={'La *categoria*'} />
      <Finestra titolo="Il campo da gioco">
        <div style={{position: 'relative', height: 640}}>
          <div style={{position: 'absolute', left: '50%', top: 0, bottom: 0, width: 4, background: '#e3ddd4'}} />
          <div style={{position: 'absolute', top: '50%', left: 0, right: 0, height: 4, background: '#e3ddd4'}} />
          {altri.map(([ax, ay], i) => <i key={i} style={{position: 'absolute', left: ax, top: ay, width: 46, height: 46, borderRadius: '50%', background: GRIGIO}} />)}
          <div style={{position: 'absolute', left: x, top: y, width: 70, height: 70, borderRadius: '50%', background: Y, border: `4px solid ${INK}`, display: 'grid', placeItems: 'center', font: `900 26px/1 ${display}`}}>Tu</div>
          <div style={{position: 'absolute', left: 470, top: 260, opacity: lab, font: `800 36px/1.2 ${display}`, background: C.gialloSoft, borderRadius: 12, padding: '8px 16px'}}>Il riferimento</div>
        </div>
      </Finestra>
      <Sotto t={'Quella di cui puoi diventare *il riferimento.*'} at={0.5} />
    </Fondo>
  );
};

const Trend: React.FC = () => {
  const d = useT(0.7, 2.2);
  const pts = [[0, 470], [100, 450], [200, 455], [300, 400], [400, 380], [500, 290], [600, 230], [700, 120], [780, 70]];
  const path = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x} ${y}`).join(' ');
  return (
    <Fondo>
      <Pill label="" step={6} />
      <Titolo t={'Il *trend*'} />
      <Finestra titolo="Cosa cerca l’ospite, anno dopo anno">
        <svg viewBox="-20 0 820 520" style={{width: '100%', height: 560}}>
          <line x1={0} y1={500} x2={800} y2={500} stroke="#e3ddd4" strokeWidth={4} />
          <path d={path} fill="none" stroke={INK} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray="1" strokeDashoffset={1 - d} />
          <circle cx={780} cy={70} r={22} fill={Y} stroke={INK} strokeWidth={5} opacity={d > 0.98 ? 1 : 0} />
        </svg>
      </Finestra>
      <Sotto t={'Quello da seguire. *Quando c’è.*'} at={0.5} />
    </Fondo>
  );
};

const Canvas: React.FC = () => {
  const voci = ['01 Bisogno', '02 Alternative', '03 Unicità', '04 Persona', '05 Categoria', '06 Trend'];
  return (
    <Fondo>
      <Pill label="Bonus" />
      <Titolo t={'Tutto su *un foglio*'} />
      <Finestra titolo="Positioning Canvas">
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 22}}>
          {voci.map((v, i) => {
            const t = useT(0.5 + i * 0.22, 0.45);
            return <div key={v} style={{opacity: t, translate: `${(1 - t) * (i % 2 ? 120 : -120)}px ${(1 - t) * 60}px`, height: 160, border: `3px solid ${INK}`, borderRadius: 20, background: i === 4 ? Y : '#fff', padding: 22, font: `800 36px/1.15 ${display}`}}>{v}</div>;
          })}
        </div>
      </Finestra>
      <Sotto t={'Sei passaggi. *Una pagina sola.*'} at={0.5} />
    </Fondo>
  );
};

const Ribalta: React.FC = () => {
  const st = useT(0.5, 0.5); const b = useT(1.1, 0.5);
  return (
    <Fondo>
      <div style={{position: 'absolute', left: 0, right: 0, top: 640, textAlign: 'center'}}>
        <span style={{position: 'relative', font: `700 84px/1 ${display}`, color: '#a39d93'}}>Abbassare il prezzo<span style={{position: 'absolute', left: 0, top: '52%', height: 8, width: `${st * 100}%`, background: '#ff5a3c', borderRadius: 4}} /></span>
        <p style={{margin: '80px 0 0', font: `900 128px/1 ${display}`, opacity: b, scale: String(0.9 + 0.1 * b)}}><span style={{background: Y, borderRadius: 18, padding: '0 .14em'}}>Farti scegliere.</span></p>
      </div>
      <Sotto t={'Smetti di inseguire *il prezzo.*'} at={0.4} />
    </Fondo>
  );
};

const Cta: React.FC = () => {
  const s = useS();
  const lib = useT(0, 0.7); const t1 = useT(0.5, 0.5); const t2 = useT(1, 0.5);
  const pulse = 1 + 0.04 * Math.max(0, Math.sin((s - 1.6) * Math.PI * 1.5));
  return (
    <Fondo>
      <Img src={staticFile('libro.webp')} style={{position: 'absolute', left: 340, top: 300, width: 400, borderRadius: 10, boxShadow: '0 40px 80px rgba(38,37,33,.28)', opacity: lib, rotate: `${(1 - lib) * 8 - 3}deg`, scale: String(0.85 + 0.15 * lib)}} />
      <p style={{position: 'absolute', left: 60, right: 60, top: 990, textAlign: 'center', margin: 0, font: `900 84px/1.08 ${display}`, opacity: t1}}>Il metodo è <span style={{background: Y, borderRadius: 14, padding: '0 .1em'}}>nel libro.</span></p>
      <p style={{position: 'absolute', left: 0, right: 0, top: 1110, textAlign: 'center', margin: 0, font: `600 44px/1.3 ${text}`, color: C.ink2, opacity: t1}}>120 pagine · 6 passaggi · 19,90 €</p>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1240, display: 'flex', justifyContent: 'center', opacity: t2}}>
        <span style={{scale: String(pulse), background: INK, color: '#fff', borderRadius: 999, padding: '30px 64px', font: `900 64px/1 ${display}`}}>Link in bio</span>
      </div>
    </Fondo>
  );
};

// ---------------------------------------------------------------- montaggio

export const SCENE: [string, React.FC, number][] = [
  ['Gancio', Gancio, 3.6], ['Promessa', Promessa, 3.0], ['Bisogno', Bisogno, 4.4], ['Alternative', Alternative, 4.2],
  ['Unicita', Unicita, 4.4], ['Persona', Persona, 4.2], ['Categoria', Categoria, 4.2], ['Trend', Trend, 3.8],
  ['Canvas', Canvas, 3.8], ['Ribalta', Ribalta, 3.0], ['Cta', Cta, 4.6],
];
export const LIBRO_S = SCENE.reduce((a, [, , d]) => a + d, 0);

export const LibroVideo: React.FC<{musica?: string}> = ({musica}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  const fine = LIBRO_S * fps;
  return (
    <>
      {musica ? <Audio src={staticFile(musica)} volume={(fr) => interpolate(fr, [0, 15, fine - 45, fine], [0, 0.8, 0.8, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} /> : null}
      <Series>
        {SCENE.map(([n, Comp, d]) => (
          <Series.Sequence key={n} name={n} durationInFrames={Math.round(d * fps)} premountFor={fps}><Comp /></Series.Sequence>
        ))}
      </Series>
      <span style={{display: 'none'}}>{f}</span>
    </>
  );
};
