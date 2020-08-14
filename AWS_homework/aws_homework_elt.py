import requests
from bs4 import BeautifulSoup
import os

# 爬蟲環境設定
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
cookies={'over18':'1'}
k=0
# AWS s3設定
import boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAR4NDUH53GWDLQFNM',
    aws_secret_access_key='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'
)
# 輸入ptt網址，並且判斷是否為ptt網址，不是的話則請使用者再次輸入，之後告知此版目前最大頁數。
while True:
    keyin_websit = input('請輸入想抓取的ptt版網址，非首頁：')
    ptt_homepage = 'https://www.ptt.cc/bbs'
    keyin_websit = keyin_websit.split('/')
    check_websit = '/'.join(keyin_websit[0:4])
    file_name = input('請輸入存放資料夾名稱：')
    if (keyin_websit[0] != 'Q') and (keyin_websit[0] != 'q'):
        if (check_websit == ptt_homepage) and (len(keyin_websit) > 4) and (keyin_websit[4] != '' and keyin_websit[4].strip() != 'index.html'):
            keyin_websit[-1]='index{}.html'
            pre_url = '/'.join(keyin_websit).strip().format('')
            pre_req = requests.post(url=pre_url,headers=headers,cookies=cookies)
            pre_soup = BeautifulSoup(pre_req.text,'html.parser')
            pre_bt = pre_soup.select('a[class="btn wide"]')[1]['href']
            total_page = int(pre_bt.replace('.html','').split('index')[1]) + 1
            input_start = '總頁數：'+ str(total_page) +'，請輸入要下載起始頁數：'
            input_end = '結束頁數：'
            k=1
            break
        else:
            print('請輸入正確網址，或Q退出程式')
    else:
        print('退出程式。')
        break
# 確定是ptt網址，進入到讓使用者想爬取的頁數範圍，若輸入非數字或超過最大頁數，則請使用者再次輸入。
if k == 1:
    while True:
        keyin_start=input(input_start)
        if keyin_start.isdigit() and (int(keyin_start)<=total_page):
            keyin_end=input(input_end)
            if (keyin_end) == ('q' or 'Q'):
                print('退出程式。')
                break

            elif keyin_end.isdigit() and (int(keyin_end)<=total_page):
                keyin_start = int(keyin_start)
                keyin_end = int(keyin_end)
                if (keyin_start - keyin_end) >= 0:
                    page = keyin_start
                    break
                elif (keyin_start - keyin_end) < 0:
                    page=keyin_end
                    break
            else:
                print('請輸入範圍內正整數，或Q退出程式')
        elif (keyin_start) == ('q' or 'Q'):
            print('退出程式。')
            break
        else:
            print('請輸入範圍內正整數，或Q退出程式')
    # 爬取檔案存放路徑，順便處理非檔名可用的字元，路徑設定為使用者桌面。
    path = os.path.expanduser('~') + '\\Desktop\\' + file_name.replace('\\', '\'反斜\'').replace('/', '／').replace('?','？') \
        .replace(':', '：').replace('*', '＊').replace('\"', '＂').replace('<', '＜').replace('>', '＞').replace('|', '｜')
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + '\\'
    print('存放位置：' + path)

    # 判斷頁數範圍。
    try:
        if keyin_start >= keyin_end:
            download_num = keyin_start - keyin_end
        else:
            download_num = keyin_end - keyin_start
        # 處理網址為統一格式。
        pre_url = pre_url.split('/')
        pre_url[-1] = 'index{}.html'
        # 正在爬取的當頁資訊。
        for ran in range(download_num + 1):
            url = '/'.join(pre_url)
            req = requests.post(url=url.format(page), headers=headers,cookies=cookies)
            soup = BeautifulSoup(req.text, 'html.parser')
            tweety=0
            # 爬取當頁文章內容。
            for tweety in range(20):
                try:
                    new_url = 'https://www.ptt.cc/' + soup.select('div[class="title"]')[tweety]('a')[0]['href']
                    new_req = requests.post(url=new_url, headers=headers,cookies=cookies)
                    new_soup = BeautifulSoup(new_req.text,'html.parser')

                    # 標題、作者、發文時間
                    title = new_soup.select('div[class="article-metaline"] span')
                    author = title[0].text + ': ' + title[1].text
                    label = title[2].text + ': ' + title[3].text
                    post_time = title[4].text + ': ' + title[5].text

                    # 推噓數處理
                    push_like = new_soup.select('div[class="push"] span')
                    j = 0;
                    push_list = []
                    for i in push_like:
                        if j % 4 == 0:
                            push_list += push_like[j].text
                        else:
                            pass
                        j += 1

                    like = push_list.count('推')
                    dislike = push_list.count('噓')
                    # 文章內容
                    content = new_soup.select('div[id="main-container"]')
                    # 檔名
                    tit = str(page)+'n'+str(tweety+1) + ''.join([title.text for title in title[0:6]]).replace(':', '')
                    # 檔案存入電腦
                    with open(path +'{}.txt'.format(tit), 'w', encoding='utf-8') as f:
                        f.write(
                            content[0].text.split('※ 發信站')[0] + '\n---split---' + '\n' +
                            '推： ' + str(like) + '\n' +
                            '噓： ' + str(dislike) + '\n' +
                            '分數： ' + str(like - dislike) + '\n' +
                            author + '\n' +
                            label + '\n' +
                            post_time)
                    # 使用s3_client上傳爬下來的資料夾至桶子內
                    s3_client.upload_file(path + '{}.txt'.format(tit), 'eb102', 'student3/' + tit)
                # 超出索引值處理，還是印下來，因為ptt刪文後就會造成索引值消失，雖然沒有內容，但可以做日後核對跟檢查用。
                except IndexError as e:
                    tit = str(page)+'n'+str(tweety+1) + str(e)
                    with open(path +'{}.txt'.format(tit), 'w', encoding='utf-8') as f:
                        f.write(
                            content[0].text.split('※ 發信站')[0] + '\n---split---' + '\n' +
                            '推： ' + str(like) + '\n' +
                            '噓： ' + str(dislike) + '\n' +
                            '分數： ' + str(like - dislike) + '\n' +
                            author + '\n' +
                            label + '\n' +
                            post_time)
                    # 使用s3_client上傳爬下來的資料夾至桶子內
                    s3_client.upload_file(path + '{}.txt'.format(tit), 'eb102', 'student3/' + tit)
                # 通常是出現非檔名字元造成，在此處理非檔名字元後重新存入。
                except OSError:
                    tit=tit.replace('\\','\'反斜\'').replace('/','／').replace('?','？').replace(':','：').replace('*','＊')\
                        .replace('\"','＂').replace('<','＜').replace('>','＞').replace('|','｜')
                    with open(path +'{}.txt'.format(tit), 'w', encoding='utf-8') as f:
                        f.write(
                            content[0].text.split('※ 發信站')[0] + '\n---split---' + '\n' +
                            '推： ' + str(like) + '\n' +
                            '噓： ' + str(dislike) + '\n' +
                            '分數： ' + str(like - dislike) + '\n' +
                            author + '\n' +
                            label + '\n' +
                            post_time)
                    # 使用s3_client上傳爬下來的資料夾至桶子內
                    s3_client.upload_file(path +'{}.txt'.format(tit), 'eb102', 'student3/' + tit)
                # 換下一篇文章
                tweety += 1
            # 換下一頁
            page-=1

        print('程式結束。')

    except:
        print('程式結束。')
else:
    print('程式結束')