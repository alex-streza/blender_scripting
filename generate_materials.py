import bpy
import random

render_path = 'C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane/renders/'

objects = bpy.context.scene.objects

for obj in objects:
    obj.select_set(obj.type == "MESH")

materials = [elem for elem in bpy.data.materials]

for obj in bpy.context.selected_objects:
    active_material = random.choice(materials)
    obj.active_material = active_material
    materials.remove(active_material)

bpy.context.scene.render.filepath = render_path + active_material.name
bpy.ops.render.render(write_still=True)
