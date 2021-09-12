import os


base_dir = 'C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane'
render_path = base_dir + '/renders/'
current_dir = base_dir + '/assets/'
description = "Humanoidz rule."
base_image_uri = "https://memphrane/nft/"
edition_dna_prefix = 0
edition_start = 1
edition_size = 1

# adds a rarity to the configuration. This is expected to correspond with a directory containing the rarity for each defined variation
# @param _id - id of the rarity
# @param _from - number in the edition to start this rarity from
# @param _to - number in the edition to generate this rarity to
# @return a rarity object used to dynamically generate the NFTs
def add_rarity (_id, _from, _to):
  rarity_weight = {
    "value": _id,
    "from": _from,
    "to": _to,
    "variation_percent": {}
  }
  return rarity_weight

# get the name without last 4 characters -> slice .png from the name
def clean_name (_str):
  name = _str[:-4];
  return name

def get_file_elements(_path, _rarity):
  path = _path + '/' + _rarity
  entries = os.listdir(path)
  elements = []
  for file_name in entries:
    elements.append({
      "name": clean_name(file_name),
      "path": path + '/' + file_name
    })
  return elements

def get_light_elements(_path, _rarity):
  light_variations = {
    "common": ["#ffffff", "#EABFCB", "#D9D9D9"],
    "rare": ["#3C6E71", "#284B63"],
    "super_rare": ["#DFEFCA", "#AFC2D5", "#CCDDD3"],
    "legendary": ["#7D2E68", "#251351 ", "#DE3C4B", "#2BC016"],
  }
  return light_variations[_rarity]

# reads the filenames of a given folder and returns it with its name and path
def get_elements (_path, _rarity, _variation_type):
  switcher = {
    "image": get_file_elements,
    "hdri": get_file_elements,
    "model": get_file_elements,
    "light": get_light_elements,
  }

  return switcher.get(_variation_type)(_path, _rarity)

# generate variation used to dynamically generate the NFTs
# it will contain the path to
# @param _variation_id - name of the variation
def add_variation (_variation_id, _variation_type):
  if not _variation_id:
    print('error adding variation, parameters id required')

  elements = {}
  element_ids_for_rarity = {}

  for i in range(len(rarity_weights)):
    rarity = rarity_weights[i]['value']
    elements_for_rarity = get_elements(current_dir + _variation_id, rarity, _variation_type)

    element_ids_for_rarity[rarity] = []
    for j in range(len(elements_for_rarity)):
      id = str(edition_dna_prefix) + "/"+ str(j)
      elements_for_rarity[j].update({'id': id})
      element_ids_for_rarity[rarity].append(id)

    elements[rarity] = elements_for_rarity

  elements_for_variation = {
    'id': _variation_id,
    'elements': elements,
    'element_ids_for_rarity': element_ids_for_rarity
  }
  return elements_for_variation

# adds variation-specific percentages to use one vs another rarity
# @param _rarityId - the id of the rarity to specifiy
# @param _variation_id - the id of the variation to specifiy
# @param _percentages - an object defining the rarities and the percentage with which a given rarity for this variation should be used
def add_rarity_percent_for_variation (_rarityId, _variation_id, _percentages):
  rarity_found = False

  for rarity_weight in rarity_weights:
    if rarity_weight["value"] == _rarityId:
      percent_array = []
      for percent_type in _percentages:
        percent_array.append({
          "id": percent_type,
          "percent": _percentages[percent_type]
        })
      rarity_weight['variation_percent'][_variation_id] = percent_array;
      rarity_found = True

  if rarity_found == False:
    print('rarity '+ _rarityId + ' not found, failed to add percentage information')


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
# for each variation, call 'add_variation' with the id
# the id would be the name of the folder in your input directory, e.g. 'background' for ./input/background
variations = [
  add_variation('skin', 'image'),
  add_variation('eye', 'image'),
  add_variation('background', 'hdri'),
  add_variation('body', 'model'),
  add_variation('light', 'light'),
]

# provide any specific percentages that are required for a given variation and rarity level
# all provided options are used based on their percentage values to decide which variation to select from
add_rarity_percent_for_variation('super_rare', 'skin', { 'legendary': 10, 'super_rare': 20, 'rare': 30, 'common': 40 })
add_rarity_percent_for_variation('super_rare', 'eye', { 'legendary': 25, 'super_rare': 25, 'rare': 25, 'common': 25 })
add_rarity_percent_for_variation('common', 'background', { 'legendary': 10, 'super_rare': 20, 'rare': 30, 'common': 40 })
add_rarity_percent_for_variation('common', 'body', { 'legendary': 25, 'super_rare': 25, 'rare': 25, 'common': 25 })
add_rarity_percent_for_variation('common', 'light', { 'legendary': 25, 'super_rare': 25, 'rare': 25, 'common': 25  })