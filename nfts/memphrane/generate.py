import sys
sys.path += ["C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane/assets/scripts"]

import config
import bpy
from random import random, choice
import time
import json
import math

render_path = config.render_path
edition_size = config.edition_size
edition = str(config.edition_dna_prefix)
variations = config.variations
rarity_weights = config.rarity_weights
base_image_uri = config.base_image_uri

objects = bpy.context.scene.objects
materials = [elem for elem in bpy.data.materials]

def select_all_objects():
  for obj in objects:
    obj.select_set(True)

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

def generate_nfts():
  select_all_objects()
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

    # load a random material
    # active_material = choice(materials)
    # materials.remove(active_material)

    # for obj in bpy.context.selected_objects:
    #     if obj.name == 'Model':
    #         obj.active_material = active_material

    # # set random light color


    # # load random background

    # nft_no = str(nft_index + 1)
    # nft_meta = generate_metadata(dna, edition, attributes)
    # nfts_meta.append(nft_meta)

    # save_metadata_single_file(nft_meta, nft_no)

    # bpy.context.scene.render.filepath = render_path + active_material.name
    # bpy.ops.render.render(write_still=True)

  save_metadata(nfts_meta)

generate_nfts()