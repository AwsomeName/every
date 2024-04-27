import requests

headers = {
    "Content-Type": "application/json"
}

url = "http://0.0.0.0:8081/api/v1/chat/"
url_upl_wav_file = "http://0.0.0.0:8081/api/v1/upload_wav_file"
url_upl_img_file = "http://0.0.0.0:8081/api/v1/upload_img_file"

# 纯文本的请求
data = {'date_str': "2024-04-29_20:00:00", 'user_id': '100100100', 'input_str': "您好"}
result = requests.post(url=url, json=data, headers=headers)
print("txt req:", result.text)
# exit()

# 图片的请求
path_file0 = "100100100@2024-04-29_20:00:00.png"
files = {'img_file':open(path_file0,'rb')}
result = requests.post(url=url_upl_img_file, files=files)
print("img req:", result.text)

# data = {'date_str': "2024-04-29_20:00:00", 'user_id': '100100100', 'input_str': "您好"}
# result = requests.post(url=url, json=data, headers=headers)
# print("txt req:", result.text)

# 音频的请求
path_file0 = "100100100@2024-04-29_20:00:00.wav"
files = {'wav_file':open(path_file0,'rb')}
result = requests.post(url=url_upl_wav_file, files=files)
print("wav req:", result.text)


# url = "http://192.168.31.9:9880/?text_language=zh"
# url += "&text=" + input_str
# response = requests.get(url)
# audio_wav = response.content
# with open("/home/lc/code/self_ai_center/tempDir/tmp_audio.mp3", 'wb') as wp:
#     wp.write(audio_wav)