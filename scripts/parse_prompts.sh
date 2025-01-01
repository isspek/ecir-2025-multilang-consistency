#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_gpt_4o_latest_translated_zh.csv \
#--output_file data/healthfc/healthFC_final_gpt_4o_latest_translated_zh_parsing_annotations.csv \
#--language Chinese

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_chatgpt_4o_latest_translated_zh.csv \
#--output_file data/healthfc/healthFC_final_chatgpt_4o_latest_translated_zh_parsing_annotations.csv \
#--language Chinese

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_llama3_translated_zh.csv \
#--output_file data/healthfc/healthFC_final_llama3_translated_zh_parsing_annotations.csv \
#--language Chinese

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_command-r_latest_translated_zh.csv \
#--output_file data/healthfc/healthFC_final_command-r_translated_zh_parsing_annotations.csv \
#--language Chinese

#echo English parsing full set
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_gpt_4o_latest_en.csv \
#--output_file data/healthfc/healthFC_final_gpt_4o_latest_en_parsing_annotations.csv \
#--language English
#
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_chatgpt_4o_latest_en.csv \
#--output_file data/healthfc/healthFC_final_chatgpt_4o_latest_en_parsing_annotations.csv \
#--language English
#
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_llama3_en.csv \
#--output_file data/healthfc/healthFC_final_llama3_en_parsing_annotations.csv \
#--language English

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_llama3_en.csv \
#--output_file data/healthfc/healthFC_final_llama3_en_parsing_annotations.csv \
#--language English

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_command-r_latest_translated_en.csv \
#--output_file data/healthfc/healthFC_final_command-r_latest_en_parsing_annotations.csv \
#--language English

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_chatgpt_4o_latest_translated_tr.csv \
#--output_file data/healthfc/healthFC_final_chatgpt_4o_latest_tr_parsing_annotations.csv \
#--language Turkish

#echo Turkish parsing full set
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_gpt_4o_translated_tr.csv \
#--output_file data/healthfc/healthFC_final_gpt_4o_latest_tr_parsing_annotations.csv \
#--language Turkish

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_llama3_tr.csv \
#--output_file data/healthfc/healthFC_final_llama3_tr_parsing_annotations.csv \
#--language Turkish

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_command-r_latest_translated_tr.csv \
#--output_file data/healthfc/healthFC_final_command-r_latest_parsing_annotations.csv \
#--language Turkish

#echo German
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_gpt_4o_latest_de.csv \
#--output_file data/healthfc/healthFC_final_gpt_4o_latest_de_parsing_annotations.csv \
#--language German
#
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_chatgpt_4o_latest_de.csv \
#--output_file data/healthfc/healthFC_final_chatgpt_4o_latest_de_parsing_annotations.csv \
#--language German
#
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_llama3_de.csv \
#--output_file data/healthfc/healthFC_final_llama3_de_parsing_annotations.csv \
#--language German

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/healthFC_final_command-r_latest_translated_de.csv \
#--output_file data/healthfc/healthFC_final_command-r_latest_de_parsing_annotations.csv \
#--language German

#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/sampled_human_rating_en_de_translated.csv \
#--output_file data/healthfc/sampled_human_rating_en_de_translated_parsing_annotations.csv \
#--section translation \
#--language English
#
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/sampled_human_rating_en_zh_translated.csv \
#--output_file data/healthfc/sampled_human_rating_en_zh_translated_parsing_annotations.csv \
#--section translation \
#--language English
#
#python -m src.llm.annotations.prompt_parsing \
#--input_file data/healthfc/sampled_human_rating_en_tr_translated.csv \
#--output_file data/healthfc/sampled_human_rating_en_tr_translated_parsing_annotations.csv \
#--section translation \
#--language English