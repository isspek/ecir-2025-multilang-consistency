MODEL=llama3
LANG=en
python -m src.evaluation.analysis \
--input_file data/healthfc/results/healthFC_final_${MODEL}_${LANG}.csv