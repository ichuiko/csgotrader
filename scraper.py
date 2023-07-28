import json
import requests
from data.db import saveOrders
import os.path as pt

def parseData(sourceId:int) :
    if sourceId == 1 :
        url = 'https://market.csgo.com/api/v2/prices/USD.json'
        r = requests.get(url)
        data = json.loads(r.text)
        info = []

        for i in data['items'] :
            item = [sourceId, data['time'] ,i['market_hash_name'].replace("'", " "), int(i['volume']), i['price']]
            info.append(item)
        
        saveOrders(info)
        print("sucsdf")

parseData(1)