from openai import OpenAI
import os

DASHSCOPE_API_KEY = "sk-5c6a0747d83c452795d5d51d1e3b9f67"
def get_response():
    print(os.getenv("DASHSCOPE_API_KEY"))
    client = OpenAI(
        api_key="sk-5c6a0747d83c452795d5d51d1e3b9f67", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': '你是谁？'}]
        )
    print(completion.model_dump_json())

if __name__ == '__main__':
    get_response()