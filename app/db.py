import sqlite3
import os

def get_db_connection():
    # 確保 instance 資料夾存在，並指定資料庫路徑
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn
