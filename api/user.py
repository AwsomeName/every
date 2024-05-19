# 总输入接口
# 关于历史对话的设计，存储根目录下，每个用户新建文件夹，然后每条对话，按照时间存储。
# 然后整体直接设计成RAG

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn, json

app = FastAPI()

# 维持一个公共的对话记录
users = {}
# history['100100101']['chat'] = None


# 维持一个用户表。用户信息和装填
# 发送验证码
# 用户不存在，那么注册并登录。用户存在，那么登录
# 用户注销
# 用户退出


@app.post("/api/v1/chat")
async def chat(request: Request):
    global evr_models
    print(evr_models)
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    input_str = json_post_list.get('input_str')
    date_str = json_post_list.get('date_str')
    user_id = json_post_list.get('user_id')
    if user_id not in history:
        return {"msg": "err_uid", "return_info": ""}

    print("input_str: ", input_str)
    # 询问模型
    last_img = history[user_id]['last_img']
    if last_img is not None:
        last_img_time = last_img['time']
        if last_img_time[:10] == date_str[:10]:
            img_path = last_img['file_path']
            try:
                resp, his = evr_models.vqa(query_str=input_str, img_path=img_path)
                history[user_id]['last_img'] = None
            except:
                return {"msg": "err_img", "return_info": ""}
        else:
            resp, his = evr_models.chat(query_str=input_str)
            
    else:
        # global evr_models
        resp, his = evr_models.chat(query_str=input_str)
    # 保存结果，并返回
    
    return {"msg": "suc", "return_info": resp}

@app.post("/api/v1/upload_wav_file")
async def upload_wav_file(wav_file: UploadFile):
    # 文件名称是 userid@datetime.wav
    # 保存到本地
    # 调用ASR
    # 调用本地模型
    global evr_models
    print("file:", wav_file)
    file_name = wav_file.filename
    try:
        uid, date_str = file_name.split("@")
        if uid is None or date_str is None:
            return {"msg": "err file_name"}
    except:
        return {"msg": "err file_name", "return_info": ""}
    
    save_path = "./history/" + uid + "/wav/" + date_str
    # wav_file.write(save_path)
    with open(save_path, "wb") as f:
        f.write(wav_file.file.read())

    input_str = evr_models.asr(save_path)['resp']

    last_img = history[uid]['last_img']
    if last_img is not None:
        last_img_time = last_img['time']
        # last_img_time = time.strptime(last_img_time, "%Y-%m-%d_%H:%M:%S")
        # query_time = time.strptime(date_str, "%Y-%m-%d_%H:%M:%S")
        if last_img_time[:10] == date_str[:10]:
            img_path = last_img['file_path']
            try:
                resp, his = evr_models.vqa(query_str=input_str, img_path=img_path)
                history[uid]['last_img'] = None
            except:
                return {"msg": "err_img", "return_info": ""}
                
        else:
            resp, his = evr_models.chat(query_str=input_str)
            
    else:
        resp, his = evr_models.chat(query_str=input_str)

    return {"msg": "suc", "return_info": resp}

@app.post("/api/v1/upload_img_file")
async def upload_img_file(img_file: UploadFile):
    # 文件名称是 userid@datetime.png
    # 保存路径，./history/uid/wav/datetime.png
    # 更新history缓存
    print("file:", img_file)
    file_name = img_file.filename
    try:
        uid, date_str = file_name.split("@")
        if uid is None or date_str is None:
            return {"msg": "err file_name"}
    except:
        return {"msg": "err file_name", "return_info": ""}
    
    save_path = "./history/" + uid + "/img/" + date_str
    # img_file.write(save_path)
    # img_file.file.write(save_path)
    with open(save_path, 'wb') as wp:
        wp.write(img_file.file.read())

    history[uid]['last_img'] = {}
    history[uid]['last_img']["time"] = date_str
    history[uid]['last_img']["file_path"] = save_path
    
    return {"msg": "suc", "return_info": ""}


@app.get("/api/v1/dlf")
async def down_file(request: Request):
    # global evr_models
    # print(evr_models)
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    file_name = json_post_list.get('file_name')
    uid, date_str = file_name.split("@")
    file_path = "./history/" + uid + "/img/" + date_str 
    return FileResponse(file_path)



if __name__ == '__main__':
    evr_models = EVR_Models()
    # evr_models = EVR_Models(
    # v_model_path = "/hy-tmp/Qwen-VL-Chat-Int4",
    # asr_model_path = "/hy-tmp/faster-whisper-large-v3")
    # resp, his = evr_models.chat(query_str="您好，测试")
    # print("resp:", resp)
    # uvicorn.run("back_api:app", host='0.0.0.0', port=8081, workers=1)
    uvicorn.run(app, host='0.0.0.0', port=8081, workers=1)

