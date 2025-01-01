import pandas as pd
from tqdm import tqdm

from src.wikidata import fetch_wd_props


def aggregate_category(props):
    print(props)
    aggregated_category = None
    if any('symptom' in phrase for phrase in props['type']) or any(
            'clinical sign' in phrase for phrase in props['type']):
        aggregated_category = 'symptom'
    elif any('cancer' in phrase for phrase in props['wd_main_class_level_1']) or \
            any('cancer' in phrase for phrase in props['wd_main_class_level_2']) or \
            'oncology' in props['health_speciality']:
        aggregated_category = 'cancer'
        return aggregated_category
    elif any('diabetes' in phrase for phrase in props['wd_main_class_level_1']) or \
            any('diabetes' in phrase for phrase in props['wd_main_class_level_2']) or \
            'diabetology' in props['health_speciality']:
        aggregated_category = 'diabetes'
        return aggregated_category
    elif any('cardiovascular disease' in phrase for phrase in props['wd_main_class_level_1']) or \
            any('cardiovascular disease' in phrase for phrase in props['wd_main_class_level_2']) or \
            'cardiology' in props['health_speciality']:
        aggregated_category = 'cardiovascular diseases'
        return aggregated_category
    elif any('urological' in phrase.split() for phrase in props['wd_main_class_level_1']) or any(
            'urological' in phrase.split() for phrase in props['wd_main_class_level_2']) \
            or (len(props['health_speciality']) == 1 and 'urology' in props['health_speciality']):
        aggregated_category = 'urological diseases'
        return aggregated_category
    elif 'infectious diseases' in props['health_speciality']:
        aggregated_category = 'infectious diseases'
        return aggregated_category
    elif 'psychiatry' in props['health_speciality'] or 'psychology' in props['health_speciality'] or any(
            'anxiety' in phrase.split() for phrase in props['wd_main_class_level_1']):
        aggregated_category = 'mental health disorders and diseases'
        return aggregated_category
    elif (len(props['health_speciality']) == 1 and 'dermatology' in props['health_speciality']) or any(
            'skin' in phrase.split() for phrase in props['wd_main_class_level_1']) or any(
            'skin' in phrase.split() for phrase in props['wd_main_class_level_2']):
        aggregated_category = 'skin diseases'
        return aggregated_category
    elif 'women\'s health' in props['facet_of']:
        aggregated_category = 'women\'s health'
        return aggregated_category
    elif 'gastroenterology' in props['health_speciality']:
        aggregated_category = 'gastrointestinal diseases'
    elif 'orthopedics' in props['health_speciality']:
        aggregated_category = 'orthopedic disorders'
    elif any('perinatal' in phrase.split() for phrase in props['wd_main_class_level_1']):
        aggregated_category = 'perinatal disease'
    elif 'neurology' in props['health_speciality']:
        aggregated_category = 'neurological disorders'
    elif 'endocrinology' in props['health_speciality']:
        aggregated_category = 'other endocrine diseases'
    else:
        aggregated_category = 'other'

    return aggregated_category


if __name__ == '__main__':
    data = pd.read_csv('data/healthfc/healthFC_diseases_wd_maps.csv')
    output = 'data/healthfc/healthFC_diseases_wd_info.csv'

    data_with_wdids = data[data['wd'] != 'no_wd']

    wd_ids = data_with_wdids['wd'].unique()

    print(f'Number of unique wds: {len(wd_ids)}')
    processed_data = []
    batches = []

    for wd_id in tqdm(wd_ids, total=len(wd_ids)):
        if wd_id in ['Q164778', 'Q15787', 'Q221179', 'Q874632']:  # todo check it later
            continue
        batches.append(wd_id)
        print(f'Checking {batches}')
        if len(batches) % 1 == 0:
            results = fetch_wd_props(batches)
            for wd_id, props in results.items():
                aggregated_category = aggregate_category(props)
                data = {
                    'wd': wd_id,
                    'type': props['type'],
                    'main_class_level_1': list(props['wd_main_class_level_1']),
                    'main_class_level_2': list(props['wd_main_class_level_2']),
                    'health_speciality': list(props['health_speciality']),
                    'facet_of': props['facet_of'],
                    'aggregated_category': aggregated_category

                }
                processed_data.append(data)
            batches.clear()

    # assign an aggregate class

    processed_data = pd.DataFrame(processed_data)
    not_categorized = len(processed_data[processed_data['aggregated_category'].isnull()])
    print('Number of not categorized wds', not_categorized)

    print(processed_data.groupby(['aggregated_category'])['wd'].count())
    processed_data.to_csv(output, index=False)
