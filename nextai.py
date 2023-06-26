import os
from dotenv import load_dotenv
from termcolor import colored
from fastapi import FastAPI
import threading
import subprocess
import httpx

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# TODO: add cors
app = FastAPI()

errors = []

@app.post("/error")
def handle_error(error):
    print("Got error", error)
    errors.append(error)

@app.get("/errors")
def get_errors():
    return errors

# launch sub process in background task while redirecting all output to /dev/null
# This caused infinite loop
# thread = threading.Thread(target=lambda: subprocess.check_output(["uvicorn", "nextai:app", "--port", "3070"]))
# thread.start()
# uvicorn.run("nextai:app", host='0.0.0.0', port=3050)

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
    chat_history.append(
        {
            "role": "system",
            "content": f"{user_input}\n\nstdout tail:\n{stdout_tail}\n\nstderr tail:\n{stderr_tail}\nerrors:\n{errors}",
        }
    )
    ai_response = call_openai_api(chat_history)
    chat_history.append({"role": "assistant", "content": ai_response})
    print_colored(ai_response, "green")
