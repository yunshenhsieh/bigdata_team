import requests
from bs4 import BeautifulSoup
import metacritic.movie_content

def main():
    page=input('想下載幾頁：')
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    for page_num in range(int(page)):
        url = 'https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc&page={}'.format(page_num)
        req = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        movie_url_list=['https://www.metacritic.com' + url_title['href'] for url_title in soup.select('a.title')]
        metacritic.movie_content.moive_content(movie_url_list)
        print('下載第',page_num + 1,'頁中…')

if __name__ == "__main__":
    main()
