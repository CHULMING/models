import requests
import json
import time
RETRY_COUNT = 5
BACKOFF = 0.5
def post_data(payload_data, type='minute'):
    count = 0
    while(count<RETRY_COUNT):
        try:
            url = 'http://localhost:3000/api/' + type
            print('start to post data\n{}'.format(url))
            r = requests.post(url, data=payload_data)
            print('done\n')
            count = 0;
            break
        except Exception as e:
            print(e)
            count = count + 1
            time.sleep(BACKOFF * count)
    if count >= RETRY_COUNT:
        print("POST failed")
        time.sleep(10)

def get_data(code, type='minute'):
    
    count = 0
    while(count<RETRY_COUNT):
        try:
            url = 'http://localhost:3000/api/' + type + '/' + code
            print('start to get data\n{}'.format(url))
            r = requests.get(url).json()
            print('done\n')
            break
        except Exception as e:
            print(e)
            count = count + 1
            time.sleep(BACKOFF * count)
    if count >= RETRY_COUNT:
        print("GET failed")
        time.sleep(10)
    return r

if __name__ == "__main__":
    data = {
        'code': '005930', 
        'open': 40000, 
        'low': 45000, 
        'high': 55000, 
        'close': 49000,
        'volume': 999999,
        'published_date': '2021-05-27T15:30'
        }

    # post_data(data, type='day')
    print(get_data(data['code'], type='day'))