echo Checking Turkish Prompts - ChatGPT-4o-latest

python -m code.llm.generate_answer \
--input_file data/healthfc/healthFC_final_translated_tr.csv \
--language tr \
--output_file data/healthfc/healthFC_final_chatgpt_4o_latest_translated_tr.csv \
--model chatgpt-4o-latest \
--run_option gpt_api