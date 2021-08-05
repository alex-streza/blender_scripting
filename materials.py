import bpy

material_name = "Ice Shelf Sharp"

for o in bpy.data.objects:
    if o.name.startswith("MetaBallObj"):
      print(o.name)
      o.select_set(True)
      if material_name in o.data.materials:
        continue

      material = bpy.data.materials.get(material_name)

      o.data.materials.append(material)