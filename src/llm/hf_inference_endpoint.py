import os
import sqlite3
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    conn = sqlite3.connect('llama3_responses.db')
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_response(prompt, response):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (prompt, response)
        VALUES (?, ?)
    ''', (prompt, response))
    conn.commit()
    conn.close()

def get_response(prompt):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT response FROM responses
        WHERE prompt = ?
    ''', (prompt,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

class HFInferenceEndpointModel:
    def __init__(self, model_id:str):
        self.model_id = model_id
        print(f'Getting answers from {self.model_id}')
        self.client = InferenceClient(model=model_id, token=os.environ["HF_TOKEN"])
        create_table()

    def request_llm(self, prompt: str, system_prompt: str = None):
        response = get_response(prompt)
        if response:
            return response

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})
        response = self.client.chat_completion(messages, max_tokens=2048, temperature=0.0, seed=0)
        response = response.choices[0].message.content
        save_response(prompt, response)
        return response


# if __name__ == '__main__':
#     model_id = 'meta-llama/Meta-Llama-3-70B-Instruct'
#     HFInferenceModel(model_id).request_llm(prompt='Daha düşük tuz diyeti kardiyovasküler hastalık olasılığını azaltır mı?')