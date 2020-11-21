import csv
from src import github, db

def main():
  # print(github._check_rate_limit())
  # print("")

  github.get_all_unit_files()
  
  fields = ["id", "name", "buildcostenergy", "buildcostmetal", "buildtime"]
  query_args = {
    "select": fields
  }

  with open("units.csv", 'w', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    for row in db.query(**query_args):
      writer.writerow(row)

if __name__ == '__main__':
  main()
