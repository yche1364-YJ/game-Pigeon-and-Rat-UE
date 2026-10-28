import math
D='/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/nyc_ui/project/'
start=open(D+'Start.dc.html').read()
head=start[:start.index('<div style="width: 1280px')].replace('<title>Pigeon &amp; Rat · Start screen</title>','<title>Pigeon &amp; Rat · Donate</title>')
bg=start[start.index('  <!-- background: comic halftone night sky -->'):start.index('  <!-- ===== left:')]
tail=start[start.index('</x-dc>'):]
L=start.split('\n')
rat='\n'.join(L[48:72])  # tail .. whiskers
pigeon='\n'.join(L[86:108])
BANG="font-family: 'Bangers', Impact, sans-serif"
def star(cx,cy,ro,ri,n,rot=0):
    pts=[]
    for k in range(2*n):
        r=ro if k%2==0 else ri*(0.85+0.3*((k*7)%5)/4)
        a=math.pi*k/n+rot
        pts.append(f"{cx+r*math.cos(a):.0f},{cy+r*math.sin(a):.0f}")
    return ' '.join(pts)
K='#111111'
# --- Chinatown street ---
shops=''
fronts=[(0,'#2F8C8C','NOODLE'),(180,'#D9A21E','DUMPLING'),(360,'#6A9A5B','CHICKEN'),(540,'#3E6FB0','RICE')]
for x,col,txt in fronts:
    shops+=f'<rect x="{x}" y="60" width="180" height="340" fill="{col}" stroke="{K}" stroke-width="5"></rect>'
    for wy in (170,236):
        for wx in (x+22,x+102):
            shops+=f'<rect x="{wx}" y="{wy}" width="56" height="56" fill="#F6E7B8" stroke="{K}" stroke-width="4"></rect><path d="M{wx+28} {wy}V{wy+56}M{wx} {wy+28}H{wx+56}" stroke="{K}" stroke-width="3"></path>'
    shops+=f'<rect x="{x+16}" y="106" width="148" height="46" rx="4" fill="#141414" stroke="{K}" stroke-width="4"></rect><text x="{x+90}" y="141" text-anchor="middle" font-family="Bangers, Impact, sans-serif" font-size="32" fill="#FFD23F" letter-spacing="3">{txt}</text>'
    shops+=f'<path d="M{x+6} 300H{x+174}L{x+164} 326H{x+16}Z" fill="#F4F1EA" stroke="{K}" stroke-width="4"></path>'
    for k in range(6): shops+=f'<path d="M{x+16+k*25} 300L{x+20+k*25} 326" stroke="{col}" stroke-width="9"></path>'
    shops+=f'<rect x="{x+60}" y="330" width="60" height="70" fill="#3A2A20" stroke="{K}" stroke-width="4"></rect>'
# lantern string
lan='<path d="M-10 10Q180 34 360 12Q540 -8 730 14" fill="none" stroke="'+K+'" stroke-width="4"></path>'
for x,y in [(60,14),(170,22),(280,16),(400,8),(510,4),(620,8)]:
    lan+=f'<path d="M{x} {y}V{y+8}" stroke="{K}" stroke-width="4"></path><ellipse cx="{x}" cy="{y+34}" rx="26" ry="24" fill="#F2A33A" stroke="{K}" stroke-width="4"></ellipse><path d="M{x-12} {y+12}Q{x-20} {y+34} {x-12} {y+56}M{x+12} {y+12}Q{x+20} {y+34} {x+12} {y+56}" stroke="#B86A14" stroke-width="3" fill="none"></path><rect x="{x-10}" y="{y+8}" width="20" height="6" fill="#FFD23F" stroke="{K}" stroke-width="2"></rect><rect x="{x-10}" y="{y+56}" width="20" height="6" fill="#FFD23F" stroke="{K}" stroke-width="2"></rect><path d="M{x} {y+62}V{y+80}" stroke="#FFD23F" stroke-width="4"></path>'
street=f'<rect x="-10" y="396" width="740" height="220" fill="#B9B4AA" stroke="{K}" stroke-width="5"></rect><path d="M-10 470H730M120 400L100 470M300 400L290 470M480 400L480 470M660 400L670 470" stroke="#8E897F" stroke-width="4"></path>'
# --- uncle with broom (facing left, swinging) ---
skin='#E9B98E'
uncle=f'''
  <ellipse cx="520" cy="572" rx="110" ry="14" fill="rgba(0,0,0,0.3)"></ellipse>
  <path d="M500 430L478 556M532 430L566 554" stroke="{K}" stroke-width="44" stroke-linecap="round"></path>
  <path d="M500 430L478 556M532 430L566 554" stroke="#4A5670" stroke-width="34" stroke-linecap="round"></path>
  <ellipse cx="468" cy="564" rx="30" ry="12" fill="#1C1C1C" stroke="{K}" stroke-width="3"></ellipse>
  <ellipse cx="578" cy="562" rx="30" ry="12" fill="#1C1C1C" stroke="{K}" stroke-width="3"></ellipse>
  <path d="M470 418Q515 440 562 418L566 440Q515 458 466 440Z" fill="#2B2B2B" stroke="{K}" stroke-width="3"></path>
  <!-- torso -->
  <path d="M478 300Q515 288 552 300L568 440Q515 452 464 440Z" fill="#F6F3EC" stroke="{K}" stroke-width="5" stroke-linejoin="round"></path>
  <path d="M490 300Q515 330 540 300" fill="{skin}" stroke="{K}" stroke-width="4"></path>
  <!-- broom held up in front, like a shield -->
  <path d="M452 196L404 500" stroke="{K}" stroke-width="16" stroke-linecap="round"></path>
  <path d="M452 196L404 500" stroke="#B07A3E" stroke-width="9" stroke-linecap="round"></path>
  <path d="M392 488L370 492L352 566L440 572L428 494Z" fill="#E2BE5E" stroke="{K}" stroke-width="5" stroke-linejoin="round"></path>
  <path d="M378 500L366 566M392 500L388 568M406 500L408 570M420 500L428 568" stroke="#A8822E" stroke-width="3"></path>
  <path d="M394 488L422 490" stroke="#3E6FB0" stroke-width="10"></path>
  <!-- arms gripping the handle -->
  <path d="M484 316L446 330L432 300" fill="none" stroke="{K}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"></path>
  <path d="M484 316L446 330L432 300" fill="none" stroke="{skin}" stroke-width="21" stroke-linecap="round" stroke-linejoin="round"></path>
  <path d="M548 314L520 382L428 360" fill="none" stroke="{K}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"></path>
  <path d="M548 314L520 382L428 360" fill="none" stroke="{skin}" stroke-width="21" stroke-linecap="round" stroke-linejoin="round"></path>
  <circle cx="436" cy="298" r="15" fill="{skin}" stroke="{K}" stroke-width="4"></circle>
  <circle cx="424" cy="358" r="15" fill="{skin}" stroke="{K}" stroke-width="4"></circle>
  <!-- head: shocked -->
  <ellipse cx="514" cy="252" rx="40" ry="44" fill="{skin}" stroke="{K}" stroke-width="5"></ellipse>
  <path d="M480 246Q470 220 482 208M548 246Q558 222 546 208M488 220L480 200M540 220L548 200" stroke="#D6D2CB" stroke-width="8" fill="none" stroke-linecap="round"></path>
  <circle cx="498" cy="248" r="13" fill="#FFFFFF" stroke="{K}" stroke-width="3.5"></circle>
  <circle cx="530" cy="248" r="13" fill="#FFFFFF" stroke="{K}" stroke-width="3.5"></circle>
  <path d="M511 248H517" stroke="{K}" stroke-width="3"></path>
  <circle cx="497" cy="248" r="3" fill="{K}"></circle><circle cx="529" cy="248" r="3" fill="{K}"></circle>
  <path d="M484 224Q496 214 508 222M520 222Q532 214 544 224" stroke="#9A958E" stroke-width="5" fill="none" stroke-linecap="round"></path>
  <ellipse cx="514" cy="282" rx="9" ry="13" fill="#7A2A22" stroke="{K}" stroke-width="3"></ellipse>
  <path d="M560 228Q572 240 566 252Q556 246 560 228Z" fill="#8FD3F5" stroke="{K}" stroke-width="2.5"></path>
  <path d="M470 196L462 176M484 186L482 166M548 188L554 168M560 200L572 184" stroke="{K}" stroke-width="5" stroke-linecap="round"></path>
'''
drum=f'<g transform="translate(150 400) rotate(-20)"><path d="M48 24L76 18" stroke="{K}" stroke-width="16" stroke-linecap="round"></path><path d="M48 24L76 18" stroke="#FFF6E2" stroke-width="9" stroke-linecap="round"></path><circle cx="80" cy="12" r="8" fill="#FFF6E2" stroke="{K}" stroke-width="4"></circle><circle cx="84" cy="22" r="8" fill="#FFF6E2" stroke="{K}" stroke-width="4"></circle><path d="M4 30Q0 2 30 4Q56 8 52 28Q48 46 24 46Q8 44 4 30Z" fill="#C9772E" stroke="{K}" stroke-width="5"></path><path d="M14 16Q22 10 30 12" stroke="#E8A45E" stroke-width="5" fill="none" stroke-linecap="round"></path></g>'
ratg=f'''
  <ellipse cx="180" cy="566" rx="120" ry="13" fill="rgba(0,0,0,0.3)"></ellipse>
  <g transform="translate(400 186) scale(-0.9 0.9)">{rat}</g>
  <path d="M370 470H430M380 500H440M376 530H426" stroke="{K}" stroke-width="6" stroke-linecap="round"></path>
  {drum}
  <g transform="translate(14 238) scale(0.72)">{pigeon}</g>
'''
burst=star(110,85,100,56,12,0.1)
panel=f'''  <div style="position: absolute; left: 40px; top: 60px; width: 720px; height: 600px; box-sizing: border-box; transform: rotate(-1.5deg); border: 7px solid {K}; background: #CFE3EA; box-shadow: 14px 14px 0 {K}; overflow: hidden">
  <svg style="position: absolute; left: 0; top: 0" width="706" height="586" viewBox="0 0 720 600" role="img" aria-label="An Asian district street with noodle, dumpling, chicken and rice shops: a startled uncle holds up his broom as the rat runs past and a pigeon swoops down to grab the drumstick on its back">
  {shops}{lan}{street}{ratg}{uncle}
  </svg>
  <div aria-hidden="true" style="position: absolute; inset: 0; background-image: radial-gradient(#C8342B 22%, transparent 24%); background-size: 12px 12px; opacity: 0.12; pointer-events: none"></div>
  <svg style="position: absolute; left: 0px; top: 262px" width="200" height="155" viewBox="0 0 220 170" aria-hidden="true"><polygon points="{burst}" fill="#FFE14D" stroke="{K}" stroke-width="6" stroke-linejoin="round"></polygon><text x="110" y="104" text-anchor="middle" transform="rotate(-12 110 85)" font-family="Bangers, Impact, sans-serif" font-size="50" letter-spacing="3" fill="#3E6FB0" stroke="{K}" stroke-width="3" paint-order="stroke">SQUAWK!</text></svg>
  <svg style="position: absolute; left: 548px; top: 168px" width="170" height="110" viewBox="0 0 170 110" aria-hidden="true"><path d="M50 84L30 108L84 90Z" fill="#FFFFFF" stroke="{K}" stroke-width="5" stroke-linejoin="round"></path><ellipse cx="86" cy="48" rx="78" ry="40" fill="#FFFFFF" stroke="{K}" stroke-width="5"></ellipse><path d="M52 82L82 90" stroke="#FFFFFF" stroke-width="7"></path><text x="86" y="62" text-anchor="middle" font-family="Bangers, Impact, sans-serif" font-size="40" letter-spacing="2" fill="{K}">WHOA!!</text></svg>
  </div>
'''
right=f'''  <div style="position: absolute; left: 812px; top: 70px; width: 430px; display: flex; flex-direction: column; align-items: center">
    <div style="width: 100%; box-sizing: border-box; background: #141414; border: 6px solid {K}; outline: 4px solid #FFFFFF; border-radius: 22px; padding: 18px 22px; display: flex; align-items: center; gap: 18px; box-shadow: 14px 14px 0 {K}; transform: rotate(2deg)">
      <div style="display: flex; flex-direction: column; gap: 8px"><span style="width: 32px; height: 32px; border-radius: 50%; background: #2B2B2B"></span><span class="lampA" style="width: 32px; height: 32px; border-radius: 50%; background: #FFB020; box-shadow: 0 0 18px #FFB020"></span><span style="width: 32px; height: 32px; border-radius: 50%; background: #2B2B2B"></span></div>
      <div style="display: flex; flex-direction: column">
        <span style="{BANG}; font-size: 68px; line-height: 0.95; letter-spacing: 2px; color: #FFD23F; -webkit-text-stroke: 2px {K}; text-shadow: 5px 5px 0 #E8261E; white-space: nowrap">DONATE MORE</span>
        <span style="{BANG}; font-size: 68px; line-height: 0.95; letter-spacing: 2px; color: #FFFFFF; -webkit-text-stroke: 2px {K}; text-shadow: 5px 5px 0 #E8261E; white-space: nowrap">PLAY MORE</span>
      </div>
    </div>
    <div style="margin-top: 40px; width: 400px; box-sizing: border-box; background: #FFFFFF; color: {K}; border: 5px solid {K}; border-radius: 12px; padding: 16px 20px; box-shadow: 9px 9px 0 {K}; transform: rotate(-1deg); display: flex; flex-direction: column; gap: 6px">
      <span style="{BANG}; font-size: 28px; line-height: 1.05; letter-spacing: 1px; color: #3E6FB0">WANT TO PLAY IN THE ASIAN DISTRICT?</span>
      <span style="font-weight: 700; font-size: 17px; line-height: 1.4">The next block is still being built.<br>Help the rat get past Uncle and his broom!</span>
    </div>
    <nav style="margin-top: 44px; width: 380px; display: flex; flex-direction: column; align-items: center; gap: 28px" aria-label="Donate or go home">
      <a href="https://example.com/contact" target="_blank" rel="noopener" style="width: 380px; height: 84px; box-sizing: border-box; border: 5px solid {K}; border-radius: 10px; background: #FFD23F; color: {K}; display: flex; align-items: center; justify-content: center; gap: 14px; {BANG}; font-size: 54px; letter-spacing: 4px; white-space: nowrap; box-shadow: 9px 9px 0 {K}; transform: rotate(-1.5deg)">
        <svg width="40" height="36" viewBox="0 0 24 22" aria-hidden="true"><path d="M12 21s-8-5-10.5-10A5.8 5.8 0 0 1 12 4.6 5.8 5.8 0 0 1 22.5 11C20 16 12 21 12 21z" fill="#E8261E" stroke="{K}" stroke-width="2.2"></path></svg>DONATE</a>
      <a href="Start.dc.html" style="width: 250px; height: 62px; box-sizing: border-box; border: 5px solid {K}; border-radius: 10px; background: #FFFFFF; color: {K}; display: flex; align-items: center; justify-content: center; {BANG}; font-size: 38px; letter-spacing: 3px; box-shadow: 8px 8px 0 {K}; transform: rotate(1deg)">HOME</a>
    </nav>
  </div>
'''
page=head+'''<div style="width: 1280px; height: 720px; position: relative; overflow: hidden; background: #0E2350; font-family: 'Inter', sans-serif; color: #FFFFFF">

'''+bg+panel+right+'''
</div>
'''+tail
open(D+'Donate.dc.html','w').write(page)
ff='<style>@font-face{font-family:Bangers;src:url(fonts/node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}</style>'
b=page[page.index('<div style="width: 1280px'):page.index('</x-dc>')]
h=page[page.index('<link href'):page.index('</style>')+8]
open('/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/Donate_prev.html','w').write('<html><head>'+ff+h+'</head><body style=margin:0>'+b+'</body></html>')
print('ok')
