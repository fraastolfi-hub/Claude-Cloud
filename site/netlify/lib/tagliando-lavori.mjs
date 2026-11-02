// I due controlli lunghi del Tagliando. Girano nella funzione in background e restituiscono
// sempre un oggetto da salvare: { ok: true, dati, firma, screenshot? } oppure { ok: false, errore, messaggio, dettaglio? }.
import { urlSicuro, leggiPagina, estrai, prove, leggiMessaggio, velocita, frasiFatteTrovate, firma, Errore } from './tagliando.mjs';

export const ID = /^[a-z0-9-]{20,64}$/;
const pacco = (dati) => ({ dati, firma: firma(dati) });

export async function esegui(parte, d) {
  try {
    if (parte === 'pagina') {
      if (!process.env.ANTHROPIC_API_KEY) return { ok: false, errore: 'configurazione' };
      const url = await urlSicuro(d.url);
      const { html, finale } = await leggiPagina(url);
      const pagina = estrai(html);
      if (pagina.parole < 30) throw new Errore('pagina', 'La pagina ha pochissimo testo leggibile: forse si carica tutta con JavaScript. Prova con l\'indirizzo di una landing o di una pagina interna.');
      const p = prove(html, pagina.testo);
      const hotel = String(d.hotel || '').slice(0, 120);
      const m = await leggiMessaggio({ url: finale, hotel, pagina });
      const frasi = frasiFatteTrovate(pagina.testo, m.frasi_fatte);
      return { ok: true, ...pacco({ url, finale, hotel, titolo: pagina.titolo, prove: p, messaggio: m, frasi, ora: Date.now() }) };
    }
    if (parte === 'velocita') {
      const url = await urlSicuro(d.url);
      const { screenshot, ...v } = await velocita(url);
      return { ok: true, screenshot, ...pacco({ url, ...v, ora: Date.now() }) };
    }
    return { ok: false, errore: 'parte' };
  } catch (e) {
    if (e instanceof Errore) return { ok: false, errore: e.codice, messaggio: e.message };
    console.error('tagliando', parte, e);
    // dettaglio tecnico breve (nessun dato segreto): serve a capire il guasto dallo schermo
    const dettaglio = [e?.constructor?.name, e?.status, String(e?.message || '').replace(/sk-[\w-]+/g, '…').slice(0, 160)].filter(Boolean).join(' · ');
    return { ok: false, errore: 'interno', dettaglio, messaggio: 'Qualcosa non ha funzionato dal nostro lato. Riprova tra qualche minuto.' };
  }
}
