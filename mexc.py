import hashlib
import json
import time
import os
import requests

def md5(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()

def mexc_crypto(key, obj):
    date_now = str(int(time.time() * 1000))
    g = md5(key + date_now)[7:]
    s = json.dumps(obj, separators=(',', ':'))
    sign = md5(date_now + s + g)
    return {'time': date_now, 'sign': sign}

def place_order(key, obj, url):
    signature = mexc_crypto(key, obj)
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'Authorization': key
    }
    response = requests.post(url, headers=headers, json=obj)
    return response.json()


key = "WEBc59...."

obj = {
    "symbol": "<SYMBOL_USDT>",
    "side": 1,
    "openType": 1,
    "type": 1,
    "vol": 2,
    "leverage": 5,
    "price": 1.2,
}

url = 'https://futures.mexc.com/api/v1/private/order/create'
response = place_order(key, obj, url)
print(response)
