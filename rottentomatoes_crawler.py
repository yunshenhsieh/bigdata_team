import requests,json
from bs4 import BeautifulSoup
url='https://www.rottentomatoes.com/top/bestofrt/?year=2019'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
req=requests.get(url=url,headers=headers)
soup=BeautifulSoup(req.text,'html.parser')

soup_list=str(soup.select('script')[1]).replace('</script>','>').split('>')

data=json.loads(soup_list[1])
