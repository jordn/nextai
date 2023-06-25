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
    """Generates text using the OpenAI API.

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
    response = openai.ChatCompletion.create(**opts, **func_opts, messages=messages)
    # print(response)

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


class ChatConversation:
    """This class can be used to persist message history across calls, or simply to track the history of calls without sending the history (amnesia mode)."""

    def __init__(
        self,
        save_dir: str = "output",
        amnesia: bool = False,
        system: Optional[str] = "You are an AI assistant.",
        functions: list[Callable] = [],
    ):
        self.amnesia = amnesia
        self.save_dir = save_dir
        # The raw responses from openAI API
        self.raw_messages: List[dict] = []

        # messages that can be passed as input to the API
        self.messages: List[dict] = []
        self.id = None
        self.folder_path = None

        self.functions = functions

        if system:
            self.messages.append({"role": "system", "content": system})

    def save(self):
        if self.id is None:
            self.id = generate()
            # self.id = get_timestamp()
            self.folder_path = os.path.join(self.save_dir, self.id)
            os.makedirs(self.folder_path)

        json_path = os.path.join(self.folder_path, f"_json.txt")
        with open(json_path, "w") as json_file:
            json_file.write(dumps(self.messages))

        summary_path = os.path.join(self.folder_path, f"_summary.txt")
        with open(summary_path, "w") as summary:
            for i, message in enumerate(self.messages):
                role = message["role"]
                file_path = os.path.join(self.folder_path, f"{i+1}_{role}.txt")
                with open(file_path, "w") as file:
                    summary.write(f"\n{i+1}. {role}:\n")
                    content = message["content"]
                    if content is not None:
                        file.write(content)
                        summary.write(content)
                    if "function_call" in message:
                        function_call = message["function_call"]
                        string = f"""
Function call: {function_call['name']}
Arguments: {function_call['arguments']}
    """
                        file.write(string)
                        summary.write(string)

        # print(f"Conversation history saved in folder: {self.folder_path}")

    def reset(self):
        self.id = None
        self.messages = []
        self.raw_messages = []

    def generate(
        self,
        message: Optional[str] = None,
        functions: list[Callable] = [],
        **kwargs,
    ) -> str:
        if message is not None:
            self.messages.append({"role": "user", "content": message})
        response = chat_generate_text(
            self.messages, max_tokens=None, functions=functions, **kwargs
        )
        self.raw_messages.append(response)
        response_message = response["choices"][0]["message"]
        if response_message not in self.messages:
            self.messages.append(dict(response_message))
        self.save()
        if self.amnesia:
            self.reset()
        return response_message.content
