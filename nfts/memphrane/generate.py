import bpy
import random
import time
import json

render_path = 'C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane/renders/'
nft_count = 1
nfts = []

objects = bpy.context.scene.objects

for obj in objects:
    obj.select_set(obj.type == "MESH")

materials = [elem for elem in bpy.data.materials]

for nft_index in range(nft_count):
  skin = { "name": random.choice(materials), }
  active_material = skin.name
  materials.remove(active_material)

  for obj in bpy.context.selected_objects:
      if obj.name == 'Model':
          obj.active_material = active_material

  nft = {
    "dna": active_material.name,
    "name": "#" + str(nft_index + 1),
    "description": "This is an NFT made by the coolest generative code.",
    "image": "https://memphrane/nft/" + str(nft_index + 1),
    "date": str(time.time()),
    "attributes": []
  }
  nfts.append(nft)

  with open(render_path + str(nft_index + 1) + '.json', 'w') as fp:
    json.dump(nft, fp)

  bpy.context.scene.render.filepath = render_path + active_material.name
  bpy.ops.render.render(write_still=True)

with open(render_path + 'metadata.json', 'w') as fp:
    json.dump(nfts, fp)
