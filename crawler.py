### Contributed by 손규빈, 최완재, 오학

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import getpass
from bs4 import BeautifulSoup
import os, re

######################
#                    #
#   Run one by one   #
#                    #
######################

# 셀레늄으로 크롬 브라우저를 연다.
driver = webdriver.Chrome()
time.sleep(2)

# '복지' 탭에 접속한다.
driver.get('https://www.open.go.kr/search/theme/theme.do?themecd=00028')

# 현재 웹 페이지의 내용을 긁어온다.
soup = BeautifulSoup(driver.page_source, 'lxml')

#########################################
#                                       #
#   Modify page per number in browser   #
#                                       #
#########################################

# 전체 문서를 한 페이지에 수동으로 로딩한다.
# README.md 참조

#####################
#                   #
#   Run all below   #
#                   #
#####################

# 원문 목록에서 파일 다운로드에 필요한 함수 인자를 가져온다.
prdnDt_list = []
prdnNstRgstNo_list= []
for tr in soup.select("#result_false tr"):
    post_script = tr.td.a['href'][11:]
    tmp = re.findall("[']([0-9]+)['], [']([a-z0-9]+)[']", post_script, re.IGNORECASE)[0]
    prdnDt_list.append(tmp[0])
    prdnNstRgstNo_list.append(tmp[1])

for prdnDt, prdnNstRgstNo in zip(prdnDt_list, prdnNstRgstNo_list):
    # start_time = time.time()

    # 현재 브라우저에서 새 탭을 열고 이동한다.
    driver.execute_script("window.open('')")
    driver.switch_to_window(driver.window_handles[1])

    # 원문 파일 다운로드 페이지에 접속한다.
    driver.get(f'https://www.open.go.kr/pa/infoWonmun/cateSearch/wonmunOrginlDetail.do?prdnDt={prdnDt}&prdnNstRgstNo={prdnNstRgstNo}')

    # 다운로드할 파일의 제목을 가져온다.
    file_soup = BeautifulSoup(driver.page_source, 'lxml')
    file_name = file_soup.select('span.fileName')[0].text

    # 파일을 다운로드 할 때 필요한 javascript 인자를 가져와서 함수를 실행한다.
    download_script = file_soup.select("p.fr")[0].a['onclick']
    driver.execute_script(download_script)

    # 파일 다운로드에 필요한 시간을 10초로 설정한다.
    delay = 10
    time.sleep(delay)
    try:
        driver.switch_to_alert().accept();
    except:
        print("[%d]초 내 다운로드 성공 : [%s]" % (delay, file_name))

    # 다운로드가 완료되었으니 새 탭을 닫고, 목록이 있는 탭으로 이동한다.
    driver.execute_script("window.close()")
    driver.switch_to_window(driver.window_handles[0])
    # print("\tElapsed time: %s seconds" %(time.time() - start_time))
