import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from datetime import datetime
import os
import re


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = { 'User-Agent' : user_agent }

def get_news_content(news_list):
    """뉴스의 내용을 가져오는 함수

    Args:
        news_list (list): 정보를 받아올 뉴스의 제목과 url이 담긴 딕셔너리를 담은 리스트

    Returns:
        list: 뉴스의 제목, url, 내용이 담긴 딕셔너리를 담은 리스트
    """
    for i, news in enumerate(news_list):
        url = news['url']
        # 뉴스의 url로 get() 요청을 보내서 응답을 받아옴
        response = requests.get(url, headers=headers)
        
        # #mArticle > div.news_view.fs_type1 > div.article_view > section > p:nth-child(4)
        # #mArticle > div.news_view.fs_type1 > div.article_view > section > p:nth-child(7)
        # #mArticle > div.news_view.fs_type1 > div.article_view > section > p:nth-child(7)
        
        # 요청이 성공했을 경우
        if response.status_code == 200:
            # 요청을 beutifulsoup에 넣어서 파싱
            soup = bs(response.text, 'lxml')
            # 뉴스 내용을 가져오는 css selector
            tags = soup.select('#mArticle > div.news_view section > p')
            # 가져온 내용들을 하나의 문자열로 만들어서 news['content']에 저장
            for tag in tags:
                news['content'] += tag.text.replace('\n', ' ').strip()
        # 요청이 실패했을 경우, 상태코드를 출력
        else:
            pprint(response.status_code)
        
        news_list[i] = news
    
    return news_list

def get_news_list():
    """다음 뉴스의 제목과 url, 내용을 가져오는 함수

    Returns:
        list: 뉴스의 제목, url, 내용이 담긴 딕셔너리를 담은 리스트
    """
    daum_news_url = r'https://news.daum.net/'

    # 유저에이전트가 웹 크롤러일 경우 서버에서 차단할 수 있음
    # 다음 뉴스의 메인 페이지로 get() 요청을 보내서 응답을 받아옴
    response = requests.get(daum_news_url, headers=headers)

    # body > div.container-doc > main > section > div > div.content-article
    # > div.box_g.box_news_issue > ul > li:nth-child(1) > div > div > strong > a
    # body > div.container-doc > main > section > div > div.content-article
    # > div.box_g.box_news_issue > ul > li:nth-child(1) > div > div > strong > a
    # body > div.container-doc > main > section > div > div.content-article
    # > div.box_g.box_news_issue > ul > li:nth-child(7) > div > div > strong > a

    # 뉴스의 제목과 url을 저장할 리스트
    news_list = []
    # 요청이 성공했을 경우
    if response.status_code == 200:
        # 요청을 beutifulsoup에 넣어서 파싱
        soup = bs(response.text, 'lxml')
        
        # 메인 뉴스를 모두 가져오기 위한 반복문
        i = 0
        while True:
            try: 
                i += 1
                # 메인 뉴스의 제목과 url을 가져오는 css selector
                tag = soup.select_one(f'div.box_g.box_news_issue > ul > li:nth-child({i}) > div > div > strong > a')
                # 가져온 제목과 url을 딕셔너리로 만들어서 news_list에 저장,
                # 뉴스 내용은 아직 가져오지 않음
                t = { 'title' : tag.text.replace('\n', ' ').strip(), 'url' : tag['href'], 'content' : ''}
                news_list.append(t)
            except:
                break
    # 요청이 실패했을 경우, 상태코드를 출력
    else:
        pprint(response.status_code)
    
    # 뉴스의 컨텐츠를 가져오는 함수 호출
    news_list = get_news_content(news_list)
    
    # 가져온 뉴스의 제목, url, 컨텐츠를 데이터프레임으로 만들어서 반환
    df = pd.DataFrame({
            'title' : [news['title'] for news in news_list],
            'url' : [news['url'] for news in news_list],
            'content' : [news['content'] for news in news_list]
        })
        
    return  df

d = datetime.now().strftime('%Y-%m-%d') # strftime : 문자열로 변환
file_path = r'news_and_contents_{}.csv'.format(d)
result = get_news_list()
result.to_csv(file_path, index=False)

file_path = r'.\news\{}'.format(d)
# 폴더가 없으면 생성
os.makedirs(file_path, exist_ok=True)
for title, news in zip(result['title'], result['content']):
    # 파일명에 사용할 수 없는 문자를 제거
    title = re.sub(r'[\W]', '', title)
    with open(file_path + f'\{title}.txt', 'wt', encoding='utf-8') as f:
        f.write(news)