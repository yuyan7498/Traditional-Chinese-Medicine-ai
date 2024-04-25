import openai
import gradio as gr
from datetime import date
from dotenv import dotenv_values

#今天日期
today = date.today()
month = today.month
day = today.day
# 讀取 .env 檔案中的設定
config = dotenv_values("./.env")
try:
    openai.api_key = config["API-KEY"]
except KeyError:
    print("Error: API-KEY not found in .env file. Please make sure it is properly configured.")
    exit()

# 定義生成回答的函數
def generate_ans(text):
    # 初始對話消息列表，包含了對話中的問題和回答
    messages=[
        {"role": "user", "content": f"請你把自己當成一個五運六氣以及中醫相關的專家，並且記住今天的日期是{month}/{day}日提問者可能會詢問關於中醫理論等知識，請用繁體中文給提問者解答。根據以下格式，條列出答案。"},
        {"role": "assistant", "content": "你好我是精通五運六氣的專家，請問有什麼需要幫忙的嗎？"},
        {"role": "user", "content": "五運指的是什麼？它們代表什麼元素？"},
        {"role": "user", "content": "五運指的是木、火、土、金、水這五行元素，它們分別代表了生、長、收、藏、藏的運行規律。木生火，火生土，土生金，金生水，水生木，形成了一個循環的生剋關係。"},
        {"role": "assistant", "content": "在中醫醫學中，五運六氣理論被用來分析人體健康與疾病之間的關係。醫師會根據患者的體質、症狀以及當時的氣候環境等因素來診斷和治療疾病。"},
        {"role": "user", "content": "五運六氣與中國傳統節氣的關係是什麼？"},
        {"role": "assistant", "content": "五運六氣與中國傳統節氣密切相關，節氣是根據太陽黃經和地球黃經相對位置的變化來確定的，而五運六氣則是根據陰陽五行的運行規律和氣候現象來描述的，兩者相互補充和互相影響。"},
        {"role": "user", "content": f"{text}"},  # 使用者提問的部分
    ]
    try:
        # 生成回答
        res = openai.chat.completions.create(model='gpt-3.5-turbo-0125', messages=messages, max_tokens=300)
        return res.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# 定義 Gradio 使用的介面
demo = gr.Interface(
    fn=generate_ans,  # 使用 generate_ans 函數
    inputs=["text"],  # 接受文字輸入
    outputs=["text"],  # 輸出文字
    title="五運六氣專家",
    description="有什麼問題盡管問我吧",
    allow_flagging="never"  # 禁用標記功能
)

# 啟動 Gradio 介面
demo.launch(share=True)  # 啟用共享模式
