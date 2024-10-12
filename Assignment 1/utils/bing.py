from bs4 import BeautifulSoup
from selenium  import webdriver
import time

# to find elements by id
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import scrapper_utils as utils

def init(search):
    """This function initialises the driver and search"""
    driver = webdriver.Firefox()
    driver.get('https://www.bing.com/news/')
    time.sleep(1)

    input = driver.find_element(By.ID, 'sb_form_q')
    input.send_keys(search)
    time.sleep(1)
    input.send_keys(Keys.ENTER)
    time.sleep(1)

    return driver


def bing_scrapping(data, data_dict):
    """This function takes data input and returns the scraping result for bing search engine"""
    for company in data['Companies']:
        for keyword in data['Keywords']:
            search = company+' '+keyword
            driver = init(search)
            pg = 0
            while pg != data['Page_number']:
                try:
                    driver.execute_script("window.scrollBy(0, 10000);")
                    pg=pg+1
                except Exception as e:
                    print("Cannot scroll anymore", e)
            
            source = source = driver.execute_script('return document.documentElement.outerHTML')
            soup = BeautifulSoup(source, 'html.parser')

            #Extract the data
            news_cards = soup.find_all('div',{'class':'news-card newsitem cardcommon'})
            # print(len(news_cards))
            for e in news_cards:
                title = e.get('data-title')
                link = e.get('url')
                media_name = e.get('data-author')
                date = utils.extract_date_from_meta(link)

                data_dict['Companies'].append(company)
                data_dict['Keywords'].append(keyword)
                data_dict['Search'].append(search)
                data_dict['Search Engine'].append('Bing')
                data_dict['Link'].append(link)
                data_dict['Media name'].append(media_name)
                title = title.replace('\n', ' ')
                data_dict['Title'].append(title)

                date_time = utils.extract_date_from_meta(link)
                data_dict['Time Stamp'].append(date_time)
            
            driver.quit()

    return data_dict

