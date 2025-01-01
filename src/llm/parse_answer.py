import pandas as pd
from argparse import ArgumentParser
from tqdm import tqdm

from src.llm.openai import request_openai
from src.llm.prompts import PARSING_PROMPT

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--model', default='gpt-4o-mini')
    parser.add_argument('--input_file')
    parser.add_argument('--output_file')
    parser.add_argument('--language')

    args = parser.parse_args()

    model = args.model
    input_file = args.input_file
    output_file = args.output_file
    data = pd.read_csv(input_file)

    languages = {
        'en': 'en_claim',
        'de': 'de_claim'
    }

    corresponding_column = languages[args.language]

    responses = []
    for index, row in tqdm(data.iterrows(), total=len(data)):
        question = row[corresponding_column]
        answer = row['model_output']
        prompt = f'Question:\n{question}\nAnswer:\n{answer}'
        generated_sentence = request_openai(prompt=prompt, model=model, system_prompt=PARSING_PROMPT)
        row['parsed_answer'] = generated_sentence
        responses.append(row)

    responses = pd.DataFrame(responses)
    responses.to_csv(output_file, index=False)
