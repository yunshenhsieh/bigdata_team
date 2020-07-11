import pandas as pd
# with open('./movie_add12.csv','r',encoding='utf-8-sig')as f:
#     a=f.readlines()
# ts=[]
# for i in a:
#     s=i.replace("[",'').replace("'","").replace("]",'').replace('\n','').split(',')
#     tmp=s[:4]
#     s='|'.join(tmp) + '|' +str(s[4:]).replace("[",'').replace("'","").replace("]",'')
#     ts=s.split('|')
#     with open('./test_check.csv','a',encoding='utf-8')as f:
#          f.write(str(s) + '\n')


with open('./test_check.csv','r',encoding='utf-8')as f:
    data_view=f.readlines()

data=[item.split('|') for item in data_view]
df=pd.DataFrame(data=[item for item in data[1:]],columns=data_view[0].split('|'))
print(df)