from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


import os
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
fiat = 'USD'
key_path = './config/coinmarketcap.json'

with open(key_path, 'r') as f:
    API_KEY = json.load(f)['key']

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

params = {
    'start':'1',
    'limit':'5000',
    'convert':fiat
}

session = Session()
session.headers.update(headers)

try:
    r = session.get(url, params=params)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

# print(r.json())

res = r.json()

def save_json(path, obj):
    with open(path+'tmp', 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.rename(path+'tmp', path)


file_path = './data/coinmarket/coin_{}.json'.format(res['status']['timestamp'])
print(file_path)

save_json(file_path, res)