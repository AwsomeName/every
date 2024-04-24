from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
torch.manual_seed(1234)


class EVR_Models():
    def __init__(
        self,
        emb_path: str = "",
        v_model_path: str = "",
        faiss_demension:int = 521,
    ) -> None:
        
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

    def draw_box_vqa(self, query_str, img_path, history):
        response, history = self.v_model.chat(self.tokenizer, '输出"击掌"的检测框', history=history)
        print(response)
        image = self.tokenizer.draw_bbox_on_latest_picture(response, history)
        if image:
            image.save('1.jpg')
        else:
            print("no box")
