
# 뉴스 목록 csv 파일에 저장된 url을 aiohttp를 이용해 비동기로 크롤링

import asyncio
import aiohttp
from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup as bs

async def get_news_content(url, sess):
    contents = ''
    # url에서 개별 뉴스를 크롤링 해주는 비동기 함수
    async with sess.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = bs(html, 'lxml')
            tags = soup.select('#mArticle > div.news_view section > p')
            for tag in tags:
                contents += tag.text
    return contents

async def main(urls):
    # 메인 루틴
    # 뉴스 갯수만큼 get_news_content()를 코루틴 생성해 이벤트 루프에 등록
    # 컴프리헨션으로 코루틴 생성
    async with aiohttp.ClientSession() as sess:
        result = await asyncio.gather(*[get_news_content(url, sess) for url in urls])
    return result

if __name__ == '__main__':
    d = datetime.now().strftime('%Y-%m-%d')
    file_path = r'.\testfiles\news_{}{}.csv'
    df = pd.read_csv(file_path.format('',d))       # csv을 읽어서 DataFrame 생성

    start = time.time()
    contents = asyncio.run(main(df['url']))     # 비동기로 뉴스 내용 가져오기
    end = time.time()
    print('total time : {:2f} sec'.format(end - start)) # 비동기로 뉴스 내용 가져오는데 걸린 시간
    
    df['contents'] = contents                   # DataFrame에 뉴스 내용 추가
    df.to_csv(file_path.format('and_contents_',d), index=False) # 뉴스 내용이 추가된 DataFrame을 csv로 저장
