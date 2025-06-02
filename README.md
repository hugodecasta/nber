# nber
NoteBook MakER - a tool to transform your root projet folder into a python notebook

## Install

```bash
git clone git@github.com:hugodecasta/nber.git
cd nber
python setup.py
source ~/.bashrc
```

## Usage

The goal here is to recognize a set of python files prefixed by `parse` as notebook cells without having theme as a variable sharing environnement.

Example of file structure

```
project_root/
├── parseUBPhys_0_load_ds.py
├── parseUBPhys_1_create_df.py
├── parseUBPhys_2_torch_model.py
├── parseUBPhys_3_train.py
└── parseUBPhys_4_test_disp.py
```

### Executing the full notebook

If you want `nber` system to recognize the `parseUBPhys_` prefix as a notebook environnement and execute the files as cells, for example here from the top cell (cell `0`), use:

```bash
nber parseUBPhys_
```

### Execution from cell to end

If you want to execute the notebook from a specific starting cell, for example here all cells from cell `1`, use:

```bash
nber parseUBPhys_ 1
```

### Execution from cell to cell

If you want to execute a specific range of cells for example from cell `0` to cell `2`, use:

```bash
nber parseUBPhys_ 0 2
```

### Visual environnement separation

Sometimes, it can occurs that you have multiple execution environnement in your root directory (for test purposes for example) as such:

```
project_root/
├── DSS
│    └─ some files...
├── parseDSS_1_read_csv.py
├── parseDSS_2_tSNE.py
├── parseDSS_3_interactive_vizu.py
├── parseUBPhys_0_load_ds.py
├── parseUBPhys_1_create_df.py
├── parseUBPhys_2_torch_model.py
├── parseUBPhys_3_train.py
├── parseUBPhys_4_test_disp.py
├── test_mpc.py
└── utils.py
```

Here you can see the root directory is kind of a mess when it comes to quickly identifying where are the `nber` environnements and notebooks cells.

In order to help you quickly identify your work files, `nber` proposes to create speration empty files to separate each environnement using:

```bash
nber --sep
```

Transforming your root directory into

```
project_root/
├── DSS
│    └─ some files...
├── parseDSS_-1_skip_--------------------.py
├── parseDSS_1_read_csv.py
├── parseDSS_2_tSNE.py
├── parseDSS_3_interactive_vizu.py
├── parseUBPhys_-1_skip------------------.py
├── parseUBPhys_0_load_ds.py
├── parseUBPhys_1_create_df.py
├── parseUBPhys_2_torch_model.py
├── parseUBPhys_3_train.py
├── parseUBPhys_4_test_disp.py
├── parseUBPhys_10000_skip---------------.py
├── test_mpc.py
└── utils.py
```

### Pushing new files in beetween

At some point, you might be figuring out that you needed a step in beetween step `1` and step `2`.

Instead of have to create the new file and renaming alllll file after this one, `nber` allows you to push everything.

First create your file to have the following example root directory:

```
project_root/
├── parseUBPhys_0_load_ds.py
├── parseUBPhys_1_create_df.py
├── parseUBPhys_2_create_torch_dataset.py    <-- new file to insert
├── parseUBPhys_2_torch_model.py
├── parseUBPhys_3_train.py
└── parseUBPhys_4_test_disp.py
```

And use:

```bash
nber --pushfrom parseUBPhys_2_create_torch_dataset.py
```

Transform your root directory into:

```
project_root/
├── parseUBPhys_0_load_ds.py
├── parseUBPhys_1_create_df.py
├── parseUBPhys_2_create_torch_dataset.py
├── parseUBPhys_3_torch_model.py
├── parseUBPhys_4_train.py
└── parseUBPhys_5_test_disp.py
```

### Re-numeroting your steps

At some point in your project, you might have deleted some files, leaving holes in your environnement. In general, this is not an issue as `nber` can work its way through holes.

But if you want a correct environment numerotation, `nber` allows you to clear your root directory using:

```bash
nber --clear parseUBPhys_
```

You can also only apply the re-numerotation from one cell only or from one cell to another using:

```bash
# renumerotation from cell 1 to the end
nber --clear parseUBPhys_ 1

# renumerotation from cell 1 to cell 3
nber --clear parseUBPhys_ 1 3
```