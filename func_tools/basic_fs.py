import os
import subprocess
from termcolor import colored

should_log = True


def print_user(text: str):
    if should_log:
        print(colored(text, "white"))


def print_assistant(text: str):
    if should_log:
        print(colored(text, "green"))


def print_debug(text: str):
    if should_log:
        print(colored(text, "blue"))


def print_system(text: str):
    if should_log:
        print(colored(text, "blue"))


def traverse_path(path: str) -> str:
    abs_path = os.path.abspath(path)
    rel_to_curr = os.path.relpath(abs_path)
    path_components = rel_to_curr.split(os.sep)
    if path_components[0] == "":
        path_components[0] = "."
    if path_components[0] == "..":
        return "Error: You can only read within the current repository."
    return rel_to_curr


def ls(path: str) -> str:
    """List files in a directory."""
    print_debug(f"ls {path}")
    clean_path = traverse_path(path)
    files = os.listdir(clean_path)
    return "\n".join(files)


def cat(path: str) -> str:
    """
    List the contents of a file.
    """
    print_debug(f"cat {path}")
    clean_path = traverse_path(path)
    with open(clean_path, "r") as file:
        contents = file.read()
    return contents


# WARNING!!! This function is dangerous. It can delete any file on your computer.
# def rm(path: str) -> str:
#     """
#     Remove a file.
#     """
#     print_debug("calling rm", path)
#     clean_path = traverse_path(path)
#     os.remove(clean_path)
#     return "Success"


def tree() -> str:
    """
    Show a tree of the current repository.
    """
    print_debug("tree")
    result = subprocess.run(["rg --files | tree --fromfile"], capture_output=True)
    return result.stdout.decode("utf-8")

# TODO: add a smart diff function instead of this. i.e. takes in filename, old_code, and new_code, then replaces the old_code with the new_code in the file.
def write_to_file(path: str, contents: str) -> str:
    """
    Writes to a file.
    """
    print_debug(f"write ({path}): {contents[:20]}...")

    # TODO: do this in a better place.
    # Idea is that when a change is made,
    # we want to only deal with fresh errors afterwards.
    # Clear stdout.log and stderr.log
    with open("stdout.log", "w") as file:
        file.write("")
    with open("stderr.log", "w") as file:
        file.write("")

    clean_path = traverse_path(path)
    with open(clean_path, "w") as file:
        # Make the directory if it doesn't exist
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        file.write(contents)
    return "Success"


# TODO: handle stdout, stderr. Does this work automatically?
def execute_bash_command(command: str) -> str:
    """
    Executes a bash command.
    Allowed commands: npm, node, mkdir
    """
    print_debug(f"bash: {command}")

    # Clear stdout.log and stderr.log
    with open("stdout.log", "w") as file:
        file.write("")
    with open("stderr.log", "w") as file:
        file.write("")

    whitelist = ["npm", "node", "mkdir", "npx"]
    command_components = command.split(" ")
    start_command = command_components[0]
    if start_command not in whitelist:
        return f"Error: Command {start_command} not allowed."
    result = subprocess.run(command_components, capture_output=True)
    return result.stdout.decode("utf-8")

def execute_bash_command(command: str) -> None:
    """
    Executes a bash command.
    Allowed commands: npm, node, mkdir
    """

    print("running command", command)
    whitelist = ["npm", "node", "mkdir", "npx"]
    command_components = command.split(" ")
    start_command = command_components[0]
    if start_command not in whitelist:
        print(f"Error: Command {start_command} not allowed.")
        return

    proc = subprocess.Popen(
        command_components,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )

    try:
        while proc.poll() is None:
            output = proc.stdout.readline()
            if output:
                print(output.decode(), end="")
            else:
                break

    except KeyboardInterrupt:
        proc.terminate()

    proc.communicate()

def edit_file(path: str, old_snippet: str, new_snippet: str) -> str:
    """
    Edits part of a file.
    Use this to replace a snippet of code in the file with a new snippet of code.
    i.e. edit_file("index.js", "console.log('hello')", "console.log('goodbye')")
    """
    print_debug(f"edit ({path}):")

    # Clear stdout.log and stderr.log
    with open("stdout.log", "w") as file:
        file.write("")
    with open("stderr.log", "w") as file:
        file.write("")

    clean_path = traverse_path(path)
    with open(clean_path, "r") as file:
        contents = file.read()
    if old_snippet not in contents:
        print("Snippet not found in file.")
        print(old_snippet)
        raise Exception("Snippet not found in file. TODO: use a fuzzy string match algo.")
    new_contents = contents.replace(old_snippet, new_snippet)
    with open(clean_path, "w") as file:
        file.write(new_contents)

    return "Success"


functions = [ls, cat, tree, write_to_file, execute_bash_command, edit_file]
