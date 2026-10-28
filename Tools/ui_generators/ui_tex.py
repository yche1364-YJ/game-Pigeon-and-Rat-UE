import re, json, sys
sys.path.insert(0,'gen')
D='nyc_ui/project/'
F=open(D+'Final.dc.html').read()
def svg_by_label(lbl):
    i=F.index('aria-label="%s"'%lbl); s=F.rindex('<svg',0,i); e=F.index('</svg>',i)+6
    x=F[s:e]
    x=re.sub(r'style="[^"]*"','',x,1)
    return x
rat=svg_by_label('Rat'); home=svg_by_label('Home'); tri=svg_by_label('You are here')
# food icons from generator
src=open('gen/screens2.py').read()
ns={}
exec(src[src.index("O='#1E1B18'"):src.index("CHECK=")],ns)
ICON=ns['ICON']
FF='<style>@font-face{font-family:Bangers;src:url(fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}@font-face{font-family:STM;src:url(fonts/node_modules/@fontsource/share-tech-mono/files/share-tech-mono-latin-400-normal.woff2)}body{margin:0;background:transparent}#t{display:inline-block}</style>'
items={}
def sv(inner,vb='0 0 48 48',size=128):
    return f'<svg width="{size}" height="{size}" viewBox="{vb}">{inner}</svg>'
for k,n in [('dog','HotDog'),('pizza','Pizza'),('cheese','Cake'),('soda','Soda')]:
    items['T_Icon_'+n]=sv(ICON[k])
def resize(s,w,h):
    s=re.sub(r'width="[\d.]+"',f'width="{w}"',s,1); s=re.sub(r'height="[\d.]+"',f'height="{h}"',s,1); return s
items['T_RatHead']=resize(rat,128,128)
items['T_HomeBubble']=resize(home,128,121)
items['T_RatMarker']=resize(tri,120,126)
items['T_Check']=sv('<path d="M6 19L14 27L30 9" fill="none" stroke="#141414" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 19L14 27L30 9" fill="none" stroke="#3BD16F" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>','0 0 36 36')
items['T_Heart']=sv('<path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.5 6c-2.5 4.5-9.5 9-9.5 9z" fill="#FF5A5A" stroke="#FFFFFF" stroke-width="1.5"/>','0 0 24 24',96)
items['T_HeartEmpty']=sv('<path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.5 6c-2.5 4.5-9.5 9-9.5 9z" fill="none" stroke="#6E6E6E" stroke-width="2"/>','0 0 24 24',96)
items['T_Dot']=sv('<circle cx="32" cy="32" r="30" fill="#FFFFFF"/>','0 0 64 64',64)
items['T_Ring']=sv('<circle cx="32" cy="32" r="26" fill="#FFFFFF" stroke="#141414" stroke-width="10"/>','0 0 64 64',64)
items['T_Arrow']=sv('<path d="M44 4L84 50H62V92H26V50H4Z" fill="#F6C343" stroke="#141414" stroke-width="6" stroke-linejoin="round"/>','0 0 88 96',192)
items['T_BtnHelp']=sv('<circle cx="32" cy="32" r="29" fill="#F6C343" stroke="#141414" stroke-width="5"/><text x="32" y="44" text-anchor="middle" font-family="Inter,Arial" font-weight="800" font-size="34" fill="#141414">?</text>','0 0 64 64',128)
items['T_BtnHome']=sv('<circle cx="32" cy="32" r="29" fill="#F6C343" stroke="#141414" stroke-width="5"/><g transform="translate(18 17) scale(1.17)"><path fill-rule="evenodd" d="M12 2.5L1.5 11.5H4.5V21.5H19.5V11.5H22.5ZM10 21.5V15H14V21.5Z" fill="#141414"/></g>','0 0 64 64',128)
items['T_Title']='<div style="width:200px;height:128px;background:#141414;border-radius:24px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Bangers;font-size:50px;line-height:.95;letter-spacing:2px"><span style="color:#F6C343">PIGEON</span><span style="color:#fff">&amp; RAT</span></div>'
items['T_Jaywalk']='<div style="width:680px;box-sizing:border-box;background:#141414;border:8px solid #3A3A3A;border-radius:28px;padding:18px 26px;display:flex;align-items:center;gap:26px"><span style="width:88px;height:88px;flex:none;border-radius:50%;background:#FF3B2F;box-shadow:0 0 34px #FF3B2F"></span><span style="font-family:STM;font-size:92px;line-height:1;letter-spacing:8px;color:#FF3B2F;text-shadow:0 0 22px #FF3B2F">JAYWALK</span></div>'
items['T_PigeonWarn']='<div style="display:inline-flex;align-items:center;gap:12px;background:#E8261E;border:6px solid #141414;border-radius:40px;padding:10px 26px;font-family:Bangers;font-size:54px;letter-spacing:3px;color:#fff">PIGEON! <span style="font-size:44px">&#9650;</span></div>'
# How to play / Paused panels (2x)
howto=f'''<div style="width:920px;box-sizing:border-box;background:#141414;border:12px solid #3A3A3A;border-radius:40px;padding:36px 44px 40px;display:flex;flex-direction:column;gap:32px;font-family:STM">
<div style="display:flex;align-items:center;gap:24px"><span style="width:44px;height:44px;border-radius:50%;background:#FFB020;box-shadow:0 0 24px #FFB020"></span><span style="flex:1;font-size:68px;line-height:1;letter-spacing:6px;color:#FFB020;text-shadow:0 0 20px #FFB020">HOW TO PLAY</span><span style="width:80px;height:80px;border-radius:50%;border:6px solid #3A3A3A;background:#222;color:#E8E3D8;font-size:44px;display:flex;align-items:center;justify-content:center">&times;</span></div>
<div style="display:flex;align-items:center;gap:44px;background:#0B0B0B;border-radius:24px;padding:28px 36px"><div style="display:grid;grid-template-columns:repeat(3,96px);grid-template-rows:repeat(2,96px);gap:12px">{''.join(('<span></span>' if c=='' else f'<span style="border:6px solid #33D17A;border-radius:20px;color:#33D17A;text-shadow:0 0 16px #33D17A;font-size:56px;display:flex;align-items:center;justify-content:center">{c}</span>') for c in ['','&uarr;','','&larr;','&darr;','&rarr;'])}</div><span style="font-size:60px;letter-spacing:6px;color:#33D17A;text-shadow:0 0 20px #33D17A">HOP</span></div>
<div style="display:flex;align-items:center;gap:28px;color:#E8E3D8;font-size:44px;letter-spacing:2px">{sv(ICON['pizza'],size=80)}<span>TOUCH FOOD = GRAB</span></div>
<div style="display:flex;align-items:center;gap:28px;color:#E8E3D8;font-size:44px;letter-spacing:2px"><svg width="80" height="80" viewBox="0 0 40 40"><path d="M20 4L36 22H26V36H14V22H4Z" fill="#F6C343" stroke="#1E1B18" stroke-width="3" stroke-linejoin="round"/></svg><span>FOLLOW ARROW &rarr; NEST</span></div>
<div style="border:6px solid #FF3B2F;border-radius:20px;padding:20px 24px;text-align:center;font-size:44px;letter-spacing:4px;color:#FF3B2F;text-shadow:0 0 20px #FF3B2F">WATCH OUT! IF YOU CROSS THE ROAD</div></div>'''
items['T_HowTo']=howto
paused='''<div style="width:760px;box-sizing:border-box;background:#141414;border:12px solid #3A3A3A;border-radius:40px;padding:40px 48px 48px;display:flex;flex-direction:column;align-items:center;gap:32px;font-family:STM">
<div style="display:flex;align-items:center;gap:24px"><span style="width:44px;height:44px;border-radius:50%;background:#FFB020;box-shadow:0 0 24px #FFB020"></span><span style="font-size:80px;line-height:1;letter-spacing:8px;color:#FFB020;text-shadow:0 0 20px #FFB020">PAUSED</span></div>
<div id="b_resume" style="width:100%;height:112px;box-sizing:border-box;border-radius:24px;border:6px solid #33D17A;background:#0B0B0B;color:#33D17A;text-shadow:0 0 16px #33D17A;font-size:52px;letter-spacing:6px;display:flex;align-items:center;justify-content:center">&#9654; RESUME</div>
<div id="b_menu" style="width:100%;height:112px;box-sizing:border-box;border-radius:24px;border:6px solid #E8E3D8;background:#0B0B0B;color:#E8E3D8;font-size:52px;letter-spacing:6px;display:flex;align-items:center;justify-content:center">MENU</div>
<div id="b_exit" style="width:100%;height:112px;box-sizing:border-box;border-radius:24px;border:6px solid #FF3B2F;background:#0B0B0B;color:#FF3B2F;text-shadow:0 0 16px #FF3B2F;font-size:52px;letter-spacing:6px;display:flex;align-items:center;justify-content:center">EXIT</div></div>'''
items['T_Paused']=paused
json.dump(items,open('ui/items.json','w'))
print(len(items))
