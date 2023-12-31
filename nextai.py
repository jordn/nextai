from dotenv import load_dotenv
from termcolor import colored

from tools import functions
from utils.openai import chat_generate_text

load_dotenv()

def print_colored(text, color="green"):
    print(colored(text, color))


def read_file_tail(file_path, n_lines=10):
    with open(file_path, "r") as file:
        lines = file.readlines()
        tail = lines[-n_lines:]
    return "".join(tail)


model = "gpt-4-32k-0613"


def call_openai_api(chat_history):
    # Loads env vars (OPENAI_API_KEY) automatically
    return chat_generate_text(
        chat_history, model=model, functions=functions
    )["choices"][0]["message"]["content"]


system_message = """
    You are an AI assistant. Your job is to help the user with their programming tasks.
    The current environment is using node with npm with Nextjs, Typescript, and TailwindCSS.
    You can access some recent outputs of the Nextjs app. The full logs are in stdout.log and stderr.log.

    - use env vars for secrets like OPENAI_API_KEY
    - do not run 'npm run dev', VSCode is already running it for you
    - When you think of an action to take, do it yourself!
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

    # stdout_tail = read_file_tail("stdout.log")
    # stderr_tail = read_file_tail("stderr.log")
    chat_history.append(
        {
            "role": "user",
            "content": user_input,
        }
    )
    ai_response = call_openai_api(chat_history)
    chat_history.append({"role": "assistant", "content": ai_response})
    print_colored(ai_response, "green")
