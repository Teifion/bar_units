# I've made this into a module with getter/setter functions so
# this can be changed into an actual DB later with less effort

_data = {}

def put(key, value):
  value["id"] = key
  _data[key] = value

def get(key):
  return _data[key]

def preprocess_data(d):
  for k, row in d.items():
    row["techlevel"] = row.get("customparams", {}).get("techlevel", 1)
    row["arm"] = "ARM" in row["objectname"]
    row["core"] = "COR" in row["objectname"]
    row["armorcore"] = row["arm"] or row["core"]

    if "TANK" in row.get("movementclass", ""): row["type"] = "tank"
    elif "BOT" in row.get("movementclass", ""): row["type"] = "bot"
    else:
      if row.get("canfly", False) == True: row["type"] = "air"
      elif row.get("canmove", False) == True: row["type"] = "ship"
      else: row["type"] = "building"
      
    
    yield (k, row)

def query(**kwargs):
  d = preprocess_data(_data)
  filters = kwargs.get("filters", [])

  for f in filters:
    [field, comp, value] = f

    if comp in ("eq", "is", "==", "="):
      d = _search_eq(d, field, value)
    elif comp == "in":
      d = _search_in(d, field, value)
    elif comp in ("not", "not eq"):
      d = _search_not(d, field, value)
    elif comp == "not in":
      d = _search_not_in(d, field, value)
    elif comp == "does not contain":
      d = _search_not_contain(d, field, value)

  return select(d, kwargs["select"])

def select(d, selection):
  result = []
  for k, row in d:
    result.append(_get_fields(row, selection))
  return result

def _get_fields(row, selection):
  return {k:v for k, v in row.items() if k in selection}

def _search_in(d, key, value_list):
  for k, v in d:
    if v[key] in value_list:
      yield (k, v)

def _search_eq(d, key, value):
  for k, v in d:
    if v[key] == value:
      yield (k, v)

def _search_not_in(d, key, value_list):
  for k, v in d:
    if v[key] not in value_list:
      yield (k, v)

def _search_not_eq(d, key, value):
  for k, v in d:
    if v[key] != value:
      yield (k, v)

def _search_not_contain(d, key, value):
  for k, v in d:
    if value_list not in v[key]:
      yield (k, v)
