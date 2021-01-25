import csv
from src import github, db, output

def main():
  github._check_rate_limit()
  github.get_all_unit_files()

  output.write(
    select = ["id", "name", "buildcostenergy", "buildcostmetal", "buildtime", "weapondefs"],
    filters = [
      # ["name", "in", [
      #   "Peewee", "Warrior", "Samson",
      #   "A.K.", "Thud", "Morty", "Sumo"
      # ]]
      ["type", "is", "bot"],
      ["techlevel", "is", 1],
      ["armorcore", "is", True]
    ],
    output = ["id", "name", "buildcostenergy", "buildcostmetal", "buildtime", "dps1"]
  )

if __name__ == '__main__':
  main()
