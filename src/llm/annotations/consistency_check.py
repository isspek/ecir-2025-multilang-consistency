import pandas as pd
import json
from tqdm import tqdm
from argparse import ArgumentParser
from src.llm.openai import OpenAIModel
from typing import List
from pydantic import BaseModel
from src.llm.annotations.utils import lang_mapping
from tqdm import tqdm

class Consistency(BaseModel):
    Label: str

parsing_prompt = "Evaluate the consistency between two answers, one in English and the other in <<LANGUAGE>>. Based on their content, return a consistency label without any explanation.\n" \
    "Consistency labels:\n" \
    "Consistent: If the English answer and the <<LANGUAGE>> answers are fully consistent or fully semantically aligned.\n" \
    "Partially consistent: If the English and the <<LANGUAGE>> answers partially agree, overlap or support each other with some irrelevant or contradictory content."\
    "Contradict: If the answers contradict each other.\n" \
    "Irrelevant: If the answers discuss different topics and are unrelated.\n\n" \
    "Think step by step."

discourse_elements =  {
    "answer_summary": "answer summary",
    "health_benefits_and_outcomes": "health benefits and outcome",
    "clinical_guidelines_and_evidence": "clinical guidelines and evidence",
    "individual_considerations_caveats": "individual considerations and caveats",
    "public_health_professional_advice": "public health and professional advice"
}

if __name__ == '__main__':
    openai_client = OpenAIModel(model_id='gpt-4o')
    parser = ArgumentParser()

    parser.add_argument('--bilingual')
    parser.add_argument('--second_language')
    parser.add_argument('--english_parsed_answers')
    parser.add_argument('--other_parsed_answers')
    parser.add_argument('--output_file')

    args = parser.parse_args()

    bilingual = args.bilingual
    second_language = args.second_language
    abb_lang = lang_mapping[second_language]

    english_parsed_answers = pd.read_csv(args.english_parsed_answers)[['en_claim', 'en_parsed_result']]
    english_parsed_answers = english_parsed_answers.to_dict(orient='records')

    other_parsed_answers = pd.read_csv(args.other_parsed_answers)
    other_parsed_answers = other_parsed_answers.to_dict(orient='records')

    output_file = args.output_file

    results = []
    for (english_answer, other_answer) in tqdm(zip(english_parsed_answers, other_parsed_answers),
                                               total=len(english_parsed_answers)):
        other_answer['en_parsed_result'] = english_answer['en_parsed_result']
        english_answer = json.loads(english_answer['en_parsed_result'])
        other_answer  = json.loads(other_answer[f'{abb_lang}_parsed_result'])



        for discourse_element_key, discourse_element_name in discourse_elements.items():
            _parsing_prompt = parsing_prompt.replace('<<LANGUAGE>>', second_language)

            english_discourse_unit = english_answer.get(discourse_element_key, None)
            other_discourse_unit = other_answer.get(discourse_element_key, None)

            if (english_discourse_unit is None) or (other_discourse_unit is None) or (len(english_discourse_unit)==0) or (len(other_discourse_unit)==0):
                label = ''
                if english_discourse_unit is None or len(english_discourse_unit) == 0:
                   label += 'NA for English '
                if other_discourse_unit is None or len(other_discourse_unit) == 0:
                    label += 'NA for Other'
                other_answer[discourse_element_key] = label
            else:
                client_prompt = f'===English===\n{english_discourse_unit}\n==={second_language}===\n{other_discourse_unit}'
                output = openai_client.request_llm(prompt=client_prompt, system_prompt=_parsing_prompt,
                                                   response_format=Consistency)
                other_answer[discourse_element_key] = output
        results.append(other_answer)
    results = pd.DataFrame(results)
    results.to_csv(output_file)