"""An image generation agent implemented by assistant"""

import json
import os
import urllib.parse

import json5

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.tools.base import BaseTool, register_tool
from sympy.polys.polyconfig import query

from TravelNewBeer.Information.RequestApi import get_scene_list
from TravelNewBeer.Information.WhetheApi import get_whether_info

os.environ["DASHSCOPE_API_KEY"] = "sk-5c6a0747d83c452795d5d51d1e3b9f67"

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')


# Add a custom tool named get_scene_list：
@register_tool('get_scene_list')
class GetSceneList(BaseTool):
    description = '给定一个地点，获得该城市的所有景点及相关信息。'
    parameters = [{
        'name': 'city_name',
        'type': 'string',
        'description': '城市的名字，例如杭州。',
        'required': True,
    }]

    def call(self, params: str, **kwargs) -> str:
        city_name = json5.loads(params)['city_name']
        return get_scene_list(city_name)

@register_tool('get_whether_info')
class GetWhetherInfo(BaseTool):
    description = '给定一个城市，获得该城市未来15天的天气情况。'
    parameters = [{
        'name': 'city_name',
        'type': 'string',
        'description': '城市的名字，例如杭州。',
        'required': True,
    }]

    def call(self, params: str, **kwargs) -> str:
        city_name = json5.loads(params)['city_name']
        return get_whether_info(city_name)

def init_agent_service():
    llm_cfg = {'model': 'qwen-max'}
    system = ("你是一个旅游规划专家，你要根据用户的需求，调用旅行商接口，根据接口返回的信息，"
              "以markdown的格式给出一个旅游规划方案，在合适的位置添加有趣的emoji图案，并在重点处以不同颜色、字体、加粗、斜体等方式突出。"
              "旅游规划方案需要包含景点（包含名称、地址、开放时间、推荐游玩时长、推荐游玩原因、费用），交通方式（包括工具、预计花费时间），住宿（包括名称、地址、预计费用），当地美食，天气情况，注意事项等。"
              "景点和住宿要按照方案展示顺序排列。"
              "最终额外以json的格式返回方案中的景点名称、序号、及其对应的经纬度。")

    tools = [
        'get_scene_list',
        'get_whether_info',
    ]
    bot = Assistant(
        llm=llm_cfg,
        name='Tranvel Planing',
        description='Tranvel plan service',
        system_message=system,
        function_list=tools,
    )

    return bot


def travel_plan(query: str):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = [{'role': 'user', 'content': query}]
    for response in bot.run(messages=messages):
        print('bot response:', response)



if __name__ == '__main__':
    query = "我想去长白山玩四天三晚"
    travel_plan(query=query)