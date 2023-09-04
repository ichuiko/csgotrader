import sqlite3
import os.path as pt
import json
import requests
import xml.etree.ElementTree as ET

#cursor.execute("""CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT , market_hash_name TEXT NOT NULL, buff163_id INTEGER)""")
#cursor.execute("""CREATE TABLE IF NOT EXISTS orders (sourceId INTEGER NOT NULL, time INTEGER NOT NULL, market_hash_name TEXT NOT NULL, volume INTEGER , price TEXT, checked_buff163 INTEGER)""")
#cursor.execute("""CREATE TABLE IF NOT EXISTS sendings (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT , is_sended INTEGER)""")

def saveOrders(data:list):
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE IF EXISTS orders""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders (sourceId INTEGER NOT NULL, time INTEGER NOT NULL, market_hash_name TEXT NOT NULL, volume INTEGER , price TEXT, checked_buff163 INTEGER)""")

    query = f"""INSERT INTO orders VALUES(?,?,?,?,?,?)"""
    cursor.executemany(query,data)
    conn.commit()

def getItemsToCompare(limit:int) :
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()

    query = f"""SELECT items.buff163_id, orders.market_hash_name ,orders.price, orders.volume FROM orders INNER JOIN items ON items.market_hash_name = orders.market_hash_name WHERE orders.checked_buff163 = 0 ORDER BY RANDOM() LIMIT {limit}"""
    cursor.execute(query)
    data = cursor.fetchall()

    return data

def setCheckedOrder(name:str) :
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()

    query = f"""UPDATE orders SET checked_buff163 = 1 WHERE market_hash_name = '{name}'"""
    cursor.execute(query)
    conn.commit()

    return True

def getSendings():
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()
    query = """SELECT * FROM sendings WHERE is_sended = 0 ORDER BY id DESC"""
    cursor.execute(query)
    data = cursor.fetchall()

    return data

def createSending(data:dict):
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()
    query = f"""INSERT INTO sendings (data) VALUES('{json.dumps(data)}')"""
    cursor.execute(query)
    conn.commit()

    return True

def updateSending(id:int):
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()
    query = f"""UPDATE sendings SET is_sended = 1 WHERE id = {id}"""
    cursor.execute(query)
    conn.commit()

