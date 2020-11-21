import os.path

def get(key, f):
  if not check(key):
    _put(key, f())
  return _get(key)

def check(key):
  return bool(os.path.isfile(f".cache/{key}"))

def _put(key, value):
  with open(f".cache/{key}", 'w', encoding="utf8") as f:
    f.write(value)

def _get(key):
  with open(f".cache/{key}", 'r', encoding="utf8") as f:
    return f.read()
