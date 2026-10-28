import bpy, glob, sys, math, os, bmesh
from mathutils import Vector
U='/mnt/user-data/uploads/'
OUT=os.path.abspath('out')
# name: (fbx glob, normal glob, target longest size m, subdiv, max tris)
J={
 'Rat':('cartoon+mouse+3d+model/*.fbx','cartoon+mouse+3d+model/*.fbm/*normal*',0.50,2,20000),
 'Pigeon':('bird+cartoon+3d+model/*.fbx','bird+cartoon+3d+model/*.fbm/*normal*',0.45,2,20000),
 'Pizza':('pizza+slice+3d+model/*.fbx','pizza+slice+3d+model/*.fbm/*Normal*',0.30,0,12000),
 'HotDog':('hot+dog+3d+model/*.fbx','hot+dog+3d+model/*.fbm/*normal*',0.30,0,12000),
 'Soda':('red+soda+can+3d+model/*.fbx','red+soda+can+3d+model/*.fbm/*normal*',0.20,0,12000),
 'Cheesecake':('strawberry+cheesecake+3d+model/*.fbx','strawberry+cheesecake+3d+model/*.fbm/*normal*',0.24,0,12000),
}
only=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(J)
for name in only:
    fbx,nrm,size,sub,maxt=J[name]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=glob.glob(U+fbx)[0])
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    for o in bpy.context.scene.objects: o.select_set(False)
    for o in meshes: o.select_set(True)
    bpy.context.view_layer.objects.active=meshes[0]
    if len(meshes)>1: bpy.ops.object.join()
    ob=bpy.context.view_layer.objects.active
    # remove non-mesh (armatures/empties) after parenting cleared
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    for o in list(bpy.context.scene.objects):
        if o!=ob: bpy.data.objects.remove(o)
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    tris=sum(len(p.vertices)-2 for p in ob.data.polygons)
    if name=='Pizza':
        import numpy as np
        from mathutils import Matrix
        P=np.array([v.co[:] for v in ob.data.vertices]); P-=P.mean(0)
        w,V=np.linalg.eigh(np.cov(P.T)); n=Vector(V[:,0])
        if n.z<0: n=-n
        R=n.rotation_difference(Vector((0,0,1))).to_matrix().to_4x4()
        ob.data.transform(R)
    # normalize size, origin at bottom-center
    xs=[v.co for v in ob.data.vertices]
    mn=Vector((min(c.x for c in xs),min(c.y for c in xs),min(c.z for c in xs)))
    mx=Vector((max(c.x for c in xs),max(c.y for c in xs),max(c.z for c in xs)))
    dim=mx-mn; s=size/max(dim)
    ctr=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z))
    for v in ob.data.vertices: v.co=(v.co-ctr)*s*100.0
    if tris>maxt:
        m=ob.modifiers.new('dec','DECIMATE'); m.ratio=maxt/tris
        bpy.ops.object.modifier_apply(modifier='dec')
    if sub:
        m=ob.modifiers.new('sub','SUBSURF'); m.levels=sub; m.render_levels=sub; m.uv_smooth='PRESERVE_BOUNDARIES'
        bpy.ops.object.modifier_apply(modifier='sub')
    bpy.ops.object.shade_smooth()
    # material: graded base color + normal, matte
    mat=bpy.data.materials.new('M_'+name); mat.use_nodes=True
    nt=mat.node_tree; bsdf=nt.nodes.get('Principled BSDF')
    tb=nt.nodes.new('ShaderNodeTexImage'); tb.image=bpy.data.images.load(f'{OUT}/T_{name}_BaseColor.png')
    nt.links.new(tb.outputs['Color'],bsdf.inputs['Base Color'])
    nf=glob.glob(U+nrm)
    if nf:
        tn=nt.nodes.new('ShaderNodeTexImage'); tn.image=bpy.data.images.load(nf[0]); tn.image.colorspace_settings.name='Non-Color'
        nm=nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value=0.6
        nt.links.new(tn.outputs['Color'],nm.inputs['Color']); nt.links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
    bsdf.inputs['Roughness'].default_value=0.7; bsdf.inputs['Metallic'].default_value=0.0
    ob.data.materials.clear(); ob.data.materials.append(mat)
    ob.name='SM_'+name; ob.data.name='SM_'+name
    tris2=sum(len(p.vertices)-2 for p in ob.data.polygons)
    bpy.ops.export_scene.fbx(filepath=f'{OUT}/SM_{name}.fbx',use_selection=False,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',
        path_mode='COPY',embed_textures=True,mesh_smooth_type='FACE',add_leaf_bones=False,bake_anim=False,object_types={'MESH'})
    # preview render
    sc=bpy.context.scene
    cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam)
    d=size*260; cam.location=(d*0.8,-d,d*0.6)
    cam.rotation_euler=(Vector((0,0,size*30))-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.clip_end=100000; sc.camera=cam
    sun=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN')); sun.data.energy=4; sun.rotation_euler=(0.8,0.2,0.6); sc.collection.objects.link(sun)
    w=bpy.data.worlds.new('w'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs['Color'].default_value=(0.8,0.8,0.82,1); w.node_tree.nodes['Background'].inputs['Strength'].default_value=0.8; sc.world=w
    sc.render.engine='CYCLES'; sc.cycles.samples=12; sc.cycles.device='CPU'
    sc.render.resolution_x=sc.render.resolution_y=360
    sc.render.filepath=f'{OUT}/prev_{name}.png'; bpy.ops.render.render(write_still=True)
    print('DONE',name,tris,'->',tris2,'dim',[round(x*s*100,1) for x in dim])
