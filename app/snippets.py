from django.core import serializers
from django.core.exceptions import ValidationError
import re
import json

# Serializador de Models
def serializer(queryset):
  dataset = json.loads(serializers.serialize("json",queryset))
  items = []
  for item in dataset:
    obj = item['fields']
    obj['id'] = item['pk']
    items.append(obj)
  if len(items)==1:
    return items[0]
  else:
    return items

def validates_model(fields,model):
  try:
    excludes = fields['exclude'] if 'exclude' in fields.keys() else []
    fields.pop('exclude',None)
    valid = model(**fields)
    valid.full_clean(exclude=excludes)
  except ValidationError as e:
    return e.message_dict

def to_snake_case(word):
  return re.sub(r'(?<!^)(?=[A-Z])', '_', word).lower()
    
def filter_keys(d,keys,mode='in'):
  if mode=='in':
    return {k:v for k,v in d.items() if k in keys}
  else:
    return {k:v for k,v in d.items() if not(k in keys)}


