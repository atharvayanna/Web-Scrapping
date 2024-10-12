from bs4 import BeautifulSoup
from selenium  import webdriver
import time

# to find elements by id
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import scrapper_utils as utils

def init(search):
    """This function initializes all the searching part"""
    driver = webdriver.Firefox()
    driver.get('https://www.google.com/')
    time.sleep(1)
    input = driver.find_element(By.ID, 'APjFqb')
    input.send_keys(search)
    input.send_keys(Keys.ENTER)
    time.sleep(1)
    news = driver.find_element(By.PARTIAL_LINK_TEXT, "News")
    news.click()
    time.sleep(1)
    return driver


def google_scraping(data, data_dict):
    """This Function takes an data(Dictionary to search) and data_dict(To store result) input and returns a data_dict of scraping result for google search engine"""

    #Iterate for every company and keyword
    for company in data['Companies']:
        for keyword in data['Keywords']:
            search = company+" "+keyword
            flag = True
            pg = 0
            driver = init(search)
            while pg != data['Page_number']:
                if flag:
                    source = driver.execute_script('return document.documentElement.outerHTML')
                    time.sleep(2)
                    soup = BeautifulSoup(source, 'html.parser')

                    #Iterrate and extract data for news displayed in cards
                    card_news = soup.find_all('div',{'class':'m7jPZ'})
                    len(card_news)

                    for e in card_news:
                        link = e.find('a',{'class':'WlydOe'}).get('href')
                        title = e.find('div',{'class':'n0jPhd ynAwRc tNxQIb nDgy9d'}).text
                        media_name = e.find('div',{'class':'MgUUmf NUnG9d'}).find('span').text
                        data_dict['Companies'].append(company)
                        data_dict['Keywords'].append(keyword)
                        data_dict['Search'].append(search)
                        data_dict['Search Engine'].append('Google')
                        data_dict['Link'].append(link)
                        data_dict['Media name'].append(media_name)
                        title = title.replace('\n', ' ')
                        data_dict['Title'].append(title)

                        date_time = utils.extract_date_from_meta(link)
                        data_dict['Time Stamp'].append(date_time)
                else:
                    source = driver.execute_script('return document.documentElement.outerHTML')
                    time.sleep(2)
                    soup = BeautifulSoup(source, 'html.parser')
                
                flag = False
                news_cards = soup.find_all('div', {'class':'SoaBEf'})

                #Iterrate and extract data for news displayed in list
                for news in news_cards:
                    link =news.find('a',{'class':'WlydOe'}).get('href') 
                    title =news.find('div',{'class':'n0jPhd ynAwRc MBeuO nDgy9d'}).text
                    media_name =news.find('div',{'class':'MgUUmf NUnG9d'}).find('span').text
                    data_dict['Companies'].append(company)
                    data_dict['Keywords'].append(keyword)
                    data_dict['Search'].append(search)
                    data_dict['Search Engine'].append('Google')
                    data_dict['Link'].append(link)
                    data_dict['Media name'].append(media_name)
                    title = title.replace('\n', ' ')
                    data_dict['Title'].append(title)

                    date_time = utils.extract_date_from_meta(link)
                    data_dict['Time Stamp'].append(date_time)

                #Check Weather next Page is availabe if yes then go to next Page else stop scraping for current search
                try:
                    next_page = driver.find_element(By.ID, 'pnnext')
                    next_page.click()
                    pg = pg + 1

                except Exception as e:
                    print('Error occured', e)
                    break

            driver.quit()
    
    return data_dict
    
    
            
