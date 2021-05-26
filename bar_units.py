import csv
import sys
from src import github, db, output

default_filters = [
  ["armorcore", "is", True]
]

site_filters = [
  ["armorcore", "is", True]
]

"""
Example filters
All T2 tanks
filters = [
  ["type", "is", "tank"],
  ["techlevel", "is", 2],
  ["dps1", ">", 0]
] + default_filters,

Two specific tanks
filters = [
  ["name", "in", ["Bulldog", "Reaper"]],
],

# All T1 arm bots
filters = [
  ["type", "is", "bot"],
  ["techlevel", "is", 1],
  ["arm", "is", True],
] + default_filters,
"""

def main():
  if len(sys.argv) == 1:
    filters = []
  elif len(sys.argv) == 2:
    fname = sys.argv[1]
    if fname == "site":
      filters = site_filters
    else:
      filters = default_filters

  github._check_rate_limit()
  github.get_all_unit_files()

  output.write(
    filters = filters,
    select = [
      "id", "name", "faction", "categories",
      "buildoptions", "buildcostmetal", "buildcostenergy", "energymake", "metalmake", "buildtime",
      "dps", "range", "dps_per_metal", "speed", "health",
      "radardistance", "height"
    ]
  )

if __name__ == '__main__':
  main()
