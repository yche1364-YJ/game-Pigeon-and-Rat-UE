const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const items=JSON.parse(fs.readFileSync('ui/items.json'));const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1});
const FF='<style>@font-face{font-family:Bangers;src:url(file://'+process.cwd()+'/fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}@font-face{font-family:STM;src:url(file://'+process.cwd()+'/fonts/node_modules/@fontsource/share-tech-mono/files/share-tech-mono-latin-400-normal.woff2)}body{margin:0;background:transparent}#t{display:inline-block;padding:0}</style>';
const rects={};
for(const [k,h] of Object.entries(items)){fs.writeFileSync('ui_tmp.html','<html><head>'+FF+'</head><body><div id="t">'+h+'</div></body></html>');await p.goto('file://'+process.cwd()+'/ui_tmp.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
const el=await p.$('#t');await el.screenshot({path:'ui/'+k+'.png',omitBackground:true});
if(k=='T_Paused'){const base=await el.boundingBox();rects[k]={size:[base.width,base.height]};for(const id of ['b_resume','b_menu','b_exit']){const bb=await (await p.$('#'+id)).boundingBox();rects[k][id]=[bb.x-base.x,bb.y-base.y,bb.width,bb.height];}}
if(k=='T_HowTo'){const base=await el.boundingBox();rects[k]={size:[base.width,base.height]};}}
fs.writeFileSync('ui/rects.json',JSON.stringify(rects));await b.close();})();
