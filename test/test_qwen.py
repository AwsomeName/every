from http import HTTPStatus
import dashscope

def simple_multimodal_conversation_call():
    messages = [
        {
            "role": "user",
            "content": [
                # {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
                {"image": "file:///home/lc/code/every/api/100100100@2024-04-29_20:00:00.png"},
                {"text": "这是什么?"}
            ]
        }
    ]
    # response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
    response = dashscope.MultiModalConversation.call(model='qwen-vl-max',
                                                     messages=messages)

    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print(response.code)  # 错误码
        print(response.message)  # 错误信息


if __name__ == '__main__':
    simple_multimodal_conversation_call()