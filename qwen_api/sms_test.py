from unisdk.sms import UniSMS
from unisdk.exception import UniException

# 初始化
client = UniSMS("Ng4u25NAqerzJHZwjMVZDUJ9Bk4VUbYQr32tgR2cLVHDaJ7cy") # 若使用简易验签模式仅传入第一个参数即可

try:
  # 发送短信
  res = client.send({
    "to": "15063036754",
    "signature": "深芯智造",
    "templateId": "pub_verif_basic",
    "templateData": {
      "code": 7777
    }
  })
  print(res.data)
except UniException as e:
  print(e)