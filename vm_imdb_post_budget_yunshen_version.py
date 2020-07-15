import requests,time,random
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import smtplib

def send_mail_for_me(e):
    '利用 Gmail 的服務寄發通知信'
    send_gmail_user = 'XXXXXXXX@gmail.com'
    send_gmail_password = email password
    rece_gmail_user = 'XXXXXXXX@gmail.com'

    msg = MIMEText('imdb預算及海報爬蟲已停止')

    msg['Subject'] = (e)
    msg['From'] = send_gmail_user
    msg['To'] = rece_gmail_user

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_gmail_user, send_gmail_password)
    server.send_message(msg)
    server.quit()

with open('./movielist.csv', 'r', encoding='utf-8') as e:
    m_list = e.readlines()
with open('E:/movie_project/budget_log.csv','r',encoding='utf-8')as f:
    nn=f.read()

nn=int(nn)
for m_id in m_list[nn-1:]:
    m_id = m_id.replace('\n','')
    url = 'https://www.imdb.com/title/{}/?ref_=adv_li_tt'.format(m_id)
    try:
        res = requests.post(url)
        while res.status_code != 200:
            res = requests.post(url)
            time.sleep(random.randint(60,100))
    except:
        e='第一段exception'
        print(e)
        print(res.status_code)
        send_mail_for_me(e)
    soup = BeautifulSoup(res.text, 'html.parser')

    #取得海報
    post_url = soup.select('div[class="poster"] img')[0]['src']
    try:
        res_img = requests.get(post_url)
        while res_img.status_code != 200:
            res_img = requests.get(url)
            time.sleep(random.randint(60,100))
    except:
        e='第二段exception'
        print(e)
        print(res.status_code)
        send_mail_for_me(e)


    img_content = res_img.content  #取得圖片的文字檔(二進制)
    print(post_url)
    with open('E:/movie_project/imdb_post/' + m_id +'.jpg', 'wb') as f:
        f.write(img_content)   #二進制要用wb寫入

    #取得預算
    budget_list = soup.select('div[class="txt-block"]')
    for i in budget_list:
        a = i.text
        if 'Budget:' in a:
            a = a.replace(' ', '').replace('\n', '').replace('Budget:', '').replace('(estimated)', '')
            with open('E:/movie_project/Budget.csv', 'a', encoding='utf-8') as f:
                f.write(m_id + '|' + a)
                f.write('\n')

    print(nn)
    nn += 1
    with open('E:/movie_project/budget_log.csv','w',encoding='utf-8')as f:
        f.write(str(nn))
    time.sleep(random.randint(4, 8))

