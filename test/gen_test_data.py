import json

all_data = []
querys = []
ans = []
with open("Alpaca_data_gpt4_zh.jsonl", 'r') as fp:
    for line in fp.readlines():
        line = line.strip()
        infos = json.loads(line)
        query = infos['instruction_zh']
        output = infos['output_zh']
        # print(query)
        # print(output)
        # exit()
        querys.append(query)
        ans.append(output)

        
total = len(querys)

cnt = 0
# with open("all_data.json", 'w') as wp:
    

all_info = []
cnt = 0
# with open("/home/lc/books_list.txt", 'r') as fp:
#     for line in fp.readlines():
#         line = line.strip()
        

if True:
    for i in range(total):
        cnt += 1
        if cnt >= 600:
            break
        if i % 2 == 0:
            it = True
        else:
            it = False
            
        infos = {}
        infos["id"] = "identity_" + str(cnt)
        infos['conversations'] = []
        info = {}
        info['from'] = "user"
        if it:
            info['value'] = """下面是一段对话中的提问和回答，请判断这个回答是否准确、全面的回答了问题，如果回答的内容准确就回答了问题就返回'是'，否则回答'否'。提问的问题：'""" + querys[i] + """' 回答的内容：'""" + ans[i] + """'--- 这个回答是否完美的回答了问题？答："""
        else:
            info['value'] = """下面是一段对话中的提问和回答，请判断这个回答是否准确、全面的回答了问题，如果回答的内容准确就回答了问题就返回'是'，否则回答'否'。提问的问题：'""" + querys[i] + """' 回答的内容：'""" + ans[-i] + """'--- 这个回答是否完美的回答了问题吗？答："""
            
        infos['conversations'].append(info)
        info = {}
        info['from'] = "assistant"
        if it:
            info['value'] = "是"
        else:
            info['value'] = "否"
        infos['conversations'].append(info)
        cnt += 1
        all_info.append(infos)
            
    
with open("ft.json", 'w') as wp:
    json.dump(all_info, wp) 