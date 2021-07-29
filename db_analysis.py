import sqlite3
con = sqlite3.connect('gy_tidy.db')
cur = con.cursor()
cur.execute('''SELECT district, village, AVG(area) FROM cats
        GROUP BY village ORDER BY AVG(area)''')
with open('gy_avg_acq_area.txt','w') as file:
    file.write('\n'.join([str(i) for i in list(cur)]))
cur.execute('''SELECT district, year, COUNT(id) FROM cats
        WHERE year=19 GROUP BY district''')
before_covid = list(cur)
cur.execute('''SELECT district, year, COUNT(id) FROM cats
        WHERE year LIKE '2%' GROUP BY district''')
after_covid = list(cur)
print(before_covid, end='\n')
print(after_covid)
cur.execute('''SELECT nation, COUNT(id) FROM cats
        GROUP BY nation HAVING COUNT(id) > 6 
        ORDER BY COUNT(id) DESC''')
print(*list(cur), sep='\n')
con.close()
