import json
from inspect import signature
import os

from docstring_parser import parse
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class Message:
    role: str
    name: str
    content: str


def parse_function(func):
    """Creates JSON Schema from docstring and type annotations.

    Automatically create a signature for GPT functions

    :param func:
    :return:
    """
    docs = parse(func.__doc__)
    param_docs = {p.arg_name: p for p in docs.params}
    sig = signature(func)
    required = [
        k for k, v in sig.parameters.items() if v.kind == v.POSITIONAL_OR_KEYWORD
    ]

    properties = {
        name: parse_parameter(p.annotation, param_docs.get(name))
        for name, p in sig.parameters.items()
    }
    descriptor = {
        "name": func.__name__,
        "description": docs.short_description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }
    return descriptor


def call_functions(response, *functions):
    """Execute the functions using the initial responses.

    :param response:
    :param functions:
    :return:
    """
    messages = []
    should_continue = False
    # todo: this doesn't make much sense. There should only be one choice unless n > 1
    # and then if that was the case we wouldn't just want to append them all to a flat list.
    for c in response["choices"]:
        if c["finish_reason"] == "function_call":
            msg = c["message"]
            messages.append(msg)
            func_data = msg["function_call"]
            try:
                args = json.loads(func_data["arguments"])
            except:
                print("Error parsing arguments for function call")
                print("Function call:", func_data)
                # TODO: raise an error here
                raise
                input("What to do?")
            name = func_data["name"]

            for f in functions:
                if f.__name__ == name:
                    try:
                        result = f(**args)
                    except Exception as e:
                        # TODO: raise an error here
                        result = f"Error: e"
                    if result != "__pass__":
                        # TODO: does this ever happen?
                        should_continue = True
                    messages.append(
                        {
                            "role": "function",
                            "name": name,
                            "content": json.dumps(result),
                        }
                    )
    return messages, should_continue


def parse_annotation(annotation):
    """Convert the type annotation to type string for json

    :param annotation:
    :return:
    """
    # TODO how to reliably map python type hint to json type?
    return {"str": "string", "int": "number", "float": "number", "bool": "boolean"}[
        annotation.__name__
    ]


def parse_parameter(annotation, docs):
    """Convert the parameter signature and docstring
    to json for function API.

    :param annotation:
    :param docs:
    :return:
    """
    type_name = parse_annotation(annotation)
    return {
        "type": type_name,
        "description": docs.description if docs is not None else "",
    }
