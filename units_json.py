import os
import sys
import traceback
import json
import re
from argparse import ArgumentParser
from pathlib import Path
from src import parse

re_newline = re.compile('\n')

class UnitParseError(Exception):
    def __init__(self, unit_path, message='Failed to load unit'):
        self.unit_path = unit_path
        self.message = message

    def __str__(self):
        return self.message + ' from ' + str(self.unit_path)


def main ():
    args = get_args()
    units_root_path = get_units_path(args.path_to_bar)
    dest_path = get_dest_path(args.output_dest)
    failures = []

    #     for unit_path in Path(units_root_path).rglob('*.lua'):
    # for unit_path in Path(units_root_path).glob('armcom.lua'):
    for unit_path in get_unit_file_list(units_root_path):
        try:
            dest_file = get_dest_file(dest_path, (len(units_root_path.parts) -1, int(args.output_depth)), unit_path)
            # print(dest_file)
            # print(lua_to_json(unit_path))
            add_unit_to_file(unit_path, dest_file)
        except Exception as e:
            if get_args().verbose:
                print(e)
                traceback.print_tb(e.__traceback__)
            failures.append(e)
            # raise e
            continue

    if len(failures)>0:
        print('\n\n!!!  --- Failed to process '+str(len(failures))+' units ---  !!!')
        for e in failures:
            if get_args().verbose:
                print(e)
            else:
                print('   ' + str(e))
                if e.__cause__:
                    print('      cause: ' + str(e.__cause__))



def get_args ():
    ap = ArgumentParser()
    ap.add_argument('-p', '--path', dest='path_to_bar', help='path to root of BAR', default='../Beyond-All-Reason/')
    ap.add_argument('-o', '--output', dest='output_dest', help='path to output resulting file(s)', default='../')
    ap.add_argument('-d', '--depth', dest='output_depth', help='how deep to walk directory to determine output filename, smaller gives fewer (larger) files. (Warning: 0 makes 1 file, but needs RAM)', default='1')
    ap.add_argument('-v', '--verbose', dest='verbose', help='show every unit name and where it will be saved', action='store_true')
    ap.add_argument('-t', '--test', dest='testing', help='turn on testing -- will only access armcom and corcom', action='store_true')
    return ap.parse_args()


def get_units_path (bar_path):
    unit_path = Path(bar_path + 'units/')
    if not unit_path.is_dir():
        sys.exit('path_to_bar [-p] does not include a units directory.')
    if not Path(bar_path + 'units/armcom.lua').is_file():
        sys.exit('path_to_bar [-p] seems to be incorrect. Could not find armcom.')
    return unit_path


def get_unit_file_list (units_root_path):
    if get_args().testing:
        return Path(units_root_path).glob('*com.lua')

    return Path(units_root_path).rglob('*.lua')


def lua_to_json (unit_path):
    data = parse.eval_string(unit_path.read_text())
    if data:
        return strip_newline(json.dumps(data[1]))


def strip_newline (string):
    return re_newline.sub('', string)


def get_dest_path (output_path):
    dest_path = Path(output_path)
    if not dest_path.is_dir() or not os.access(dest_path, os.W_OK):
        sys.exit('output path [-o] is not writable.')
    final_dest = Path(dest_path, 'jsonunits')
    if not get_args().testing:
        if final_dest.exists():
            for file in final_dest.glob('*'):
                file.unlink()
        else:
            final_dest.mkdir(mode=0o744, parents=True)
    return final_dest


def get_dest_file (dest_path, depth, unit_path):
    if depth[1] == 0:
        return Path(dest_path,'units.json')

    s = depth[0] # start (BAR/units/)
    d = depth[1] # depth

    name = ''
    for i in range(s, s+d+1):
        if len(unit_path.parts)-1 > i and unit_path.parts[i][-3:] != 'lua':
            name += '_'
            name += unit_path.parts[i]
    if name != '_units':
        name = name[6:] #_units_something -> _something
    name +='.json'

    # return Path(dest_path,name[1:]), unit_path
    return Path(dest_path,name[1:])


def add_unit_to_file (unit_path, dest_path):
    unitname = unit_path.parts[-1][:-4]
    groupname = dest_path.parts[-1][:-5]

    try:
        unitdata_string = lua_to_json(unit_path)
    except Exception as e:
        raise UnitParseError(unit_path, 'Failed to load '+unitname) from e

    if not unitdata_string:
        raise UnitParseError(unit_path, 'Failed to load '+unitname)

    if groupname=='units':
        groupname = 'root'

    if get_args().verbose:
        print(unitname.ljust(20, ' ') +' --> '+ dest_path.parts[-1])

    if not get_args().testing:
        if not dest_path.exists():
            dest_path.write_text('{"unitgroup": "'+groupname+'"}')

        with dest_path.open(mode='a+') as f:
            # if not empty
            f.seek(f.tell() - 1, os.SEEK_SET)
            f.truncate()
            f.writelines(',\n' + unitdata_string + '}')
            f.close()

main()
