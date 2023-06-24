import os
from typing import Callable, Optional, Union, List
import openai
from nanoid import generate
from json import loads, dumps

from .openaifuncs import call_functions, parse_function
import backoff
from openai.error import APIError, APIConnectionError

DEFAULT_BASE_URL = "https://api.openai.com/v1"


# From https://gist.github.com/pszemraj/c643cfe422d3769fd13b97729cf517c5, adds type information


@backoff.on_exception(backoff.expo, (APIError, APIConnectionError))
def chat_generate_text(
    messages: list[dict] | str,
    api_key: str = None,
    api_base_url: str = DEFAULT_BASE_URL,
    model: str = "gpt-3.5-turbo-16k-0613",
    temperature: float = 0.5,
    max_tokens: int = 256,
    n: int = 1,
    stop: Optional[Union[str, list]] = None,
    presence_penalty: float = 0,
    frequency_penalty: float = 0.1,
    functions: list[Callable] = [],
) -> List[str]:
    """
    chat_generate_text - Generates text using the OpenAI API.
    :param str prompt: prompt for the model
    :param str api_key: api key for the OpenAI API, defaults to None
    :param str api_base_url: api key for the OpenAI API, defaults to https://api.openai.com/v1
    :param str model: model to use, defaults to "gpt-3.5-turbo"
    :param str system_prompt: initial prompt for the model, defaults to "You are a helpful assistant."
    :param float temperature: _description_, defaults to 0.5
    :param int max_tokens: _description_, defaults to 256
    :param int n: _description_, defaults to 1
    :param Optional[Union[str, list]] stop: _description_, defaults to None
    :param float presence_penalty: _description_, defaults to 0
    :param float frequency_penalty: _description_, defaults to 0.1
    :return List[str]: _description_
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", None)
    assert api_key is not None, "OpenAI API key not found."

    if api_base_url is DEFAULT_BASE_URL:
        api_base_url = os.environ.get("OPENAI_API_BASE", DEFAULT_BASE_URL)

    openai.api_key = api_key
    openai.api_base = api_base_url

    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    opts = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "n": n,
        "stop": stop,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
    }
    func_opts = (
        {"functions": [parse_function(f) for f in functions]}
        if len(functions) > 0
        else {}
    )
    response = openai.ChatCompletion.create(**opts, **func_opts, messages=messages,stream=True)
    output = []
    for chunk in response:
        output.append(chunk)
        print(chunk)
    # print(response)

    raise Exception("TODO: implement this")

    if not any([c["finish_reason"] == "function_call" for c in response["choices"]]):
        return response

    new_messages, should_continue = call_functions(response, *functions)

    def process(dct):
        return loads(dumps(dct))

    messages.extend(process(new_messages))
    if should_continue:
        return chat_generate_text(
            messages,
            api_key,
            api_base_url,
            model,
            temperature,
            max_tokens,
            n,
            stop,
            presence_penalty,
            frequency_penalty,
            functions,
        )
    else:
        return response


key = os.environ.get("OPENAI_API_KEY", None)

if key is None:
    raise Exception("OpenAI API key not found.")

def ls(path:str)->str:
    """
    Lists the files in a directory.
    """
    return "a.txt\nb.txt\nc.txt"


chat_generate_text("What files are in the current directory?", api_key=key,functions=[ls])