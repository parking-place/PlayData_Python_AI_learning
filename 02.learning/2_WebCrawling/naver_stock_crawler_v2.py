# 네이버 금융에서 주식 정보를 가져오는 크롤러
# 비동기 방식을 사용하여 속도를 높임
# 각 코루틴간의 변수 동시 접근 문제를 해결하기 위해 큐를 사용
# 크롤링한 데이터를 csv파일로 저장

import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from datetime import datetime
import time
import os


base_url = r'https://finance.naver.com/sise/sise_market_sum.naver?&page={}'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = { 'User-Agent' : user_agent }

stock_d = dict()        # 주식 정보를 담을 딕셔너리

# stock_d를 초기화하는 함수
def dict_init():
    global stock_d
    stock_d = {
        'title' : [],
        'current price' : [],
        'full day fee' : [],
        'fluctuation rate' : [],
        'face value' : [],
        'market cap' : [],
        'number of listed shares' : [],
        'foreigner ratio' : [],
        'trading volume' : [],
        'PER' : [],
        'ROE' : []
    }
    return

# 받아온 td tag에서 데이터를 추출하는 코루틴
async def get_stock_info(stock : bs):
    global stock_d
    # 타이틀이 없는 경우는 제외
    title = stock.select_one('td > a.tltle')
    if title == None:
        return
    
    # td tag에서 데이터를 추출, stock_d에 삽입
    for k, i in zip(stock_d.keys(), range(2,13)):
        if i == 2: 
            stock_d['title'] = title.text
            continue
        if i == 4:
            full_day_fee = stock.select_one('td.number:nth-child(4)').text.strip()
            try:
                alt = stock.select_one('td.number:nth-child(4) > img')['alt']
                if alt == None:
                    alt = '상한' if stock.select_one('td.number:nth-child(4) > img')['src'].endswith('ico_up.jpg') else '하한'
                stock_d[k] = alt + full_day_fee
            except:
                stock_d[k] = full_day_fee
            continue
        stock_d[k] = stock.select_one('td.number:nth-child({})'.format(i)).text.strip()

# 한 페이지의 주식정보들을 가져오는 코루틴
async def get_stocks_in_page(url, sess):
    async with sess.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = bs(html, 'lxml')
            try:
                stocks = soup.select('div.box_type_l > table.type_2 > tbody > tr')
                # 주식 정보들로 다시 코루틴들을 생성
                await asyncio.gather(*[get_stock_info(stock) for stock in stocks]) 
            except Exception as e:
                pprint(e)
                return

# 네이버 주식 페이지들을 코루틴에 넣어서 실행하는 코루틴
async def get_naver_stock():
    # 네이버 주식 페이지들의 url
    urls = [base_url.format(i) for i in range(1,42)]
    
    async with aiohttp.ClientSession(headers=headers) as sess:  # 세션 생성
        await asyncio.gather(*[get_stocks_in_page(url, sess) for url in urls]) # url과 세션을 넘겨주면서 코루틴을 실행
        
    df = pd.DataFrame(stock_d)  # 데이터를 담은 딕셔너리를 데이터프레임으로 변환
    return df

# 메인 코루틴
async def main():
    df = await get_naver_stock()
    return df

# 데이터프레임을 csv로 저장하는 함수
def save_to_csv(df):
    d = datetime.now().strftime('%Y-%m-%d')             # 현재 날짜
    file_path = r'.\testfiles\stock'                    # 파일 경로
    file_name = r'{}\stock_{}.csv'.format(file_path, d) # 파일 이름
    os.makedirs(file_path, exist_ok=True)               # 경로가 없으면 생성
    df.to_csv(file_name, index=False)                   # 데이터프레임을 csv로 저장
    
if __name__ == '__main__':
    start = time.time()                 # 시작 시간
    
    dict_init()                         # 딕셔너리 초기화
    df = asyncio.run(main())            # 메인 코루틴 실행
    save_to_csv(df)                     # 데이터프레임을 csv로 저장
    
    end = time.time()                   # 종료 시간
    print('time : {} sec'.format(end-start)) # 소요 시간 출력
    print(f'number of stocks : {len(df)}')
