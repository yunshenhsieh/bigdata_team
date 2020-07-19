
with open(r'E:\movie_project\Budget.csv','r',encoding='utf-8')as f:
    content=f.read()
with open(r'./budget_code.csv','r',encoding='utf-8')as f:
    money=f.read().split('\n')
money=[item.split('|')[:-1] for item in money[:-1]]
money=dict(money)
raw=[item.split('|') for item in content.replace(',','').replace('$','').split('\n')]

for i in range(len(raw)-1):
    # print(raw[i][1])
    try:
        raw[i][1]=int(raw[i][1])
        raw[i][1]=str(raw[i][1])
        raw[i].insert(1,'NA')
    except:
        # print(money[raw[i][1][0:3]])
        # print(raw[i][1][3:])
        money_tmp=float(raw[i][1][3:]) * float(money[raw[i][1][0:3]])
        money_tmp=int(money_tmp)
        money_tmp=str(money_tmp)
        raw[i].append(money_tmp)
f=open('./budget_changed.csv','a',encoding='utf-8')
for item in raw:
    f.write('|'.join(item) + '\n')

