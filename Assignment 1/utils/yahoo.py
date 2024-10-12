from bs4 import BeautifulSoup
from selenium  import webdriver
import time

# to find elements by id
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import scrapper_utils as utils

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init(company, keyword):
    """This function is used to initialize the drivers and search and return the driver"""
    driver = webdriver.Firefox()
    driver.get(f'https://in.news.search.yahoo.com/search;_ylt=AwrPo63OUtlmhQQAy127HAx.;_ylu=Y29sbwNzZzMEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p={company}+{keyword}&fr2=piv-web&fr=sfp')
    time.sleep(2)

    return driver


def yahoo_scraping(data, data_dict):
    """This function takes data(dictionary for search input) and returns data_dict(dictionary with scraping data)"""
    for company in data['Companies']:
        for keyword in data['Keywords']:
            search = company + ' ' + keyword
            
            pg = 0
            driver = init(company, keyword)
            while pg != data['Page_number']:
                source = driver.execute_script('return document.documentElement.outerHTML')
                soup = BeautifulSoup(source, 'html.parser')

                news_cards = soup.find_all('div', {'class': 'dd NewsArticle'})

                for news in news_cards:
                    title = news.find('a').get('title')
                    link = news.find('a').get('href')
                    media_name = news.find('span', {'class': 's-source mr-5 cite-co'}).text
                    date = utils.extract_date_from_meta(link)
                    if title == None:
                        continue

                    data_dict['Companies'].append(company)
                    data_dict['Keywords'].append(keyword)
                    data_dict['Search'].append(search)
                    data_dict['Search Engine'].append('Yahoo')
                    data_dict['Link'].append(link)
                    data_dict['Media name'].append(media_name)
                    title = title.replace('\n', ' ')
                    data_dict['Title'].append(title)
                    data_dict['Time Stamp'].append(date)
                
                try:
                    next_page = driver.find_element(By.CLASS_NAME, 'next')
                    next_page.click()
                    pg += 1
                except Exception as e:
                    print('Error occurred:', e)
                    break
            
            driver.quit()

    return data_dict
