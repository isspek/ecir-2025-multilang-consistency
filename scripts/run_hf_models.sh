echo run Llama3

echo Turkish prompting -- Llama3

python -m src.llm.generate_answer \
--input_file data/healthfc/healthFC_final_sampled_translated_tr.csv \
--language tr \
--output_file data/healthfc/healthFC_final_sampled_llama3_tr_answers.csv \
--model meta-llama/Llama-3.1-8B-Instruct \
--run_option hf_tf