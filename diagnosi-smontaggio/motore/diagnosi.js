#!/usr/bin/env node
// Diagnosi immediata dello Smontaggio.
//   node diagnosi.js <url> [--risposta "..."] [--nome "..."] [--localita "..."]
//   node diagnosi.js --estrazione file.json [...]   (usa un'estrazione già fatta, senza aprire il browser)
import { readFileSync, writeFileSync } from 'node:fs';
import { estrai } from './estrai.js';
import { analizza } from './analizza.js';
import { calcola } from './voto.js';

function argomenti(argv) {
  const a = { url: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) a[argv[i].slice(2)] = argv[++i];
    else a.url = argv[i];
  }
  return a;
}

export async function diagnosi({ url, estrazione, risposta, nome, localita }) {
  const e = estrazione || await estrai(url);
  const d = e.desktop;
  const fuori = [`Title: ${e.title}`, `Meta description: ${e.meta || '(nessuna)'}`,
    `H1 sotto la piega: ${d.h1_fuori.join(' | ') || '(nessuno)'}`, `Seconda schermata: ${d.seconda_schermata.join(' | ') || '(niente)'}`].join('\n');
  const ai = await analizza({ nome: nome || e.title, localita, hero: d, fuori, risposta });
  return { url: e.url || url, ...calcola(e, ai) };
}

function stampa(r) {
  const p = r.parametri;
  console.log(`\n${r.url}\n${r.voto}/100 · ${r.verdetto}\n`);
  console.log(`Headline:    ${r.hero.headline || '(nessuna)'}`);
  console.log(`Sottotitolo: ${r.hero.sottotitolo || '(nessuno)'}`);
  if (r.hero.supporto.length) console.log(`Supporto:    ${r.hero.supporto.join(' | ')}`);
  console.log(`\n${r.frase_posizionamento}\n`);
  console.log(`Posizionamento ${p.posizionamento.totale}/45 (target ${p.posizionamento.target} · beneficio ${p.posizionamento.beneficio} · differenziazione ${p.posizionamento.differenziazione})`);
  console.log(`Hook ${p.hook}/15 · Cliché ${p.cliche}/15 · Riprova ${p.riprova}/15 · Azione ${p.azione}/10 · Penalità ${p.penalita}`);
  console.log(`Cliché: ${r.cliche_trovati.join(', ') || '-'} · Concreti: ${r.elementi_concreti.join(', ') || '-'}`);
  if (r.prova_migliore) console.log(`Prova: ${r.prova_migliore.tipo} a ${r.prova_migliore.schermate} schermate («${r.prova_migliore.testo.slice(0, 80)}»)`);
  for (const s of r.segnalazioni) console.log(`! ${s.testo}${s.citazioni ? ' ' + JSON.stringify(s.citazioni) : ''}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const a = argomenti(process.argv.slice(2));
  const estrazione = a.estrazione ? JSON.parse(readFileSync(a.estrazione, 'utf8')) : null;
  if (!a.url && !estrazione) {
    console.error('Uso: node diagnosi.js <url> | --estrazione file.json [--risposta "..."]');
    process.exit(1);
  }
  const r = await diagnosi({ url: a.url, estrazione, risposta: a.risposta, nome: a.nome, localita: a.localita });
  stampa(r);
  if (a.salva) writeFileSync(a.salva, JSON.stringify(r, null, 2));
}
