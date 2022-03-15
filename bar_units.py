import json
import sys
import os
import subprocess
import re
from src import github, files, process, parse, output
filterOptions = {
    "default": (
        [["armorcore", "is", True]],
        [
            "id"
        ]
    ),
    "site": (
        [["armorcore", "is", True]],
        [
            "id", "faction", "categories",
            "buildoptions", "buildcostmetal", "buildcostenergy", "energymake", "metalmake", "buildtime",
            "dps", "range", "dps_per_metal", "speed", "health",
            "radardistance", "height"
        ]
    ),
    "metalmake": (
        [
            ["armorcore", "is", True],
            ["energymake", ">", 5],
            ["type", "is", "building"]
        ],
        [
            "id", "faction", "buildcostmetal", "buildcostenergy", "energymake"
        ]
    )
}

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


def setup():
    if not os.path.exists('generated'):
        os.mkdir('generated')

    output = subprocess.check_output("git --version", shell=True)
    major = re.search("(\d+)\.(\d+)\.(\d+)", str(output)).group(1)
    minor = re.search("(\d+)\.(\d+)\.(\d+)", str(output)).group(2)
    patch = re.search("(\d+)\.(\d+)\.(\d+)", str(output)).group(3)

    if int(major) < 2 or int(minor) < 25:
        # you can try it with an older version git but there are no guarantees
        raise Exception(
            "you need a newer version of git to run this program at least 2.25.0. Please download it from https://git-scm.com/")


def main(filters, selection):
    # setup some things like checking versions and if the output dictionary is presset
    setup()
    # clone the github to get the files
    github.clone()

    # filter out all the lua files
    unitFiles = files.getFiles()

    # parseout all the files and create a giant dictionary
    # use intermediate format to create both a raw output and a extended output
    unitTupleList = [parse.eval_string(unitFile) for unitFile in unitFiles]
    rawUnits = {id: value for id, value in unitTupleList}

    # write the json to disk
    with open('generated/units.json', 'w', encoding = 'utf-8') as f:
        json.dump(rawUnits, f, ensure_ascii = False, indent = 4)

    # extend the dict with extra information
    units = {id: value for id, value in [
        process.preprocess(unit) for unit in unitTupleList]}
    
    with open('generated/unitsExtended.json', 'w', encoding = 'utf-8') as f:
        json.dump(units, f, ensure_ascii = False, indent = 4)

    output.write(
        filters = filters,
        select = selection,
        data = units
    )


if __name__ == '__main__':
    # see if the a filter is specified on the command line
    if len(sys.argv) == 1:
        filters, selection=filterOptions["default"]
    elif len(sys.argv) == 2:
        filterName=sys.argv[1]

        if filterName in filterOptions:
            filters, selection=filterOptions[filterName]
        else:
            filters, selection=filterOptions["default"]

    main(filters, selection)
