# bar CSV and JSON output

This project converts the unit files into CSV and JSON output.


## Install

```pip3 install -r requirements.txt```

This project also uses git and requirements a version higher than 2.25.0.
you can get git from https://git-scm.com/ or get it from the os package manager

## Usage

for a basic output, you can issue the following command:
```python3 bar_units.py```

this command will output three files into the `generated` folder:

A CSV file according to the provided settings
A JSON file is a direct translation for all units from the Lua files
And another JSON file which all the units with extra precalculated values.

To use a preset, use the following command:
```python3 bar_units.py site```

There are three presets available: default, site, metalmake

## settings 
 
The first argument on the command line is used to look up the settings.

These settings are located at: https://github.com/Teifion/bar_units/blob/master/bar_units.py#L7

The first array in the table defines the filters and the second one the output parameters
