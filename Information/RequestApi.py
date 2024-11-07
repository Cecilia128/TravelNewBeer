import requests
from TravelNewBeer.Information.scene import SceneObject, Point

HOST = 'https://scenicspot.market.alicloudapi.com'
PATH = '/lianzhuo/scenicspot'
METHOD = 'GET'
APPCODE = 'fcf88d75061343f98747931946373f19'


def get_scene_list(city_name: str, spot: str=''):
    if spot == "":
        params = {'city_name': city_name}
    params = {'city': city_name}
    headers = {'Authorization': 'APPCODE ' + APPCODE}
    r = requests.get(HOST + PATH, params=params, headers=headers)
    return r.json().get('data').get("record")


def info2scene(info):
    """
          {
        "grade": "",
        "spot": "趵突泉景区",
        "lng": "117.022525987",
        "addr": "济南市历下区趵突泉南路1号",
        "lat": "36.6670831758",
        "visittime": "建议2-3小时",
        "type": "泉",
        "opentime": "4月10日-10月9日：7:00-19:00，10月10日-次年4月9日：7:00-18:00。",
        "tel": "0531-86920680",
        "url": "http://www.txdyq.cn/"
      }
    :param info:
    :return:
    """
    return SceneObject(info['spot'], Point(info['lng'], info['lat']), info['addr'], info['opentime'], info['visittime'])


if __name__ == '__main__':
    result = get_scene_list("长白山")
    print(result)
    for item in result:
        print(item)
        a = info2scene(item)
        b = 1