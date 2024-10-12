from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from urllib import request,error
import logging

# Create and configure the logging
logging.basicConfig(filename=r"Assignment 3/error_zee_news.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object logger
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

def extract_article_body(link):
    """This function takes link and extracts the article from the link"""
    content = []
    # This header mimics as if the request is from web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = request.Request(link, headers=headers)
    try:
        with request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            s = BeautifulSoup(html, 'html.parser')
            
            article = s.find('div', {'id': 'fullArticle'})
            
            title = s.find('div',{'class':'article_content'}).find('h1').text
            p = article.find('p')
            cleaned_text = re.sub(r'\n\s*\n', '\n', p.text.strip())
            content.append(title)
            content.append(cleaned_text)   
    except error.HTTPError as e:
        return [f"HTTP Error: {e.code} - {e.reason}"]
    except Exception as e:
        return [str(e)]

    return content

def zee_news():
    """This function does webscraping for zee news media channel news"""
    #This list contains all the article according to category
    news_article = []

    #Init the browser for zee news
    zee = 'https://zeenews.india.com'
    driver = webdriver.Firefox()
    driver.get(zee)
    source = driver.execute_script('return document.documentElement.outerHTML')
    time.sleep(1)
    driver.close()
    soup = BeautifulSoup(source,'html.parser')

    #This extracts all the news sections category wise
    header = soup.find_all('div', {'class':'home-section-container'})

    #Iterate all the news section according to category 
    for e in header:
        if e.find('a'):
            news_obj = {
                'category':'',
                'articles':[]
            }
            #Get the category of the news section
            Category = e.find('a').text
            news_obj['category'] = Category

            #Find all the news article and iterate them to extract body from them
            news = e.find_all('div',{'class':'news_description'})
            for e2 in news:
                link = zee+e2.find('a').get('href')
                #Extract all the body of the article
                body = extract_article_body(link)
                if len(body) == 2:
                    obj = {
                        'title': body[0],
                        'link':link,
                        'body':body[1]

                    }
                    news_obj['articles'].append(obj)
                else:
                    logger.info('Unable to fetch article')
                    logger.exception(body[0])
            news_article.append(news_obj)

    return news_article

    