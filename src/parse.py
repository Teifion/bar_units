import lupa
from lupa import LuaRuntime
lua = LuaRuntime()


def eval_string(path):
    """
    runs the lua file and transforms the lua table to a dict
    path: path to the lua file for the unit
    """
    # read the contents of a unit file
    f = open(path, "r")
    string = f.read()

    # capture the unit name
    unit_name = string.partition('\n')[0].replace("local unitName = ", "")

    """
    in the lua code there are references to Spring.I18n
    this function is unavailable in our environment
    so we need to change 
    local unitName = Spring.I18N('units.names.armaca')
    to
    local unitName = "units.names.armaca"
    and
    description = Spring.I18N('units.heap', { name = unitName }),
    to
    description = "units.heap.armsomethingsomething",
    """
    if "Spring.I18N('" in string:
        unit_name = unit_name.replace(
            "Spring.I18N('", "\"").replace("')", "\"", 1)
        string = string \
            .replace("Spring.I18N('", "\"") \
            .replace("', { name = unitName }", "." + unit_name.split(".")[-1].replace("\"", "") + "'") \
            .replace("')", "\"")

    string = string.replace("units.names.", "").replace("units.names.", "")

    try:
        data = lua.execute(string)
        if(not lupa.lua_type(data) == "table"):
            print("found broken thing at " + path)
        return open_unit_table(data)
    except lupa._lupa.LuaError as e:
        if "attempt to index a nil value" in e.args[0] or (
                "attempt to index global" in e.args[0] and "(a nil value)" in e.args[0]):
            return None
        print("encountered the following error while parsing " + path)
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
