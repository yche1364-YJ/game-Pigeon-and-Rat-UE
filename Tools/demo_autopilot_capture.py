import unreal, json, time, os, glob
for f in glob.glob(unreal.Paths.project_saved_dir()+'Screenshots/*/*.png'): os.remove(f)
W = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
GS = unreal.GameplayStatics
ALL = GS.get_all_actors_of_class(W, unreal.Actor)
def of(n): return [a for a in ALL if a.get_class().get_name().startswith(n)]
RAT = of('BP_NYC_Rat')[0]
SPAWNERS = of('BP_NYC_LaneSpawner')
FOODS = of('BP_NYC_PizzaBench')
SLOMO = 0.35
VDUR = 31.0             # video seconds
S = {'t0': None, 'vt': 0.0, 'last_real': None, 'last_shot': -1, 'shots': [], 'events': [],
     'started': False, 'prev': {}, 'done': False, 'tgt': None}
def g(n):
    try: return RAT.get_editor_property(n)
    except Exception: return None
def ev(name): S['events'].append([name, round(S['vt'], 3)])

def peds():
    return [a for a in GS.get_all_actors_of_class(W, unreal.Actor) if a.get_class().get_name().startswith('BP_NYC_Pedestrian')]

def danger(x, y, horizon):
    for p in PEDS:
        pl = p.get_actor_location()
        if abs(pl.x - x) < 90 and abs(pl.y - y) < 230: return True
    if abs(y) >= 1790: return False
    for sp in SPAWNERS:
        if abs(sp.get_actor_location().y - y) > 150: continue
        d = sp.get_editor_property('Direction'); hl = sp.get_editor_property('HalfLength')
        f = sp.custom_time_dilation
        sps = list(sp.get_editor_property('CurSpeeds'))
        for i, v in enumerate(sp.get_editor_property('Vehicles')):
            if v is None: continue
            vx = v.get_actor_location().x
            spd = (sps[i] if i < len(sps) else 600) * f
            u = d * (x - vx)
            if -(hl + 120) < u < hl + 120 + spd * horizon: return True
    return False

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

def act():
    if g('State') != 1 or g('Hopping'): return
    loc = RAT.get_actor_location(); carrying = (g('Carrying') or 0) > 0
    oncart = loc.z > 100
    if carrying:
        tx, ty, kind = -200.0, -1800.0, 'home'; S['tgt'] = None
    else:
        t = S['tgt']
        if t is None or not t[1].get_editor_property('Available'):
            t = pick_target(loc); S['tgt'] = t
        if t is None: return
        tx, ty, kind = t[2], 1800.0, ('cart' if t[3] == 1 else 'food')
    fwd = -1 if carrying else 1
    def lat(sx):  # world dx sign -> function (HopRight moves -x when not carrying)
        return 'HopLeft' if (sx > 0) != carrying else 'HopRight'
    cmd = None
    on_sw = abs(loc.y) >= 1790
    if oncart:
        cmd = 'HopUp' if carrying else None
    elif on_sw and abs(loc.y - ty) < 10:
        if abs(tx - loc.x) > 50:
            nx = loc.x + (200 if tx > loc.x else -200)
            if not danger(nx, loc.y, 0.5): cmd = lat(1 if tx > loc.x else -1)
        elif kind == 'cart': cmd = 'HopUp'
    elif on_sw:
        if abs(tx - loc.x) > 50:
            nx = loc.x + (200 if tx > loc.x else -200)
            if not danger(nx, loc.y, 0.5): cmd = lat(1 if tx > loc.x else -1)
        elif not danger(loc.x, loc.y + 400 * fwd, 0.75): cmd = 'HopUp'
    else:
        ny = loc.y + 400 * fwd
        if not danger(loc.x, ny, 0.75): cmd = 'HopUp'
        elif danger(loc.x, loc.y, 0.45):
            back = loc.y - 400 * fwd
            if not danger(loc.x, back, 0.6): cmd = 'HopDown'
    if cmd:
        RAT.call_method(cmd); ev('hop')

def watch():
    cur = {'State': g('State'), 'Carrying': g('Carrying'), 'Lives': g('Lives'), 'Delivered': g('Delivered')}
    p = S['prev']
    if p:
        if cur['Carrying'] and not p['Carrying']: ev('pickup')
        if cur['Delivered'] != p['Delivered']: ev('deliver')
        if p['Carrying'] and not cur['Carrying'] and cur['Delivered'] == p['Delivered']: ev('lostfood')
        if cur['Lives'] < p['Lives']: ev('hit')
        if cur['State'] != p['State']: ev('state%d' % cur['State'])
    S['prev'] = cur

PEDS = []
def tick(dt):
    global PEDS
    if S['done']: return
    now = time.time()
    if S['t0'] is None:
        if dt > 0.5: return           # wait for hitch to pass
        S['t0'] = now; S['last_real'] = now
    rd = now - S['last_real']; S['last_real'] = now
    S['vt'] += rd * (SLOMO if S['started'] else 1.0)
    if S['vt'] >= VDUR:
        S['done'] = True
        unreal.unregister_slate_post_tick_callback(S['h'])
        GS.set_global_time_dilation(W, 1.0)
        json.dump({'shots': S['shots'], 'events': S['events']}, open(unreal.Paths.project_saved_dir() + 'demo_log.json', 'w'))
        return
    try:
        if not S['started'] and S['vt'] > 2.5:
            RAT.call_method('StartGame'); S['started'] = True; ev('start')
        if S['started']:
            if g('State') == 1: GS.set_global_time_dilation(W, SLOMO)
            PEDS = peds()
            watch(); act()
    except Exception as e:
        ev('err:' + str(e)[:80])
    unreal.SystemLibrary.execute_console_command(W, 'shot')
    S['shots'].append(round(S['vt'], 3))

S['h'] = unreal.register_slate_post_tick_callback(tick)
