# NoteBook(er) to transform your folder in notebooks
# create files parse_<nb>_blablabla.py
# user `nber parse_ 0` and it'll run your folder trough 0 to n
# use cases:
#   `nber parse_ 0`
#   `nber parse_ 1 10` (run from 1 to 10)
#   `nber parse_ 3.5`  (float are allowed)
#   `nber parseWS_ 3.5`  (use any prefix)

import os
import sys
import subprocess

# region ----------------------------------------------------------------------------------- UTILS


def get_all_notebooks():
    files = os.listdir('.')
    files = [f.split('_')[0] for f in files if f.endswith('.py') and f.startswith('parse') and not '_skip' in f]
    files = list(set(files))
    return files


def usage():
    print("Usage 1: nber --sep (to create file separators)")
    print("Usage 2: nber <prefix> <from_number> [<to_number>] [<args>]")
    print("Example: nber parse_ 0")
    print("Example: nber parse_ 1 10")
    print("Example: nber parse_ 3.5")
    print("Example: nber parseWS_ 3.5")
    exit(1)

# region ----------------------------------------------------------------------------------- ARG PARSE


if len(sys.argv) < 1:
    usage()

prefix = sys.argv[1]

if prefix == '--sep':
    sep_len = 30
    notebooks = get_all_notebooks()
    for notebook in notebooks:
        prefix = notebook + '_-1_'
        nb_bar = sep_len - len(notebook)
        with open(prefix + ('-' * nb_bar) + '.py', 'w') as f:
            f.write(f"# {notebook} notebook separator\n")
    exit(0)

if len(sys.argv) < 2:
    usage()

from_number = float(sys.argv[2])
to_number = float(sys.argv[3]) if len(sys.argv) > 3 else None
all_args = sys.argv[4:]

# region ----------------------------------------------------------------------------------- GATHER

all_files = os.listdir('.')
all_files = [f for f in all_files if f.startswith(prefix) and f.endswith('.py') and not '_skip' in f]
all_files = sorted(all_files, key=lambda x: float(x.split('_')[1]))
all_files = [
    (f, float(f.split('_')[1]))
    for f in all_files
]

if len(all_files) == 0:
    print(f"No files found with prefix {prefix}")
    exit(1)

if to_number is None:
    to_number = all_files[-1][1]

for file, nb in all_files:
    if nb < from_number or nb > to_number:
        continue
    print('-' * 100, 'NoteBookER:', file)
    code = subprocess.run(['python3', file, *all_args]).returncode
    if code != 0:
        print('-' * 50, f"Error in {file}")
        exit(1)
