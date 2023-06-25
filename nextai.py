import os
import sys
from pprint import pformat, pprint

import requests
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def print_colored(text, color="green"):
    print(colored(text, color))


def read_file_tail(file_path, n_lines=10):
    with open(file_path, "r") as file:
        lines = file.readlines()
        tail = lines[-n_lines:]
    return "".join(tail)


from old_code.ai_utils.simplechat import chat_generate_text

model = "gpt-4-32k-0613"
from func_tools.basic_fs import functions


def call_openai_api(chat_history):
    return chat_generate_text(
        chat_history, OPENAI_API_KEY, model=model, functions=functions
    )["choices"][0]["message"]["content"]


system_message = """
    You are a coder. Your job is to build things for your project manager.
    The current environment is using node with npm with Nextjs, Typescript, and TailwindCSS.
    You will be given some recent outputs of the Nextjs app. The full logs are in stdout.log and stderr.log.

    - use env vars for secrets like OPENAI_API_KEY
    - When you want think of a command/action, do it yourself! Use cat, ls, write_to_file, execute_bash_command, etc.
"""

# Set up
chat_history = [{"role": "system", "content": system_message}]

print_colored(
    "Welcome to the chatbot! Type your message below or type 'exit' to quit.", "blue"
)


while True:
    print(">", end=" ")
    user_input = input()
    if user_input.lower() == "exit":
        break

    stdout_tail = read_file_tail("stdout.log")
    stderr_tail = read_file_tail("stderr.log")
    chat_history.append(
        {
            "role": "system",
            "content": f"{user_input}\n\nstdout tail:\n{stdout_tail}\n\nstderr tail:\n{stderr_tail}",
        }
    )
    print(chat_history)
    ai_response = call_openai_api(chat_history)
    chat_history.append({"role": "assistant", "content": ai_response})
    print_colored(ai_response, "green")
