from http import HTTPStatus
import dashscope
from openai import OpenAI
import os
import json
from dashscope.audio.tts import SpeechSynthesizer
from dashscope import MultiModalConversation

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
            used = response['usage']
            token_used = used['input_tokens'] + used['output_tokens'] + used['image_tokens']
            return response["output"]['choices'][0]["message"]['content'][0]["text"], token_used
        else:
            print(response.code)  # 错误码
            print(response.message)  # 错误信息
            return response.code, None

    def vqa_open_ai(self, query_str, img_url, history=None):
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
        )
        
        completion = client.chat.completions.create(
            model="qwen-vl-plus",
            messages = [{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": query_str
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url
                        # "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                    }
                }]
            }],
            stream=True)
        
        res = ""
        for chunk in completion:
            print(chunk.model_dump_json())
            infos = json.loads(chunk.model_dump_json())
            if infos['usage'] is not None:
                resp_info = infos['choices'][0]['delta']['content']
                if resp_info is not None:
                    res += resp_info[0]['text']
        return res, None


    def chat_qwen_openai_stream(self, query_str, history=None):
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
        )
        
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': query_str}],
            # stream=True
            )
        res = ""
        # print(completion)
        for chunk in completion:
            print(chunk.model_dump_json())
            infos = json.loads(chunk.model_dump_json())
            resp_info = infos['choices'][0]['delta']['content']
            if len(resp_info)>0:
                print("resp_info:", resp_info)
                res += resp_info
        return res, None

    def chat_qwen_openai(self, query_str, history=None):
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
        )
        
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': query_str}],
            # stream=True
            )
        res = ""
        # print(completion)
        # used = completion.usage
        res = completion.choices[0].message.content
        return res, completion.usage.total_tokens
            
    def asr_r(self, file_path):
        messages = [{
            'role': 'system',
            'content': [{
                'text': 'You are a helpful assistant.'
        }]}, {
            'role':
            'user',
            'content': [{
                'audio': file_path
            },
            {
                'text': '给出音频的文本内容'
            },
        ]}]
        response = MultiModalConversation.call(model='qwen-audio-chat', messages=messages)
        print(response)
        token_used = None
        if response['status_code'] == 200:
            response_txt = response["output"]["choices"][0]['message']['content'][0]['text']
            used_info = response['usage']
            token_used = used_info['input_tokens'] + used_info['output_tokens'] + used_info['audio_tokens']
        else:
            response_txt = ""
        return response_txt, token_used

    def tts_r(self, query_str, uid):
        dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

        result = SpeechSynthesizer.call(model='sambert-zhichu-v1',
                                text=query_str,
                                sample_rate=48000,
                                format='wav')
        file_path = '/tmp/every/history/' + uid + '/wav/tmp_output.wav'
        if result.get_audio_data() is not None:
            with open(file_path, 'wb') as f:
                f.write(result.get_audio_data())
        print('  get response: %s' % (result.get_response()))
        
        return file_path

if __name__ == "__main__":
    file_path = "/home/lc/data/radio/yuanshen_zh/雷电将军/sr16000/997ee8950033ce78a1e1204cef725d51226_145647756923704119.mp3"
    EVR = EVR_Models()
    # print(EVR.asr_r(file_path))
    print(EVR.tts_r("今天天气非常好啊！", "100100100"))
    # img_path = 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'
    # img_path = "/home/lc/code/every/api/100100100@2024-04-29_20:00:00.png"
    # img_url = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
    # print(EVR.vqa_open_ai("这是什么", img_url=img_url))
    # print(EVR.vqa_r("这是什么", img_path=img_path))
    # print(EVR.chat_qwen_openai("可以介绍一下你自己吗"))
    # EVR.tts("今天天气挺好的")
    