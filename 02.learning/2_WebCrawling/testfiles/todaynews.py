import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from datetime import datetime


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = { 'User-Agent' : user_agent }

def get_news_list():
    daum_news_url = r'https://news.daum.net/'

    # 유저에이전트가 웹 크롤러일 경우 서버에서 차단할 수 있음
    response = requests.get(daum_news_url, headers=headers)

    # body > div.container-doc > main > section > div > div.content-article
    # > div.box_g.box_news_issue > ul > li:nth-child(1) > div > div > strong > a

    # body > div.container-doc > main > section > div > div.content-article
    # > div.box_g.box_news_issue > ul > li:nth-child(1) > div > div > strong > a

    # body > div.container-doc > main > section > div > div.content-article
    # > div.box_g.box_news_issue > ul > li:nth-child(7) > div > div > strong > a

    news_list = []

    if response.status_code == 200:
        soup = bs(response.text, 'lxml')
        for i in range(1, 20):
            try: 
                tag = soup.select_one(f'div.box_g.box_news_issue > ul > li:nth-child({i}) > div > div > strong > a')
                t = [tag.text.replace('\n', ' ').strip(), tag['href']]
                news_list.append(t)
            except:
                break
        
    else:
        pprint(response.status_code)
        
    df = pd.DataFrame({
            'title' : [news[0] for news in news_list],
            'url' : [news[1] for news in news_list]
        })
        
        
    return  df

d = datetime.now().strftime('%Y-%m-%d') # strftime : 문자열로 변환
file_path = r'news_{}.csv'.format(d)
result = get_news_list()
result.to_csv(file_path, index=False)
