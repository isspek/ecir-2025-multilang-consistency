import os
from dotenv import load_dotenv
import ollama

load_dotenv()


class OllamaModel:
    def __init__(self, model_id: str):
        self.model_id = model_id

    def request_llm(self, prompt: str, system_prompt: str = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = ollama.chat(model=self.model_id, messages=messages, options = {'temperature': 0, 'max_new_tokens': 2048, 'do_sample': False})
        response = response['message']['content']
        return response
