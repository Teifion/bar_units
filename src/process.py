def preprocess(unit):
    """
    this function add some derived information to the units

    Args:
        unit (tuple): the units as a python dict

    Returns:
        tuple: the unit with additional information
    """
    unitID = unit[0]
    unitStats = unit[1]

    # add the tech level
    unitStats["techlevel"] = unitStats.get(
        "customparams", {}).get("techlevel", 1)

    # add the faction
    unitStats["arm"] = "ARM" in unitStats["objectname"]
    unitStats["core"] = "COR" in unitStats["objectname"]
    unitStats["armorcore"] = unitStats["arm"] or unitStats["core"]

    if unitStats["arm"]:
        unitStats["faction"] = "arm"
    elif unitStats["core"]:
        unitStats["faction"] = "core"

    # maxdamage is a alias for health
    unitStats["health"] = unitStats["maxdamage"]

    # add a type category
    # TODO: Pelican has movement class HOVER5, but it is a bot. Also hovercraft are not represented.
    if "TANK" in unitStats.get("movementclass", ""):
        unitStats["type"] = "tank"
    elif "BOT" in unitStats.get("movementclass", ""):
        unitStats["type"] = "bot"
    else:
        if unitStats.get("canfly", False) == True:
            unitStats["type"] = "air"
        elif unitStats.get("canmove", False) == True:
            unitStats["type"] = "ship"
        else:
            unitStats["type"] = "building"

    # add information about the weapons
    unitStats["weapon_count"] = len(unitStats.get("weapondefs", []))
    unitStats["dps1"] = _dps(unitStats, 1)
    unitStats["dps2"] = _dps(unitStats, 2)
    unitStats["dps3"] = _dps(unitStats, 3)
    unitStats["dps"] = unitStats["dps1"] + \
        unitStats["dps2"] + unitStats["dps3"]

    # split out the catagories for easy use
    cat_list = unitStats.get("category", "").split(" ")
    unitStats["categories"] = ", ".join(cat_list)

    build_dict = unitStats.get("buildoptions", {})
    unitStats["buildoptions"] = ", ".join([v for v in build_dict.values()])

    # add defaults to some options
    unitStats["metalmake"] = unitStats.get("metalmake", None)
    unitStats["energymake"] = unitStats.get("energymake", None)

    unitStats["radardistance"] = unitStats.get("radardistance", None)
    unitStats["maxvelocity"] = unitStats.get("maxvelocity", None)

    # add a alias for the speed
    unitStats["speed"] = unitStats["maxvelocity"]
    # TODO: is this really not ascertainable
    unitStats["height"] = "?"

    # add the rage of a unit
    unitStats["range1"] = _range(unitStats, 1)
    unitStats["range2"] = _range(unitStats, 2)
    unitStats["range3"] = _range(unitStats, 3)
    unitStats["range"] = max(
        unitStats["range1"], unitStats["range2"], unitStats["range3"])

    # add pre metal stats
    unitStats["dps_per_metal"] = unitStats["dps"] / \
        max(unitStats["buildcostmetal"], 1)
    unitStats["health_per_metal"] = unitStats["health"] / \
        max(unitStats["buildcostmetal"], 1)

    return (unitID, unitStats)


def _dps(row, x):
    if "weapondefs" not in row:
        return 0
    if len(row["weapondefs"]) < x:
        return 0

    keys = list(row["weapondefs"].keys())
    weapon = row["weapondefs"][keys[x-1]]

    if "reloadtime" not in weapon:
        return 0
    if weapon["reloadtime"] <= 0:
        return 0
    if "default" not in weapon["damage"]:
        return 0

    dps = weapon["damage"]["default"] / weapon["reloadtime"]
    dps = dps * weapon.get("burst", 1)
    return dps


def _range(row, x):
    if "weapondefs" not in row:
        return 0
    if len(row["weapondefs"]) < x:
        return 0

    keys = list(row["weapondefs"].keys())
    weapon = row["weapondefs"][keys[x-1]]

    return weapon["range"]
