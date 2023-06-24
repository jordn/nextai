import sys
import requests
import os
from termcolor import colored
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# HUMANLOOP_API_KEY = os.environ["HUMANLOOP_API_KEY"]


def print_colored(text, color="green"):
    print(colored(text, color))


def read_file_tail(file_path, n_lines=10):
    with open(file_path, "r") as file:
        lines = file.readlines()
        tail = lines[-n_lines:]
    return "".join(tail)


def call_openai_api(chat_history):
    print(chat_history)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {"model": "gpt-3.5-turbo", "messages": chat_history}
    response = requests.post(url, json=data, headers=headers)
    print(response.content)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"OpenAI Error: {response.status_code}"


def call_humanloop_api(chat_history):
    url = "https://api.humanloop.com/v4/chat"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        # "X-API-KEY": HUMANLOOP_API_KEY,
    }
    payload = {
        "messages": chat_history,
        "model_config": {
            "provider": "openai",
            "endpoint": "chat",
            "chat_template": [{"role": "system", "content": system_message}],
            "max_tokens": -1,
        },
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["messages"][-1]["message"]
    else:
        return f"Humanloop Error: {response.status_code}"


system_message = """
You are a helpful assistant that is extremely proficient at writing code, especially python and nextjs with Typescript and Tailwindcss. You are given a running nextjs app and are given the last stdout and stderr messages. Please assist the user in fixing and changing the app as they ask.

    - use typing (or type hints)
    - Think step by step
    - write pseudocode first before you write code as it is helpful
    - separate all code with 3 backticks
    - use env vars for secrets like OPENAI_API_KEY
"""

# Set up
chat_history = [{"role": "system", "message": system_message}]
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
    user_message = (
        f"{user_input}\n\nstdout tail:\n{stdout_tail}\n\nstderr tail:\n{stderr_tail}"
    )
    chat_history.append({"role": "user", "content": user_message})

    ai_response = call_openai_api(chat_history)
    chat_history.append({"role": "assistant", "content": ai_response})

    print_colored(ai_response, "green")
