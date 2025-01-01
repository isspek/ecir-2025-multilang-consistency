import pandas as pd
from argparse import ArgumentParser
from tqdm import tqdm

from src.wikidata import find_alternate_names_from_wd_api

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_file')
    parser.add_argument('--output_file')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    data = pd.read_csv(input_file)

    data['wd'] = data['item'].map(lambda x: x.replace('http://www.wikidata.org/entity/', ''))

    processed_data = []
    for idx, row in tqdm(data.iterrows(), total=len(data)):
        processed_data.append(row)
        alt_labels = find_alternate_names_from_wd_api(row['wd'])

        if len(alt_labels) > 0:
            for alt_label in alt_labels:
                new_sample = row.copy()
                new_sample['itemLabel'] = alt_label
                processed_data.append(new_sample)

    processed_data = pd.DataFrame(processed_data)
    processed_data.to_csv(output_file)
