// Fotografa report.html (1600x900) e salva PNG ad alta risoluzione.
// Uso: node render.mjs   (serve playwright installato; poi build_webp.py converte in webp)
import { createRequire } from 'module';
import { execSync } from 'child_process';
import path from 'path';
const req = createRequire(import.meta.url);
let pw; try { pw = req('playwright'); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const here = path.dirname(new URL(import.meta.url).pathname);
const b = await pw.chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
await p.goto('file://' + path.join(here, 'report.html'));
await p.waitForTimeout(1500); // font
await p.screenshot({ path: path.join(here, 'report.png') });
await b.close();
console.log('report.png');
