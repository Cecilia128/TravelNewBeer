# Reference: https://platform.openai.com/docs/guides/function-calling
import json
import os

from qwen_agent.llm import get_chat_model

from TravelNewBeer.Information.RequestApi import get_scene_list
os.environ["DASHSCOPE_API_KEY"] = "sk-5c6a0747d83c452795d5d51d1e3b9f67"
os.environ["TOGETHER_API_KEY"] = "3ce3f8571f44cbbcd603dd49f0a3a36cdcbd487b6b85f0da2567698b0ef3727a"

# DASHSCOPE_API_KEY = "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"

def test(query):
    llm = get_chat_model({
        # Use the model service provided by DashScope:
        # 'model': 'qwen1.5-14b-chat',
        # 'model_server': 'dashscope',
        # 'api_key': os.getenv('DASHSCOPE_API_KEY'),

        # Use the OpenAI-compatible model service provided by DashScope:
        'model': 'qwen2.5-72b-instruct',
        'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'api_key': os.getenv('DASHSCOPE_API_KEY'),

        # Use the model service provided by Together.AI:
        # 'model': 'Qwen/Qwen2.5-72B-Instruct-Turbo',
        # 'model_server': 'https://api.together.xyz/v1',  # api_base
        # 'api_key': os.getenv('TOGETHER_API_KEY'),

        # Use your own model service compatible with OpenAI API:
        # 'model': 'Qwen/Qwen1.5-72B-Chat',
        # 'model_server': 'http://localhost:8000/v1',  # api_base
        # 'api_key': 'EMPTY',
    })

    # Step 1: send the conversation and available functions to the model
    messages = [{'role': 'user', 'content': query}]
    functions = [{
        'name': 'get_scene_list',
        'description': '给定一个地点，获得该城市的所有景点及相关信息。',
        'parameters': {
            'type': 'object',
            'properties': {
                'city_name': {
                    'type': 'string',
                    'description': '城市的名字，例如杭州',
                },
            },
            'required': ['city_name'],
        },
    }]

    print('# Assistant Response 1:')

    responses = []
    for responses in llm.chat(
            messages=messages,
            functions=functions,
            stream=True,
    ):
        print(responses)

    # If you do not need streaming output, you can either use the following trick:
    #   *_, responses = llm.chat(messages=messages, functions=functions, stream=True)
    # or use stream=False:
    #   responses = llm.chat(messages=messages, functions=functions, stream=False)

    messages.extend(responses)  # extend conversation with assistant's reply

    # Step 2: check if the model wanted to call a function
    last_response = messages[-1]
    if last_response.get('function_call', None):

        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            'get_scene_list': get_scene_list,
        }  # only one function in this example, but you can have multiple
        function_name = last_response['function_call']['name']
        function_to_call = available_functions[function_name]
        function_args = json.loads(last_response['function_call']['arguments'])
        function_response = function_to_call(
            city_name=function_args.get('city_name'),
        )
        print('# Function Response:')
        print(function_response)

        # Step 4: send the info for each function call and function response to the model
        messages.append({
            'role': 'function',
            'name': function_name,
            'content': str(function_response),
        })  # extend conversation with function response

        print('# Assistant Response 2:')
        for responses in llm.chat(
                messages=messages,
                functions=functions,
                stream=True,
        ):  # get a new response from the model where it can see the function response
            print(responses)


if __name__ == '__main__':
    template = "你是一个旅游规划专家，你要根据用户的需求，调用旅行商接口，根据接口返回的信息，以markdown的格式给出一个旅游规划方案，包括景点，行程，交通，住宿等。最终额外以json的格式返回方案中的景点名称及其对应的经纬度。\nQUERY"
    query = "我要去杭州玩，要玩三天。"
    test(query=template.replace('QUERY', query))
