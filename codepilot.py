import os
import selectors
import subprocess
import threading

from dotenv import load_dotenv
from termcolor import colored

from tools import functions
from utils.logging import print_assistant, print_system
from utils.openai import chat_generate_text

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = "gpt-4-32k-0613"


def read_file_tail(file_path, n_lines=10):
    with open(file_path, "r") as file:
        lines = file.readlines()
        tail = lines[-n_lines:]
    return "".join(tail)


def call_openai_api(chat_history):
    response = chat_generate_text(chat_history, model=MODEL, functions=functions)
    return response["choices"][0]["message"]["content"]


def run_server():
    nextjs_dir = os.path.join(os.getcwd(), "nextjs")
    with open(stdout_file_path, "wb") as stdout_file, open(
        stderr_file_path, "wb"
    ) as stderr_file:
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=nextjs_dir,
            text=True,
        )
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        selector.register(process.stderr, selectors.EVENT_READ)

        while process.poll() is None:
            for key, _ in selector.select():
                line = key.fileobj.readline()
                # TODO: right align?
                if key.fileobj == process.stdout:
                    print(colored("  " + line.strip()))
                    stdout_file.write(line.encode())
                elif key.fileobj == process.stderr:
                    print(colored("  " + line.strip(), "red"))
                    stderr_file.write(line.encode())

        process.communicate()
        process.communicate()


system_message = """
You are an senior staff software engineer.
Your job is to build things for your project manager.
The current environment is using node with npm with Nextjs, Typescript, and TailwindCSS.
You will be given some recent outputs of the Nextjs app.
The full logs are in stdout.txt and stderr.txt

- use env vars for secrets like OPENAI_API_KEY
- When you think of an action to take, do it yourself!
- do not run 'npm run dev', VSCode is already running it for you
- write clean, terse code. Look for simplifications and helpful abstractions.
- Channel your inner Rich Hickley. Aim for simple, non-complex code.
"""
chat_history = [{"role": "system", "content": system_message}]


stdout_file_path = "stdout.txt"
stderr_file_path = "stderr.txt"


def main():
    nextjs_dir = os.path.join(os.getcwd(), "nextjs")
    if not os.path.exists(nextjs_dir):
        print("Initializing Next.js app...")
        subprocess.run(["npx", "create-next-app", "nextjs"], check=True)
        print("Next.js app initialized successfully!")
    else:
        print("Next.js app already exists, skipping initialization.")

    if os.path.exists(stdout_file_path) or os.path.exists(stderr_file_path):
        print(
            "Log files exist, assuming 'npm run dev' is already running. Please stop the existing process before running this script."
        )
        return

    print("Running 'npm run dev' in the 'nextjs' subdirectory...")
    command_thread = threading.Thread(target=run_server)
    command_thread.start()

    try:
        print_system(
            "Welcome to CodePilot! Type your message below. Use Ctrl+C to quit."
        )
        while True:
            # TODO: get this to be pinned to the bottom.
            print(">", end=" ")
            user_input = input()
            if user_input.lower() == "exit":
                break
            stdout_tail = read_file_tail(stdout_file_path)
            stderr_tail = read_file_tail(stderr_file_path)
            chat_history.append(
                {
                    "role": "system",
                    "content": f"stdout tail:\n{stdout_tail}\n\nstderr tail:\n{stderr_tail}",
                }
            )
            chat_history.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )
            ai_response = call_openai_api(chat_history)
            chat_history.append({"role": "assistant", "content": ai_response})
            print_assistant(ai_response)
    except KeyboardInterrupt:
        print("\nCtrl+C detected, terminating server...")
    finally:
        if os.path.exists(stdout_file_path):
            os.remove(stdout_file_path)
        if os.path.exists(stderr_file_path):
            os.remove(stderr_file_path)


if __name__ == "__main__":
    main()
