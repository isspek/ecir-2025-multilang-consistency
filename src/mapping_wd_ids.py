import pandas as pd
from tqdm import tqdm

from src.wikidata import label_to_wd

preprocessing_mapping = {
    'covid 19 disease': 'covid 19',
    'covid-19 disease': 'covid 19',
    'diabetes-related retinal diseases': 'diabetic retinopathy',
    'infection with hiv': 'human immunodeficiency virus infectious disease',
    'corona infections': 'covid 19',
    'corona infection': 'covid 19',
    'lip herpes': 'herpes labialis',
    'cardiomyopathy': 'heart muscle weakness',
    'benign enlarged prostate': 'prostatic hypertrophy',
    'bacterial or fungal infection': 'fungal infectious disease',
    'infection with coronavirus': 'covid 19'
}


def preprocess(disease: str):
    if disease in preprocessing_mapping:
        disease = preprocessing_mapping[disease]
    return disease


if __name__ == '__main__':
    data = pd.read_json('data/healthfc/healthFC_annotated_with_entities.jsonl', lines=True)
    output = 'data/healthfc/healthFC_diseases_wd_maps.csv'
    data = data[data['mentioning_disease']]

    wd_mapping = pd.read_csv('data/wd_augmented_data.csv')

    print(f'Number of samples with mentioning disease: {len(data)}')

    flatten_diseases = set()

    for disease_lst in data['diseases'].tolist():
        for disease in disease_lst:
            flatten_diseases.add(disease)

    flatten_diseases = list(flatten_diseases)

    not_found = 0
    processed_data = []
    for disease in tqdm(flatten_diseases, total=len(flatten_diseases)):
        sample = {'disease': disease}
        disease = disease.lower()
        disease = preprocess(disease)
        results = wd_mapping[wd_mapping['itemLabel'] == disease]['wd'].values

        if len(results) > 0:
            wd_id = results[0]
        else:
            wd_id = label_to_wd(disease)
            if not wd_id:
                print(f'{disease} has no associated wd')
                not_found += 1
                wd_id = 'no_wd'
        sample['wd'] = wd_id
        processed_data.append(sample)

    pd.DataFrame(processed_data).to_csv(output, index=False)
    print(f"not found wd ids: {not_found}")
