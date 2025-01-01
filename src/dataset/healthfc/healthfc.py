import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
from typing import Dict, List


def tag_disease_category(diseases: List[str])-> str:
    for disease in diseases:
        if disease not in disease_categories:
            continue
        else:
            return disease_categories[disease]
    return 'Other health topic'

if __name__ == '__main__':
    data_path = 'data/healthfc/healthFC_annotated_with_entities.jsonl'
    icd10_mapping = pd.read_csv('data/healthfc/healthFC_diseases_wd_icd10_maps_v2.csv')
    # output_main_file = 'data/healthfc/healthFC_final.csv'
    # output_sampled_file = 'data/healthfc/healthFC_final_sampled.csv'
    output_sampled_file = 'data/healthfc/healthFC_small_sampled.csv'

    disease_categories = {}
    for idx, row in icd10_mapping.iterrows():
        disease = row['disease']
        disease_category = row['icd_disease_category']
        if disease not in disease_categories:
            disease_categories[disease] = disease_category

    data = pd.read_json(data_path, lines=True)

    print('Number of samples-FULL set', len(data))

    samples_mentioning_diseases = data[data['mentioning_disease']]
    print(f'Number of samples mentioning diseases: {len(samples_mentioning_diseases)}')

    # catgeorized disease
    samples_mentioning_diseases['Disease_Category'] = samples_mentioning_diseases['diseases'].apply(
        lambda x: tag_disease_category(x))

    # filter out samples tagged with 'Other health topic'
    samples_mentioning_diseases = samples_mentioning_diseases[samples_mentioning_diseases['Disease_Category'] != 'Other health topic']

    print(f'Filtered number of samples: {len(samples_mentioning_diseases)}')

    category_counts = samples_mentioning_diseases.groupby('Disease_Category')['en_claim'].count()
    categories_with_20_or_more = category_counts[category_counts >= 20].index
    filtered_samples = samples_mentioning_diseases[
        samples_mentioning_diseases['Disease_Category'].isin(categories_with_20_or_more)]


    # check stats
    ranked_disease_categories = filtered_samples.groupby('Disease_Category')['en_claim'].count().sort_values(
        ascending=False)
    print(ranked_disease_categories)

    print(f'Number of filtered samples: {len(filtered_samples)}')

    # filtered_samples.to_csv(output_main_file, index=False)

    # sampled_data = filtered_samples.groupby('Disease_Category', group_keys=False).apply(
    #     lambda x: x.sample(n=20, random_state=42) if len(x) >= 20 else x
    # )
    sampled_data = filtered_samples.groupby('Disease_Category', group_keys=False).apply(
        lambda x: x.sample(n=1, random_state=42) if len(x) >= 1 else x
    )

    print(f'Number of sampled data: {len(sampled_data)}')
    sampled_data.to_csv(output_sampled_file, index=False)

