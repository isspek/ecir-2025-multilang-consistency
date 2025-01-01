import pandas as pd

if __name__ == '__main__':
    disease_wd_mapping = pd.read_csv('data/wd_diseases_enriched.csv')
    disease_wd_mapping_v2 = pd.read_csv('data/wd_diseases_enriched_v2.csv')
    syndrome_wd_mapping = pd.read_csv('data/wd_syndrome_enriched.csv')
    clinical_signs_wd_mapping = pd.read_csv('data/wd_clinical_signs_enriched.csv')
    symptom_wd_mapping = pd.read_csv('data/wd_symptoms_enriched.csv')

    augmented_data = pd.concat(
        [disease_wd_mapping, disease_wd_mapping_v2, symptom_wd_mapping, syndrome_wd_mapping, clinical_signs_wd_mapping])
    augmented_data['itemLabel'] = augmented_data['itemLabel'].apply(lambda x: x.lower())
    augmented_data.drop_duplicates(keep='first', inplace=True)

    print(f'Number of samples: {len(augmented_data)}')

    augmented_data.to_csv('data/wd_augmented_data.csv', index=False)
