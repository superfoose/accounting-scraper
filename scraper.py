from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
financial_datas = []
def scrape_maya():
    print("scraping maya")



    url = f'https://www.tase.co.il/he'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

    r = requests.get(url, headers=headers, allow_redirects=True)
    print(r.content)
    soup = BeautifulSoup(r.content)
    print(soup)
    sac_hon = soup.find_all('div', attrs={'class', "tableCol col_2 ltr ng-binding ng-scope"})[16].text
    # total_assets = soup.find_all('div', attrs={'class', "tableCol col_2 ltr ng-binding ng-scope"})[10].text
    print("###################RESULT: ", sac_hon)

    financial_data = {"company": 1006, "דיבידנט": float(1), "שוק להון": float(sac_hon)}
    financial_datas.append(financial_data)



    financial_df = pd.DataFrame(financial_datas)
    financial_df.to_excel("financial_data.csv")
scrape_maya()
