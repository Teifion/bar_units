import csv
from src import github, db, output

default_filters = [
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
  github._check_rate_limit()
  github.get_all_unit_files()

  output.write(
    filters = [
      ["type", "is", "bot"],
      ["techlevel", "is", 1],
      ["arm", "is", True],
    ] + default_filters,
    select = ["id", "name", "buildcostmetal", "buildcostenergy", "buildtime", "health", "dps", "range", "dps_per_metal", "health_per_metal"]
  )

if __name__ == '__main__':
  main()
