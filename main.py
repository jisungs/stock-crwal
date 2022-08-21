from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os

url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='

browser = webdriver.Chrome(executable_path=r'C:\Users\s1\Documents\Dev\chrome_driver\chromedriver.exe')
# browser.maximize_window()

#1 페이지 이동
browser.get(url)

#2. 조회항목 초기화 (체크되어 있는 항목 체크 해제)

chekcboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in chekcboxes:
    if checkbox.is_selected():
        checkbox.click()
#3. 조회항목 설정(원하는 항목)

items_to_select = ['시가총액', '영업이익', 'PER', 'ROE', 'ROA','당기순이익']
for checkbox in chekcboxes:
    parent = checkbox.find_element(By.XPATH,'..') # 부모 엘리먼트찾기
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text)
    if label.text in items_to_select:#선택항목과 일치한다면
        checkbox.click()

#4.적용하기
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()


for idx in range(1, 40):

    browser.get(url + str(idx))

    #5.데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0:
        break

    #6.파일저장
    f_name= 'sise.csv'
    if os.path.exists(f_name):#파일이 있다면 ? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:#파일이 없다면 헤더포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)

    print(f'{idx} 페이지 완료')

browser.quit()