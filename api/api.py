from fastapi import FastAPI, Request
import uvicorn, json
from ..models.models import EVR_Models

app = FastAPI()

@app.post("/api/v1/vqa")
async def vqa(request: Request):
    global evr_models
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    input_str = json_post_list.get('input_str')
    file_path = json_post_list.get('file_path')
    output_str = evr_models.vqa(file_path, input_str)

    return output_str

if __name__ == '__main__':
    evr_models = EVR_Models()
    uvicorn.run(app, host='0.0.0.0', port=11073, workers=1)
