def preprocess(row):
  row["techlevel"] = row.get("customparams", {}).get("techlevel", 1)
  if "4" in row["id"]: row["techlevel"] = 4

  row["arm"] = "ARM" in row["objectname"]
  row["core"] = "COR" in row["objectname"]
  row["armorcore"] = row["arm"] or row["core"]

  if row["arm"]:
    row["faction"] = "arm"
  elif row["core"]:
    row["faction"] = "core"

  row["health"] = row["maxdamage"]

  if "TANK" in row.get("movementclass", ""): row["type"] = "tank"
  elif "BOT" in row.get("movementclass", ""): row["type"] = "bot"
  else:
    if row.get("canfly", False) == True: row["type"] = "air"
    elif row.get("canmove", False) == True: row["type"] = "ship"
    else: row["type"] = "building"

  row["weapon_count"] = len(row.get("weapondefs", []))
  row["dps1"] = _dps(row, 1)
  row["dps2"] = _dps(row, 2)
  row["dps3"] = _dps(row, 3)
  row["dps"] = row["dps1"] + row["dps2"] + row["dps3"]

  cat_list = row.get("category", "").split(" ")
  row["categories"] = ", ".join(cat_list)

  build_dict = row.get("buildoptions", {})
  row["buildoptions"] = ", ".join([v for v in build_dict.values()])

  row["metalmake"] = row.get("metalmake", None)
  row["energymake"] = row.get("energymake", None)

  row["radardistance"] = row.get("radardistance", None)
  row["maxvelocity"] = row.get("maxvelocity", None)

  row["speed"] = row["maxvelocity"]
  row["height"] = "?"

  row["range1"] = _range(row, 1)
  row["range2"] = _range(row, 2)
  row["range3"] = _range(row, 3)
  row["range"] = max(row["range1"], row["range2"], row["range3"])
  
  row["dps_per_metal"] = row["dps"]/max(row["buildcostmetal"],1)
  row["health_per_metal"] = row["health"]/max(row["buildcostmetal"],1)

  return row

def _dps(row, x):
  if "weapondefs" not in row: return 0
  if len(row["weapondefs"]) < x: return 0

  keys = list(row["weapondefs"].keys())
  weapon = row["weapondefs"][keys[x-1]]

  if "reloadtime" not in weapon: return 0
  if weapon["reloadtime"] <= 0: return 0
  if "default" not in weapon["damage"]: return 0

  dps = weapon["damage"]["default"] / weapon["reloadtime"]
  dps = dps * weapon.get("burst", 1)
  return dps

def _range(row, x):
  if "weapondefs" not in row: return 0
  if len(row["weapondefs"]) < x: return 0

  keys = list(row["weapondefs"].keys())
  weapon = row["weapondefs"][keys[x-1]]

  return weapon["range"]
