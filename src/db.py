# I've made this into a module with getter/setter functions so
# this can be changed into an actual DB later with less effort

_data = {}

def put(key, value):
  value["id"] = key
  _data[key] = value

def get(key):
  return _data[key]

def query(**kwargs):
  d = _data
  if "name" in kwargs:
    if isinstance(kwargs["name"]) == list:
      _search_name_in(d, kwargs["name"])
    elif isinstance(kwargs["name"]) == str:
      _search_name_eq(d, kwargs["name"])
  return select(d, kwargs["select"])

def select(d, selection):
  result = []
  for k, row in d.items():
    result.append(_get_fields(row, selection))
  return result

def _get_fields(row, selection):
  return [row[k] for k in selection]

# def _search_name_in(d, names):
#   pass

# def _search_name_eq(d, name):
#   [x.f() for x in the_list if x.f() == 1]
#   return {k:v for k, v in d.items() if k == d}
      
