import os
from dotenv import load_dotenv
from termcolor import colored
import httpx

load_dotenv()

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
        chat_history, model=model, functions=functions
    )["choices"][0]["message"]["content"]


system_message = """
You are a helpful assistant that is extremely proficient at writing code, especially python and nextjs with Typescript and Tailwindcss. You are given a running nextjs app and are given the last stdout and stderr messages. Please assist the user in fixing and changing the app as they ask.

    - use typing (or type hints)
    - separate all code with 3 backticks
    - use env vars for secrets like OPENAI_API_KEY
"""

# Set up
chat_history = [{"role": "system", "content": system_message}]
print_colored("Starting the dev server", "blue")

# Kick off the dev server piping stdout and stderr to files
os.system("npm run dev > stdout.log 2> stderr.log &")

print_colored(
    "Welcome to the chatbot! Type your message below or type 'exit' to quit.", "yellow"
)


while True:
    print(">", end=" ")
    user_input = input()
    if user_input.lower() == "exit":
        break

    stdout_tail = read_file_tail("stdout.log")
    stderr_tail = read_file_tail("stderr.log")
    frontend_errors = httpx.get("http://localhost:3070/errors").json()
    chat_history.append(
        {
            "role": "system",
            "content": f"{user_input}\n\nstdout tail:\n{stdout_tail}\n\nstderr tail:\n{stderr_tail}\nerrors:\n{frontend_errors}",
        }
    )
    ai_response = call_openai_api(chat_history)
    chat_history.append({"role": "assistant", "content": ai_response})
    # Takes two tries to fix the error, if we delete before then it won't fix by itself
    # httpx.delete("http://localhost:3070/errors")
    print_colored(ai_response, "green")
