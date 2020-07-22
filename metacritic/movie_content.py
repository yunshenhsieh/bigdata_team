import requests
from bs4 import BeautifulSoup
import metacritic.movie_user_comment
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def moive_content(title_url_list):
    title_num=0
    for title_url in title_url_list:
        req_content = requests.get(url=title_url, headers=headers)
        soup_content = BeautifulSoup(req_content.text, 'html.parser')
        user_score_url = 'https://www.metacritic.com' + soup_content.select('div[class="title_bump pad_btm1 oswald fh40"] a')[1]['href']
        title_num+=1
        metacritic.movie_user_comment.user_score_comment(user_score_url)


