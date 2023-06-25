import os
from typing import List

from .ai_utils.simplechat import ChatConversation

from func_tools.basic_fs import functions,cat

system = """
You are BabyAGI, a helpful AI.
Your job is to complete an objective for the user.
You are very forgetful, so you must occasionally write down your thoughts/insights/plans in a notebook.
"""

objective = "There's a codebase in the current directory. Tell the user how it works (in plain English). Then write a README.md file that explains how it works."


import os
api_key = os.environ['OPENAI_API_KEY']

convo = ChatConversation(system=system)
convo.messages.append({
    "role":"user",
    "content":objective,
})

print("\n"*10,"Starting","\n"*10)

while True:
    print("-" * 50 + "Running new iter" + "-" * 50)
    completion = convo.generate(functions=functions)
    print(completion)
    resp = input("Press enter to continue. Press q to quit.")
    if resp == "q":
        break
    else:
        convo.messages.append({
            "role":"user",
            "content":resp,
        })

print(cat("README.md"))
print(f"Done. Saved in folder {convo.id}.")