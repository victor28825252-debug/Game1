"""Original Blender 3D props and two rendered rooms for the Godot game."""
import bpy
import math
from mathutils import Vector
from pathlib import Path

OUT = Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def mat(name, color, metal=0, rough=.55, emission=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    if emission:
        p.inputs['Emission Color'].default_value = (*color, 1)
        p.inputs['Emission Strength'].default_value = emission
    return m

slate=mat('blue slate',(.035,.08,.115)); floor=mat('weathered teal',(.07,.15,.16))
dark=mat('shadow',(.018,.033,.055)); brass=mat('warm brass',(.75,.43,.12),.65)
gold=mat('key gold',(.95,.65,.14),.65,.24); cream=mat('paper',(.88,.77,.52))
cyan=mat('glowing aqua',(.18,.78,.78),.1,.3,2.5)
amber=mat('glowing amber',(.99,.55,.16),.1,.3,3)
red=mat('quiet coral',(.59,.18,.19)); coat=mat('child raincoat',(.86,.49,.15))

def cube(name, loc, scale, material, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new('soft edges','BEVEL'); mod.width=bevel; mod.segments=2
        o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    return o

def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material)
    bpy.ops.object.shade_smooth(); return o

def cylinder(name, loc, radius, depth, material, vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(material); return o

def torus(name, loc, major, minor, material, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=loc, rotation=rotation)
    o=bpy.context.object; o.name=name; o.data.materials.append(material); return o

def light(loc, color, power, size):
    data=bpy.data.lights.new('soft area','AREA'); data.energy=power; data.color=color; data.shape='DISK'; data.size=size
    o=bpy.data.objects.new('soft area',data); bpy.context.collection.objects.link(o); o.location=loc
    o.rotation_euler=(Vector((0,0,1.4))-o.location).to_track_quat('-Z','Y').to_euler()

def camera():
    data=bpy.data.cameras.new('story camera'); o=bpy.data.objects.new('story camera',data)
    bpy.context.collection.objects.link(o); o.location=(0,-15,7.2)
    o.rotation_euler=(Vector((0,0,2.0))-o.location).to_track_quat('-Z','Y').to_euler()
    data.type='ORTHO'; data.ortho_scale=13.8; bpy.context.scene.camera=o

def room(level):
    cube('stone floor',(0,0,-.11),(15,8,.3),floor,.08)
    cube('back wall',(0,3.5,3),(15,.35,6.7),slate,.08)
    for x in (-6.4,-3.1,.2,3.5,6.5):
        cube('tall wall rib',(x,3.13,3.1),(.26,.48,6.2),dark,.04)
    for x in (-5,-2.5,0,2.5,5):
        cube('floor seam',(x,-.4,.055),(.025,6,.015),dark)
    cube('arched doorway',(4.9,3.0,2.1),(2.5,.45,4.3),brass,.16)
    cube('door inset',(4.9,2.7,2.05),(2.1,.18,3.95),dark,.13)
    for z in (1.15,2.3,3.4): cube('door crossbar',(4.9,2.5,z),(1.95,.12,.07),brass,.02)
    sphere('door knob',(5.7,2.41,2),(.13,.13,.13),gold)
    cube('puzzle desk',(-2.6,1.55,.94),(3.2,1.7,.18),brass,.08)
    for x in (-3.9,-1.3): cube('desk leg',(x,1.55,.47),(.18,.18,.95),dark,.02)
    cube('puzzle plinth',(-2.6,1.55,1.3),(1.6,.9,.62),dark,.1)
    cube('puzzle screen',(-2.6,.96,1.54),(1.28,.08,.38),cyan if level==1 else amber,.04)
    for x in (-2.9,-2.6,-2.3): sphere('console button',(x,.84,1.16),(.08,.05,.05),gold)
    for x in (-5.4,6.1):
        cylinder('hanging lantern post',(x,2.5,3.8),.05,2.8,brass)
        sphere('gentle wall lantern',(x,2.45,2.4),(.3,.2,.4),cyan if level==1 else amber)
    # Original child explorer, seen from the back: poncho, boots, and a small lamp.
    sphere('hood',(0,-1.7,1.45),(.36,.31,.39),coat)
    cube('raincoat body',(0,-1.72,.89),(.76,.45,.92),coat,.18)
    for x in (-.23,.23): cube('tiny boot',(x,-1.85,.25),(.22,.45,.45),dark,.07)
    sphere('hand lantern',(.52,-1.85,.66),(.16,.15,.22),amber)
    torus('lantern handle',(.52,-1.85,.88),.16,.025,brass,rotation=(math.pi/2,0,0))
    if level==1:
        for x in (-4.8,-4.3,-3.8):
            cylinder('savings coin',(x,1.6,.18),.27,.1,gold)
        cube('savings jar',(-4.3,1.65,.46),(1.2,.8,.42),dark,.16)
        cube('coin slot',(-4.3,1.19,.72),(.68,.04,.06),gold,.02)
    else:
        for x,col in ((-4.7,cyan),(-4.1,gold),(-3.5,red)):
            cube('three different baskets',(x,1.65,.47),(.46,.55,.5),col,.07)
        sphere('risk orb',(-.9,2.5,2),(.42,.42,.42),amber)
    # Foreground silhouettes keep the eerie picture-book atmosphere.
    for x in (-7.1,7.1):
        cube('foreground tower',(x,-2.4,2.1),(.9,1,4.5),dark,.12)
    light((-4,-4,7),(.42,.84,1),500,7)
    light((4,0,5),(1,.57,.27),380,5)
    camera()
    scene=bpy.context.scene
    scene.render.engine='CYCLES'; scene.cycles.samples=24
    scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.world.color=(.1,.1,.1)
    scene.view_settings.view_transform='AgX'
    scene.render.filepath=str(OUT / f'room_{level}.png')
    bpy.ops.render.render(write_still=True)

for i in (1,2):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    room(i)

# Export a real, reusable 3D key model as GLB.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
cylinder('key bow outer',(0,0,0),.43,.09,gold)
cylinder('key bow hole',(0,0,.055),.21,.015,dark)
cube('key shaft',(0,-.76,0),(.16,1.16,.14),gold,.04)
cube('key tooth left',(-.16,-1.24,0),(.3,.18,.14),gold,.02)
cube('key tooth right',(.15,-1.04,0),(.22,.18,.14),gold,.02)
bpy.ops.export_scene.gltf(filepath=str(OUT/'golden_key.glb'),export_format='GLB')
print('Wrote original Blender renders and GLB to',OUT)
