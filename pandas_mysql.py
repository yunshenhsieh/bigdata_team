import pandas as pd
import os
import pymysql
host = 'localhost'
port = 3306
user = 'root'
passwd = 'mysqlroo'
db = 'test'
charset = 'utf8mb4'

data=pd.read_csv('./data.tsv','\t')
i=0
while True:
    if i == 60000:break
    sql = 'INSERT INTO bigdata (na,nb,nc,nd,ne,nf,ng,nh,ni) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}");'\
        .format(str(data.loc[i][0]).replace('"','＂'),
                str(data.loc[i][1]).replace('"','＂'),
                str(data.loc[i][2]).replace('"','＂'),
                str(data.loc[i][3]).replace('"','＂'),
                str(data.loc[i][4]).replace('"','＂'),
                str(data.loc[i][5]).replace('"','＂'),
                str(data.loc[i][6]).replace('"','＂'),
                str(data.loc[i][7]).replace('"','＂'),
                str(data.loc[i][8]).replace('"','＂'))
        # .format(.replace('"','＂'))
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()
    ce = cursor.execute(sql)
    cc = conn.commit()
    print('EI：', ce, cc)
    i+=1
cursor.close()
conn.close()
print(i)