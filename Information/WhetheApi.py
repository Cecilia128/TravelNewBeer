import requests

HOST = 'https://weather01.market.alicloudapi.com'
PATH = '/day15'
METHOD = 'GET'
APPCODE = 'fcf88d75061343f98747931946373f19'


def get_whether_info(city_name: str):
    params = {'area': city_name}
    headers = {'Authorization': 'APPCODE ' + APPCODE}
    r = requests.get(HOST + PATH, params=params, headers=headers)
    return r.json()

if __name__ == '__main__':
    print(get_whether_info('杭州'))