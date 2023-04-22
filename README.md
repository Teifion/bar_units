# Install:

```pip3 install -r requirements.txt```

# Usage:

## Load Data Directly from Github 

```python3 bar_units.py```

It will cache downloads from github into .cache to prevent hitting rate limits. There is currently no way to re-cache from the script.

## Build JSON of units from local clone of BAR Github

```python3 units_json.py```

Options: 
 - `-p` Path to BAR project root. (default: `-p ../Beyond-All-Reason/`)
 - `-o` Path to output json files. (default: `-o ../`)
   - DEFAULT creates at least one file : `../jsonunits/units.json`
 - `-d` Folder depth to split json files. (default: `-d 1` )
   - DEFAULT will create one json file for each directory in `BAR/units` (not recursive), and will recursively include all the units in that folder.
   - `-d 0` will create a single file `units.json` containing every unit in BAR.
     - __The whole reason I built this thing.__ 
 - `-v` Verbose (default: false)
 - `-t` Testing (default: false)
   - Will only attempt to process armcom and corcom, and will not modify files.