import sqlite3
import pandas as pd
con = sqlite3.connect('gy_tidy.db')
cur = con.cursor()
cur.execute('''CREATE TABLE cats
        (id INT PRIMARY KEY, purpose TEXT, area FLOAT, nation TEXT, permit BOOL, district TEXT, village TEXT, year INT)''')
gy = pd.read_csv('gy_tidy.csv')
gy.index = gy.index.astype(float)
gy['연도'] = gy['연도'].astype(float)
cur.executemany('INSERT INTO cats VALUES ('+('?,'*8)[:-1]+')', gy.to_records())
con.commit()
con.close()
