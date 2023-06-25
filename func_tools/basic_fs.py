import os

should_log = True
custom_print = print if should_log else (lambda x:None)

def traverse_path(path:str) -> str:
    abs_path = os.path.abspath(path)
    rel_to_curr = os.path.relpath(abs_path)
    path_components = rel_to_curr.split(os.sep)
    if path_components[0] == "..":
        return "Error: You can only read within the current repository."
    return rel_to_curr

def ls(path:str) -> str:
    """List files in a directory."""
    custom_print("calling ls",path)
    clean_path = traverse_path(path)
    files = os.listdir(clean_path)
    return "\n".join(files)

# print(ls("././old_code"))

def cat(path:str) -> str:
    """
    List the contents of a file.
    """
    custom_print("calling cat",path)
    clean_path = traverse_path(path)
    with open(clean_path, "r") as file:
        contents = file.read()
    return contents

def rm(path:str) -> str:
    """
    Remove a file.
    """
    custom_print("calling rm",path)
    clean_path = traverse_path(path)
    os.remove(clean_path)
    return "Success"

# print(cat("README.md"))

import subprocess
def tree() -> str:
    """
    Show a tree of the current repository.
    """
    custom_print("calling tree")
    result = subprocess.run(["tree"], capture_output=True)
    return result.stdout.decode("utf-8")

# print(tree())

# TODO: add a smart diff function instead of this. i.e. takes in filename, old_code, and new_code, then replaces the old_code with the new_code in the file.
def write_to_file(path:str, contents:str) -> str:
    """
    Writes to a file.
    """
    custom_print("writing",path,contents[:50])
    clean_path = traverse_path(path)
    with open(clean_path, "w") as file:
        file.write(contents)
    return "Success"

# TODO: handle stdout, stderr. Does this work automatically?
def execute_bash_command(command:str) -> str:
    """
    Executes a bash command.
    Allowed commands: npm, node, mkdir
    """

    custom_print("running command",command)
    whitelist = ["npm","node","mkdir","npx"]
    command_components = command.split(" ")
    start_command = command_components[0]
    if start_command not in whitelist:
        return f"Error: Command {start_command} not allowed."
    result = subprocess.run(command_components, capture_output=True)
    return result.stdout.decode("utf-8")

functions = [ls, cat, tree, write_to_file, execute_bash_command]