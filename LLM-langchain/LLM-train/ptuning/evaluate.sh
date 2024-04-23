PRE_SEQ_LEN=128
CHECKPOINT=adgen-chatglm2-6b-pt-128-2e-2
STEP=3000
NUM_GPUS=1

torchrun --standalone --nnodes=1 --nproc-per-node=$NUM_GPUS main.py \
    --do_predict \
    --validation_file /root/autodl-tmp/fix-helper/LLM-langchain/Generate-from-openai/generate_file.json \
    --test_file /root/autodl-tmp/fix-helper/LLM-langchain/Generate-from-openai/generate_file.json \
    --overwrite_cache \
    --prompt_column question \
    --response_column answer \
    --model_name_or_path /root/autodl-tmp/chatglm2-6b-int4 \
    --ptuning_checkpoint ./output/$CHECKPOINT/checkpoint-$STEP \
    --output_dir ./output/$CHECKPOINT \
    --overwrite_output_dir \
    --max_source_length 128 \
    --max_target_length 512 \
    --per_device_eval_batch_size 1 \
    --predict_with_generate \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4
