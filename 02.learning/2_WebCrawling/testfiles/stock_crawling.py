
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from datetime import datetime
import os
import re

d = datetime.now().strftime('%Y-%m-%d') # strftime : 문자열로 변환

base_url = r'https://finance.naver.com/sise/sise_market_sum.naver?&page={}'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = { 'User-Agent' : user_agent }

stock_d = dict()

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

def get_stock_info(stock : bs):
    global stock_d
    # pprint(stock)
    title = stock.select_one('td > a.tltle')
    # print('이름 : ',title)
    if title == None:
        return
    
    title = title.text
    # td_num_l = stock.select('td.number')
    # pprint(td_num_l)
    
    for k, i in zip(stock_d.keys(), range(2,13)):
        if i == 2: 
            stock_d['title'].append(title)
            continue
        if i == 4:
            full_day_fee = stock.select_one('td.number:nth-child(4)').text.strip()
            try:
                alt = stock.select_one('td.number:nth-child(4) > img')['alt']
                if alt == None:
                    alt = '상한' if stock.select_one('td.number:nth-child(4) > img')['src'].endswith('ico_up.jpg') else '하한'
                stock_d[k].append(alt + full_day_fee)
            except:
                stock_d[k].append(full_day_fee)
            continue
        stock_d[k].append(stock.select_one('td.number:nth-child({})'.format(i)).text.strip())
        
    # 이전 코드 -> 반복문으로 변경
    # current_price = stock.select_one('td.number:nth-child(3)').text.strip()
    # full_day_fee = stock.select_one('td.number:nth-child(4)').text.strip()
    # try:
    #     alt = stock.select_one('td.number:nth-child(4) > img')['alt']
    #     if alt == None:
    #         alt = '상한' if stock.select_one('td.number:nth-child(4) > img')['src'].endswith('ico_up.jpg') else '하한'
    #     stock_d[k].append(alt + full_day_fee)
    # except:
    #     pass
    # fluctuation_rate = stock.select_one('td.number:nth-child(5)').text.strip()
    # face_value = stock.select_one('td.number:nth-child(6)').text.strip()
    # number_of_listed_shares = stock.select_one('td.number:nth-child(7)').text.strip()
    # market_cap = stock.select_one('td.number:nth-child(8)').text.strip()
    # foreigner_ratio = stock.select_one('td.number:nth-child(9)').text.strip()
    # trading_volume = stock.select_one('td.number:nth-child(10)').text.strip()
    # per = stock.select_one('td.number:nth-child(11)').text.strip()
    # roe = stock.select_one('td.number:nth-child(12)').text.strip()
    
    # stock_d['title'].append(title)
    # stock_d['current price'].append(current_price)
    # stock_d['full day fee'].append(full_day_fee)
    # stock_d['fluctuation rate'].append(fluctuation_rate)
    # stock_d['face value'].append(face_value)
    # stock_d['number of listed shares'].append(number_of_listed_shares)
    # stock_d['market cap'].append(market_cap)
    # stock_d['foreigner ratio'].append(foreigner_ratio)
    # stock_d['trading volume'].append(trading_volume)
    # stock_d['PER'].append(per)
    # stock_d['ROE'].append(roe)
    # print(stock_d)
    
def get_naver_stock():
    dict_init()
    for i in range(1,42):
        url = base_url.format(i)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # pprint(url)
            soup = bs(response.text, 'lxml')
            try:
                # table.type_2 > tbody > tr
                # #contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2)
                # #contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2)
                stocks = soup.select('div.box_type_l > table.type_2 > tbody > tr')
                for stock in stocks:
                    # print(type(stock))
                    get_stock_info(stock)
                pass
            except Exception as e:
                pprint(e)
                break
    
    df = pd.DataFrame(stock_d)
    
    return df

file_path = r'.\stock'
file_name = r'{}\stock_{}.csv'.format(file_path, d)
os.makedirs(file_path, exist_ok=True)
result = get_naver_stock()
result.to_csv(file_name, index=False)
