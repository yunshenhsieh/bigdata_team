def get_index1(lst=None, item=''):
    return [index for (index,value) in enumerate(lst) if value == item]

def onehot():
    with open('classic.csv','r',encoding='utf-8')as f:
        cla=f.read()
    import pandas_csv
    total=pandas_csv.clus()
    cla=cla.strip().replace(' TEXT','')
    cla=cla.split(',')[:-1]

    d={}
    for i in total:
        tmp = '0' * 25
        tmp = list(tmp)
        onehot=[]
        cl=i[1].split('|')
        for j in cl:
            for ji in cla:
                if ji.strip() == j.strip():
                    onehot.append('1')
                else:
                    onehot.append('0')
        for k in get_index1(onehot, '1'):
            tmp[k % 25] = '1'
        d[i[0]]=tmp
    return cla,d

# with open('movie_onehot.csv','w',encoding='utf-8')as f:
#     for i in d.items():
#         f.write(str(i).replace('(','').replace(')','') + '\n')
