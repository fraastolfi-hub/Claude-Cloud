// Fotografa report.html (scena 1600x900, scala 1.5) e scrive le due immagini del sito:
//   src/assets/img/report-dove-colpire.webp     1600x900
//   src/assets/img/report-dove-colpire@2x.webp  2400x1350
// Uso: node render.mjs   (serve playwright installato globalmente e python3 con Pillow)
import { execSync } from 'child_process';
import { existsSync, unlinkSync } from 'fs';
import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const out = path.resolve(here, '../../src/assets/img');
let pwPath = path.join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs');
if (!existsSync(pwPath)) pwPath = '/opt/node22/lib/node_modules/playwright/index.mjs';
const { chromium } = await import(pwPath);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
await p.goto('file://' + path.join(here, 'report.html'));
await p.waitForTimeout(1500);
const fonts = await p.evaluate(async () => { await document.fonts.ready;
  return ['700 40px "Inter Tight"', '400 16px "Inter"'].map(f => f + ': ' + (document.fonts.check(f) ? 'ok' : 'fallback')); });
const png = path.join(here, 'report.png');
await p.screenshot({ path: png });
await b.close();
execSync(`python3 -c "
from PIL import Image
im = Image.open('${png}').convert('RGB')
im.save('${out}/report-dove-colpire@2x.webp', 'WEBP', quality=84, method=6)
im.resize((1600, 900), Image.LANCZOS).save('${out}/report-dove-colpire.webp', 'WEBP', quality=86, method=6)
"`);
unlinkSync(png);
console.log('font', fonts.join(' · '));
console.log('scritti', out + '/report-dove-colpire.webp', '+ @2x');
