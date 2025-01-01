import pandas as pd

if __name__ == '__main__':
    input_file = 'data/healthfc/healthFC_annotated_with_entities.jsonl'
    data = pd.read_json(input_file, lines=True)
    data.to_csv('data/healthfc/diseases_processed.csv', index=False)
