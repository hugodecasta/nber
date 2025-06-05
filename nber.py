import os
import sys

# region ----------------------------------------------------------------------------------- UTILS

# region .... usage


def usage():
    print("Usage: nber <notebook_prefix> [start_cell] [end_cell]")
    print()
    print("Options:")
    print("  <notebook_prefix> [start_cell] [end_cell]")
    print("      Execute all or specific cell range in the notebook with the specified prefix.")
    print("  --sep")
    print("      Create separation empty files to visually separate each notebook environment in the root directory.")
    print("  --push <filename>")
    print("      Insert a new cell and renumber subsequent cells automatically.")
    print("  --clear <notebook_prefix> [start_cell] [end_cell]")
    print("      Renumber notebook cells for a given prefix, optionally from a specific cell or range.")
    print()
    print("Examples:")
    print("  nber parseUBPhys_")
    print("      Execute all cells in the notebook with prefix 'parseUBPhys_'.")
    print("  nber parseUBPhys_ 1")
    print("      Execute all cells from cell 1 to the end.")
    print("  nber parseUBPhys_ 0 2")
    print("      Execute cells from cell 0 to cell 2.")
    print("  nber --sep")
    print("      Add visual separation files for each notebook environment.")
    print("  nber --push parseUBPhys_2_create_torch_dataset.py")
    print("      Insert a new cell and renumber subsequent cells.")
    print("  nber --clear parseUBPhys_")
    print("      Renumber all cells for the given prefix.")
    print("  nber --clear parseUBPhys_ 1")
    print("      Renumber from cell 1 to the end.")
    print("  nber --clear parseUBPhys_ 1 3")
    print("      Renumber from cell 1 to cell 3.")
    print()
    print("For more details, see the README.md.")


# region .... find_arg

def find_arg(arg_id, default='---error---'):
    arg = sys.argv[arg_id] if len(sys.argv) > arg_id else default
    if arg == '---error---':
        usage()
        exit(1)
    return arg


# region .... parse filename

def parse_filename(filename: str):
    return (
        filename.split('_')[0] + '_',
        int(filename.split('_')[1]),
        filename,
        '_'.join(filename.split('_')[2:])
    )


# region .... gather notebooks

def get_all_notebooks():
    files = os.listdir('.')
    files = [f for f in files if f.endswith('.py') and f.startswith('parse') and not '_skip' in f]
    files = [parse_filename(f) for f in files]
    files = sorted(files, key=lambda x: x[1])
    prefixes = sorted(set([ff[0] for ff in files]))
    notebooks = dict([(p, [ff for ff in files if ff[0] == p]) for p in prefixes])
    return notebooks


# region .... exec notebook


def execute_notebook(notebook, start_cell=None, end_cell=None):

    start_cell = notebook[0][1] if start_cell is None else start_cell
    end_cell = notebook[-1][1] if end_cell is None else end_cell

    start_cell = int(start_cell)
    end_cell = int(end_cell)

    for notebook_name, cell_number, filename, file_info in notebook:
        if cell_number < start_cell or cell_number > end_cell:
            continue
        print("-" * 70, notebook_name, cell_number, file_info)
        command = f"python3 {filename}"
        code = os.system(command)
        if code != 0:
            print(f"Error executing {filename}. Exiting.")
            exit(1)


# region .... sep


def create_separator_file(notebook_prefix, number=-1):
    sep_len = 40
    prefix = notebook_prefix + str(number) + '_skip_sep'
    nb_bar = sep_len - len(prefix)
    with open(prefix + ('-' * nb_bar) + '.py', 'w') as f:
        f.write(f"# {notebook_prefix} notebook separator\n")


# region .... push from


def push_from(filename):
    file_data = parse_filename(filename)
    notebook_prefix = file_data[0]
    if not notebook_prefix in notebooks:
        print(f"Notebook with prefix '{notebook_prefix}' not found.")
        exit(1)
    notebook = notebooks[notebook_prefix]
    number = file_data[1]
    for _, file_number, full_filename, infos in notebook:
        if file_number >= number and full_filename != filename:
            new_filename = f"{notebook_prefix}{file_number + 1}_{infos}"
            os.rename(full_filename, new_filename)


# region .... clear notebook

def clear_notebook(prefix):
    if prefix not in notebooks:
        print(f"Notebook with prefix '{prefix}' not found.")
        exit(1)
    notebook = notebooks[prefix]
    start_cell = find_arg(3, None)
    end_cell = find_arg(4, None)
    start_cell = start_cell if start_cell is not None else notebook[0][1]
    end_cell = end_cell if end_cell is not None else notebook[-1][1]

    start_cell = int(start_cell)
    end_cell = int(end_cell)

    files = [f for f in notebook if start_cell <= f[1] <= end_cell]

    for i in range(len(files)):
        actual_cell_number = i + start_cell
        notebook_name, cell_number, filename, file_info = files[i]
        if cell_number != actual_cell_number:
            new_filename = f"{notebook_name}{actual_cell_number}_{file_info}"
            os.rename(filename, new_filename)


# region .... check version

def check_version():
    my_version = open('version.txt', 'r').read().strip()
    # online get https://raw.githubusercontent.com/hugodecasta/nber/refs/heads/main/version.txt
    raw_version = os.popen('curl -s https://raw.githubusercontent.com/hugodecasta/nber/refs/heads/main/version.txt').read().strip()
    if my_version != raw_version:
        print(f"Your version ({my_version}) is different from the online version ({raw_version}).")
        print("Please update nber by running 'nber --update' or 'git pull origin main'.")
        exit(1)


# region .... update
def update():
    print("Updating nber...")
    os.system('git pull origin main')

# region ----------------------------------------------------------------------------------- GATHER NOTEBOOKS


notebooks = get_all_notebooks()

# region ----------------------------------------------------------------------------------- FINDING ARGS


is_sep = False
is_pushfrom = False
is_clear = False
is_update = False

first_arg = find_arg(1)

if first_arg == '--sep':
    is_sep = True
elif first_arg == '--push':
    is_pushfrom = True
elif first_arg == '--clear':
    is_clear = True
elif first_arg == '--update':
    is_update = True

# region ----------------------------------------------------------------------------------- Execution

# region .... notebook exec

if not is_sep and not is_pushfrom and not is_clear and not is_update:
    notebook_prefix = find_arg(1)
    start_cell = find_arg(2, None)
    end_cell = find_arg(3, None)
    notebook = notebooks.get(notebook_prefix, None)
    if notebook is None:
        print(f"Notebook with prefix '{notebook_prefix}' not found.")
        exit(1)
    execute_notebook(notebook, start_cell, end_cell)

# region .... sep

elif is_sep:
    sep_len = 30
    for i, notebook_prefix in enumerate(notebooks.keys()):
        create_separator_file(notebook_prefix, -1)
        if i == len(notebooks) - 1:
            create_separator_file(notebook_prefix, 10000)

# region .... pushfrom

elif is_pushfrom:
    filename = find_arg(2)
    push_from(filename)

# region .... clear

elif is_clear:
    prefix = find_arg(2)
    clear_notebook(prefix)

# region .... update

elif is_update:
    update()
