import os

from dotenv import load_dotenv
from termcolor import colored

from tools import functions
from utils.logging import print_assistant, print_system
from utils.openai import chat_generate_text

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def read_file_tail(file_path, n_lines=10):
    with open(file_path, "r") as file:
        lines = file.readlines()
        tail = lines[-n_lines:]
    return "".join(tail)


model = "gpt-4-32k-0613"


def call_openai_api(chat_history):
    response = chat_generate_text(chat_history, model=model, functions=functions)
    return response["choices"][0]["message"]["content"]


system_message = """
You are a coder. Your job is to build things for your project manager.
The current environment is using node with npm with Nextjs, Typescript, and TailwindCSS.
You will be given some recent outputs of the Nextjs app.
The full logs are in stdout.log and stderr.log.

- use env vars for secrets like OPENAI_API_KEY
- When you think of an action to take, do it yourself!
- do not run 'npm run dev', VSCode is already running it for you
- write clean, terse code. Look for simplifications and helpful abstractions.
- Channel your inner Rich Hickley. Aim for simple, non-complex code.
"""

# Set up
chat_history = [{"role": "system", "content": system_message}]

print_system("Welcome to CodePilot! Type your message below or type 'exit' to quit.")


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
    ai_response = call_openai_api(chat_history)
    chat_history.append({"role": "assistant", "content": ai_response})
    print_assistant(ai_response)
