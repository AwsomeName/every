from paddlespeech.cli.tts.infer import TTSExecutor

tts = TTSExecutor()

tts(text="今天天气非常好，晴朗无云", output="output.wav")