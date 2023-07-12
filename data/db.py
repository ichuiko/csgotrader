import sqlite3
import os.path as pt
import json
import requests

#dbFilename = pt.abspath('data.db')
#conn = sqlite3.connect(dbFilename,check_same_thread=False)
#cursor = conn.cursor()
#cursor.execute("""CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT , market_hash_name TEXT NOT NULL)""")
#cursor.execute("""CREATE TABLE IF NOT EXISTS trades (itemId INTEGER NOT NULL  ,price INTEGER NOT NULL, volume INTEGER NOT NULL, time INTEGER NOT NULL , FOREIGN KEY(itemId) REFERENCES items(id) )""")

def parseData():
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()
    url = 'https://market.csgo.com/api/v2/prices/RUB.json'
    r = requests.get(url)    
    data = json.loads(r.text)

    query = f"""SELECT * FROM items"""
    cursor.execute(query)
    items = cursor.fetchall()
        
    for i in data['items'] :
        name = i['market_hash_name'].lower()
        for j in items:
            dbName = j[1].lower()
            if dbName == name:
                query = f"""INSERT INTO trades VALUES({j[0]}, {i['price']}, {i['volume']}, {data['time']})"""
                cursor.execute(query)
                conn.commit()
    return "True"
