from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from faster_whisper import WhisperModel
import torch
# import numpy as np
# import soundfile as sf
torch.manual_seed(1234)


class EVR_Models():
    def __init__(
        self,
        emb_path: str = "local:/home/lc/models/BAAI/bge-small-zh-v1.5",
        v_model_path: str = "/home/lc/data_e/tmp/Qwen-VL-Chat-Int4",
        # asr_model_path: str = "/home/lc/models/Systran/faster-whisper-large-v3",
        asr_model_path: str = "/home/lc/models/Systran/faster-whisper-small",
        # tts_model_path: str = "/home/lc/models/",
        # spk_emb_path: str = "/home/lc/hf_dataset/Matthijs/cmu-arctic-xvectors/spkrec-xvect/cmu_us_rms_arctic-wav-arctic_b0088.npy",
        faiss_demension:int = 512,
    ) -> None:
        
        # speaker_embeddings = np.load(spk_emb_path)
        # self.speaker_embeddings = torch.tensor(speaker_embeddings).unsqueeze(0)
        # self.processor = SpeechT5Processor.from_pretrained(tts_model_path + "microsoft/speecht5_tts")
        # self.tts_model = SpeechT5ForTextToSpeech.from_pretrained(tts_model_path + "microsoft/speecht5_tts")
        # self.vocoder = SpeechT5HifiGan.from_pretrained(tts_model_path + "microsoft/speecht5_hifigan")
        self.asr_model_path = asr_model_path
        self.asr_model = WhisperModel(self.asr_model_path)
        print("load whispher done")
        self.v_model_path = v_model_path 
        self.tokenizer = AutoTokenizer.from_pretrained(v_model_path, trust_remote_code=True)
        self.v_model = AutoModelForCausalLM.from_pretrained(
            self.v_model_path, 
            device_map="auto", 
            trust_remote_code=True).eval()

    def vqa(self, query_str, img_path, history=None):
        query = self.tokenizer.from_list_format([
            {'image': img_path},
            {'text': query_str},
        ])
        response, n_history = self.v_model.chat(self.tokenizer, query=query, history=history)
        print(response)
        return response, n_history

    def chat(self, query_str, history=None):
        # query = self.tokenizer.from_list_format([
            # {'image': img_path},
            # {'text': query_str},
        # ])
        response, n_history = self.v_model.chat(self.tokenizer, query=query_str, history=history)
        print(response)
        return response, n_history

    def draw_box_vqa(self, query_str, img_path, history):
        response, history = self.v_model.chat(self.tokenizer, '输出"击掌"的检测框', history=history)
        print(response)
        image = self.tokenizer.draw_bbox_on_latest_picture(response, history)
        if image:
            image.save('1.jpg')
        else:
            print("no box")
            
    def asr(self, file_path):
        segments, info = self.asr_model.transcribe(file_path)
        response_txt = ""
        for sgm in segments:
            response_txt += sgm.text
        return {"resp": response_txt}

    # def tts(self, query_str, file_path=None):
    #     inputs = self.processor(text=query_str, return_tensors="pt")
    #     speech = self.tts_model.generate_speech(
    #         inputs["input_ids"], 
    #         self.speaker_embeddings, 
    #         vocoder=self.vocoder)
    #     sf.write("speech.wav", speech.numpy(), samplerate=16000)
    #     return speech.numpy()

if __name__ == "__main__":
    file_path = "/home/lc/data/radio/yuanshen_zh/雷电将军/sr16000/997ee8950033ce78a1e1204cef725d51226_145647756923704119.mp3"
    EVR = EVR_Models()
    print(EVR.asr(file_path))
    img_path = 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'
    print(EVR.vqa("这是什么", img_path=img_path))
    # EVR.tts("今天天气挺好的")
    