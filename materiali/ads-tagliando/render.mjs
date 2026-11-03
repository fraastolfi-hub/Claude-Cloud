// Render degli HTML in PNG (playwright preinstallato). Uso: node render.mjs <cartella>
import pw from '/opt/node22/lib/node_modules/playwright/index.js'; const { chromium } = pw;
import { readdirSync } from 'node:fs'; import path from 'node:path';
const dir = path.resolve(process.argv[2]); const b = await chromium.launch();
for (const f of readdirSync(dir).filter(f => f.endsWith('.html'))) {
  const H = f.includes('_916') ? 1920 : 1350;
  const p = await b.newPage({ viewport: { width: 1080, height: H } });
  await p.goto('file://' + path.join(dir, f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')) }); await p.close();
}
await b.close(); console.log('render ok');
