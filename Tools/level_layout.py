import unreal, math, json
EL = unreal.EditorLevelLibrary
log = []
actors = EL.get_all_level_actors()
def lab(a): return a.get_actor_label()
CUBE = unreal.load_asset('/Engine/BasicShapes/Cube.Cube')
CYL = unreal.load_asset('/Engine/BasicShapes/Cylinder.Cylinder')
M = {n: unreal.load_asset('/Game/NYCrossing/Materials/' + n) for n in ['MI_Orange','MI_Green','MI_Dark','MI_Ivory','MI_Blue','MI_Brick','MI_Concrete']}

def smesh(label, mesh, mat, loc, scale, yaw=0.0, folder='NYCrossing/Props'):
    a = EL.spawn_actor_from_object(mesh, unreal.Vector(*loc), unreal.Rotator(0, 0, yaw))
    a.set_actor_scale3d(unreal.Vector(*scale))
    a.static_mesh_component.set_material(0, M[mat])
    a.set_actor_label(label)
    a.set_folder_path(folder)
    return a

# ---- 0. clean previous run
for a in actors:
    if str(a.get_folder_path()) in ('NYCrossing/Props', 'NYCrossing/Markings/Extra'):
        a.destroy_actor()
actors = EL.get_all_level_actors()

# ---- 1. extra crosswalks at x = -1500, +1500
for cx in (-1500, 1500):
    for i in range(21):
        y = -1530 + 150 * i
        if y > 1470: break
        a = EL.spawn_actor_from_object(CUBE, unreal.Vector(cx, y, 2), unreal.Rotator(0, 0, 0))
        a.set_actor_scale3d(unreal.Vector(5.5, 0.8, 0.03))
        a.static_mesh_component.set_material(0, M['MI_Ivory'])
        a.set_actor_label('Crosswalk_X%d' % cx)
        a.set_folder_path('NYCrossing/Markings/Extra')
# hide lane dashes that overlap new crosswalks
for a in actors:
    if lab(a).startswith('LaneDash'):
        x = a.get_actor_location().x
        if any(abs(x - cx) < 400 for cx in (-1500, 1500)):
            a.set_actor_hidden_in_game(True); a.set_is_temporarily_hidden_in_editor(True)
            a.static_mesh_component.set_visibility(False)

# ---- 2. static benches: delete far side, scatter near side
for a in actors:
    l = lab(a)
    if l.startswith('Bench_') and a.get_actor_location().y > 0:
        a.destroy_actor()
actors = EL.get_all_level_actors()
def place_group(sgn, cx, ncx, ny_off, yaw):
    r = math.radians(yaw)
    parts = [a for a in actors if lab(a).startswith('Bench_') and a.get_actor_location().y < 0 and (a.get_actor_location().x > 0) == (sgn > 0)]
    legs = sorted([a for a in parts if lab(a).startswith('Bench_Leg')], key=lambda a: a.get_actor_location().x)
    orig = []
    for a in parts:
        l = lab(a)
        if l.startswith('Bench_Seat'): orig.append((a, cx, -2010, 55))
        elif l.startswith('Bench_Back'): orig.append((a, cx, -2040, 87))
    for i, a in enumerate(legs): orig.append((a, cx - 70 + 140 * i, -2010, 27))
    for a, ox, oy, oz in orig:
        dx, dy = ox - cx, oy - (-2010)
        nx = ncx + dx * math.cos(r) - dy * math.sin(r)
        ny = -2010 + ny_off + dx * math.sin(r) + dy * math.cos(r)
        a.set_actor_location(unreal.Vector(nx, ny, oz), False, False)
        a.set_actor_rotation(unreal.Rotator(0, 0, yaw), False)
    log.append(['benchgroup', sgn, len(parts)])
place_group(-1, -1300, -1150, -60, 7)
place_group(1, 1500, 1700, -110, -6)

# ---- 3. props
def crate(x, y, h=60, yaw=0, stack=False, label='Crate'):
    smesh(label, CUBE, 'MI_Orange', (x, y, 10 + h / 2), (0.7, 0.7, h / 100), yaw)
    smesh(label + '_Tape', CUBE, 'MI_Ivory', (x, y, 10 + h + 0.5), (0.72, 0.12, 0.01), yaw)
    top = 10 + h
    if stack:
        smesh(label + '_Top', CUBE, 'MI_Orange', (x + 6, y - 4, top + 30), (0.6, 0.6, 0.6), yaw + 14)
        top += 60
    return top
def trash(x, y, label='TrashCan'):
    smesh(label, CYL, 'MI_Green', (x, y, 10 + 47), (0.62, 0.62, 0.94))
    smesh(label + '_Rim', CYL, 'MI_Dark', (x, y, 10 + 96), (0.68, 0.68, 0.06))
    return 10 + 99
def newsbox(x, y, yaw=0):
    smesh('NewsBox', CUBE, 'MI_Blue', (x, y, 10 + 50), (0.45, 0.42, 1.0), yaw)
    smesh('NewsBox_Top', CUBE, 'MI_Dark', (x, y, 10 + 101), (0.47, 0.44, 0.03), yaw)

# ---- 4. food pickups (type, prop, x, y, yaw)
# FoodMesh sits at z=62 above actor origin (non-hotdog)
plan = [
    (2, 'ground', -1650, 1890, 25),
    (2, 'trash',  -1350, 1990, 0),
    (4, 'crate',  -1100, 1960, 12),
    (3, 'bench',   -650, 2100, 8),
    (2, 'stack',    650, 1940, -10),
    (4, 'ground',   900, 1880, -30),
    (2, 'trash',   1350, 1990, 0),
    (3, 'crate',   1750, 2040, -8),
    (2, 'bench',  -1850, 2110, -10),
]
cls = unreal.EditorAssetLibrary.load_blueprint_class('/Game/NYCrossing/Blueprints/BP_NYC_PizzaBench')
benches = [a for a in actors if a.get_class().get_name() == 'BP_NYC_PizzaBench_C' and lab(a) != 'HotDogPickup']
names = {2: 'Pizza', 3: 'Cheesecake', 4: 'Soda'}
for i, (ft, prop, x, y, yaw) in enumerate(plan):
    if i < len(benches):
        a = benches[i]
    else:
        a = EL.spawn_actor_from_class(cls, unreal.Vector(x, y, 0), unreal.Rotator(0, 0, 0))
    if prop == 'ground': top = 10
    elif prop == 'trash': top = trash(x, y, 'TrashCan_F%d' % i)
    elif prop == 'crate': top = crate(x, y, 60, yaw, False, 'Crate_F%d' % i)
    elif prop == 'stack': top = crate(x, y, 60, yaw, True, 'Crate_F%d' % i)
    else: top = 62
    z = top - 62
    a.set_editor_property('FoodType', ft)
    a.set_editor_property('ShowBench', prop == 'bench')
    a.set_actor_location(unreal.Vector(x, y, z), False, False)
    a.set_actor_rotation(unreal.Rotator(0, 0, yaw if prop in ('bench', 'ground') else 0), False)
    a.set_actor_label('%s_%s_%d' % (names[ft], prop.capitalize(), i))
    a.set_folder_path('NYCrossing/Food')
    log.append([lab(a), ft, prop, x, y, z])

# ---- 5. decor (both sidewalks), avoids rat rows (y = +-1800)
trash(-700, -2090, 'TrashCan_D1')
crate(620, -2110, 60, 9, True, 'Crate_D1')
crate(720, -2160, 45, -15, False, 'Crate_D2')
newsbox(-1620, -2130, 4)
trash(1950, -2100, 'TrashCan_D2')
newsbox(1560, 2170, -6)
crate(-250, 2190, 50, 20, False, 'Crate_D3')
crate(1050, 2180, 40, -25, False, 'Crate_D4')
trash(250, 2180, 'TrashCan_D3')

open(unreal.Paths.project_saved_dir() + 'layout_log.json', 'w').write(json.dumps(log))
