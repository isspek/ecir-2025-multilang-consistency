import os
import pandas as pd
import requests
import time
import urllib
from SPARQLWrapper import SPARQLWrapper, JSON
from bson.son import SON
from diskcache import Cache
from dotenv import load_dotenv
from pymongo import MongoClient
from tqdm import tqdm
from typing import List

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_UNAME = os.getenv("UNAME")
MONGO_PASS = os.getenv("PASS")
MONGO_DB_URL = f"mongodb://{MONGO_UNAME}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

client = MongoClient(MONGO_DB_URL)
db = client['WIKIDATA']
collection = db['wikidata5m_ents_props']
collection.create_index([("wd_id", 1)])
collection.create_index([("label", 1)])

SPARQL = SPARQLWrapper("https://query.wikidata.org/sparql")

WD_API_ENDPOINT = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=ENTITY_LABEL&language=en&format=json"
CACHE_WD_API = Cache("cache_wd_api")
CACHE_WD_PROPS = Cache("cache_wd_api_props")


@CACHE_WD_PROPS.memoize()
def fetch_wd_props(wd_ids: List[str]):
    wd_ids = list(map(lambda wd_id: f"wd:{wd_id}", wd_ids))
    wd_ents_as_str = " ".join(wd_ids)

    wd_props = f"""
        SELECT ?wd_ent ?wd_ent_type_label ?wd_main_class_level_1_label ?wd_main_class_level_2_label ?wd_health_speciality_label ?wd_facet_of_label
        WHERE {{
          VALUES ?wd_ent {{ {wd_ents_as_str} }}

          OPTIONAL {{
            ?wd_ent wdt:P31 ?wd_ent_type.
            ?wd_ent_type rdfs:label ?wd_ent_type_label.
            FILTER(LANG(?wd_ent_type_label) = "en")
          }}

          OPTIONAL {{
            ?wd_ent wdt:P279 ?wd_main_class_level_1.
            ?wd_main_class_level_1 rdfs:label ?wd_main_class_level_1_label.
            FILTER(LANG(?wd_main_class_level_1_label) = "en")
          }}
          
         OPTIONAL {{
            ?wd_main_class_level_1 wdt:P279 ?wd_main_class_level_2.
            ?wd_main_class_level_2 rdfs:label ?wd_main_class_level_2_label.
            FILTER(LANG(?wd_main_class_level_2_label) = "en")
          }}

          OPTIONAL {{
            ?wd_ent wdt:P1995 ?wd_health_speciality.
            ?wd_health_speciality rdfs:label ?wd_health_speciality_label.
            FILTER(LANG(?wd_health_speciality_label) = "en")
          }}
          
          OPTIONAL {{
            ?wd_ent wdt:P1269 ?wd_facet_of.
            ?wd_facet_of rdfs:label ?wd_facet_of_label.
            FILTER(LANG(?wd_facet_of_label) = "en")
          }}
          
        }}
        """

    SPARQL.setQuery(wd_props)
    SPARQL.setReturnFormat(JSON)

    sparql_results = SPARQL.query().convert()

    results = {

    }

    for result in sparql_results['results']['bindings']:
        # Extract and print only if each key exists in the result
        wd_ent = result.get('wd_ent', {}).get('value', None)
        wd_ent = wd_ent.replace('http://www.wikidata.org/entity/', '')

        if wd_ent not in results:
            results[wd_ent] = {'type': set(), 'wd_main_class_level_1': set(), 'health_speciality': set(),
                               'wd_main_class_level_2': set(),
                               'facet_of': set()}

        wd_ent_type = result.get('wd_ent_type_label', {}).get('value', None)
        if wd_ent_type:
            results[wd_ent]['type'].add(wd_ent_type)

        wd_main_class_level_1_label = result.get('wd_main_class_level_1_label', {}).get('value', None)
        if wd_main_class_level_1_label:
            results[wd_ent]['wd_main_class_level_1'].add(wd_main_class_level_1_label)

        wd_main_class_level_2_label = result.get('wd_main_class_level_2_label', {}).get('value', None)
        if wd_main_class_level_2_label:
            results[wd_ent]['wd_main_class_level_2'].add(wd_main_class_level_2_label)

        wd_health_speciality = result.get('wd_health_speciality_label', {}).get('value', None)

        if wd_health_speciality:
            results[wd_ent]['health_speciality'].add(wd_health_speciality)

        facet_of = result.get('wd_facet_of_label', {}).get('value', None)

        if facet_of:
            results[wd_ent]['facet_of'].add(facet_of)

    return results


@CACHE_WD_API.memoize()
def request_wid_from_wd_api(url: str):
    data = requests.get(url).json()
    return data


@CACHE_WD_API.memoize()
def find_alternate_names_from_wd_api(wd_id: str):
    query = f"""
    SELECT ?alias WHERE {{
      wd:{wd_id} skos:altLabel ?alias.
      FILTER(LANG(?alias) = "en")
    }}
    """
    SPARQL.setQuery(query)

    # Set the return format to JSON
    SPARQL.setReturnFormat(JSON)

    try:
        results = SPARQL.query().convert()
        aliases = [result["alias"]["value"] for result in results["results"]["bindings"]]
        return aliases
    except urllib.error.HTTPError as e:
        print("Got exception!!!")
        print(e)
        if e.code == 429:  # Too many requests
            print(f"Rate limit hit. Waiting for 10 seconds before retrying...")
            wait_time = 10
            time.sleep(wait_time)
            return find_alternate_names_from_wd_api(wd_id)  # Retry
        else:
            raise e


def find_alternate_names(label: str) -> List[str]:
    result = collection.find_one({'label': label})
    if not result:
        return None
    wd_id = result['wd_id']
    results = collection.find({'wd_id': wd_id})
    alt_names = []
    for result in results:
        if 'label' in result:
            alt_names.append(result['label'])
    return alt_names


def label_to_wd(label: str):
    wd_id = None
    if label in ['upper', 'strains', 'the knee']:
        return wd_id
    result = collection.find_one({'label': label})
    if not result:
        url = WD_API_ENDPOINT.replace("ENTITY_LABEL", label)
        response = request_wid_from_wd_api(url)
        results = response['search']
        if len(results) == 0:
            return wd_id
        elif len(results) > 1:
            for result in results:
                if 'description' not in result:
                    continue
                if any(word in result['description'] for word in ['disease', 'effects']):
                    return result['id']
    else:
        wd_id = result['wd_id']
    return wd_id


if __name__ == '__main__':
    # label = 'diabetes type 1'
    # alt_names = find_alternate_names(label)
    #
    # for alt_name in alt_names:
    #     print(alt_name)

    data = pd.read_json('data/healthfc/healthFC_annotated_with_entities.jsonl', lines=True)
    data = data[data['mentioning_disease']]

    print(f'Number of samples with mentioning disease: {len(data)}')

    flatten_diseases = set()

    for disease_lst in data['diseases'].tolist():
        for disease in disease_lst:
            flatten_diseases.add(disease)

    flatten_diseases = list(flatten_diseases)

    for disease in flatten_diseases:
        wd_id = label_to_wd(disease)
        if not wd_id:
            print(f'{disease} has no wd_id')
