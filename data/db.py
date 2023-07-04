import sqlite3
import os.path as pt
import json
import requests

dbFilename = pt.abspath('data/data.db')
conn = sqlite3.connect(dbFilename,check_same_thread=False)
cursor = conn.cursor()

token = '5521071937:AAFVUpbOsHj2aSxsVv_PMkdGKf57Ds3I72M'
channel = '@botTraderTesting'

#SCHEMA
cursor.execute("""CREATE TABLE IF NOT EXISTS items (market_hash_name text, price real , time integer)""")


def parseData():
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()

    url = 'https://market.csgo.com/api/v2/prices/RUB.json'
    r = requests.get(url)

    data = json.loads(r.text)
    for i in data['items'] :
        item = [i['market_hash_name'], i['price']]
        name = i['market_hash_name'].replace("'", "")
        name.replace("★", "")
        query = f"""INSERT INTO items VALUES('{name}',{i['price']}, {data['time']})"""
        cursor.execute(query)
        conn.commit()

def selectData():
    query = """SELECT market_hash_name FROM items GROUP BY market_hash_name"""
    cursor.execute(query)
    names = cursor.fetchall()
    cursor.execute("""CREATE TABLE journal (market_hash_name text, price_diff real)""")

    for name in names:
        query = f"""SELECT * FROM items WHERE market_hash_name = '{name[0]}' ORDER BY time DESC """
        cursor.execute(query)
        data = cursor.fetchall()
        if len(data) > 1:
            priceDiff = data[0][1] - data[1][1]
            if priceDiff < 1:
                continue
            else:
                query = f"""INSERT INTO journal VALUES('{data[0][0]}', {priceDiff})"""
                cursor.execute(query)
                conn.commit()
        else:
            continue
    
    query = f"""SELECT * FROM journal ORDER BY price_diff DESC"""
    cursor.execute(query)
    result = cursor.fetchall()

    message = ""
    for res in result[:15] :
        message += f"{res[0]} - {res[1]} \n"

    cursor.execute("""DROP TABLE journal""")

    return message

def sendMessage(message:str) :
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': channel,
        'text': message
    }

    r = requests.get(url=url, params=params)
    print(r.text)

def parser():
    message = selectData()
    sendMessage(message=message)

parser()

