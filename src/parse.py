import lupa
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

def eval_string(string):
  try:
    data = lua.execute(string)
    return open_unit_table(data)
  except lupa._lupa.LuaError as e:
    if "attempt to index a nil value" in e.args[0]:
      return None
    raise
  
def open_unit_table(data):
    unit_key = list(data)[0]
    results = table_to_dict(data[unit_key])
    return (unit_key, results)

def table_to_dict(table):
  return {k: convert_field(k, v) for k, v in table.items()}

def convert_field(field, value):
  if isinstance(value, float):
    return value
  elif isinstance(value, str):
    return value
  elif isinstance(value, int):
    return value
  elif lupa.lua_type(value) == "table":
    return table_to_dict(value)
  else:
    raise Exception(f"No handler for type {type(value)}")

