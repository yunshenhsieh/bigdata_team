import requests,sqlite3,datetime
from bs4 import BeautifulSoup
import pandas as pd



def crawler_boxoffice(year):
    url='https://www.boxofficemojo.com/year/world/{}/'.format(year)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    res = requests.get(url=url,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    data=soup.select('td')

    data = [item.text.replace('-','NA') for item in data]
    data2=[data[item:item+7] for item in range(0,len(data),7)]

    df=pd.DataFrame(data=data2,columns=['rank','movie_name','worldwide_gross',
                             'domestic_gross','domestic_gross_percent',
                             'foreign_gross','foreign_gross_percent'])

    table_name='boxoffice_' + str(year)

    conn=sqlite3.connect("boxoffice_worldwide_gross.sqlite")
    sql_create_table='CREATE TABLE IF NOT EXISTS {}(' \
                     'rank TEXT,movie_name TEXT,worldwide_gross TEXT,' \
                     'domestic_gross TEXT,domestic_gross_percent TEXT,' \
                     'foreign_gross TEXT,foreign_gross_percent TEXT);'.format(table_name)
    cursor = conn.cursor()
    cursor.execute(sql_create_table)
    i=0
    while True:
        # if i == 32:break
        sql_insert = 'INSERT INTO {} (rank,movie_name,worldwide_gross,domestic_gross,domestic_gross_percent,foreign_gross,foreign_gross_percent) ' \
              'VALUES ("{}","{}","{}","{}","{}","{}","{}");'\
            .format(
            table_name,
            str(df.loc[i][0]).replace('"','＂').replace("%",'％'),
            str(df.loc[i][1]).replace('"','＂').replace("%",'％'),
            str(df.loc[i][2]).replace('"','＂').replace("%",'％'),
            str(df.loc[i][3]).replace('"','＂').replace("%",'％'),
            str(df.loc[i][4]).replace('"','＂').replace("%",'％'),
            str(df.loc[i][5]).replace('"','＂').replace("%",'％'),
            str(df.loc[i][6]).replace('"','＂').replace("%",'％'))
    #         # str(data.loc[i][7]).replace('"','＂'),
    # #                 str(data.loc[i][8]).replace('"','＂')
    # #
        ce=cursor.execute(sql_insert)
        conn.commit()
        i+=1
        print('EI：', ce,'No：',i)
    cursor.close()
    conn.close()


def main():
    year=input('要從幾年開始下載：')
    try:
        year=int(year)
        crawler_boxoffice(year)
    except:
        try:
            while datetime.date.today().year > year:
                try:
                    year+=1
                    crawler_boxoffice(year)
                except:
                    year+=1
                    crawler_boxoffice(year)
        except:
            print(year)

if __name__ == '__main__':
    main()