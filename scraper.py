import json
import requests
from data.db import saveOrders, getItemsToCompare, setCheckedOrder, createSending
import os.path as pt
from bs4 import BeautifulSoup

class Market():

    def parse(self) :
        url = 'https://market.csgo.com/api/v2/prices/USD.json'
        r = requests.get(url)
        data = json.loads(r.text)
        info = []

        for i in data['items'] :
            if int(i['volume']) >= 30 and float(i['price']) >= 3:
                item = [1, data['time'] ,i['market_hash_name'].replace("'", " "), int(i['volume']), i['price'], 0]
                info.append(item)
            
        saveOrders(info)

class Buff():
    currency = 0.14
    def getInfoByBuffId(self, buffId:int) :
        url = f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={buffId}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1691749431491'
        r = requests.get(url=url)
        if r.status_code == 200:
            data = json.loads(r.text)
            volume = data['data']['total_count'] * 10
            price = float(data['data']['items'][0]['price']) * self.currency
            url = f"https://buff.163.com/goods/{buffId}?from=market#tab=selling"
            info = [volume,price,url]
            return info
        else: 
            return 'error'
        
    def parse(self) :
        items = getItemsToCompare(limit=15)
        for i in items:
            buffData = self.getInfoByBuffId(i[0])
            setCheckedOrder(name=i[1])
            a = float(i[2])
            b = float(buffData[1])
            if a < b:
                profit = ((b-a)/a)*100 
            else:
                profit = ((a-b)/a)*100
            
            if profit >= 30:
                model = {
                    'marketHashName' : i[1],
                    'profit' : profit,
                    'marketPriceUsd' : a,
                    'buffPriceUsd' : b,
                    'marketVolume' : i[3],
                    'buffVolume' : buffData[0],
                    'marketUrl' : f'https://market.csgo.com/ru/{i[1]}',
                    'buffUrl' : buffData[2]
                }
                createSending(model)
                print(model)
