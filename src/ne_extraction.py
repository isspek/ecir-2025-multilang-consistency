import pandas as pd
from flair.data import Sentence
from flair.nn import Classifier
# import spacy
from typing import List

# nlp = spacy.load("en_core_sci_md")
tagger = Classifier.load("hunflair2")


def ner_entity_extraction(text: str) -> List[str]:
    sentence = Sentence(text)
    tagger.predict(sentence)
    return sentence.to_dict()


if __name__ == '__main__':
    data_path = 'data/healthfc/healthFC_annotated.csv'
    output_path = 'data/healthfc/healthFC_annotated_with_entities.jsonl'
    data = pd.read_csv(data_path)

    data['ner'] = data['en_claim'].apply(lambda x: ner_entity_extraction(x))

    processed_data = []
    for idx, row in data.iterrows():
        diseases = []
        species = []
        chemicals = []
        genes = []

        entities = row['ner']['entities']
        for ent in entities:
            for label in ent['labels']:
                if label['value'] == 'Disease':
                    diseases.append(ent['text'])
                elif label['value'] == 'Species':
                    species.append(ent['text'])
                elif label['value'] == 'Chemical':
                    chemicals.append(ent['text'])
                elif label['value'] == 'Gene':
                    genes.append(ent['text'])

        row['diseases'] = diseases
        row['species'] = species
        row['chemicals'] = chemicals
        row['genes'] = genes
        row['mentioning_disease'] = True if len(diseases) > 0 else False
        row['mentioning_species'] = True if len(species) > 0 else False
        row['mentioning_chemical'] = True if len(chemicals) > 0 else False
        row['mentioning_gene'] = True if len(genes) > 0 else False

        processed_data.append(row)

    processed_data = pd.DataFrame(processed_data)
    processed_data.to_json(output_path, orient='records', lines=True)
