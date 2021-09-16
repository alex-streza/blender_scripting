import sys
sys.path += ['C:/Users/astre/Blockchain/generative_art/nfts/memphrane/']
sys.path += ['C:/Users/astre/AppData/Roaming/Python/Python39/site-packages']

import os
import config
import bpy
from random import random
from time import sleep
import time
import json
import math
import shutil
import pip
pip.main(['install', 'pillow', '--user'])

from PIL import Image, ImageFont, ImageDraw

output_path = config.output_path
blend_file_path = config.blend_file_path
assets_dir = config.assets_dir
edition_size = config.edition_size
edition_starts_at = config.edition_starts_at
edition_ends_at = config.edition_ends_at
base_dir = config.base_dir
edition = str(config.edition_dna_prefix)
variations = config.variations
rarity_weights = config.rarity_weights
base_image_uri = config.base_image_uri

objects = bpy.context.scene.objects

def select_object_by_name(_name = 'Model1'):
  for obj in objects:
    obj.select_set(obj.name == _name)

def is_dna_unique(_dna_list = [], _dna = []):
	found_dna = any( dna1 ==  dna2 for dna1 in _dna_list for dna2 in _dna)
	return found_dna == 0

def get_rarity(_nft_index):
  rarity = 'Unknown'
  for rarity_weight in rarity_weights:
    if _nft_index >= rarity_weight['from'] and _nft_index <= rarity_weight['to']:
      rarity = rarity_weight['value']

  return rarity

def create_dna(_variations, _rarity):
  rand_nums = []

  for variation in _variations:
    random_num = math.floor(random() * 100)
    num = 0
    for element in variation['elements'][_rarity]:
      if random_num >= 100 - element['weight']:
        num = element['id']

    rand_nums.append(num)

  return rand_nums

def save_metadata_single_file(_nft, _nft_no):
  with open(output_path + _nft_no + '.json', 'w') as fp:
    json.dump(_nft, fp)

def save_metadata(_nfts):
  with open(output_path + 'metadata.json', 'w') as fp:
    json.dump(_nfts, fp)

def generate_metadata(_dna, _nft_no, _attributes ):
  date_time = str(time.time())
  temp_metadata = {
    'dna': _dna,
    'name': '#' + _nft_no,
    'description': 'This is an NFT made by the coolest generative code.',
    'image': base_image_uri + _nft_no,
    'date': date_time,
    'attributes': _attributes
  }
  return temp_metadata

def load_hdri(_path):
  # Get the environment node tree of the current scene
  node_tree = bpy.context.scene.world.node_tree
  tree_nodes = node_tree.nodes

  # Clear all nodes
  tree_nodes.clear()

  # Add Background node
  node_background = tree_nodes.new(type='ShaderNodeBackground')

  # Add Environment Texture node
  node_environment = tree_nodes.new('ShaderNodeTexEnvironment')
  # Load and assign the image to the node property
  node_environment.image = bpy.data.images.load(_path) # Relative path
  node_environment.location = -300,0

  # Add Output node
  node_output = tree_nodes.new(type='ShaderNodeOutputWorld')
  node_output.location = 200,0

  # Link all nodes
  links = node_tree.links
  link = links.new(node_environment.outputs['Color'], node_background.inputs['Color'])
  link = links.new(node_background.outputs['Background'], node_output.inputs['Surface'])

def hex_to_rgb(colorstring):
    ''' convert #RRGGBB to an (R, G, B) tuple '''
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError('input #%s is not in #RRGGBB format' % colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) / 255.0 for n in (r, g, b)]
    return (r, g, b)

def update_light_color(_color = '#ffffff'):
  select_object_by_name('Light')
  for obj in bpy.context.selected_objects:
    obj.data.color = hex_to_rgb(_color)

def load_material(_path, _object_name):
  select_object_by_name(_object_name)

  with bpy.data.libraries.load(_path, link=False) as (data_from, data_to):
    data_to.materials = data_from.materials
    active_material = bpy.data.materials.get(data_from.materials[0])

    sleep(5)

    for obj in bpy.context.selected_objects:
      obj.active_material = active_material

def load_model(_model):
  model = bpy.data.objects[_model]
  model.location = [0, 0, 0]

  return model

def sign_nft(_path, _nft_no):
  nft_image = Image.open(_path)
  font = ImageFont.truetype('./Geometria-Bold.ttf', 120)
  image_editable = ImageDraw.Draw(nft_image)
  image_editable.text((40, 40), "#" + _nft_no, (255, 255, 255), font=font)
  nft_image.save(_path)

def render_nft(_nft_no):
  bpy.context.scene.render.filepath = output_path + _nft_no
  bpy.ops.render.render(write_still=True)

def generate_nft(_new_dna, _rarity, _variations, _nft_index):
  # load a random body
  model_name = _variations[3]['elements'][_rarity][_new_dna[3]]['value']
  model = load_model(model_name)

  # load a random skin material
  load_material(_variations[0]['elements'][_rarity][_new_dna[0]]['value'], model_name)

  # set random light color
  update_light_color(_variations[4]['elements'][_rarity][_new_dna[4]]['value'])

  # # load random background
  load_hdri(_variations[2]['elements'][_rarity][_new_dna[2]]['value'])

  nft_no = str(_nft_index + 1)

  nft_meta = generate_metadata(_new_dna, nft_no, {})

  save_metadata_single_file(nft_meta, nft_no)

  render_nft(nft_no)

  model.location = [20, 0, 0]

  # shutil.copyfile(blend_file_path, output_path + '/' + nft_no +'.blend')

  return nft_meta

def generate_nfts():
  dna_list_by_rarity = {}
  nfts_meta = []

  for rarity_weight in rarity_weights:
    dna_list = []

  for nft_index in range(edition_size):
    nft_no = str(nft_index + 1)
    print('-----------------')
    print('creating NFT ' +  nft_no + ' of ' + str(edition_size))

    rarity = get_rarity(nft_index + 1)
    print('- rarity: ' + rarity)

    new_dna = create_dna(variations, rarity)

    if is_dna_unique(dna_list, new_dna):

      print('- dna: ' + '-'.join(str(elem) for elem in new_dna))

      dna_list.append(new_dna)

      nfts_meta.append(generate_nft(new_dna, rarity, variations, nft_index))

      sign_nft(output_path + nft_no + '.png', nft_no)

    else: print('DNA exists!')

  save_metadata(nfts_meta)

generate_nfts()
