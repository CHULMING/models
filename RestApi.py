import requests
import json

def post_data(payload_data, type='minute'):
    url = 'http://localhost:8080/api/' + type
    print('start to post data\n{}'.format(url))
    r = requests.post(url, data=payload_data)
    print('done\n')

def get_data(code, type='minute'):
    url = 'http://localhost:8080/api/' + type + '/' + code
    print('start to get data\n{}'.format(url))
    r = requests.get(url).json()
    print('done\n')
    return r

if __name__ == "__main__":
    data = {
        'code': '005930', 
        'start': 40000, 
        'low': 45000, 
        'high': 55000, 
        'close': 49000,
        'volume': 999999,
        'published_date': '2021-05-27T15:30'
        }

    # post_data(data, type='day')
    print(get_data(data['code'], type='day'))