import re
import pandas as pd

ICD_MAPPING = {
    'A00-B99': 'Certain infectious and parasitic diseases',
    'C00-D49': 'Neoplasms',
    'D50-D89': 'Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism',
    'E00-E89': 'Endocrine, nutritional and metabolic diseases',
    'F00-F99': 'Mental, Behavioral and Neurodevelopmental disorders',
    'G00-G99': 'Diseases of the nervous system',
    'H00-H59': 'Diseases of the eye and adnexa',
    'H60-H95': 'Diseases of the ear and mastoid process',
    'I00-I99': 'Diseases of the circulatory system',
    'J00-J99': 'Diseases of the respiratory system',
    'K00-K95': 'Diseases of the digestive system',
    'L00-L99': 'Diseases of the skin and subcutaneous tissue',
    'M00-M99': 'Diseases of the musculoskeletal system and connective tissue',
    'N00-N99': 'Diseases of the genitourinary system',
    'O00-O99': 'Pregnancy, childbirth and the puerperium',
    'P00-P96': 'Certain conditions originating in the perinatal period',
    'Q00-Q99': 'Congenital malformations, deformations and chromosomal abnormalities',
    'R00-R99': 'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified',
    'S00-T88': 'Injury, poisoning and certain other consequences of external causes',
    'V00-Y99': 'External causes of morbidity',
    'Z00-Z99': 'Factors influencing health status and contact with health services',
    'U00-U49': 'etiology or emergency use'
}


class ICD10Code:
    def __init__(self):
        self.data = pd.read_csv('data/other_materials/ICD-10-CSV-master/2020/diagnosis.csv')

    def _extract_prefix_and_number(self, code):
        match = re.match(r'([A-Z]+)(\d+)', code)
        if match:
            prefix, number = match.groups()
            return prefix, int(number)
        # If no numeric part, default to 0
        elif re.match(r'([A-Z]+)', code):  # Handle cases like 'B'
            return code[0], 0
        return None, None

    def assign_code_to_disease_category(self, code):
        """
        Assigns the ICD code to a disease category based on the predefined ICD_MAPPING ranges.
        """
        prefix, number = self._extract_prefix_and_number(code)

        if prefix is None or number is None:
            return None  # Invalid code format

        for icd_range, category in ICD_MAPPING.items():
            start, end = icd_range.split('-')

            start_prefix, start_num = self._extract_prefix_and_number(start)
            end_prefix, end_num = self._extract_prefix_and_number(end)

            # Ensure both the start and end prefix are valid
            if start_prefix is None or end_prefix is None:
                continue

            # Compare the prefixes first
            if start_prefix <= prefix <= end_prefix:
                if start_prefix == prefix and number < start_num:
                    continue
                if end_prefix == prefix and number > end_num:
                    continue

                return category
        return None

    def fetch_icd10_code(self, disease: str) -> str:
        if disease == 'Headache, unspecified':
            disease = 'Tension-type headache'
        elif disease == 'Depression, unspecified':
            disease = 'Major depressive disorder, single episode, unspecified'
        elif disease == 'Acute candidiasis of vulva and vagina':
            disease='Candidiasis of vulva and vagina'
        elif disease == 'Low back pain, unspecified' or disease=='Other low back pain':
            disease = 'Low back pain'
        elif disease == 'Cough, unspecified':
            disease = 'Cough'

        return self.data[(self.data['LongDescription'] == disease)|(self.data['ShortDescription'] == disease)]['CodeWithSeparator'].values[0]

    def fetch_disease_category(self, icd10_code: str) -> str:
        corresponding_row = self.data[self.data['CodeWithSeparator'] == icd10_code]
        if len(corresponding_row) == 0:
            main_code = icd10_code
        else:
            main_code = corresponding_row['Code'].values[0][:3]
        category = self.assign_code_to_disease_category(main_code)
        return category

    def label_with_disease_category(self, disease: str) -> str:
        if not disease:
            return 'Other health topic'
        code = self.fetch_icd10_code(disease=disease)
        disease_category = self.fetch_disease_category(icd10_code=code)
        return disease_category
