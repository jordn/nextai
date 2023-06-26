ui = f'''Given this app idea: {app_idea}

Describe the UI in detail'''

filesystem = f'''You are using Typescript and Chakra UI. Output a detailed filesystem layout for the code for the app above like the tree command JSON output with a description of each file. For example:
```
{"type":"directory","name":"new-project","contents":[
    {"type":"file","name":"NewProject.tsx"},
    {"type":"file","name":"schema.json"}
]}
```
'''

file_order = f'''
Given the above description of files, in which order should you implement the files so that you start with the interfaces/components which are reused the most and move to ones that are not depended upon
'''

commands = f'''
Given the description of the app, which commands would you run to set it up? Output only a JSON list of commands:
'''

# In what order should you implement the files based on the description above, prioritizing the interfaces/components that are most frequently reused and then proceeding to those that have fewer dependencies?


# Given the description of the app, what's the order to implement the files in the order of most reused interfaces/components and no dependencies?

# What's the optimal order for implementing files, starting with most reused interfaces/components and avoiding dependencies?