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
