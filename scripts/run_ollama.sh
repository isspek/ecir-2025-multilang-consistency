#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --gpus=1
#SBATCH --ntasks=1

ollama serve &

# Wait until Ollama service has been started
sleep 2

echo "Server started"

#ollama run command-r-plus
#ollama ps

echo Turkish - Command-R-Plus

python -m src.llm.generate_answer \
--input_file data/healthfc/healthFC_final_sampled_translated_tr.csv \
--language tr \
--output_file src/dataset/healthfc/healthFC_final_sampled_command-r_answers.csv \
--model command-r-plus \
--run_option ollama

