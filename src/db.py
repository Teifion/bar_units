# I've made this into a module with getter/setter functions so
# this can be changed into an actual DB later with less effort

data = {}

def set(key, value):
  data[key] = value

def get(key):
  return data[key]

def query(**kwargs):
  d = data
  if "name" in kwargs:
    if type(kwargs["name"]) == list:
      _search_name_in(d, kwargs["name"])
    elif type(kwargs["name"]) == str:
      _search_name_eq(d, kwargs["name"])
  return d

# def _search_name_in(d, names):
#   pass

# def _search_name_eq(d, name):
#   [x.f() for x in the_list if x.f() == 1]
#   return {k:v for k, v in d.items() if k == d}
      
