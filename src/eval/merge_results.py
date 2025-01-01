import numpy as np
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from nmtscore import NMTScorer
from tqdm import tqdm

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--first_answer')
    parser.add_argument('--second_answer')
    parser.add_argument('--first_lang')
    parser.add_argument('--second_lang')
    parser.add_argument('--output')

    args = parser.parse_args()

    first_answer = pd.read_csv(args.first_answer)
    second_answer = pd.read_csv(args.second_answer)

    merged_df = pd.merge(second_answer, first_answer, on='en_claim', how='inner')

    first_lang = args.first_lang
    second_lang = args.second_lang

    output = args.output

    # scorer = NMTScorer()

    processed_data = []
    for idx, row in tqdm(merged_df.iterrows(),total=len(merged_df)):
        if second_lang != 'de':
            column_name = 'translation'
        else:
            column_name = 'de_claim'

        processed_data.append({'en_claim': row['en_claim'],
                               f'{second_lang}_claim': row[column_name],
                               'en_result': row['model_output_y'],
                               f'{second_lang}_result': row['model_output_x']})
    pd.DataFrame(processed_data).to_csv(output, index=False)
