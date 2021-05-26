import csv
from src import db, calculator

filename = "units.csv"
default_fields = ["id", "name", "buildcostenergy", "buildcostmetal", "buildtime", "weapondefs"]

def write(**kwargs):
  query_args = {
    "filters": kwargs.get("filters", []),
  }
  fields = kwargs.get("select", default_fields)

  with open(filename, 'w', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    for (key, row) in db.query(**query_args):
      row = convert_to_list(row, fields)
      writer.writerow(row)
  
  print(f"Results output to {filename}")

def convert_to_list(row, output_fields):
  return [row[k] for k in output_fields]
