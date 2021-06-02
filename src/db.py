# I've made this into a module with getter/setter functions so
# this can be changed into an actual DB later with less effort

from . import calculator

_data = {}

def put(key, value):
  value["id"] = key
  _data[key] = value

def get(key):
  return _data[key]

def preprocess_data(d):
  for k, row in d.items():
    yield (k, calculator.preprocess(row))

def query(**kwargs):
  d = preprocess_data(_data)
  filters = kwargs.get("filters", [])

  for f in filters:
    [field, comp, value] = f

    if comp in ("eq", "is", "==", "="):
      d = _search_eq(d, field, value)
    elif comp == ">":
      d = _search_gt(d, field, value)
    elif comp == "in":
      d = _search_in(d, field, value)
    elif comp in ("not", "not eq"):
      d = _search_not_eq(d, field, value)
    elif comp == "not in":
      d = _search_not_in(d, field, value)
    elif comp == "does not contain":
      d = _search_not_contain(d, field, value)

  return d

# def select(d, selection):
#   result = []
#   for k, row in d:
#     result.append(_get_fields(row, selection))
#   return result

# def _get_fields(row, selection):
#   return {k:v for k, v in row.items() if k in selection}

def _search_in(d, key, value_list):
  for k, v in d:
    if v[key] in value_list:
      yield (k, v)

def _search_gt(d, key, value):
  for k, v in d:
    if v[key] == None:
      continue
    if v[key] > value:
      yield (k, v)

def _search_eq(d, key, value):
  for k, v in d:
    if v[key] == value:
      yield (k, v)

def _search_not_in(d, key, value_list):
  for k, v in d:
    if v[key] == None:
      continue
    if v[key] not in value_list:
      yield (k, v)

def _search_not_eq(d, key, value):
  for k, v in d:
    if v[key] != value:
      yield (k, v)

def _search_not_contain(d, key, value):
  for k, v in d:
    if value not in v[key]:
      yield (k, v)
