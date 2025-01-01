#python -m code.translate \
#--target_language zh-cn \
#--input_file data/healthfc/healthFC_final_sampled.csv \
#--output_file data/healthfc/healthFC_final_sampled_translated_zh.csv


#python -m code.translate \
#--target_language tr \
#--input_file data/healthfc/healthFC_final_sampled.csv \
#--output_file data/healthfc/healthFC_final_sampled_translated_tr.csv

#python -m code.translate \
#--target_language tr \
#--input_file data/healthfc/healthFC_final.csv \
#--output_file data/healthfc/healthFC_final_translated_tr.csv

#python -m code.translate \
#--target_language zh-cn \
#--input_file data/healthfc/healthFC_final.csv \
#--output_file data/healthfc/healthFC_final_translated_zh.csv

#python -m code.translate \
#--input_file data/healthfc/sampled_human_rating_en_zh.csv \
#--section model_output_y \
#--output_file data/healthfc/sampled_human_rating_en_zh_translated.csv \
#--target_language en

#python -m code.translate \
#--input_file data/healthfc/sampled_human_rating_en_tr.csv \
#--section model_output_y \
#--output_file data/healthfc/sampled_human_rating_en_tr_translated.csv \
#--target_language en

python -m code.translate \
--input_file data/healthfc/sampled_human_rating_en_de.csv \
--section model_output_y \
--output_file data/healthfc/sampled_human_rating_en_de_translated.csv \
--target_language en

