PRE_SEQ_LEN=128
LR=1e-2
NUM_GPUS=1

torchrun --standalone --nnodes=1 --nproc-per-node=$NUM_GPUS main.py \
    --do_train \
    --train_file /root/autodl-tmp/fix-helper/LLM-langchain/Generate-from-openai/generate_file2.json \
    --validation_file /root/autodl-tmp/fix-helper/LLM-langchain/Generate-from-openai/generate_file.json \
    --preprocessing_num_workers 10 \
    --prompt_column question \
    --response_column answer \
    --history_column history \
    --overwrite_cache \
    --model_name_or_path /root/autodl-tmp/chatglm2-6b-int4 \
    --output_dir output/output-$PRE_SEQ_LEN-$LR \
    --overwrite_output_dir \
    --max_source_length 256 \
    --max_target_length 256 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --predict_with_generate \
    --max_steps 3000 \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate $LR \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4

