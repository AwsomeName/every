from transformers import pipeline
import scipy

# synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")
synthesiser = pipeline("text-to-audio", "/home/lc/models/tts/bark-small")

# music = synthesiser("lo-fi music with a soothing melody", forward_params={"do_sample": True})
music = synthesiser("今天天气不错，万里无云", forward_params={"do_sample": True})

scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])
