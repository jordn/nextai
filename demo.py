import subprocess

# Set up the subprocess to run an interactive bash session
proc = subprocess.Popen(
    "bash",
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,
)

# Loop to read user input and pass it to the subprocess
# Then, print subprocess output to the screen
try:
    while proc.poll() is None:
        # Read user input from the CLI and encode it
        user_input = input().encode()

        # Write the user input to the subprocess stdin
        proc.stdin.write(user_input + b'\n')
        proc.stdin.flush()

        # Print the subprocess output
        while True:
            output = proc.stdout.readline()
            if not output:
                break
            print(output.decode(), end="")
except KeyboardInterrupt:
    # Close the subprocess in case of Ctrl+C
    proc.terminate()