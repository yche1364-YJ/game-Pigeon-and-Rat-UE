const {chromium}=require('playwright');const fs=require('fs');
const P='nyc_ui/project/';
const FF='<style>@font-face{font-family:Bangers;src:url(fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}@font-face{font-family:"Share Tech Mono";src:url(fonts/node_modules/@fontsource/share-tech-mono/files/share-tech-mono-latin-400-normal.woff2)}@font-face{font-family:"Barlow Condensed";src:url(fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}body{margin:0}</style>';
function page(f,mod){let s=fs.readFileSync(P+f,'utf8');let b=s.slice(s.indexOf('<div style="width: 1280px'),s.indexOf('</x-dc>'));let h=s.slice(s.indexOf('<style>'),s.indexOf('</style>')+8);if(mod)b=mod(b);return '<html><head>'+FF+h+'</head><body>'+b+'</body></html>';}
(async()=>{const br=await chromium.launch();const p=await br.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1.5});const R={};
async function shot(name,f,mod,sels){fs.writeFileSync('scr_tmp.html',page(f,mod));await p.goto('file://'+process.cwd()+'/scr_tmp.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 R[name]={};for(const [k,sel] of Object.entries(sels)){const els=await p.$$(sel.q);const e=els[sel.i||0];const bb=await e.boundingBox();R[name][k]=[Math.round(bb.x),Math.round(bb.y),Math.round(bb.width),Math.round(bb.height)];}
 await p.screenshot({path:'ui/'+name+'.png'});}
await shot('T_ScrStart','Start.dc.html',null,{play:{q:'nav a'},exit:{q:'nav button'}});
await shot('T_ScrDonate','Donate.dc.html',null,{donate:{q:'nav a',i:0},home:{q:'nav a',i:1}});
const blank=b=>b.replace(/(<div style="margin-top: \d+px; width: 420px; box-sizing: border-box; background: #141414; border: 4px solid #FFFFFF; border-radius: 12px; padding: [^"]*?)transform: rotate\(-1deg\)">/,'$1transform: none" id="card">').replace('</style>','');
const css=b=>blank(b)+'<style>#card>*{visibility:hidden}</style>';
await shot('T_ScrGameOver','GameOver.dc.html',css,{card:{q:'#card'},retry:{q:'nav a',i:0},menu:{q:'nav a',i:1}});
await shot('T_ScrClear','StageClear.dc.html',css,{card:{q:'#card'},next:{q:'nav a',i:0},menu:{q:'nav a',i:1}});
fs.writeFileSync('ui/screens.json',JSON.stringify(R));await br.close();})();
