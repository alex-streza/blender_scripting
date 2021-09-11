import os


# adds a rarity to the configuration. This is expected to correspond with a directory containing the rarity for each defined layer
# @param _id - id of the rarity
# @param _from - number in the edition to start this rarity from
# @param _to - number in the edition to generate this rarity to
# @return a rarity object used to dynamically generate the NFTs
def add_rarity (_id, _from, _to):
  rarity_weight = {
    "value": _id,
    "from": _from,
    "to": _to,
    "layer_percent": {}
  }
  return rarity_weight

# get the name without last 4 characters -> slice .png from the name
def clean_name (_str):
  name = _str.slice(0, -4);
  return name

# reads the filenames of a given folder and returns it with its name and path
def get_elements (_path, _elementCount):
  entries = os.listdir(_path)
  elements = []
  for file_name in entries:
    elements.append({
      "id": -1,
      "name": clean_name(file_name),
      "path": _path+'/' + file_name
    })
  return elements

# generate variation used to dynamically generate the NFTs
# it will contain the path to
# @param _variation_id - name of the variation
def add_variation (_variation_id):
  if not _variation_id:
    print('error adding layer, parameters id required')

  elements = []
  element_ids_for_rarity = {}

  for i in range(len(rarity_weights)):
    rarity = rarity_weights[i].value
    elements_for_rarity = get_elements(f'{current_dir}/{_variation_id}/{rarity}')

    element_ids_for_rarity[rarity] = []
    for j in range(len(elements_for_rarity)):
      elements_for_rarity[j].id = f'{edition_dna_prefix}/j'
      elements.append(elements_for_rarity[j]);
      element_ids_for_rarity[rarity].push(elements_for_rarity[j].id);

    elements[rarity] = elements_for_rarity

  elements_for_variation = {
    'id': _variation_id,
    'elements': elements,
    'element_ids_for_rarity': element_ids_for_rarity
  }
  return elements_for_variation

# adds variation-specific percentages to use one vs another rarity
# @param _rarityId - the id of the rarity to specifiy
# @param _layerId - the id of the layer to specifiy
# @param _percentages - an object defining the rarities and the percentage with which a given rarity for this layer should be used
def add_rarity_percent_for_layer (_rarityId, _layer_id, _percentages):
  rarity_found = False

  for rarity_weight in rarity_weights:
    if rarity_weight["value"] == _rarityId:
      percent_array = []
      for percent_type in _percentages:
        percent_array.append({
          "id": percent_type,
          "percent": _percentages[percent_type]
        })
      rarity_weight.layerPercent[_layer_id] = percent_array;
      rarity_found = True

  if rarity_found == False:
    print('rarity ${_rarityId} not found, failed to add percentage information')


##############
# BEGIN CONFIG
##############

rarity_weights = [
  add_rarity('legendary', 1, 1),
  add_rarity('super_rare', 2, 3),
  add_rarity('rare', 4, 6),
  add_rarity('common', 7, 10)
]

# create required variations
# for each layer, call 'add_variation' with the id
# the id would be the name of the folder in your input directory, e.g. 'background' for ./input/background
variations = [
  add_variation('skin'),
  add_variation('eye'),
  add_variation('background'),
  add_variation('body'),
  add_variation('light'),
];

# provide any specific percentages that are required for a given variation and rarity level
# all provided options are used based on their percentage values to decide which layer to select from
add_rarity_percent_for_layer('super_rare', 'skin', { 'super_rare': 33, 'rare': 33, 'common': 33 });
add_rarity_percent_for_layer('super_rare', 'eye', { 'super_rare': 50, 'rare': 25, 'common': 25 });
add_rarity_percent_for_layer('original', 'background', { 'super_rare': 50, 'rare': 25, 'common': 25 });
add_rarity_percent_for_layer('original', 'body', { 'super_rare': 50, 'rare': 25, 'common': 25 });
add_rarity_percent_for_layer('original', 'light', { 'super_rare': 50, 'rare': 25, 'common': 25 });

base_dir = 'C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane'
current_dir = base_dir + '/input/'
render_path = base_dir + '/renders/'
description = "Humanoidz rule."
base_image_uri = "https://memphrane/nft"
edition_start = 1
edition_size = 1
edition_dna_prefix = 0
