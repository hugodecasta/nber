import os
import subprocess


def add_alias_to_bashrc():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    nber_path = os.path.join(current_dir, "nber.py")
    alias_command = f'\n\nalias nber="python {nber_path}"'
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, 'r') as bashrc:
        content = bashrc.read()
        if f'alias nber="python {nber_path}"' in content:
            print(f"Alias already exists in {bashrc_path}")
            return
    with open(bashrc_path, 'a') as bashrc:
        bashrc.write(alias_command)


if __name__ == "__main__":
    add_alias_to_bashrc()
