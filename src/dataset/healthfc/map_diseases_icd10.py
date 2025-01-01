from src.utils import ICD10Code
import pandas as pd

if __name__ == '__main__':
    icd10code = ICD10Code()
    output_file = 'data/healthfc/healthFC_diseases_wd_icd10_maps_v2.csv'
    diseases_wd_mapping = pd.read_csv('data/healthfc/healthFC_diseases_wd_icd10_maps.csv')
    diseases_wd_mapping['icd_disease_category'] = diseases_wd_mapping['predicted_icd10_code'].apply(lambda x: icd10code.assign_code_to_disease_category(x))
    diseases_wd_mapping.to_csv(output_file, index=False)