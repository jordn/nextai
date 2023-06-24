import os

def traverse_path(path:str) -> str:
    abs_path = os.path.abspath(path)
    rel_to_curr = os.path.relpath(abs_path)
    path_components = rel_to_curr.split(os.sep)
    if path_components[0] == "..":
        return "Error: You can only read within the current repository."
    return rel_to_curr

def ls(path:str) -> str:
    """List files in a directory."""
    clean_path = traverse_path(path)
    files = os.listdir(clean_path)
    return "\n".join(files)

# print(ls("././old_code"))

def cat(path:str) -> str:
    """
    List the contents of a file.
    """
    clean_path = traverse_path(path)
    with open(clean_path, "r") as file:
        contents = file.read()
    return contents

# print(cat("README.md"))

import subprocess
def tree() -> str:
    """
    Show a tree of the current repository.
    """
    result = subprocess.run(["tree"], capture_output=True)
    return result.stdout.decode("utf-8")

# print(tree())

# TODO: add a smart diff function instead of this. i.e. takes in filename, old_code, and new_code, then replaces the old_code with the new_code in the file.
def write_to_file(path:str, contents:str) -> str:
    """
    Writes to a file.
    """
    clean_path = traverse_path(path)
    with open(clean_path, "w") as file:
        file.write(contents)
    return "Success"