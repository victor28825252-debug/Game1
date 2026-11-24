"""Render original GLB key as a small transparent Godot animation.

Adapts the installed blender-skills turntable camera rig to batch bpy because
the Blender MCP addon is unavailable in this environment.
"""
import bpy
import math
from pathlib import Path
from mathutils import Vector

HERE = Path(__file__).resolve().parent
DEST = HERE.parent / "godot" / "assets" / "key_frames"
DEST.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(HERE / "golden_key.glb"))
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
center = sum((o.matrix_world.translation for o in meshes), Vector()) / len(meshes)
center.y -= 0.45
bpy.ops.object.empty_add(type="PLAIN_AXES", location=center)
target = bpy.context.object
target.name = "TurntableTarget"
bpy.ops.object.camera_add(location=(0, -0.55, 4.1))
cam = bpy.context.object
cam.name = "TurntableCamera"
cam.data.type = "ORTHO"
cam.data.ortho_scale = 2.75
track = cam.constraints.new(type="TRACK_TO")
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
bpy.context.scene.camera = cam
world = bpy.data.worlds.new("Neutral world")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
for location, power, color, size in [
    ((2, -3, 5), 600, (1.0, 0.78, 0.45), 4),
    ((-3, 1, 4), 400, (0.6, 0.85, 1.0), 4),
]:
    bpy.ops.object.light_add(type="AREA", location=location)
    lamp = bpy.context.object
    lamp.data.energy = power
    lamp.data.color = color
    lamp.data.size = size
    lamp.rotation_euler = (center - lamp.location).to_track_quat("-Z", "Y").to_euler()
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 12
scene.render.resolution_x = 192
scene.render.resolution_y = 192
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.view_settings.view_transform = "AgX"
for frame in range(8):
    angle = math.tau * frame / 8
    cam.location = center + Vector((3.4 * math.sin(angle), -0.55, 3.4 * math.cos(angle)))
    scene.render.filepath = str(DEST / f"key_{frame:02d}.png")
    bpy.ops.render.render(write_still=True)
print(f"Wrote eight turntable frames to {DEST}")
