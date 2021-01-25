import csv
from src import db, calculator

default_select_fields = ["id", "name", "buildcostenergy", "buildcostmetal", "buildtime", "weapondefs"]
default_output_fields = ["id", "name", "buildcostenergy", "buildcostmetal", "buildtime", "dps1"]

def write(**kwargs):
  query_args = {
    "filters": kwargs.get("filters", []),
    "select": kwargs.get("fields", default_select_fields)
  }
  output_fields = kwargs.get("output", default_output_fields)

  with open("units.csv", 'w', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(output_fields)
    for row in db.query(**query_args):
      row = calculator.process_row(row, output_fields)
      row = convert_to_list(row, output_fields)
      print(row)
      writer.writerow(row)

def convert_to_list(row, output_fields):
  return [row[k] for k in output_fields]
  # return {k:v for k, v in row.items() if k in output_fields}