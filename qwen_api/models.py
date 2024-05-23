# import torch
# import numpy as np
# import soundfile as sf
# torch.manual_seed(1234)
from http import HTTPStatus
import dashscope


class EVR_Models():
    def __init__(
        self,
    ) -> None:
        pass
        

    def vqa_r(self, query_str, img_path, history=None):
        messages = [
        {
            "role": "user",
            "content": [
                # {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
                # {"image": "/tmp/every/api/" + img_path},
                {"image": img_path},
                {"text": query_str}
            ]
        }
        ]
        # response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
        response = dashscope.MultiModalConversation.call(model='qwen-vl-max',
                                                        messages=messages)

        if response.status_code == HTTPStatus.OK:
            # print(response)
            return response["output"]['choices'][0]["message"]['content'][0]["text"], None
        else:
            print(response.code)  # 错误码
            print(response.message)  # 错误信息
            return response.code, None
        

    def chat_r(self, query_str, history=None):
        # query = self.tokenizer.from_list_format([
            # {'image': img_path},
            # {'text': query_str},
        # ])
        response, n_history = self.v_model.chat(self.tokenizer, query=query_str, history=history)
        print(response)
        return response, n_history

            
    def asr_r(self, file_path):
        # segments, info = self.asr_model.transcribe(file_path)
        response_txt = ""
        # for sgm in segments:
        #     response_txt += sgm.text
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
    