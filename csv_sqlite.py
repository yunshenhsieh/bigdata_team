import sqlite3
import pandas as pd
import os

i=0
conn=sqlite3.connect("six_million_6958382.sqlite")
sql_create_table='CREATE TABLE IF NOT EXISTS bigdata(' \
    'tconst TEXT,titleType TEXT,' \
    'primaryTitle TEXT,originalTitle TEXT,' \
    'isAdult TEXT,startYear TEXT,' \
    'endYear TEXT,runtimeMinutes TEXT,genres TEXT);'
cursor = conn.cursor()
def check_use():
    sel = 'SELECT * FROM bigdata;'
    cursor.execute(sel)
    mes = cursor.fetchall()
    print(mes)
    for item in mes[:10]:
        sel_ten= 'SELECt * FROM bigdata WHERE tconst = "{}"'.format(item[0])
        cursor.execute(sel_ten)
        print(cursor.fetchall())


# cursor.execute(sql_create_table)
# data=pd.read_csv('./data.tsv','\t')
# while True:
#     # if i == 10:break
#     sql_insert = 'INSERT INTO bigdata (tconst,titleType,primaryTitle,originalTitle,isAdult,startYear,endYear,runtimeMinutes,genres) ' \
#           'VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}");'\
#         .format(str(data.loc[i][0]).replace('"','＂'),
#                 str(data.loc[i][1]).replace('"','＂'),
#                 str(data.loc[i][2]).replace('"','＂'),
#                 str(data.loc[i][3]).replace('"','＂'),
#                 str(data.loc[i][4]).replace('"','＂'),
#                 str(data.loc[i][5]).replace('"','＂'),
#                 str(data.loc[i][6]).replace('"','＂'),
#                 str(data.loc[i][7]).replace('"','＂'),
#                 str(data.loc[i][8]).replace('"','＂'))
#         # .format(.replace('"','＂'))
#
#     ce=cursor.execute(sql_insert)
#     conn.commit()
#     i+=1
#     print('EI：', ce,'No：',i)
check_use()
cursor.close()
conn.close()


# if __name__ == '__main__':
#     check_use()