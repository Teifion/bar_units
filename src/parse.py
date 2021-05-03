import lupa
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

def eval_string(string):
  # change stuff like this:
  # local unitName = Spring.I18N('units.names.armaca')
  # description = Spring.I18N('units.heap', { name = unitName }),
  # to this:
  # local unitName = "units.names.armaca"
  # description = "units.heap.armsomethingsomething",
  unit_name = string.partition('\n')[0].replace("local unitName = ", "")
  if "Spring.I18N('" in string:
    unit_name = unit_name.replace("Spring.I18N('", "\"").replace("')", "\"", 1)
    string = string \
      .replace("Spring.I18N('", "\"") \
      .replace("', { name = unitName }", "." + unit_name.split(".")[-1].replace("\"", "") + "'") \
      .replace("')", "\"")

  try:
    data = lua.execute(string)
    return open_unit_table(data)
  except lupa._lupa.LuaError as e:
    if "attempt to index a nil value" in e.args[0]:
      return None
    print(e)
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

