import pandas as pd
from argparse import ArgumentParser
from tqdm import tqdm
from src.llm.openai import OpenAIModel
from typing import List
from pydantic import BaseModel
from src.llm.annotations.utils import lang_mapping

class DiscourseStructure(BaseModel):
    answer_summary: str
    health_benefits_and_outcomes: List[str]
    clinical_guidelines_and_evidence: List[str]
    individual_considerations_caveats: List[str]
    public_health_professional_advice: List[str]

parsing_prompt = "Your task is to parse and categorize answers in <<LANGUAGE>> based on a discourse structure. I will provide an ontology for this discourse structure. If an element from the ontology is not present in the discourse of the answer, label it as N/A (Not Applicable). When parsing and categorizing, use the exact text from the answer without paraphrasing.\n" \
    "The elements of the discourse ontology are as follows:\n" \
    "answer_summary: The portion of the answer that directly addresses the question. Sentences that explain or elaborate on the summary are not part of the answer_summary.\n" \
    "health_benefits_and_outcomes: Describes the positive effects or results of a medical intervention or behavior.\n" \
    "clinical_guidelines_and_evidence: Refers to established guidelines or research that support the recommendations.\n" \
    "individual_considerations_caveats: Acknowledges variability among individuals emphasizes the need for personalized advice.\n" \
    "public_health_professional_advice: Highlights the importance of consulting healthcare professionals and adhering to public health recommendations. This also includes specific health recommendations or strategies that are  generally advised to improve health outcomes (e.g., dietary changes, exercise, or lifestyle modifications).\n" \
    "Think step by step."



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_file')
    parser.add_argument('--output_file')
    parser.add_argument('--language')
    parser.add_argument('--section', default='model_output')

    args = parser.parse_args()
    model = 'gpt-4o'
    openai_client = OpenAIModel(model_id=model)

    output_file = args.output_file
    data = pd.read_csv(args.input_file)
    language = args.language
    abbv_lang = lang_mapping[language]
    section = args.section

    results = []
    for idx, row in tqdm(data.iterrows(), total=len(data)):
        sample = row[section]
        _parsing_prompt = parsing_prompt.replace('<<LANGUAGE>>', language)
        output = openai_client.request_llm(prompt=sample, system_prompt=_parsing_prompt, response_format= DiscourseStructure)
        row[f'{abbv_lang}_parsed_result'] = output
        results.append(row)
    results = pd.DataFrame(results)
    results.to_csv(output_file)