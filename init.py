import sqlite3
import os

APP_PATH = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'db.sqlite3'

db = sqlite3.connect(os.path.join(APP_PATH, DB_NAME))

cur = db.cursor()
cur.execute("""
    create table if not exists blog(
    id integer primary key autoincrement,
    title text not null,
    content text not null)
    """)
cur.execute("""
   create table if not exists user(
   username char(20),
   password char(50))
    """)

db.commit()
cur.close()
db.close()
