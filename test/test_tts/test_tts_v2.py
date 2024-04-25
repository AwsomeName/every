from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

text = '今天天气非常好，27度'
# model_id = 'speech_tts/speech_sambert-hifigan_tts_zh-cn_multisp_pretrain_16k'
model_id = "/home/lc/models/tts/speech_sambert-hifigan_tts_zh-cn_multisp_pretrain_16k"
sambert_hifigan_tts = pipeline(task=Tasks.text_to_speech, model=model_id)
output = sambert_hifigan_tts(input=text)
wav = output[OutputKeys.OUTPUT_WAV]
with open('output.wav', 'wb') as f:
    f.write(wav)