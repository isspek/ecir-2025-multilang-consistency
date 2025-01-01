import os
from typing import List, Dict
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from dotenv import load_dotenv
import ollama

load_dotenv()

class HFTFInferenceModel:
    def __init__(self, model_id:str):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id)

    def request_llm(self, prompt:str, system_prompt:str = None):        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        input_ids = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
        
        gen_tokens = self.model.generate(
            input_ids, 
            max_new_tokens=2048, 
            do_sample=False, 
            temperature=0.0,
            )

        response = self.tokenizer.decode(gen_tokens[0])
        return response
    
    
    