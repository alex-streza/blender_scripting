import sys
sys.path += ["C:/Users/astre/Blockchain/generative_art/nfts/memphrane/"]

import config
import bpy
from random import random, choice
import time
import json
import math
import shutil

render_path = config.render_path
blend_file_path = config.blend_file_path
edition_size = config.edition_size
base_dir = config.base_dir
edition = str(config.edition_dna_prefix)
variations = config.variations
rarity_weights = config.rarity_weights
base_image_uri = config.base_image_uri

objects = bpy.context.scene.objects
materials = [elem for elem in bpy.data.materials]

def select_object_by_name(_name = 'Model'):
  for obj in objects:
    obj.select_set(obj.name == _name)

def is_dna_unique(_dna_list = [], _dna = []):
	found_dna = any(''.join(elem) == ''.join(_dna) for elem in _dna_list)
	return (len(found_dna) == 0)

def get_random_rarity(_rarity_options):
	random_percent = random() * 100
	percent_count = 0

	for i in range(len(_rarity_options)):
		percent_count += _rarity_options[i].percent
		if percent_count >= random_percent:
			print('use random rarity' +  _rarity_options[i].id)
			return _rarity_options[i].id
	return _rarity_options[0].id

def get_rarity(_edition_count):
  rarity_for_edition = []
  if len(rarity_for_edition) == 0:
    for rarity_weight in rarity_weights:
      for i in range(rarity_weight['from'], rarity_weight['to']):
        rarity_for_edition.append(rarity_weight['value'])

  return rarity_for_edition[edition_size - _edition_count]

def create_dna(_variations, _rarity):
  rand_nums = []
  rarity_weight = any(elem['value'] == _rarity for elem in rarity_weights)[0]

  for variation in _variations:
    print(variation)
    num = math.floor(random() * len(variation['element_ids_for_rarity'][_rarity]))

    if rarity_weight and rarity_weight['variation_percent'][variation.id]:
      rarity_for_layer = get_random_rarity(rarity_weight['variation_percent'][variation.id])
      num = math.floor(random() * len(variation['element_ids_for_rarity'][rarity_for_layer]))
      rand_nums.append(variation['element_ids_for_rarity'][rarity_for_layer][num])
    else:
      rand_nums.append(variation['element_ids_for_rarity'][_rarity][num])

  return rand_nums

def save_metadata_single_file(_nft, _nft_no):
  with open(render_path + _nft_no + '.json', 'w') as fp:
    json.dump(_nft, fp)

def save_metadata(_nfts):
  with open(render_path + 'metadata.json', 'w') as fp:
    json.dump(_nfts, fp)

def generate_metadata(_dna, _edition, _attributes ):
  date_time = str(time.time())
  temp_metadata = {
    "dna": _dna,
    "name": "#" + _edition,
    "description": "This is an NFT made by the coolest generative code.",
    "image": base_image_uri + _edition,
    "date": date_time,
    "attributes": _attributes
  }
  return temp_metadata

def construct_layer_to_dna(_new_dna, _variations, _rarity):
  print("- construct layer to dna")
  results = {}
  for variation in _variations:
    print(variation)

  return results

# load and set hdri from path
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
  link = links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
  link = links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

def hex_to_rgb(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) / 255.0 for n in (r, g, b)]
    return (r, g, b)

def update_light_color(_color = '#ffffff'):
  select_object_by_name('Light')
  for obj in bpy.context.selected_objects:
    print(hex_to_rgb(_color))
    obj.data.color = hex_to_rgb(_color)

def load_material(_path, _name, _object_name = 'Model'):
  select_object_by_name(_object_name)

  with bpy.data.libraries.load(_path, link=False) as (data_from, data_to):
    data_to.materials = data_from.materials

    active_material = bpy.data.materials.get(_name)

    for obj in bpy.context.selected_objects:
      obj.active_material = active_material


def generate_nfts():
  select_object_by_name('Model')
  # holds which dna has already been used during generation
  dna_list_by_rarity = {}
  # holds metadata for all NFTs
  nfts_meta = []

  # prepare dna_list object
  for rarity_weight in rarity_weights:
    dna_list_by_rarity[rarity_weight['value']] = []

  for nft_index in range(edition_size):
    dna = 0
    attributes = []

    print("-----------------")
    print("creating NFT %d of %d", nft_index, edition)

		# get rarity from to config to create NFT as
    rarity = get_rarity(nft_index)
    print("- rarity: " + rarity)

    # calculate the NFT dna by getting a random part for each layer/feature
		# based on the ones available for the given rarity to use during generation
    new_dna = create_dna(variations, rarity)
    while not is_dna_unique(dna_list_by_rarity[rarity], new_dna):
			# recalculate dna as this has been used before.
      print("found duplicate DNA " + "-".join(new_dna) + ", recalculate...")
      new_dna = create_dna(variations, rarity)

    print("- dna: " + "-".join(new_dna))

		# propagate information about  required layer contained within config into a mapping object
    results = construct_layer_to_dna(new_dna, variations, rarity)

    # load a random body

    # # load a random material
    # load_material('C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane/assets/skin/legendary/galaxy/galaxy.blend', 'Galaxy')

    # # set random light color
    # update_light_color("#251351")

    # # load random background
    # load_hdri('C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane/assets/background/legendary/outer_space_1/outer_space_2_8k.exr')

    # nft_no = str(nft_index + 1)
    # nft_meta = generate_metadata(dna, edition, attributes)
    # nfts_meta.append(nft_meta)

    # save_metadata_single_file(nft_meta, nft_no)

    # bpy.context.scene.render.filepath = render_path + active_material.name
    # bpy.ops.render.render(write_still=True)

    # generate blend file copy
    # shutil.copyfile(blend_file_path, base_dir + '/' + nft_no +'.blend')


  save_metadata(nfts_meta)

# generate_nfts()