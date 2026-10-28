import math, re, os
D='/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/nyc_ui/project/'
start=open(D+'Start.dc.html').read()
head=start[:start.index('<div style="width: 1280px')]
bg=start[start.index('  <!-- background: comic halftone night sky -->'):start.index('  <!-- ===== left:')]
tail=start[start.index('</x-dc>'):]

def star(cx,cy,ro,ri,n,rot=0):
    pts=[]
    for k in range(2*n):
        r=ro if k%2==0 else ri*(0.85+0.3*((k*7)%5)/4)
        a=math.pi*k/n+rot
        pts.append(f"{cx+r*math.cos(a):.0f},{cy+r*math.sin(a):.0f}")
    return ' '.join(pts)

O='#1E1B18'
ICON={
'pizza':f'<path d="M6 42L20 10Q33 7 41 26Z" fill="#FFD95A" stroke="{O}" stroke-width="3" stroke-linejoin="round"/><path d="M18 11Q33 2 45 25L40 29Q32 13 22 15Z" fill="#F2A14A" stroke="{O}" stroke-width="3" stroke-linejoin="round"/><circle cx="22" cy="23" r="4" fill="#E04A2F" stroke="{O}" stroke-width="2"/><circle cx="30" cy="24" r="3.5" fill="#E04A2F" stroke="{O}" stroke-width="2"/><circle cx="16" cy="33" r="3.5" fill="#E04A2F" stroke="{O}" stroke-width="2"/>',
'dog':f'<g transform="rotate(-25 24 24)"><rect x="5" y="18" width="38" height="14" rx="7" fill="#F2B562" stroke="{O}" stroke-width="3"/><rect x="2" y="15" width="44" height="10" rx="5" fill="#D9542F" stroke="{O}" stroke-width="3"/><path d="M8 19l3-2.5 3 2.5 3-2.5 3 2.5 3-2.5 3 2.5 3-2.5 3 2.5 3-2.5 3 2.5" stroke="#FFD13B" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><rect x="7" y="23" width="34" height="11" rx="5.5" fill="#F7C77C" stroke="{O}" stroke-width="3"/></g>',
'cheese':'<path d="M5 28L29 11L44 20Z" fill="#FFF3D2" stroke="#1E1B18" stroke-width="3" stroke-linejoin="round"></path><path d="M5 28L44 20V33L5 41Z" fill="#FBE0A0" stroke="#1E1B18" stroke-width="3" stroke-linejoin="round"></path><path d="M5 36.5L44 29V33L5 41Z" fill="#B5733A" stroke="#1E1B18" stroke-width="1.8" stroke-linejoin="round"></path><path d="M12 26.5L29 15L40 19.5L22 24.8Z" fill="#E0384A"></path><path d="M23 24.4V30Q23 32 25 32Q27 32 27 30V23.6Z" fill="#E0384A"></path><path d="M29 15Q31 8 36 11.5Q38 16 33 18.5Q28 18 29 15Z" fill="#E0384A" stroke="#1E1B18" stroke-width="1.8" stroke-linejoin="round"></path><path d="M30 10.5L32.5 12.5L35.5 9" stroke="#3BA55C" stroke-width="2" fill="none" stroke-linecap="round"></path>',
'soda':f'<g transform="rotate(15 24 24)"><rect x="14" y="7" width="20" height="34" rx="5" fill="#E3342F" stroke="{O}" stroke-width="3"/><rect x="14" y="19" width="20" height="9" fill="#FFFFFF" stroke="{O}" stroke-width="2"/><path d="M17 8h14" stroke="#B9B9B9" stroke-width="3" stroke-linecap="round"/></g>',
}
CHECK='<svg style="position: absolute; left: 7px; top: 7px" width="40" height="40" viewBox="0 0 36 36" aria-hidden="true"><path d="M6 19L14 27L30 9" fill="none" stroke="#141414" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"></path><path d="M6 19L14 27L30 9" fill="none" stroke="#3BD16F" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
def tiles(order):
    out=[]
    for kind,got in order:
        if got:
            out.append(f'<div style="position: relative; width: 54px; height: 54px; box-sizing: border-box; border-radius: 10px; border: 2px solid #4A4640; display: flex; align-items: center; justify-content: center"><svg style="opacity: 0.35" width="42" height="42" viewBox="0 0 48 48" aria-hidden="true">{ICON[kind]}</svg>{CHECK}</div>')
        else:
            out.append(f'<div style="width: 54px; height: 54px; border-radius: 10px; background: #FFFFFF; display: flex; align-items: center; justify-content: center"><svg width="42" height="42" viewBox="0 0 48 48" aria-hidden="true">{ICON[kind]}</svg></div>')
    return '<div style="display: flex; gap: 8px">'+''.join(out)+'</div>'

BANG="font-family: 'Bangers', Impact, sans-serif"
def panel(rays, dots, svg, extra):
    return f'''  <div style="position: absolute; left: 44px; top: 60px; width: 600px; height: 600px; box-sizing: border-box; transform: rotate(-2deg); border: 7px solid #111111; background: repeating-conic-gradient(from 0deg at 55% 40%, {rays[0]} 0deg 7deg, {rays[1]} 7deg 14deg); box-shadow: 14px 14px 0 #111111; overflow: hidden">
  <div aria-hidden="true" style="position: absolute; inset: 0; background-image: radial-gradient({dots} 26%, transparent 28%); background-size: 12px 12px; opacity: 0.28"></div>
{svg}
{extra}
  </div>
'''
def title_box(lamp_idx, lamp_col, big, big_col, sub):
    lamps=''
    for k in range(3):
        if k==lamp_idx:
            lamps+=f'<span class="lampA" style="width: 36px; height: 36px; border-radius: 50%; background: {lamp_col}; box-shadow: 0 0 20px {lamp_col}"></span>'
        else:
            lamps+='<span style="width: 36px; height: 36px; border-radius: 50%; background: #2B2B2B"></span>'
    return f'''    <div style="width: 100%; box-sizing: border-box; background: #141414; border: 6px solid #111111; outline: 4px solid #FFFFFF; border-radius: 22px; padding: 18px 26px; display: flex; align-items: center; gap: 22px; box-shadow: 14px 14px 0 #111111; transform: rotate(2deg)">
      <div style="display: flex; flex-direction: column; gap: 8px">{lamps}</div>
      <div style="display: flex; flex-direction: column; gap: 6px">
        <span style="{BANG}; font-size: 70px; line-height: 0.92; letter-spacing: 2px; color: {big_col}; -webkit-text-stroke: 2px #111111; text-shadow: 6px 6px 0 #E8261E; white-space: nowrap">{big}</span>
        <span style="{BANG}; font-size: 28px; letter-spacing: 2px; color: #FFFFFF">{sub}</span>
      </div>
    </div>
'''
def buttons(primary, href_primary, secondary, href_secondary, arrow):
    ic = '<svg width="34" height="28" viewBox="0 0 26 22" aria-hidden="true"><path d="M2 11h18M13 3l9 8-9 8" stroke="#111111" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></svg>' if arrow else ''
    return f'''    <nav style="margin-top: 52px; width: 380px; display: flex; flex-direction: column; align-items: center; gap: 30px" aria-label="Next step">
      <a href="{href_primary}" style="width: 380px; height: 84px; box-sizing: border-box; border: 5px solid #111111; border-radius: 10px; background: #FFD23F; color: #111111; display: flex; align-items: center; justify-content: center; gap: 14px; {BANG}; font-size: 54px; letter-spacing: 4px; white-space: nowrap; box-shadow: 9px 9px 0 #111111; transform: rotate(-1.5deg)">{primary}{ic}</a>
      <a href="{href_secondary}" style="width: 250px; height: 62px; box-sizing: border-box; border: 5px solid #111111; border-radius: 10px; background: #FFFFFF; color: #111111; display: flex; align-items: center; justify-content: center; {BANG}; font-size: 38px; letter-spacing: 3px; box-shadow: 8px 8px 0 #111111; transform: rotate(1deg)">{secondary}</a>
    </nav>
'''
def page(title, panel_html, right_html):
    h=head.replace('<title>Pigeon &amp; Rat · Start screen</title>',f'<title>{title}</title>')
    return h+'''<div style="width: 1280px; height: 720px; position: relative; overflow: hidden; background: #0E2350; font-family: 'Inter', sans-serif; color: #FFFFFF">

'''+bg+panel_html+'''
  <div style="position: absolute; left: 680px; top: 56px; width: 520px; display: flex; flex-direction: column; align-items: center">
'''+right_html+'''  </div>

</div>
'''+tail


from parts import GO_RAT, GO_TAXI, GO_PIG, CL_RAT
_f=lambda t: t.replace("{ICON['pizza']}",ICON['pizza']).replace("{ICON['cheese']}",ICON['cheese'])
GO_PIG=_f(GO_PIG).replace("translate(96 120)","translate(98 100)"); CL_RAT=_f(CL_RAT).replace("translate(262 186)","translate(262 128)").replace("M232 214l-20-10M240 190l-16-18M428 214l20-10M420 190l16-18","M232 170l-20-10M240 146l-16-18M428 170l20-10M420 146l16-18")
def side_panel(left, rot, rays, dots, svg, extra, label):
    return f"""  <div style="position: absolute; left: {left}px; top: 70px; width: 340px; height: 580px; box-sizing: border-box; transform: rotate({rot}deg); border: 7px solid #111111; background: repeating-conic-gradient(from 0deg at 50% 40%, {rays[0]} 0deg 7deg, {rays[1]} 7deg 14deg); box-shadow: 12px 12px 0 #111111; overflow: hidden">
  <div aria-hidden="true" style="position: absolute; inset: 0; background-image: radial-gradient({dots} 26%, transparent 28%); background-size: 12px 12px; opacity: 0.28"></div>
  <svg style="position: absolute; left: 0; top: 0" width="326" height="566" viewBox="0 0 340 580" role="img" aria-label="{label}">
{svg}
  </svg>
{extra}
  </div>
"""
def stripes(y0):
    return ''.join(f'<rect x="{x}" y="{y0+18}" width="40" height="{580-y0}" rx="4" fill="#E8E3D8"></rect>' for x in (20,90,160,230,300))
def bricks(h):
    d=[]
    for k,y in enumerate(range(0,h,50)):
        d.append(f'M0 {y}H340')
        off=0 if k%2==0 else 50
        for x in range(off+40,340,100): d.append(f'M{x} {y}V{y+50}')
    return f'<rect x="0" y="0" width="340" height="{h}" fill="#B5523A"></rect><path d="{"".join(d)}" stroke="#7E3324" stroke-width="5"></path>'
def bubble(left, top, w, h, lines, tail_left=True):
    rx, ry = w/2-6, h/2-14
    cx, cy = w/2, h/2-8
    tx = cx-rx*0.45 if tail_left else cx+rx*0.45
    tail = f'M{tx-6:.0f} {cy+ry*0.8:.0f}L{tx-30 if tail_left else tx+30:.0f} {h-2}L{tx+30:.0f} {cy+ry*0.85:.0f}Z' if tail_left else f'M{tx+6:.0f} {cy+ry*0.8:.0f}L{tx+30:.0f} {h-2}L{tx-30:.0f} {cy+ry*0.85:.0f}Z'
    txt=''
    n=len(lines)
    for k,(t,size,col) in enumerate(lines):
        y=cy+(k-(n-1)/2)*size*0.95+size*0.35
        txt+=f'<text x="{cx}" y="{y:.0f}" text-anchor="middle" font-family="Bangers, Impact, sans-serif" font-size="{size}" letter-spacing="1" fill="{col}">{t}</text>'
    return f'<svg style="position: absolute; left: {left}px; top: {top}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true"><path d="{tail}" fill="#FFFFFF" stroke="#111111" stroke-width="5" stroke-linejoin="round"></path><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" stroke="#111111" stroke-width="5"></ellipse>{txt}</svg>'
def burst_svg(left, top, word, fill, txt, size):
    pts=star(120,95,110,62,12,0.2)
    return f'<svg style="position: absolute; left: {left}px; top: {top}px" width="240" height="190" viewBox="0 0 240 190" aria-hidden="true"><polygon points="{pts}" fill="{fill}" stroke="#111111" stroke-width="6" stroke-linejoin="round"></polygon><text x="120" y="{95+size*0.35:.0f}" text-anchor="middle" transform="rotate(-10 120 95)" font-family="Bangers, Impact, sans-serif" font-size="{size}" letter-spacing="3" fill="{txt}" stroke="#111111" stroke-width="3" paint-order="stroke">{word}</text></svg>'

def page3(title, lp, rp, center):
    h=head.replace('<title>Pigeon &amp; Rat · Start screen</title>',f'<title>{title}</title>')
    return h+"""<div style="width: 1280px; height: 720px; position: relative; overflow: hidden; background: #0E2350; font-family: 'Inter', sans-serif; color: #FFFFFF">

"""+bg+lp+rp+"""
  <div style="position: absolute; left: 400px; top: 60px; width: 480px; display: flex; flex-direction: column; align-items: center">
"""+center+"""  </div>

</div>
"""+tail

# ---------------- GAME OVER ----------------
go_l=side_panel(28,-2,('#FF5A4E','#FF8C6B'),'#8E1A12',
  f'<rect x="0" y="300" width="340" height="300" fill="#3A3B3F"></rect>{stripes(300)}<g transform="translate(0 70) scale(0.8)">{GO_RAT}</g>',
  burst_svg(30,40,'SPLAT!','#FFE14D','#E8261E',62),'The rat lies flattened on the crosswalk with a tire track across it')
go_r=side_panel(912,2,('#FF5A4E','#FF8C6B'),'#8E1A12',
  f'<rect x="0" y="380" width="340" height="220" fill="#3A3B3F"></rect>{stripes(380)}<g transform="translate(-2 360) scale(1.1)">{GO_TAXI.replace("translate(330 150)","translate(0 0)")}</g><g transform="translate(-10 170) scale(1.2)">{GO_PIG.replace("translate(30 150) scale(0.7)","translate(0 0) scale(0.7)")}</g>',
  bubble(110,30,200,120,[('THANKS!',38,'#111111')]),'A taxi drives off while the pigeon flies away with the pizza')
go_c=title_box(0,'#FF3B2F','GAME OVER','#FFD23F','FLATTENED BY A TAXI · 2ND AVE')+f"""
    <div style="margin-top: 44px; width: 420px; box-sizing: border-box; background: #141414; border: 4px solid #FFFFFF; border-radius: 12px; padding: 16px 20px; display: flex; flex-direction: column; align-items: center; gap: 14px; box-shadow: 9px 9px 0 #111111; transform: rotate(-1deg)">
      <div style="display: flex; align-items: baseline; gap: 14px">
        <span style="{BANG}; font-size: 30px; letter-spacing: 2px">SCORE</span>
        <span style="font-family: 'Share Tech Mono', monospace; font-size: 46px; line-height: 1; color: #FFD23F">1,240</span>
      </div>
      {tiles([('pizza',True),('dog',True),('cheese',True),('soda',False),('pizza',False)])}
    </div>
"""+buttons('TRY AGAIN','Final.dc.html','MENU','Start.dc.html',False)
open(D+'GameOver.dc.html','w').write(page3('Pigeon &amp; Rat · Game over',go_l,go_r,go_c))

# ---------------- LEVEL CLEAR ----------------
cl_l=side_panel(28,-2,('#5FD68A','#B6F06A'),'#1E7A45',
  f'<g transform="translate(0 150)">{bricks(300)}</g><rect x="0" y="440" width="340" height="160" fill="#B9B4AA" stroke="#111111" stroke-width="5"></rect><g transform="translate(-162 40)"><ellipse cx="330" cy="460" rx="100" ry="13" fill="rgba(0,0,0,0.3)"></ellipse>{CL_RAT}</g>',
  burst_svg(20,20,'YUM!','#3BD16F','#FFE14D',66),'The rat holds a slice of cheesecake over its head')
cl_r=side_panel(912,2,('#5FD68A','#B6F06A'),'#1E7A45',
  f"""<g transform="translate(0 150)">{bricks(300)}</g><rect x="0" y="440" width="340" height="160" fill="#B9B4AA" stroke="#111111" stroke-width="5"></rect>
  <path d="M95 442V330Q95 250 170 250Q245 250 245 330V442Z" fill="#141414" stroke="#111111" stroke-width="6"></path>
  <g transform="translate(18 372) scale(1.8)">{ICON['soda']}</g>
  <g transform="translate(222 400) scale(1.9) rotate(-10 24 24)">{ICON['pizza']}</g>
  <g transform="translate(96 420) scale(1.9)">{ICON['dog']}</g>
  <g transform="translate(170 452) scale(1.7)">{ICON['cheese']}</g>
  <g transform="translate(20 452) scale(1.7) rotate(20 24 24)">{ICON['pizza']}</g>""",
  bubble(60,40,230,130,[('HOME SWEET',30,'#111111'),('HOME!',36,'#E8261E')]),'The rat home in the wall with all the food piled in front')
row=lambda a,b: f'<div style="display: flex; justify-content: space-between; width: 100%; font-family: \'Share Tech Mono\', monospace; font-size: 18px; line-height: 1.15; color: #E8E3D8"><span>{a}</span><span>{b}</span></div>'
cl_c=title_box(2,'#33D17A','STREET CLEAR!','#3BD16F','W 34TH ST · RAIDED!')+f"""
    <div style="margin-top: 34px; width: 420px; box-sizing: border-box; background: #141414; border: 4px solid #FFFFFF; border-radius: 12px; padding: 12px 22px; display: flex; flex-direction: column; align-items: center; gap: 6px; box-shadow: 9px 9px 0 #111111; transform: rotate(-1deg)">
      {tiles([('pizza',True),('dog',True),('cheese',True),('soda',True),('pizza',True)])}
      <div style="width: 100%; margin-top: 4px; display: flex; flex-direction: column; gap: 2px">{row('FOOD','+600')}{row('RISKY COMBO','+420')}{row('LIVES x2','+200')}</div>
      <div style="width: 100%; height: 3px; background: #FFFFFF"></div>
      <div style="width: 100%; display: flex; align-items: center; justify-content: space-between">
        <span style="{BANG}; font-size: 32px; letter-spacing: 2px">TOTAL</span>
        <span style="display: flex; align-items: center; gap: 10px"><span style="{BANG}; font-size: 20px; letter-spacing: 1px; background: #E8261E; color: #FFFFFF; border: 3px solid #111111; border-radius: 6px; padding: 1px 8px; transform: rotate(-4deg)">NEW BEST!</span><span style="font-family: 'Share Tech Mono', monospace; font-size: 40px; line-height: 1; color: #FFD23F">2,460</span></span>
      </div>
    </div>
"""+buttons('NEXT BLOCK','Donate.dc.html','MENU','Start.dc.html',True).replace('margin-top: 52px','margin-top: 34px').replace('gap: 30px','gap: 24px')
open(D+'StageClear.dc.html','w').write(page3('Pigeon &amp; Rat · Level clear',cl_l,cl_r,cl_c))

# previews
for f in ['GameOver','StageClear','Start']:
    s=open(D+f+'.dc.html').read()
    b=s[s.index('<div style="width: 1280px'):s.index('</x-dc>')]
    h=s[s.index('<link href'):s.index('</style>')+8]
    ff='<style>@font-face{font-family:Bangers;src:url(fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}@font-face{font-family:"Share Tech Mono";src:url(fonts/node_modules/@fontsource/share-tech-mono/files/share-tech-mono-latin-400-normal.woff2)}</style>'
    open(f'/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/{f}_prev.html','w').write('<html><head>'+ff+h+'</head><body style=margin:0>'+b+'</body></html>')
print('ok')
