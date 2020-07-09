import sqlite3
conn=sqlite3.connect("db.sqlite")
# SQL='CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT);'
# sql = 'INSERT INTO users (name) VALUES ("{}");'.format('it is test')
sel='SELECT * FROM users;'
cursor = conn.cursor()
# cursor.execute(SQL)
# cursor.execute(sql)
cursor.execute(sel)
conn.commit()
mes=cursor.fetchall()
cursor.close()
conn.close()
print(mes)