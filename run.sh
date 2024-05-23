# export DASHSCOPE_API_KEY="sk-91070ccd02954e0ba4ac"
# python api/api.py 2>&1 >/dev/null &
# export DASHSCOPE_API_KEY=sk-91070ccd02954e0ba4a0fa3c2feb

conda activate py10
# conda activate every
# export EVERY_ENV='online'
# mkdir history

nohup python qwen_api/back_api.py 2>&1 >/dev/null &