import time

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_companies():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    url = f'https://market.tase.co.il/he/market_data/tase-companies/public'
    driver.get(url)
    time.sleep(1)


    # print(soup)
    # rows = soup.find_all('tr', attrs={'class': 'ng-star-inserted'})


    def get_button():
        buttons = driver.find_elements(By.CLASS_NAME, 'ng-star-inserted')
        i = 0

        for b in buttons:
            try:
                if b.text == 'הבא':
                    i += 1
                    # print(b.text)
                    if i > 1:
                        return b
            except:
                continue



    def press_button(page):


        for i in range(page):
            try:
                button = get_button()
                # print(button)
                button.click()
                print("Click")

                time.sleep(1)
            except:
                print("ERROR")
                button = get_button()
                # print(button)
                button.click()
                print("Click")

                time.sleep(1)


    # press_button(3)

    # html_code2 = driver.page_source
    # print(html_code2)
    # # print(button)
    # # button.click()
    stocks = []
    for d in range(21):
        time.sleep(1)
        html_code = driver.page_source
        soup = BeautifulSoup(html_code, 'html.parser')
        rows = soup.find_all('tr', attrs={'class': 'ng-star-inserted'})
        for i in range((len(rows))):
            if i > 0:
                row = rows[i]
                name = row.find('a', attrs={'class': 'item-name'}).text
                number = row.find('td', attrs={'class': 'ColW_2 ng-star-inserted'}).text
                subject = row.find('td', attrs={'class': 'ColW_5 break-words ng-star-inserted'}).text
                stock = {"name": name, "number": number, "subject": subject}
                stocks.append(stock)
                print(name, subject, number)

        # Click the button
        press_button(1)

    df = pd.DataFrame(stocks)
    df.to_excel("stocks.xlsx", index=False)

    driver.quit()
# get_companies()