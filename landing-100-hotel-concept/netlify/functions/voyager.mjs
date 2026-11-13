// API del diario di bordo Hotel Voyager (pagina /amsterdam/ e prossimi viaggi).
//
// GET  ?viaggio=amsterdam&codice=…           → stato del viaggio (hotel, note, sfide, risposte, sintesi)
// GET  ?controllo=1                           → configurazione (solo sì/no, nessun valore segreto)
// POST { viaggio, codice, azione, ... }       → aggiunge o modifica (vedi AZIONI sotto)
//
// Ognuno si identifica col nome che scrive all'ingresso: è un gruppo di 6-8 persone che si conoscono,
// il codice del viaggio tiene fuori gli estranei. Nicola modera con la chiave admin.

import { VIAGGIO, store, vuoto, nuovoId, t, json, leggiCorpo, codiceOk, adminOk, modifica, v2 } from '../lib/voyager.mjs';

const TIPI_NOTA = ['rubare', 'evitare', 'dettaglio', 'domanda', 'stimolo'];
const AREE = ['management', 'comunicazione', 'design', 'esperienza', ''];
const MAX = 2000; // elementi per elenco: un viaggio ne produce qualche centinaio

const togliVoto = (el, chi) => { el.voti = (el.voti || []).filter((v) => v !== chi); };

const gestisci = async (event) => {
  const q = event.queryStringParameters || {};
  const env = process.env;

  if (event.httpMethod === 'GET' && q.controllo) {
    return json(200, {
      VOYAGER_CODICE: !!env.VOYAGER_CODICE, VOYAGER_ADMIN: !!env.VOYAGER_ADMIN, ANTHROPIC_API_KEY: !!env.ANTHROPIC_API_KEY,
    });
  }

  if (event.httpMethod === 'GET') {
    const viaggio = t(q.viaggio, 40);
    if (!VIAGGIO.test(viaggio)) return json(400, { ok: false, errore: 'viaggio' });
    if (!codiceOk(q.codice)) return json(401, { ok: false, errore: 'codice' });
    const stato = (await store().get(`${viaggio}/stato`, { type: 'json' })) || vuoto();
    return json(200, { ok: true, stato, ai: !!env.ANTHROPIC_API_KEY });
  }

  if (event.httpMethod !== 'POST') return json(405, { ok: false });
  const d = leggiCorpo(event);
  if (!d) return json(400, { ok: false, errore: 'richiesta' });
  const viaggio = t(d.viaggio, 40);
  if (!VIAGGIO.test(viaggio)) return json(400, { ok: false, errore: 'viaggio' });
  const admin = adminOk(d.admin);
  if (!admin && !codiceOk(d.codice)) return json(401, { ok: false, errore: 'codice' });

  const chi = t(d.autore, 60);
  const chiave = `${viaggio}/stato`;
  const ts = Date.now();

  try {
    switch (d.azione) {
      case 'ingresso': {
        if (!chi) return json(400, { ok: false, errore: 'nome' });
        await modifica(chiave, (s) => {
          const p = s.partecipanti.find((x) => x.nome.toLowerCase() === chi.toLowerCase());
          if (p) { p.struttura = t(d.struttura, 120) || p.struttura; return; }
          s.partecipanti.push({ nome: chi, struttura: t(d.struttura, 120), ts });
        });
        return json(200, { ok: true });
      }

      case 'hotel': {
        const nome = t(d.nome, 100);
        if (!nome || !chi) return json(400, { ok: false, errore: 'dati' });
        const id = nuovoId();
        await modifica(chiave, (s) => {
          if (s.hotel.length >= 200) throw new Error('troppi hotel');
          if (s.hotel.some((h) => h.nome.toLowerCase() === nome.toLowerCase())) return false;
          s.hotel.push({ id, nome, zona: t(d.zona, 100), giorno: t(d.giorno, 20), autore: chi, ts });
        });
        return json(200, { ok: true, id });
      }

      case 'nota': {
        const testo = t(d.testo);
        const tipo = TIPI_NOTA.includes(d.tipo) ? d.tipo : 'rubare';
        if (!testo || !chi) return json(400, { ok: false, errore: 'dati' });
        const id = nuovoId();
        await modifica(chiave, (s) => {
          if (s.note.length >= MAX) throw new Error('archivio pieno');
          s.note.push({
            id, tipo, testo, autore: chi, ts, voti: [],
            hotelId: t(d.hotelId, 20) || null,
            area: AREE.includes(d.area) ? d.area : '',
            applicazione: t(d.applicazione, 800),
            cartaId: t(d.cartaId, 20) || null,
            domanda: t(d.domanda, 300),
          });
        });
        return json(200, { ok: true, id });
      }

      case 'sfida': {
        const testo = t(d.testo);
        if (!testo || !chi) return json(400, { ok: false, errore: 'dati' });
        const id = nuovoId();
        await modifica(chiave, (s) => {
          if (s.sfide.length >= 100) throw new Error('troppe sfide');
          s.sfide.push({ id, autore: chi, struttura: t(d.struttura, 160), testo, provato: t(d.provato, 800), ts, voti: [] });
        });
        return json(200, { ok: true, id });
      }

      case 'risposta': {
        const testo = t(d.testo);
        if (!testo || !chi || !d.sfidaId) return json(400, { ok: false, errore: 'dati' });
        const id = nuovoId();
        await modifica(chiave, (s) => {
          if (!s.sfide.some((x) => x.id === d.sfidaId)) throw new Error('sfida non trovata');
          if (s.risposte.length >= MAX) throw new Error('archivio pieno');
          s.risposte.push({ id, sfidaId: t(d.sfidaId, 20), hotelId: t(d.hotelId, 20) || null, testo, autore: chi, ts, voti: [] });
        });
        return json(200, { ok: true, id });
      }

      case 'voto': {
        if (!chi || !d.id) return json(400, { ok: false, errore: 'dati' });
        await modifica(chiave, (s) => {
          const el = [...s.note, ...s.sfide, ...s.risposte].find((x) => x.id === d.id);
          if (!el) return false;
          if ((el.voti || []).includes(chi)) togliVoto(el, chi);
          else el.voti = [...(el.voti || []), chi];
        });
        return json(200, { ok: true });
      }

      case 'elimina': {
        if (!d.id) return json(400, { ok: false, errore: 'dati' });
        let negato = false;
        await modifica(chiave, (s) => {
          for (const k of ['note', 'sfide', 'risposte', 'hotel']) {
            const el = s[k].find((x) => x.id === d.id);
            if (!el) continue;
            if (!admin && el.autore !== chi) { negato = true; return false; }
            s[k] = s[k].filter((x) => x.id !== d.id);
            if (k === 'sfide') s.risposte = s.risposte.filter((r) => r.sfidaId !== d.id);
            if (k === 'hotel') s.note.forEach((n) => { if (n.hotelId === d.id) n.hotelId = null; });
            return;
          }
          return false;
        });
        return negato ? json(403, { ok: false, errore: 'puoi eliminare solo i tuoi contributi' }) : json(200, { ok: true });
      }

      case 'carta': {
        if (!admin) return json(403, { ok: false });
        await modifica(chiave, (s) => { s.cartaDelGiorno = d.cartaId ? t(d.cartaId, 20) : null; });
        return json(200, { ok: true });
      }

      case 'testimonial': {
        if (!chi) return json(400, { ok: false, errore: 'nome' });
        const risposte = Array.isArray(d.risposte) ? d.risposte.slice(0, 12).map((r) => ({ domanda: t(r.domanda, 300), risposta: t(r.risposta, 2000) })).filter((r) => r.risposta) : [];
        if (!risposte.length) return json(400, { ok: false, errore: 'risposte' });
        await modifica(`${viaggio}/testimonial`, (s) => {
          s.voci = (s.voci || []).filter((v) => v.autore.toLowerCase() !== chi.toLowerCase()); // l'ultima versione vince
          s.voci.push({
            autore: chi, ruolo: t(d.ruolo, 120), struttura: t(d.struttura, 160), citta: t(d.citta, 80),
            risposte, consenso: !!d.consenso, contatto: t(d.contatto, 160), ts,
          });
        }, () => ({ voci: [] }));
        return json(200, { ok: true });
      }

      case 'testimonial-lista': {
        if (!admin) return json(403, { ok: false });
        const tst = (await store().get(`${viaggio}/testimonial`, { type: 'json' })) || { voci: [] };
        return json(200, { ok: true, voci: tst.voci });
      }

      default:
        return json(400, { ok: false, errore: 'azione' });
    }
  } catch (e) {
    console.error('voyager', d.azione, e);
    return json(500, { ok: false, errore: e.message || 'errore' });
  }
};

export default v2(gestisci);
