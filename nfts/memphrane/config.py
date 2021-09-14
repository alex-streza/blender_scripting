import os


base_dir = 'C:/Users/astre/OneDrive/1_year_of_blender/september 2021/Memprhrane'
output_path = base_dir + '/output/'
assets_dir = base_dir + '/assets/'
blend_file_path = base_dir + '/GenerateMaterial.blend'
description = 'Humanoidz rule.'
base_image_uri = 'https://memphrane/nft/'
edition_dna_prefix = 0
edition_starts_at = 1
edition_ends_at = 10
edition_size = 10

def add_rarity (_id, _from, _to):
  rarity_weight = {
    'value': _id,
    'from': _from,
    'to': _to,
  }
  return rarity_weight

def clean_name (_str):
  name = _str[:-4];
  return name

def get_file_elements(_path, _rarity):
  path = _path + '/' + _rarity
  entries = os.listdir(path)
  elements = []
  for file_name in entries:
    elements.append({
      'name': clean_name(file_name),
      'value': path + '/' + file_name
    })
  return elements

def get_model_elements(_path, _rarity):
  return [{"value": "thin", "name": "Humanoid1"}]

def get_light_elements(_path, _rarity):
  light_variations = {
    'common': [
      {
        'id': '0/0',
        'value': '#ffffff',
        'weight': 50,
      },
      {
        'id': '1/0',
        'value': '##EABFCB',
        'weight': 15,
      },
      {
        'id': '2/0',
        'value': '#D9D9D9',
        'weight': 35,
      }
    ],
    'rare': [
      {
        'id': '0/0',
        'value': '#3C6E71',
        'weight': 50,
      },
      {
        'id': '1/0',
        'value': '#284B63',
        'weight': 50,
      }
    ],
    'super_rare': [{
      'id': '0/0',
      'value': '##AFC2D5',
      'weight': 100,
    }],
    'legendary': [
      {
        'id': '0/0',
        'value': '#7D2E68',
        'weight': 25,
      },
      {
        'id': '1/0',
        'value': '#251351',
        'weight': 25,
      },
      {
        'id': '2/0',
        'value': '#DE3C4B',
        'weight': 25,
      },
      {
        'id': '3/0',
        'value': '#2BC016',
        'weight': 25,
      }
    ],
  }
  return light_variations[_rarity]

def get_elements (_path, _rarity, _variation_type):
  switcher = {
    'image': get_file_elements,
    'hdri': get_file_elements,
    'model': get_model_elements,
    'light': get_light_elements,
  }

  return switcher.get(_variation_type)(_path, _rarity)

def add_variation (_variation_id, _variation_type):
  if not _variation_id:
    print('error adding variation, parameters id required')

  elements = {}

  for i in range(len(rarity_weights)):
    rarity = rarity_weights[i]['value']
    elements_for_rarity = get_elements(assets_dir + _variation_id, rarity, _variation_type)

    for j in range(len(elements_for_rarity)):
      id = str(edition_dna_prefix) + '/'+ str(j)
      if _variation_type != 'light':
        elements_for_rarity[j].update({'id': id, 'weight': 100})

    elements[rarity] = elements_for_rarity

  elements_for_variation = {
    'id': _variation_id,
    'elements': elements,
  }
  return elements_for_variation

##############
# BEGIN CONFIG
##############
rarity_weights = [
  add_rarity('legendary', 1, 1),
  add_rarity('super_rare', 2, 3),
  add_rarity('rare', 4, 6),
  add_rarity('common', 7, edition_ends_at)
]

variations = [
  add_variation('skin', 'image'),
  add_variation('eye', 'image'),
  add_variation('background', 'hdri'),
  add_variation('body', 'model'),
  add_variation('light', 'light'),
]