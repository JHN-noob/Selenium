import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from tkinter import messagebox



def run_crawling(출발지, 도착지, 출발월일, 도착월일, 직항):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 창 안 뜨게 함
    options.add_argument("--disable-gpu")  # (일부 환경에서 필수)
    options.add_argument("--no-sandbox")   # (리눅스일 때 유용)
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f"https://flight.naver.com/flights/international/{출발지}-{도착지}-2025{출발월일}/{도착지}-{출발지}-2025{도착월일}?adult=1&isDirect={직항}&fareType=Y")
        # 페이지 항공사 긁어오기
        def wait_for_company(driver, selector="b[class*='airline_name']", timeout=5):
            def condition(d):
                els = d.find_elements(By.CSS_SELECTOR, selector)
                return len(els) > 0
            try:
                WebDriverWait(driver, timeout).until(condition)
                time.sleep(5)
                flight_company = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(flight_company) == 0:
                    return None
                flight_company_text = []
                for i in flight_company:
                    try:
                        flight_company_text.append(i.text)
                    except StaleElementReferenceException:
                        flight_company_text.append("조회 필요")
                return flight_company_text[:5]
            except TimeoutException:
                return None

        # 페이지 내 출발, 도착시간 긁어오기
        def wait_for_n_times(driver, selector="b[class*='route_time']", timeout=1):
            def condition(d):
                els = d.find_elements(By.CSS_SELECTOR, selector)
                return len(els) > 0
            try:
                WebDriverWait(driver, timeout).until(condition)
                n_times = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(n_times) == 0:
                    messagebox.showinfo("검색 결과 없음", "해당 조건에 맞는 항공편이 없습니다.")
                    return None
                n_times_text = []
                for i in n_times:
                    try:
                        n_times_text.append(i.text)
                    except StaleElementReferenceException:
                        n_times_text.append("조회 필요")
                n_times_text = [n_times_text[i:i+4] for i in range(0, len(n_times_text), 4)]
                return n_times_text[:5]
            except TimeoutException:
                return None
            
        # 페이지 내 소요시간 긁어오기
        def wait_for_n_cost_times(driver, selector="button[class*='route_details']", timeout=1):
            def condition(d):
                els = d.find_elements(By.CSS_SELECTOR, selector)
                return len(els) > 0
            try:
                WebDriverWait(driver, timeout).until(condition)
                n_cost_times = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(n_cost_times) == 0:
                    messagebox.showinfo("검색 결과 없음", "해당 조건에 맞는 항공편이 없습니다.")
                    return None
                n_cost_times_text = []
                for i in n_cost_times:
                    try:
                        if 직항 == "true":
                            n_cost_times_text.append(i.text[4:])
                        else:
                            n_cost_times_text.append(i.text)
                    except StaleElementReferenceException:
                        n_cost_times_text.append("조회 필요")
                n_cost_times_text = [n_cost_times_text[i:i+2] for i in range(0, len(n_cost_times_text), 2)]
                return n_cost_times_text[:5]
            except TimeoutException:
                return None
            
        # 페이지 내 가격 긁어오기
        def wait_for_n_costs(driver, selector="i[class*='item_num']", timeout=1):
            def condition(d):
                els = d.find_elements(By.CSS_SELECTOR, selector)
                return len(els) > 0
            try:
                WebDriverWait(driver, timeout).until(condition)
                n_costs = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(n_costs) == 0:
                    messagebox.showinfo("검색 결과 없음", "해당 조건에 맞는 항공편이 없습니다.")
                    return None
                n_costs_text = []
                for i in n_costs:
                    try:
                        n_costs_text.append(i.text)
                    except StaleElementReferenceException:
                        n_costs_text.append("조회 필요")
                return n_costs_text[:5]
            except TimeoutException:
                return None

        flight_company_text = wait_for_company(driver)
        if not flight_company_text:
            return None
        n_times_text = wait_for_n_times(driver)
        if not flight_company_text:
            return None
        n_cost_times_text = wait_for_n_cost_times(driver)
        if not flight_company_text:
            return None
        n_costs_text = wait_for_n_costs(driver)
        if not flight_company_text:
            return None
        # print(flight_company_text)
        # print(n_times_text)
        # print(n_cost_times_text)
        # print(n_costs_text)
        return flight_company_text, n_times_text, n_cost_times_text, n_costs_text
    finally:
        driver.quit()
