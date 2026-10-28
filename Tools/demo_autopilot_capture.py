import unreal, json, time, os, glob, random
random.seed(11)
for f in glob.glob(unreal.Paths.project_saved_dir()+'Screenshots/*/*.png'): os.remove(f)
W = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
GS = unreal.GameplayStatics
def allof(n): return [a for a in GS.get_all_actors_of_class(W, unreal.Actor) if a.get_class().get_name().startswith(n)]
RAT = allof('BP_NYC_Rat')[0]
SPAWNERS = allof('BP_NYC_LaneSpawner')
FOODS = allof('BP_NYC_PizzaBench')
SIG = allof('BP_NYC_Signal')[0]
SLOMO = 0.5
S = {'t0': None, 'vt': 0.0, 'last': None, 'shots': [], 'events': [], 'phase': 'menu', 'pt': 0.0,
     'prev': {}, 'done': False, 'tgt': None}
def g(n, a=None):
    try: return (a or RAT).get_editor_property(n)
    except Exception: return None
def ev(name): S['events'].append([name, round(S['vt'], 3)])
PEDS = []

def danger(x, y, horizon, cars=True):
    for p in PEDS:
        pl = p.get_actor_location()
        if abs(pl.x - x) > 95: continue
        if not g('Walking', p):
            if abs(pl.y - y) < 70: return True
            continue
        d = g('Dir', p) or 1.0
        ahead = (y - pl.y) * d      # >0: ped walking toward cell
        if -80 < ahead < 330 * horizon + 80: return True
    if not cars or abs(y) >= 1790: return False
    st = g('State', SIG); cd = g('Countdown', SIG) or 0
    soon_go = (st == 2) or (st == 1 and cd <= 2)
    for sp in SPAWNERS:
        if abs(sp.get_actor_location().y - y) > 150: continue
        d = sp.get_editor_property('Direction'); hl = sp.get_editor_property('HalfLength')
        for v in sp.get_editor_property('Vehicles'):
            if v is None: continue
            vx = v.get_actor_location().x
            u = d * (x - vx)
            vel = VEL.get(v.get_name(), 0.0)
            if abs(u) < hl + 120:
                if vel > 30 or soon_go: return True
            elif u > 0 and u < hl + 120 + max(vel, 0) * horizon + (600 * horizon if soon_go else 0):
                return True
    return False

VEL = {}; LASTX = {}
def update_vel(dtg):
    if dtg <= 0: return
    for sp in SPAWNERS:
        d = sp.get_editor_property('Direction')
        for v in sp.get_editor_property('Vehicles'):
            if v is None: continue
            n = v.get_name(); x = v.get_actor_location().x
            if n in LASTX:
                sp_ = d * (x - LASTX[n]) / dtg
                if abs(sp_) < 5000: VEL[n] = 0.6 * VEL.get(n, sp_) + 0.4 * sp_
            LASTX[n] = x

def needs():
    o = list(g('Order') or []); dn = list(g('Done') or [])
    return [o[i] for i in range(len(o)) if i < len(dn) and not dn[i]]

def pick_target(loc):
    nd = needs(); best = None
    for f in FOODS:
        if not f.get_editor_property('Available'): continue
        ft = f.get_editor_property('FoodType')
        if ft not in nd: continue
        gx = max(-2000, min(2000, round(f.get_actor_location().x / 200.0) * 200.0))
        c = abs(gx - loc.x)
        if best is None or c < best[0]: best = (c, f, gx, ft)
    return best

CW = (-1500.0, 0.0, 1500.0)
def col(tx):
    cands = [c * 200.0 for c in range(-10, 11) if min(abs(c * 200.0 - w) for w in CW) >= 400]
    return min(cands, key=lambda c: abs(c - tx))

def hop(cmd):
    RAT.call_method(cmd); ev('hop')

def act_win():
    if g('State') != 1 or g('Hopping'): return
    loc = RAT.get_actor_location(); carrying = (g('Carrying') or 0) > 0
    oncart = loc.z > 100
    if carrying:
        tx, ty, kind = -400.0, -1800.0, 'home'; S['tgt'] = None
    else:
        t = S['tgt']
        if t is None or not t[1].get_editor_property('Available'):
            t = pick_target(loc); S['tgt'] = t
        if t is None: return
        tx, ty, kind = t[2], 1800.0, ('cart' if t[3] == 1 else 'food')
    fwd = -1 if carrying else 1
    def lat(sx): return 'HopLeft' if (sx > 0) != carrying else 'HopRight'
    st = g('State', SIG); cd = g('Countdown', SIG) or 0
    walk_ok = (st == 0 and cd >= 3) or (st == 1 and cd >= 4)
    on_sw = abs(loc.y) >= 1790
    if oncart:
        if carrying: hop('HopUp')
        return
    if on_sw and abs(loc.y - ty) < 10:
        if abs(tx - loc.x) > 50:
            nx = loc.x + (200 if tx > loc.x else -200)
            if not danger(nx, loc.y, 0.5): hop(lat(1 if tx > loc.x else -1))
        elif kind == 'cart': hop('HopUp')
        return
    if on_sw:
        cx = col(tx)
        if abs(cx - loc.x) > 50:
            nx = loc.x + (200 if cx > loc.x else -200)
            if not danger(nx, loc.y, 0.5): hop(lat(1 if cx > loc.x else -1))
        elif walk_ok and not danger(loc.x, loc.y + 400 * fwd, 0.7): hop('HopUp')
        return
    ny = loc.y + 400 * fwd
    if not danger(loc.x, ny, 0.7): hop('HopUp')
    elif danger(loc.x, loc.y, 0.45):
        for side in (200, -200):
            if abs(loc.x + side) <= 2000 and not danger(loc.x + side, loc.y, 0.6):
                hop(lat(1 if side > 0 else -1)); return
        back = loc.y - 400 * fwd
        if not danger(loc.x, back, 0.6): hop('HopDown')

def act_fail():
    if g('State') != 1 or g('Hopping'): return
    st = g('State', SIG)
    loc = RAT.get_actor_location()
    if abs(loc.y) < 1790 and st != 2:
        return   # wait in the road for the traffic to start
    hop('HopUp')

def watch():
    cur = {k: g(k) for k in ('State', 'Carrying', 'Lives', 'Delivered')}
    p = S['prev']
    if p:
        if cur['Carrying'] and not p['Carrying']: ev('pickup')
        if cur['Delivered'] != p['Delivered']: ev('deliver')
        if p['Carrying'] and not cur['Carrying'] and cur['Delivered'] == p['Delivered']: ev('lostfood')
        if cur['Lives'] is not None and p['Lives'] is not None and cur['Lives'] < p['Lives']: ev('hit')
        if cur['State'] != p['State']: ev('state%d' % cur['State'])
    S['prev'] = cur

def goto(ph): S['phase'] = ph; S['pt'] = S['vt']; ev('phase_' + ph)

def finish():
    S['done'] = True
    try: unreal.unregister_slate_post_tick_callback(S['h'])
    except Exception: pass
    json.dump({'shots': S['shots'], 'events': S['events']}, open(unreal.Paths.project_saved_dir() + 'demo_log.json', 'w'))

def tick(dt):
    global PEDS
    if S['done']: return
    now = time.time()
    if S['t0'] is None:
        if dt > 0.5: return
        S['t0'] = now; S['last'] = now
    rd = now - S['last']; S['last'] = now
    playing = g('State') == 1
    S['vt'] += rd * (SLOMO if playing else 1.0)
    ph = S['phase']; el = S['vt'] - S['pt']
    try:
        if playing: GS.set_global_time_dilation(W, SLOMO)
        PEDS = allof('BP_NYC_Pedestrian')
        update_vel(rd * (SLOMO if playing else 1.0))
        watch()
        if ph == 'menu' and el > 2.5:
            RAT.call_method('StartGame'); goto('fail')
        elif ph == 'fail':
            if g('State') == 3: goto('over')
            else: act_fail()
        elif ph == 'over' and el > 3.0:
            RAT.call_method('StartGame'); goto('win')
        elif ph == 'win':
            if g('State') == 4: goto('clear')
            elif g('State') == 3: RAT.call_method('StartGame'); ev('retry2')
            else: act_win()
        elif ph == 'clear' and el > 3.0:
            RAT.call_method('NextBlock'); goto('donate')
        elif ph == 'donate' and el > 3.0:
            RAT.call_method('GoMenu'); goto('home')
        elif ph == 'home' and el > 2.0:
            goto('exit')
            unreal.SystemLibrary.execute_console_command(W, 'shot'); S['shots'].append(round(S['vt'], 3))
            finish()
            RAT.call_method('DoExit')
            return
        if S['vt'] > 2400: finish(); return
    except Exception as e:
        ev('err:' + str(e)[:100])
    unreal.SystemLibrary.execute_console_command(W, 'shot')
    S['shots'].append(round(S['vt'], 3))

S['h'] = unreal.register_slate_post_tick_callback(tick)
