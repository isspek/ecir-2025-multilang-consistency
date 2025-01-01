import os
import pandas as pd
import random
import time
from argparse import ArgumentParser
from dotenv import load_dotenv
from tqdm import tqdm

import openai
from openai import OpenAI

load_dotenv()


# define a retry decorator
def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 10,
        errors: tuple = (openai.RateLimitError,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specified errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


@retry_with_exponential_backoff
def chatcompletions_with_backoff(**kwargs):
    '''
    Helper function to deal with the "openai.error.RateLimitError". If not used, the script will simply
    stop once the limit is reached, not saving any of the data generated until then. This method will wait
    and then try again, hence preventing the error.

    :param kwargs: List of arguments passed to the OpenAI API for completion.
    '''
    return CLIENT.chat.completions.create(**kwargs)


# OpenAI parameters
CLIENT = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"], organization=os.environ.get("OPENAI_ORG", None)
)

class OpenAIModel:
    def __init__(self, model_id):
        self.model = model_id

    def request_llm(self, prompt, system_prompt: object = None, response_format: object = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system",
                            "content": [{
                                "type": "text",
                                "text": system_prompt
                            }]})

        messages.append({"role": "user", "content": prompt})

        if response_format:
            response = CLIENT.beta.chat.completions.parse(
                model=self.model,
                temperature=0,
                max_tokens=2048,
                messages=messages,
                response_format=response_format
            )
            message = response.choices[0].message.content
            return message

        else:
            response = chatcompletions_with_backoff(
                model=self.model,
                temperature=0,
                max_tokens=2048,
                messages=messages
            )

            text = response.choices[0].message.content
            return text
