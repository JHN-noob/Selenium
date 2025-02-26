import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

keywords = ["강남 피부과", "강남 카페"]
IDvs = ["37206778", "?"]
for IDv, keyword in zip(IDvs, keywords):
    driver.get(f"https://m.search.naver.com/search.naver?where=m&sm=top_hty&fbm=0&ie=utf8&query={keyword}&ssc=tab.m.all")
    time.sleep(3)

    try:
        # view_element = driver.find_element(By.CSS_SELECTOR, "a.YORrF")
        # 검색어마다 셀렉터가 다름
        view_element = driver.find_element(By.CSS_SELECTOR, "a.FtXwJ")
        view_element.click()
        time.sleep(1)
        view_more_element = driver.find_element(By.CSS_SELECTOR, "a.cf8PL")
        view_more_element.click()
        print("더보기 클릭")
        time.sleep(2)

    except:
        print(f"해당 키워드 {keyword}로 찾을 장소가 없습니다.")
        continue


    ID_selector = f"a[href*='/{IDv}?entry=pll']" # 해당 셀렉터가 있는 a 태그를 검색
    for _ in range(5): # 스크롤 반복문
        ID_elements = driver.find_elements(By.CSS_SELECTOR, ID_selector)
        if len(ID_elements) < 1:
            print("순위권에 업체가 없어 스크롤합니다.")
            scrollY = 20000 # 스크롤 양
            ActionChains(driver).scroll_by_amount(0, scrollY).perform() # 모바일 페이지 좌표
            time.sleep(3)
    if len(ID_elements) < 1:
        print("검색되지 않는 업체입니다.")
        continue


    ID_element = random.choice(ID_elements) # IDv가 있는 엘리멘츠들 중 랜덤 선택
    for _ in range(5): # 상위 LI 태그로 가기 위한 반복문
        target_element = ID_element.find_element(By.XPATH, './..')
        tagname = target_element.get_attribute("tagName")
        if tagname == "LI":
            # print("li 태그를 찾았습니다.")
            break
        ID_element = target_element


    all_selector = "#_list_scroll_container > div > div > div.place_business_list_wrapper > ul > li"
    all_elements = driver.find_elements(By.CSS_SELECTOR, all_selector)
    rank = 1
    for i in all_elements: # UL 태그에서 순차적으로 반복 후 LI 태그와 비교
        try: # 광고 제외
            i.find_element(By.CSS_SELECTOR, "a.gU6bV")
            continue
        except:
            pass
        if i == target_element:
            break
        rank += 1
    print("당신이 찾을 장소의 순위는 :", rank)

input()
