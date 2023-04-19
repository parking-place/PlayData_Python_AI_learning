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
stock_qu = []           # 비동기 함수들이 공유하는 큐
is_qu_use = False       # 큐를 사용중인지 아닌지를 나타내는 전역 변수

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

# 비동기 함수들이 공유하는 큐에 데이터를 넣는 코루틴
# 여럿이 동시에 넣을때 생길 수 있는 문제를 해결하기 위해 큐를 사용
async def insert_in_stock_q(stock_values):
    global is_qu_use
    if is_qu_use: return True   # 큐를 사용중이면 while을 계속 돌림
    
    is_qu_use = True                # 큐를 사용중으로 표시
    stock_qu.append(stock_values)   # 큐에 데이터를 넣음
    is_qu_use = False               # 큐를 사용중이 아님으로 표시
    #print(stock_values['title'], 'is inserted in stock_qu')
    
    return False                # while을 빠져나오기 위해 False를 반환

# 큐에서 데이터를 뽑아 stock_d에 데이터를 넣는 코루틴
# 세션과 url이 넘어갈때 같이 루프를 돌기 시작함
async def stock_qu_to_d():
    global is_qu_use
    while True:
        # 큐가 비어있으면 0.1초 대기
        if len(stock_qu) == 0:
            # print('stock_qu is empty')
            await asyncio.sleep(0.1)
            continue
        # 큐를 사용중이면 0.1초 대기
        elif is_qu_use:
            # print('stock_qu is in use')
            await asyncio.sleep(0.1)
            continue
        
        is_qu_use = True                # 큐를 사용중으로 표시
        stock_values = stock_qu.pop(0)  # 큐에서 데이터를 뽑음
        is_qu_use = False               # 큐를 사용중이 아님으로 표시
        
        # stock_d에 데이터를 삽입
        for k, v in stock_values.items(): stock_d[k].append(v)
        
        # 큐에서 데이터를 뽑은 뒤에도 큐가 비어있으면 0.5초 대기
        if len(stock_qu) == 0:
            # print('stock_qu is empty')
            await asyncio.sleep(0.5)
            # 0.5초 대기 후에도 큐가 비어있으면 모든 코루틴이 종료되었을 것이므로 while을 빠져나감
            if len(stock_qu) == 0:
                # print('stock_qu is empty 1sec later, end this corutine')
                break
            continue

# 받아온 td tag에서 데이터를 추출하는 코루틴
async def get_stock_info(stock : bs):
    global stock_d
    # 타이틀이 없는 경우는 제외
    title = stock.select_one('td > a.tltle')
    if title == None:
        return
    
    # stock들의 정보를 담을 딕셔너리
    stock_values = {}
    
    # td tag에서 데이터를 추출
    for k, i in zip(stock_d.keys(), range(2,13)):
        if i == 2: 
            stock_values['title'] = title.text
            continue
        if i == 4:
            full_day_fee = stock.select_one('td.number:nth-child(4)').text.strip()
            try:
                alt = stock.select_one('td.number:nth-child(4) > img')['alt']
                if alt == None:
                    alt = '상한' if stock.select_one('td.number:nth-child(4) > img')['src'].endswith('ico_up.jpg') else '하한'
                stock_values[k] = alt + full_day_fee
            except:
                stock_values[k] = full_day_fee
            continue
        stock_values[k] = stock.select_one('td.number:nth-child({})'.format(i)).text.strip()

    # 딕셔너리에 데이터를 넣는 함수를 호출
    # 큐에 데이터를 넣을 때까지 시도
    while await insert_in_stock_q(stock_values):
        print('insert_in_stock_q is in use')
        continue

# 한 페이지의 주식정보들을 가져오는 코루틴
async def get_stocks_in_page(url, sess):
    async with sess.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = bs(html, 'lxml')
            try:
                stocks = soup.select('div.box_type_l > table.type_2 > tbody > tr')
                await asyncio.gather(*[get_stock_info(stock) for stock in stocks])
            except Exception as e:
                pprint(e)
                return

# 네이버 주식 페이지들을 코루틴에 넣어서 실행하는 코루틴
async def get_naver_stock():
    # 네이버 주식 페이지들의 url
    urls = [base_url.format(i) for i in range(1,42)]
    
    async with aiohttp.ClientSession(headers=headers) as sess:  # 세션 생성
        # url과 세션을 넘겨주면서 코루틴을 실행,
        # 동시에 큐를 계속 확인하며 데이터를 넣는 코루틴을 실행
        await asyncio.gather(*[get_stocks_in_page(url, sess) for url in urls],  stock_qu_to_d())
        
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
