from argparse import ArgumentParser
from googletrans import Translator
from diskcache import Cache
import pandas as pd

CACHE_TRANS = Cache("cache_translations")
TRANSLATOR = Translator()

@CACHE_TRANS.memoize()
def apply_translation(text: str, target_language: str)-> str:
    translation = TRANSLATOR.translate(text, dest = target_language)
    return translation.text

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--target_language')
    parser.add_argument('--input_file')
    parser.add_argument('--output_file')
    parser.add_argument('--section', default='en_claim')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    target_language = args.target_language
    section = args.section

    input_df = pd.read_csv(input_file)


    input_df['translation'] = input_df[section].apply(lambda x: apply_translation(x, target_language=target_language))
    input_df = input_df[['en_claim', section, 'translation']]
    input_df.to_csv(output_file, index=False)
