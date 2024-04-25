from transformers import AutoProcessor, AutoModel
import soundfile as sf

# processor = AutoProcessor.from_pretrained("/home/lc/models/tts/bark-small")
# model = AutoModel.from_pretrained("/home/lc/models/tts/bark-small")

# inputs = processor(
#     text=["今天天气不错，万里无云"],
#     # text=["Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe."],
#     return_tensors="pt",
# )

# speech_values = model.generate(**inputs, do_sample=True)
# print(speech_values.shape)

# # import scipy
# import numpy as np
# sf.write("test.wav", speech_values.numpy().reshape(52,1600), sampling_rate=1600, format="wav")
# # scipy.io.wavfile.write("musicgen_out.wav", rate=16000, data=speech_values.numpy())


from transformers import pipeline
device = "cuda:0"
text = "今天天气不错，万里无云"
pp = "/home/lc/models/tts/bark-small"
classifier = pipeline("text-to-audio", model=pp)
output = classifier(text)
audio = output["audio"]
sampling_rate = output["sampling_rate"]

print(audio.shape, sampling_rate)
# audio = audio.reshape(24000, -1)
from scipy.io.wavfile import write
import numpy as np
scaled = np.int16(audio / np.max(np.abs(audio)) * 32767 + 16400)
write("output.wav", sampling_rate, scaled)

# sf.write("test.mp3", audio, sampling_rate, format="mp3")