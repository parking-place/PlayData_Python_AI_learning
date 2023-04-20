# 정식당 리뷰 크롤링
import selenium
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
# 정식당 url
url = r'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-Jungsik-Seoul.html'

service = Service('./browserdriver/msedgedriver112_64.exe')
# headless 모드 설정
options = webdriver.EdgeOptions()
options.add_argument('headless')    # headless 모드 설정 -> 화면이 안나옴
options.add_argument("disable-gpu") # GPU 사용 안함

browser = webdriver.Edge(service=service, options=options)
browser.set_window_position(2056, 677)
browser.maximize_window()
# 기본 대기 시간 설정
browser.implicitly_wait(5)
# url 접속
browser.get(url)
# 리뷰 제목, 내용을 담을 리스트
comment_titles = []
comments= []
# 리뷰 다음페이지 버튼이 없을 때까지 반복
while True:
    try:
        # 리뷰 더보기 버튼이 있으면 클릭
        more_bt = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'taLnk.ulBlueLinks')))
        
        more_bt.click()
        # 댓글 상세 로딩 대기
        time.sleep(1.5)
    except:
        # 더보기 버튼이 없는 경우,
        # 바로 크롤링
        pass
    
    # BeutifulSoup를 이용하여 html 파싱
    html = browser.page_source
    soup = bs(html, 'lxml')
    # 리뷰 제목, 내용을 리스트에 추가
    comment_titles.extend(soup.select('span.noQuotes'))
    comments.extend(soup.select('p.partial_entry'))

    try:
        # 다음 페이지 버튼이 있으면 클릭
        next_btn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'nav.next.ui_button.primary')))
        
        next_btn.click()
        # 다음 페이지 로딩 대기
        time.sleep(2)
    except:
        # 다음 페이지 버튼이 없는 경우
        # 크롤링 종료
        break
# 크롤링 종료 후 브라우저 종료
browser.quit()

# 리뷰 제목, 내용에서 text만 추출
comment_titles = [comment_title.text.strip().replace('\n', '') for comment_title in comment_titles]
comments = [comment.text.strip().replace('\n', '') for comment in comments]
# 데이터 프레임 생성
df = pd.DataFrame({'title':comment_titles, 'comment':comments})
# csv 파일로 저장
df.to_csv('./testfiles/tripadvisor.csv', index=False)
