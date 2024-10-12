#Import the funcrions and modules
from utils import google as g
from utils import yahoo as y
from utils import bing as b
from utils import scrapper_utils as utils

#config.json file path
json_path = r'C:\Users\atharva.yanna\Desktop\Python\Assignment 1\config.json'

#Dictionary to store the scraping data
data_dict = {
    "Companies":[],
    "Keywords":[],
    "Search": [],
    "Search Engine":[],
    "Title":[],
    "Link": [],
    "Time Stamp":[],
    "Media name": []
}

data = utils.read_config(json_path)

#Scraping result for google search
scraping_data = g.google_scraping(data,data_dict)
#Scraping result for yahoo search
scraping_data = y.yahoo_scraping(data, scraping_data)
#Scraping result for bing search
scraping_data = b.bing_scrapping(data, scraping_data)


#write the file to a csv 
try:
    utils.dict_to_csv(scraping_data, r'Assignment 1\data.csv')
    print("File Write Successfull")
except Exception as e:
    print(e)
