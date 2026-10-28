import json, bisect, os, random, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W='/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/video2'
A='/tmp/claude-0/-home-claude/9bec4bfc-44f2-5fc1-8bab-6a6c1cc3b203/scratchpad/audio/'
d=json.load(open('/mnt/user-data/uploads/NYCrossing/_dump/demo_log3.txt'))
sh=d['shots']; ev=d['events']
avail=sorted(int(f[1:6]) for f in os.listdir(W+'/src') if f.endswith('.jpg'))
at=[sh[i] for i in avail]
def frame_at(vt):
    k=bisect.bisect_right(at, vt)-1
    return avail[max(0,k)]
F=ImageFont.truetype(W+'/Bangers.ttf', 46); FB=ImageFont.truetype(W+'/Bangers.ttf', 120); FS=ImageFont.truetype(W+'/Bangers.ttf', 40)
# segments: (vt0, vt1, speed, caption, badge)
SEG=[(0.3,2.3,1,'',''),
     (2.6,6.6,2,'ROUND 1',''),
     (14.0,16.0,1,'ROUND 1',''),
     (163.7,167.2,1.4,'ROUND 1 · OUT OF LIVES',''),
     (167.3,169.7,1,'',''),
     (170.3,176.0,2,'ROUND 2 · DELIVER ALL 5',''),
     (176.0,212.0,7,'ROUND 2 · DELIVER ALL 5','FAST FORWARD x7'),
     (212.0,217.6,2,'LAST DELIVERY!',''),
     (217.65,220.25,1,'',''),
     (220.75,223.35,1,'DONATE PAGE',''),
     (223.75,225.4,1,'BACK TO MENU  >  EXIT','')]
FPS=30
frames=[]; tmap=[]   # (video_t, vt)
t=0.0
for a,b,sp,cap,badge in SEG:
    n=int(round((b-a)/sp*FPS))
    for k in range(n):
        vt=a+k*sp/FPS
        frames.append((frame_at(vt),cap,badge,vt,sp)); tmap.append((len(frames)/FPS, vt, sp))
def caption(im, cap, badge):
    dr=ImageDraw.Draw(im)
    if cap:
        w=dr.textlength(cap,font=F); x=(1280-w)/2; y=618
        dr.rounded_rectangle((x-22,y-6,x+w+22,y+54),12,fill=(28,27,34))
        dr.text((x,y),cap,font=F,fill=(245,197,24))
    if badge:
        w=dr.textlength(badge,font=FS); x=1280-w-40; y=96
        dr.rounded_rectangle((x-16,y-6,x+w+16,y+48),10,fill=(215,67,43))
        dr.text((x,y),badge,font=FS,fill=(246,240,225))
os.makedirs(W+'/out',exist_ok=True)
for i,(fi,cap,badge,vt,sp) in enumerate(frames):
    im=Image.open(W+'/src/f%05d.jpg'%fi).convert('RGB')
    caption(im,cap,badge)
    im.save(W+'/out/o%05d.jpg'%i,quality=92)
n0=len(frames)
# end card 1.4s
last=Image.open(W+'/out/o%05d.jpg'%(n0-1))
for k in range(int(1.4*FPS)):
    a=min(1,k/10)
    bg=Image.blend(last, Image.new('RGB',(1280,720),(28,27,34)), a)
    dr=ImageDraw.Draw(bg)
    if k>=8:
        t1='PIGEON & RAT'; w=dr.textlength(t1,font=FB)
        dr.text(((1280-w)/2+6,236),t1,font=FB,fill=(215,67,43)); dr.text(((1280-w)/2,230),t1,font=FB,fill=(246,240,225))
        t2='FREE WINDOWS DOWNLOAD ON GITHUB'; w=dr.textlength(t2,font=F); dr.text(((1280-w)/2,390),t2,font=F,fill=(245,197,24))
        t3='github.com/yche1364-YJ/game-Pigeon-and-Rat-UE'; w=dr.textlength(t3,font=FS); dr.text(((1280-w)/2,460),t3,font=FS,fill=(207,200,184))
    bg.save(W+'/out/o%05d.jpg'%(n0+k),quality=92)
total=(n0+int(1.4*FPS))/FPS
print('frames',n0,'total',total)
# ---- audio
def rd(p):
    w=wave.open(p); sr=w.getframerate(); ch=w.getnchannels()
    x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    x=x.reshape(-1,ch)
    if ch==1: x=np.repeat(x,2,axis=1)
    return x,sr
amb,sr=rd(A+'S_Ambience.wav'); sq,_=rd(A+'S_Squeak.wav'); lose,_=rd(A+'S_Lose.wav'); win,_=rd(A+'S_Win.wav')
N=int(total*sr); out=np.zeros((N,2),np.float32)
out+=np.tile(amb,(N//len(amb)+1,1))[:N]*0.5
def vt2t(v):
    # first output time whose vt passes v
    for i,(fi,cap,badge,vt,sp) in enumerate(frames):
        if vt>=v and vt-v < sp/FPS*1.01: return i/FPS
    return None
def add(x,t,g):
    a=int(t*sr); b=min(N,a+len(x)); out[a:b]+=x[:b-a]*g
random.seed(5)
for name,v in ev:
    if name=='hop':
        t=vt2t(v)
        if t is None: continue
        sp=[f[4] for f in frames][int(t*FPS)]
        if sp>2 and random.random()>0.35: continue
        p=random.uniform(0.92,1.12); s=sq[np.arange(0,len(sq)-1,p).astype(int)]
        add(s,t,0.7 if sp<=2 else 0.4)
for name,v in ev:
    if name=='state3':
        t=vt2t(v-0.01) or vt2t(167.3); add(lose,t,0.9)
    if name=='state4':
        t=vt2t(217.65); add(win,t,0.9)
f=int(0.8*sr); out[-f:]*=np.linspace(1,0,f)[:,None]
out=np.clip(out,-1,1)
w=wave.open(W+'/mix.wav','w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
