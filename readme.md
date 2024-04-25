为了做成一个对话AI，把ASR、TTS、LLM、Agent整合到一起

模块、功能开发顺序
【done】VQA
【half】ASR + TTS, 我本来以为ASR还算难的，结果TTS更麻烦，尝试了接近10种，要么安装麻烦，要么中文效果不好。所以还是用GPT-sovits的远程调用了。毕竟核心的需求是应用
【done】API支持
【】界面
【】llama_index
【】无头浏览器
【】memory
【】Agent

界面用什么？或许unity或者安卓比较合适，web互动似乎有点儿困难。
总之，先搞服务，然后webui顶替一下

环境
python = 3.10