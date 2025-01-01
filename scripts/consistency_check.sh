python -m src.llm.annotations.consistency_check \
--bilingual en_zh \
--second_language Chinese \
--english_parsed_answers data/healthfc/healthFC_final_chatgpt_4o_en_parsing_annotations.csv \
--other_parsed_answers data/healthfc/healthFC_final_chatgpt_4o_zh_parsing_annotations.csv \
--output_file data/healthfc/healthFC_final_chatgpt_4o_en_zh_consistency.csv