import time

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import threading
from openpyxl import Workbook
from openpyxl import load_workbook
from pandas import ExcelWriter
from openpyxl import load_workbook
import multiprocessing

#
# os.remove('/Users/davidlevgabbay/PycharmProjects/maya_scraper/financial_data.csv')
# os.open('/Users/davidlevgabbay/PycharmProjects/maya_scraper/financial_data.csv', os.O_CREAT)

def scrape_maya(number, name, subject):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    url = f'https://maya.tase.co.il/company/{number}?view=finance'
    driver.get(url)
    time.sleep(1)
    html_code = driver.page_source
    soup = BeautifulSoup(html_code, 'html.parser')

    shuk_hon = soup.find_all('div', attrs={'class', 'tableCol col_2 ltr ng-binding ng-scope'})[16].text
    clean_profits = soup.find_all('div', attrs={'class', 'tableCol col_2 ltr ng-binding ng-scope'})[11].text
    sach_hon = soup.find_all('div', attrs={'class', 'tableCol col_2 ltr ng-binding ng-scope'})[3].text
    total_assets = soup.find_all('div', attrs={'class', 'tableCol col_2 ltr ng-binding ng-scope'})[0].text
    clean_profits = clean_profits.replace(',', '')
    sach_hon = sach_hon.replace(',', '')

    tsua_hon = float(clean_profits)/3 * 4/float(sach_hon)*100
    print(tsua_hon)
    tsua_shuk = float(tsua_hon) / float(shuk_hon)
    space_multi = 100 / float(tsua_shuk)

    print("################### RESULT: ", number, ": ", shuk_hon, total_assets)

    financial_data = [{"name": name, "subject": subject, "company": number, 'shuk lahon': shuk_hon, "tsua lashon": tsua_hon, "tsua lashuk": tsua_shuk, "machpil revach": space_multi}]
    print(financial_data)
    financial_data = pd.DataFrame(financial_data)
    print(financial_data)
    financial_data.to_csv('financial_data.csv', mode='a', header=False, index=False)

    # financial_data.to_excel('financial_data.xlsx')




    driver.quit()

# scrape_maya(1829)
# scrape_maya(1050)

# #

def scrape_system(label):
    df = pd.read_excel('stocks.xlsx')
    def get_financial_data(start_index, end_index, label):
        for index in range(start_index, end_index):
            try:

                row = df.iloc[index]
                print(row["number"])
                if start_index == 0:
                    print("PERCENTAGE: ", index / (len(df) / 4) * 100)
                    # pct = float(index / (len(df) / 4) * 100)
                    # label.config(text="Complete: " + pct)
                number = row["number"]
                name = row["name"]
                subject = row["subject"]
                scrape_maya(number, name ,subject)

            except Exception as e:
                print(e)
                row = df.iloc[index]
                print(row["number"], "Number error")

    # if __name__ == "__main__":
    print("starting")
    num_processes = 4
    total_rows = len(df)
    chunk_size = total_rows // num_processes
    processes = []

    for i in range(num_processes):
        start_index = i * chunk_size
        # Adjust the end_index for the last process to handle any remainder
        end_index = (i + 1) * chunk_size if i < num_processes - 1 else total_rows
        process = threading.Thread(target=get_financial_data, args=(start_index, end_index, label))

        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    csv_df = pd.read_csv("financial_data.csv")
    csv_df.to_excel("financial_data.xlsx")
    os.remove("financial_data.csv")

# scrape_maya(1, 1, 1)