# Consistency Check on LLMs Answers to Health-Related Questions
## A Case Study for English, Chinese, Turkish and German

This repository contains the source code of the paper "Do LLMs Provide Consistent Answers to Health-Related Questions across Languages?" [1].

## Dataset Extension
The original dataset is based on [HealthFC](https://github.com/jvladika/HealthFC)[2]. Follow the instructions at the dataset source code for downloading it.

### Disease Classification
We categorize the diseases based on the mentioned disease entities on the text. We applied a semi-automatic method for constructing a dictionary for disease categorization.
Final dictionary is called `healthFC_diseases_wd_icd10_maps_v2.csv`.

Download ner_model:

```shell
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_md-0.5.4.tar.gz
```
Execute code for extraction of the named entities

```shell
python -m src.ne_extraction
```

Enrich entities with their alternate names at Wikidata. See the execution code:

```shell
bash scripts/enrich_wd.sh
```

### Translations
To run the translation

```shell
bash scripts/translation.sh
```

The extras of the dataset can be accessed at [this link](https://drive.google.com/drive/folders/1DAPJsgqRyNKBtSKeNYJ3aq4QGOiUC4Bp?usp=sharing). You need to fetch the corresponding cells from the original data if you want to check the English/German questions.

## Answer Generation

### HF Models (Local)

Create virtual environment

```shell
conda create --name hf_local python=3.10
conda activate hf_local

bash scripts/run_hf_models.sh
```

Alternatively, you can interact with the HF models through ollama.

```shell
bash scripts/run_ollama.sh
```

### HF Inference Endpoint
This is required for inferencing Llama3.1-70B

```shell
bash scripts/run_llama3.sh
```

### OpenAI Inference Endpoint
This is the script for inferencing the OpenAI models

```shell
bash scripts/run_openai.sh
```

## Evaluation
To evaluate consistency between answers, you first need to parse the answers, and then run the consistency-check function.

### Parsing

```shell
bash scripts/parse_prompts.sh
```

After parsing on the answers, you need to merge answer pairs.

```shell
bash scripts/merge_results.sh
```

### Checking Consistency

```shell
bash scripts/consistency_check.sh
```

## References (Bib)
[1] The citation information for our paper.
```bibtex
TODO
```

[2] The citation information for the HealthFC Original Paper

```bibtex
@inproceedings{vladika-etal-2024-healthfc-verifying,
    title = "{H}ealth{FC}: Verifying Health Claims with Evidence-Based Medical Fact-Checking",
    author = "Vladika, Juraj  and
      Schneider, Phillip  and
      Matthes, Florian",
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italy",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.709",
    pages = "8095--8107",
}
```