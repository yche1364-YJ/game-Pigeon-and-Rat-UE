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
'cheese':f'<path d="M5 30L29 12L44 22Z" fill="#FFE27A" stroke="{O}" stroke-width="3" stroke-linejoin="round"/><path d="M5 30L44 22L44 35L5 41Z" fill="#FFC93C" stroke="{O}" stroke-width="3" stroke-linejoin="round"/><ellipse cx="16" cy="34" rx="3" ry="2.4" fill="#E8A92A" stroke="{O}" stroke-width="1.8"/><ellipse cx="30" cy="30" rx="3.6" ry="2.8" fill="#E8A92A" stroke="{O}" stroke-width="1.8"/><ellipse cx="27" cy="20" rx="2.6" ry="1.6" fill="#F2C24A" stroke="{O}" stroke-width="1.6"/>',
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
        <span style="{BANG}; font-size: 82px; line-height: 0.92; letter-spacing: 3px; color: {big_col}; -webkit-text-stroke: 2px #111111; text-shadow: 6px 6px 0 #E8261E; white-space: nowrap">{big}</span>
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

# ---------------- GAME OVER ----------------
burst=star(130,100,118,64,12,0.15)
go_svg=f'''  <svg style="position: absolute; left: -14px; top: 40px" width="600" height="560" viewBox="0 0 560 520" role="img" aria-label="The rat lies flattened on the crosswalk with tire tracks across it while a taxi drives off and a pigeon makes off with the pizza">
    <rect x="-20" y="330" width="600" height="200" fill="#3A3B3F"></rect>
    <rect x="30" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect><rect x="110" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect><rect x="190" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect><rect x="270" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect><rect x="350" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect><rect x="430" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect><rect x="510" y="350" width="40" height="160" rx="4" fill="#E8E3D8"></rect>
    <!-- flattened rat -->
    <path d="M95 428C60 436 40 420 10 430" fill="none" stroke="#111111" stroke-width="13" stroke-linecap="round"></path>
    <path d="M95 428C60 436 40 420 10 430" fill="none" stroke="#F2A7A7" stroke-width="6" stroke-linecap="round"></path>
    <ellipse cx="250" cy="430" rx="160" ry="26" fill="#8C8781" stroke="#111111" stroke-width="5"></ellipse>
    <ellipse cx="370" cy="412" rx="22" ry="11" fill="#F2A7A7" stroke="#111111" stroke-width="4"></ellipse>
    <ellipse cx="404" cy="440" rx="22" ry="10" fill="#F2A7A7" stroke="#111111" stroke-width="4"></ellipse>
    <path d="M318 418L332 432M332 418L318 432M350 424L364 438M364 424L350 438" stroke="#111111" stroke-width="4.5" stroke-linecap="round"></path>
    <path d="M338 444Q346 456 354 446" fill="#E86C7A" stroke="#111111" stroke-width="3"></path>
    <circle cx="410" cy="428" r="7" fill="#E86C7A" stroke="#111111" stroke-width="3"></circle>
    <path d="M150 452L140 470M200 456L196 474M300 456L306 474" stroke="#111111" stroke-width="10" stroke-linecap="round"></path>
    <path d="M150 452L140 470M200 456L196 474M300 456L306 474" stroke="#F2A7A7" stroke-width="5" stroke-linecap="round"></path>
    <!-- tire track over the rat -->
    <g opacity="0.85"><rect x="200" y="330" width="58" height="200" fill="#1C1C1E"></rect>
    <path d="M206 344L229 356L252 344M206 372L229 384L252 372M206 400L229 412L252 400M206 428L229 440L252 428M206 456L229 468L252 456M206 484L229 496L252 484" stroke="#4A4A4E" stroke-width="6" fill="none"></path></g>
    <!-- dizzy stars -->
    <path d="M330 372l5 10 11 1-8 7 3 11-11-6-10 6 3-11-8-7 11-1z" fill="#FFE14D" stroke="#111111" stroke-width="3" stroke-linejoin="round"></path>
    <path d="M392 360l4 8 9 1-7 6 2 9-8-5-8 5 2-9-7-6 9-1z" fill="#FFE14D" stroke="#111111" stroke-width="3" stroke-linejoin="round"></path>
    <path d="M300 386q40-26 110-22" fill="none" stroke="#111111" stroke-width="3" stroke-dasharray="6 7"></path>
    <!-- taxi speeding away -->
    <g transform="translate(330 150)">
      <path d="M0 130H40M-10 100H30" stroke="#111111" stroke-width="7" stroke-linecap="round"></path>
      <path d="M70 60Q80 20 120 18H170Q206 20 214 60L222 64V128H62V64Z" fill="#FFC21A" stroke="#111111" stroke-width="5" stroke-linejoin="round"></path>
      <path d="M92 60Q98 34 124 32H166Q190 34 196 60Z" fill="#9FD3F0" stroke="#111111" stroke-width="4" stroke-linejoin="round"></path>
      <rect x="118" y="0" width="54" height="20" rx="4" fill="#FFFFFF" stroke="#111111" stroke-width="4"></rect>
      <text x="145" y="16" text-anchor="middle" font-family="Bangers, Impact, sans-serif" font-size="16" fill="#111111">TAXI</text>
      <path d="M62 84H222" stroke="#111111" stroke-width="4"></path>
      <path d="M70 92h22v12H70zM192 92h22v12h-22z" fill="#E8261E" stroke="#111111" stroke-width="3"></path>
      <rect x="114" y="98" width="56" height="16" rx="3" fill="#FFFFFF" stroke="#111111" stroke-width="3"></rect>
      <rect x="66" y="126" width="34" height="22" rx="5" fill="#111111"></rect><rect x="184" y="126" width="34" height="22" rx="5" fill="#111111"></rect>
      <circle cx="40" cy="128" r="12" fill="#FFFFFF" stroke="#111111" stroke-width="4"></circle><circle cx="22" cy="116" r="8" fill="#FFFFFF" stroke="#111111" stroke-width="4"></circle>
    </g>
    <!-- pigeon flying off with the pizza -->
    <g transform="translate(30 150) scale(0.7)">
      <path d="M100 60Q150 0 210 4Q180 40 168 70Z" fill="#767B84" stroke="#111111" stroke-width="6" stroke-linejoin="round"></path>
      <ellipse cx="120" cy="80" rx="52" ry="30" fill="#A3A7AF" stroke="#111111" stroke-width="6"></ellipse>
      <path d="M118 66Q60 10 0 22Q40 50 60 84Q90 94 118 86Z" fill="#9196A0" stroke="#111111" stroke-width="6" stroke-linejoin="round"></path>
      <circle cx="176" cy="66" r="22" fill="#6F7480" stroke="#111111" stroke-width="6"></circle>
      <path d="M196 64L218 72L196 78Z" fill="#F08A3C" stroke="#111111" stroke-width="5" stroke-linejoin="round"></path>
      <circle cx="182" cy="60" r="5" fill="#111111"></circle>
      <path d="M120 106L116 128M136 106L140 128" stroke="#F08A3C" stroke-width="7" stroke-linecap="round"></path>
      <g transform="translate(96 120) rotate(12) scale(1.3)">{ICON['pizza']}</g>
    </g>
  </svg>'''
go_extra=f'''  <svg style="position: absolute; left: 6px; top: 8px" width="260" height="200" viewBox="0 0 260 200" aria-hidden="true"><polygon points="{burst}" fill="#FFE14D" stroke="#111111" stroke-width="6" stroke-linejoin="round"></polygon><text x="130" y="122" text-anchor="middle" transform="rotate(-8 130 100)" font-family="Bangers, Impact, sans-serif" font-size="64" letter-spacing="3" fill="#E8261E" stroke="#111111" stroke-width="3" paint-order="stroke">SPLAT!</text></svg>
  <svg style="position: absolute; left: 380px; top: 22px" width="190" height="120" viewBox="0 0 190 120" aria-hidden="true"><path d="M60 92L36 116L92 98Z" fill="#FFFFFF" stroke="#111111" stroke-width="5" stroke-linejoin="round"></path><ellipse cx="96" cy="54" rx="88" ry="46" fill="#FFFFFF" stroke="#111111" stroke-width="5"></ellipse><path d="M62 92L90 98" stroke="#FFFFFF" stroke-width="7"></path><text x="96" y="66" text-anchor="middle" transform="rotate(4 96 54)" font-family="Bangers, Impact, sans-serif" font-size="34" letter-spacing="1" fill="#111111">THANKS!</text></svg>'''
go_right=title_box(0,'#FF3B2F','GAME OVER','#FFD23F','FLATTENED BY A TAXI · LEVEL 2')+f'''
    <div style="margin-top: 44px; width: 420px; box-sizing: border-box; background: #141414; border: 4px solid #FFFFFF; border-radius: 12px; padding: 16px 20px; display: flex; flex-direction: column; align-items: center; gap: 14px; box-shadow: 9px 9px 0 #111111; transform: rotate(-1deg)">
      <div style="display: flex; align-items: baseline; gap: 14px">
        <span style="{BANG}; font-size: 30px; letter-spacing: 2px">SCORE</span>
        <span style="font-family: 'Share Tech Mono', monospace; font-size: 46px; line-height: 1; color: #FFD23F">1,240</span>
      </div>
      {tiles([('pizza',True),('dog',True),('cheese',True),('soda',False),('pizza',False)])}
    </div>
'''+buttons('TRY AGAIN','Final.dc.html','MENU','Start.dc.html',False)

open(D+'GameOver.dc.html','w').write(page('Pigeon &amp; Rat · Game over', panel(('#FF5A4E','#FF8C6B'),'#8E1A12',go_svg,go_extra), go_right))

# ---------------- LEVEL CLEAR ----------------
burst2=star(120,95,110,62,12,0.25)
cl_svg=f'''  <svg style="position: absolute; left: -14px; top: 40px" width="600" height="560" viewBox="0 0 560 520" role="img" aria-label="The rat stands at its home in the wall, holding a block of cheese over its head beside a pile of collected food">
    <!-- brick wall + home hole -->
    <rect x="-20" y="150" width="600" height="250" fill="#B5523A"></rect>
    <path d="M-20 200H580M-20 250H580M-20 300H580M-20 350H580M40 150V200M140 150V200M240 150V200M340 150V200M440 150V200M540 150V200M90 200V250M190 200V250M290 200V250M390 200V250M490 200V250M40 250V300M140 250V300M240 250V300M340 250V300M440 250V300M540 250V300M90 300V350M190 300V350M290 300V350M390 300V350M490 300V350M40 350V400M140 350V400M240 350V400M340 350V400M440 350V400M540 350V400" stroke="#7E3324" stroke-width="5"></path>
    <rect x="-20" y="150" width="600" height="250" fill="none" stroke="#111111" stroke-width="5"></rect>
    <path d="M40 400V320Q40 260 100 260Q160 260 160 320V400Z" fill="#141414" stroke="#111111" stroke-width="6"></path>
    <rect x="-20" y="396" width="600" height="130" fill="#B9B4AA" stroke="#111111" stroke-width="5"></rect>
    <ellipse cx="330" cy="460" rx="120" ry="14" fill="rgba(0,0,0,0.3)"></ellipse>
    <!-- pile of food -->
    <g transform="translate(60 330) scale(1.6)">{ICON['soda']}</g>
    <g transform="translate(110 360) scale(1.7)">{ICON['dog']}</g>
    <g transform="translate(440 350) scale(1.7)">{ICON['pizza']}</g>
    <g transform="translate(470 380) scale(1.5) rotate(-10 24 24)">{ICON['pizza']}</g>
    <!-- rat standing, arms up -->
    <path d="M380 440C430 440 450 400 440 370" fill="none" stroke="#111111" stroke-width="13" stroke-linecap="round"></path>
    <path d="M380 440C430 440 450 400 440 370" fill="none" stroke="#F2A7A7" stroke-width="6" stroke-linecap="round"></path>
    <ellipse cx="305" cy="458" rx="22" ry="10" fill="#F2A7A7" stroke="#111111" stroke-width="4"></ellipse>
    <ellipse cx="360" cy="458" rx="22" ry="10" fill="#F2A7A7" stroke="#111111" stroke-width="4"></ellipse>
    <ellipse cx="332" cy="390" rx="58" ry="72" fill="#8C8781" stroke="#111111" stroke-width="5"></ellipse>
    <ellipse cx="332" cy="405" rx="36" ry="48" fill="#B5B0A9"></ellipse>
    <path d="M286 352L250 270M378 352L414 270" stroke="#111111" stroke-width="15" stroke-linecap="round"></path>
    <path d="M286 352L250 270M378 352L414 270" stroke="#8C8781" stroke-width="8" stroke-linecap="round"></path>
    <circle cx="282" cy="276" r="18" fill="#F2A7A7" stroke="#111111" stroke-width="4"></circle>
    <circle cx="382" cy="276" r="18" fill="#F2A7A7" stroke="#111111" stroke-width="4"></circle>
    <circle cx="300" cy="268" r="10" fill="#D97F86"></circle><circle cx="364" cy="268" r="10" fill="#D97F86"></circle>
    <path d="M290 300Q332 262 374 300Q384 340 332 348Q280 340 290 300Z" fill="#8C8781" stroke="#111111" stroke-width="5" stroke-linejoin="round"></path>
    <path d="M308 304Q316 296 324 304M340 304Q348 296 356 304" fill="none" stroke="#111111" stroke-width="4" stroke-linecap="round"></path>
    <path d="M316 322Q332 338 348 322Z" fill="#E86C7A" stroke="#111111" stroke-width="3" stroke-linejoin="round"></path>
    <circle cx="332" cy="316" r="5" fill="#E86C7A" stroke="#111111" stroke-width="2.5"></circle>
    <!-- cheese held overhead -->
    <g transform="translate(262 186) scale(3)">{ICON['cheese']}</g>
    <path d="M232 214l-20-10M240 190l-16-18M428 214l20-10M420 190l16-18" stroke="#111111" stroke-width="5" stroke-linecap="round"></path>
  </svg>'''
cl_extra=f'''  <svg style="position: absolute; left: 6px; top: 6px" width="240" height="190" viewBox="0 0 240 190" aria-hidden="true"><polygon points="{burst2}" fill="#3BD16F" stroke="#111111" stroke-width="6" stroke-linejoin="round"></polygon><text x="120" y="114" text-anchor="middle" transform="rotate(-10 120 95)" font-family="Bangers, Impact, sans-serif" font-size="66" letter-spacing="3" fill="#FFE14D" stroke="#111111" stroke-width="3" paint-order="stroke">YUM!</text></svg>
  <svg style="position: absolute; left: 330px; top: 30px" width="240" height="130" viewBox="0 0 240 130" aria-hidden="true"><path d="M70 100L50 128L110 106Z" fill="#FFFFFF" stroke="#111111" stroke-width="5" stroke-linejoin="round"></path><ellipse cx="120" cy="58" rx="112" ry="50" fill="#FFFFFF" stroke="#111111" stroke-width="5"></ellipse><path d="M72 100L106 106" stroke="#FFFFFF" stroke-width="7"></path><text x="120" y="52" text-anchor="middle" transform="rotate(-3 120 58)" font-family="Bangers, Impact, sans-serif" font-size="30" fill="#111111">HOME SWEET</text><text x="120" y="86" text-anchor="middle" transform="rotate(-3 120 58)" font-family="Bangers, Impact, sans-serif" font-size="34" fill="#E8261E">HOME!</text></svg>'''
row=lambda a,b: f'<div style="display: flex; justify-content: space-between; width: 100%; font-family: \'Share Tech Mono\', monospace; font-size: 18px; line-height: 1.15; color: #E8E3D8"><span>{a}</span><span>{b}</span></div>'
cl_right=title_box(2,'#33D17A','LEVEL CLEAR!','#3BD16F','LEVEL 1 · ALL FOOD HOME')+f'''
    <div style="margin-top: 34px; width: 420px; box-sizing: border-box; background: #141414; border: 4px solid #FFFFFF; border-radius: 12px; padding: 12px 22px; display: flex; flex-direction: column; align-items: center; gap: 6px; box-shadow: 9px 9px 0 #111111; transform: rotate(-1deg)">
      {tiles([('pizza',True),('dog',True),('cheese',True),('soda',True),('pizza',True)])}
      <div style="width: 100%; margin-top: 4px; display: flex; flex-direction: column; gap: 2px">{row('FOOD','+600')}{row('RISKY COMBO','+420')}{row('LIVES x2','+200')}</div>
      <div style="width: 100%; height: 3px; background: #FFFFFF"></div>
      <div style="width: 100%; display: flex; align-items: center; justify-content: space-between">
        <span style="{BANG}; font-size: 32px; letter-spacing: 2px">TOTAL</span>
        <span style="display: flex; align-items: center; gap: 10px"><span style="{BANG}; font-size: 20px; letter-spacing: 1px; background: #E8261E; color: #FFFFFF; border: 3px solid #111111; border-radius: 6px; padding: 1px 8px; transform: rotate(-4deg)">NEW BEST!</span><span style="font-family: 'Share Tech Mono', monospace; font-size: 40px; line-height: 1; color: #FFD23F">2,460</span></span>
      </div>
    </div>
'''+buttons('NEXT LEVEL','Final.dc.html','MENU','Start.dc.html',True).replace('margin-top: 52px','margin-top: 34px').replace('gap: 30px','gap: 24px')
open(D+'StageClear.dc.html','w').write(page('Pigeon &amp; Rat · Level clear', panel(('#5FD68A','#B6F06A'),'#1E7A45',cl_svg,cl_extra), cl_right))

# previews
for f in ['GameOver','StageClear','Start']:
    s=open(D+f+'.dc.html').read()
    b=s[s.index('<div style="width: 1280px'):s.index('</x-dc>')]
    h=s[s.index('<link href'):s.index('</style>')+8]
    ff='<style>@font-face{font-family:Bangers;src:url(fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}@font-face{font-family:"Share Tech Mono";src:url(fonts/node_modules/@fontsource/share-tech-mono/files/share-tech-mono-latin-400-normal.woff2)}</style>'
    open(f'/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/{f}_prev.html','w').write('<html><head>'+ff+h+'</head><body style=margin:0>'+b+'</body></html>')
print('ok')
