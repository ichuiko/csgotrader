import sqlite3
import os.path as pt
import json
import requests

#cursor.execute("""CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT , market_hash_name TEXT NOT NULL, buff163_id INTEGER)""")
#cursor.execute("""CREATE TABLE IF NOT EXISTS orders (sourceId INTEGER NOT NULL, time INTEGER NOT NULL, market_hash_name TEXT NOT NULL, volume INTEGER , price TEXT)""")

def saveOrders(data:list):
    dbFilename = pt.abspath('data/data.db')
    conn = sqlite3.connect(dbFilename,check_same_thread=False)
    cursor = conn.cursor()

    query = f"""INSERT INTO orders VALUES(?,?,?,?,?)"""
    cursor.executemany(query,data)
    conn.commit()