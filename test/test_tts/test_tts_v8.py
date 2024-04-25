from TTS.api import TTS

mp = "/home/lc/models/tts/XTTS-v2"
# TTS.list_models()
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
# mp = "tts_models/multilingual/multi-dataset/xtts_v2"
# tts = TTS(mp, gpu=True)
tts = TTS(
    # model_name="XTTS-v2",
    model_path=mp,
    config_path=mp + "/config.json",
    # vocoder_path=mp,
    # vocoder_config_path=mp,
    gpu=True)

# generate speech by cloning a voice using default settings
tts.tts_to_file(text="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
                file_path="output.wav",
                speaker_wav="/home/lc/models/tts/XTTS-v2/samples/zh-cn-sample.wav",
                language="zh")
