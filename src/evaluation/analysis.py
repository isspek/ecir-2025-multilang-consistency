import json
import pandas as pd
from json.decoder import JSONDecodeError
from argparse import ArgumentParser
import numpy as np

def extract_label(response: str):
    if response != 'Consistent':
        return 'Inconsistent'
    else:
        return 'Consistent'

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_file')
    args = parser.parse_args()
    input_file = args.input_file

    results = pd.read_csv(input_file)
    disease_category = 'Disease_Category'


    results['text_len'] = results['model_output'].apply(lambda x: len(x))

    print('Average response')
    print(np.mean(results['text_len'].to_numpy()))

    columns = ['answer_summary', 'health_benefits_and_outcomes', 'clinical_guidelines_and_evidence', 'individual_considerations_caveats' , 'public_health_professional_advice']


    for column in columns:
        results[f'{column}_label'] = results[column].apply(lambda x: extract_label(response=x))
        group_counts = results.groupby([f'{column}_label'])['en_claim'].count()
        proportions = group_counts / len(results)

        # print('Consistency-Results (Binary)')
        # print(proportions)

        category_totals = results.groupby(disease_category)['en_claim'].count()
        group_counts = results.groupby([f'{column}_label', disease_category])['en_claim'].count()
        proportions = group_counts / group_counts.index.get_level_values(disease_category).map(category_totals)
        proportions = proportions.groupby(f'{column}_label', group_keys=False).apply(
            lambda x: x.sort_values(ascending=False))

        # print('Per Disease Category Proportions')
        # print(proportions)
