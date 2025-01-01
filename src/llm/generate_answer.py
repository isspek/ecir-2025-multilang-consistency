#import sys
#sys.path.append('../parentdirectory')

import pandas as pd
from tqdm import tqdm
from src.llm.all_models import initiate_model
from argparse import ArgumentParser
import ollama

parser = ArgumentParser()
parser.add_argument('--language')
parser.add_argument('--input_file')
parser.add_argument('--output_file')
parser.add_argument('--model')
parser.add_argument('--run_option', choices=['hf_api', 'hf_tf', 'ollama', 'gpt_api'])

args = parser.parse_args()

print('Starting...')

languages = {
    'en': 'en_claim',
    'de': 'de_claim',
    'tr': 'translation',
    'zh': 'translation'
}

language = args.language
corresponding_column = languages[args.language]
input_file = args.input_file
output_file = args.output_file
data = pd.read_csv(input_file)
model = args.model
run_option = args.run_option

client = initiate_model(model_id=model, run_option=run_option)

system_prompts = {
    'tr': 'Please answer the question in Turkish',
    'zh': 'Please answer the question in Chinese'
}

responses = []
for index, row in tqdm(data.iterrows(), total=len(data)):
    if ('llama' in model.lower() or 'command-r-plus' in model.lower()) and (language == 'tr' or language=='zh'):
        system_prompt = system_prompts[language]
        generated_sentence = client.request_llm(prompt=row[corresponding_column], system_prompt=system_prompt)
    else:
        generated_sentence = client.request_llm(prompt=row[corresponding_column])
    row['model_output'] = generated_sentence
    responses.append(row)

responses = pd.DataFrame(responses)
responses.to_csv(output_file, index=False)