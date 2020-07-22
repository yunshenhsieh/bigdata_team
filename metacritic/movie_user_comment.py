import requests,time,random
from bs4 import BeautifulSoup

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
def user_score_comment(user_score_url):
    title = user_score_url.split('/')[-2]
    req_comment = requests.get(url=user_score_url,headers=headers)
    soup_comment = BeautifulSoup(req_comment.text,'html.parser')
    total_page = soup_comment.select('ul[class="pages"] li a')
    print(title,'下載中')
    if total_page == []:
        user_comment_score(soup_comment,title)
    else:
        page_num=1
        user_comment_score(soup_comment,title)
        for user_comment_page in total_page:
            page_num+=1
            print(title,'評論，第',page_num,'下載中')
            user_comment_page_url= 'https://www.metacritic.com/' + user_comment_page['href']
            req_page_comment = requests.get(url=user_comment_page_url, headers=headers)
            soup_page_comment = BeautifulSoup(req_page_comment.text, 'html.parser')
            user_comment_score(soup_page_comment,title)
            print('睡眠中…')
            time.sleep(random.randint(3,5))
def write_score(title,score):
    with open('./meta_comment_score.csv','a',encoding='utf-8')as f:
        f.write(title + '|' + score + '|')
def write_name_comment(name,comment):
    with open('./meta_comment_score.csv','a',encoding='utf-8')as f:
        f.write(name + '|' + comment + '\n')
def user_comment_score(soup_comment,title):
    score_perfect='div[class="metascore_w user large movie positive indiv perfect"]'
    score_positive='div[class="metascore_w user large movie positive indiv"]'
    score_mixed='div[class="metascore_w user large movie mixed indiv"]'
    score_negative='div[class="metascore_w user large movie negative indiv"]'
    name_comment='span[class="author"]'
    n=0
    for score in soup_comment.select('div[class="review pad_top1"]'):
        for item in score.select('div[class="summary"]'):
            try:
                if item.select('span')[2]['class'][1] == 'blurb_expanded':

                    # print('page：',n)
                    if score.select(score_perfect) != []:
                        score=score.select(score_perfect)[0].text
                        write_score(title,score)
                    elif score.select(score_positive) != []:
                        score=score.select(score_positive)[0].text
                        write_score(title, score)
                    elif score.select(score_mixed) != []:
                        score=score.select(score_mixed)[0].text
                        write_score(title, score)
                    elif score.select(score_negative) != []:
                        score=score.select(score_negative)[0].text
                        write_score(title, score)
                    name=soup_comment.select(name_comment)[n].text
                    comment=item.select('span[class="blurb blurb_expanded"]')[0].text
                    write_name_comment(name,comment)
                    n += 1
            except:

                # print('page：',n)
                if score.select(score_perfect) != []:
                    score=score.select(score_perfect)[0].text
                    write_score(title, score)
                elif score.select(score_positive) != []:
                    score=score.select(score_positive)[0].text
                    write_score(title, score)
                elif score.select(score_mixed) != []:
                    score=score.select(score_mixed)[0].text
                    write_score(title, score)
                elif score.select(score_negative) != []:
                    score=score.select(score_negative)[0].text
                    write_score(title, score)
                name=soup_comment.select(name_comment)[n].text
                comment=item.select('div[class="review_body"] span')[0].text
                write_name_comment(name,comment)
                n += 1
