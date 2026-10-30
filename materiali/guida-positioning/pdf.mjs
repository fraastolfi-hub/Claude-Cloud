import {chromium} from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.cwd()+'/guida.html');await p.waitForTimeout(800);
await p.evaluate(()=>document.fonts.ready);
const over=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((pg,i)=>{const f=pg.querySelector('.foot');const lim=f?f.getBoundingClientRect().top-6:pg.getBoundingClientRect().bottom;let max=0;pg.querySelectorAll(':scope > *:not(.foot):not(.cover-foot):not(.cover-band)').forEach(e=>{max=Math.max(max,e.getBoundingClientRect().bottom)});return [i+1,Math.round(lim-max)]}).filter(x=>x[1]<0));
console.log('pagine che sforano',JSON.stringify(over));
await p.pdf({path:'guida-positioning-hotel.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
await b.close();
