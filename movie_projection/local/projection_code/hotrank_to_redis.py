import redis,requests
from bs4 import BeautifulSoup
IP='<VM IP>'
hot_name_dict= {}
hot_url_dict= {}
hot_img_url_dict= {}
url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
res = requests.post(url)
soup = BeautifulSoup(res.text, 'html.parser')
title_list = soup.select('table[class="chart full-width"] td[class="titleColumn"]')
title_img = soup.select('img')
for n, title in enumerate(title_list[:10]):
    title_no = title.find('div').text.split('\n')[0]
    title_name = title.select('a')[0].text + title.select('span')[0].text
    title_url = 'https://www.imdb.com' + title.select('a')[0]['href']
    img_url = title_img[n]['src']
    hot_name_dict['hotname_'+str(n)]=title_name
    hot_url_dict['hoturl_'+str(n)]=title_url
    hot_img_url_dict['hotimg_'+str(n)]=img_url

red=redis.StrictRedis(host=IP,port=6379,db=0)
red.mset(hot_name_dict)
red.mset(hot_url_dict)
red.mset(hot_img_url_dict)