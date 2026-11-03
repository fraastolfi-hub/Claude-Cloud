// I 21 controlli veri di Tagliando Hotel (vedi site/netlify/lib/tagliando.mjs), divisi per area.
// ok = esito dell'ESEMPIO mostrato nei video (non un hotel reale): messaggio rosso, prove giallo, velocità verde, AI giallo.
export type Controllo = {nome: string; ok: boolean};
export type Area = {nome: string; colore: 'rosso' | 'giallo' | 'verde'; controlli: Controllo[]};

export const AREE: Area[] = [
  {nome: 'Messaggio', colore: 'rosso', controlli: [
    {nome: 'Prima schermata', ok: false}, {nome: 'Per chi è l’hotel', ok: false}, {nome: 'Promessa', ok: true},
    {nome: 'Test di sostituzione', ok: false}, {nome: 'Frasi fatte', ok: false},
  ]},
  {nome: 'Prove', colore: 'giallo', controlli: [
    {nome: 'Recensioni', ok: true}, {nome: 'Voti dei portali', ok: false}, {nome: 'Premi e guide', ok: false},
    {nome: 'Domande frequenti', ok: true}, {nome: 'Pulsante prenota', ok: true}, {nome: 'Perché prenotare diretto', ok: false},
    {nome: 'Telefono e WhatsApp', ok: true},
  ]},
  {nome: 'Velocità', colore: 'verde', controlli: [
    {nome: 'Punteggio da telefono', ok: true}, {nome: 'Prima schermata in secondi', ok: true}, {nome: 'Pagina stabile', ok: true},
    {nome: 'Peso delle foto', ok: false},
  ]},
  {nome: 'Come ti legge l’AI', colore: 'giallo', controlli: [
    {nome: 'Cosa risponde l’AI', ok: false}, {nome: 'Benefici capiti', ok: true}, {nome: 'Dati strutturati', ok: false},
    {nome: 'Descrizione', ok: true}, {nome: 'Testo leggibile', ok: true},
  ]},
];
export const TUTTI = AREE.flatMap((a) => a.controlli.map((c) => ({...c, area: a.nome})));
export const SEM = {rosso: '#ff5a3c', giallo: '#ffd22e', verde: '#5fd08a', spento: '#e3ddd4'};
