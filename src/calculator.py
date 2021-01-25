def dps(row):
  weapons = row["weapondefs"]
  return 0

def dps1(row):
  if "weapondefs" not in row: return None

  keys = list(row["weapondefs"].keys())
  weapon = row["weapondefs"][keys[0]]

  if "default" not in weapon["damage"]: return None
  dps = weapon["damage"]["default"] / weapon["reloadtime"]
  dps = dps * weapon.get("burst", 1)
  # Peewee 100
  # Warrior 185
  # AK 75
  # Thud 61
  # morty 66
  # Sumo 508
  # samson 48
  return dps

def weapon_count(row):
  return len(row["weapondefs"])

def process_row(row, fields):
  for f in fields:
    if f in funcs:
      row[f] = funcs[f](row)
  return row

funcs = {
  "dps": dps,
  "dps1": dps1,
  "weapon_count": weapon_count
}
