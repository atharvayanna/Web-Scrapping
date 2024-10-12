from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from urllib import request,error
import logging

# Create and configure the logging
logging.basicConfig(filename=r"Assignment 3/error_business_standard.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object logger
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

def extract_article_body(link):
    """This function takes a link and extracts the article from the link."""
    content = []
    # This header mimics as if the request is from web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        req = request.Request(link, headers=headers)
        with request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            s = BeautifulSoup(html, 'html.parser')

            # Extract title
            title_element = s.find('h1', {'class': 'MainStory_stryhdtp__frNSf stryhdtp'})
            title = title_element.text if title_element else 'No title found'

            # Extract article body
            article_div = s.find('div', {'class': 'MainStory_storycontent__Pe3ys storycontent'})
            if article_div:
                # filter div with by only bidy div
                body = [div for div in article_div.find_all('div', recursive=False) if not div.has_attr('class')]
                text = ''.join(e.get_text() for e in body)
                
                # Clean up the text
                cleaned_text = re.sub(r'\n\s*\n', '\n', text.strip())
            else:
                cleaned_text = 'No content found'
            
            content.append(title)
            content.append(cleaned_text)

    except error.HTTPError as e:
        return [f"HTTP Error: {e.code} - {e.reason}"]
    except Exception as e:
        return [str(e)]

    return content

def news_extraction(soup, h, classname):
    news_obj = {
        'category': '',
        'articles':[]
    }
    latest_news = soup.find('div',{'class':classname})
    category = latest_news.find(h,{'class':'section-title'}).text
    news_obj['category']=category

    tn_cards = latest_news.find_all('div',{'class':'cardlist'})
    for e in tn_cards:
        if e.find('div',{'class':'premium_ctgrlble__PdB6E ctgrlble'}):
            continue
        link = e.find('a').get('href')
        
        body = extract_article_body(link)
        if len(body) == 2:
            obj={
                'title': body[0],
                'link': link,
                'body': body[1]
            }
            if not obj['body'] == 'No content found':
                news_obj['articles'].append(obj)
        else:
            logger.info('Unable to fetch article')
            logger.exception(body[0])

    return news_obj

def extract_top_news(soup):
    """This function takes BeautifulSoup object and returns the news obj with all articles"""
    classname = 'Nws_hp_top_news section-flex topsection'
    h = 'h1'
    news_obj = news_extraction(soup,h,classname)

    return news_obj

def extract_latest_news(soup):
    """This funtion extracts news from latest news section from business standard"""
    classname = 'Nws_hp_latest_news section-div'
    h = 'h2'
    news_obj = news_extraction(soup, h, classname)

    return news_obj

def extract_market_news(soup):
    """This funtion extracts news from market section from business standard"""
    classname = 'Nws_hp_market section-div'
    h = 'h2'
    news_obj = news_extraction(soup,h, classname)
    
    return news_obj

def extract_companies_news(soup):
    """This funtion extracts news from Compaanies section from business standard"""
    classname = 'Nws_hp_cmp d-flex section-nopad'
    h = 'h2'
    news_obj = news_extraction(soup, h, classname)

    return news_obj

def extract_other_news(soup):
    """This function extracts news from all other sections i.e Technology, automobile etc"""
    news_article = []
    tech_news = soup.find_all('div',{'class':'Nws_hp_30 medium-section'})

    for e in tech_news:
        news_obj = {
            'category': '',
            'articles':[]
        }
        category = e.find('h3',{'class':'section-title'})
        if not category:
            category = e.find('h4',{'class':'section-title'})
        news_obj['category']=category.text

        tn_cards = e.find_all('div',{'class':'cardlist'})

        for e2 in tn_cards:
            if e2.find('div',{'class':'premium_ctgrlble__PdB6E ctgrlble'}):
                continue
            link = e2.find('a').get('href')
            
            body = extract_article_body(link)
            if len(body) == 2:
                obj={
                    'title': body[0],
                    'link': link,
                    'body': body[1]
                }
                if not obj['body'] == 'No content found':
                    news_obj['articles'].append(obj)

            else:
                logger.error(body[0])
        news_article.append(news_obj)
    
    return news_article

def business_standard():
    """This is the main functin which collects and extracts all the news articles and store in a list category wise"""
    #All the articles are stored in news_article list category wise
    news_articles = []

    #Init the browser
    business_standard = 'https://www.business-standard.com/'
    driver = webdriver.Firefox()
    driver.get(business_standard)
    source = driver.execute_script('return document.documentElement.outerHTML')
    time.sleep(1)
    soup = BeautifulSoup(source,'html.parser')
    
    #Get top news from the page
    top_news = extract_top_news(soup)
    news_articles.append(top_news)

    #Get latest news from the page
    latest_news = extract_latest_news(soup)
    news_articles.append(latest_news)

    #Get market news from the page
    market_news = extract_market_news(soup)
    news_articles.append(market_news)

    #Get comapany news from the page
    companies_news = extract_companies_news(soup)
    news_articles.append(companies_news)

    #load other news by scrolling news
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    source = driver.execute_script('return document.documentElement.outerHTML')
    driver.close()
    soup = BeautifulSoup(source,'html.parser')

    #Get other news like Technology, sports, IPO etc
    other_news = extract_other_news(soup)
    for e in other_news:
        news_articles.append(e)
    
    return news_articles