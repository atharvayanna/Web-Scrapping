from datetime import date
from utils import utils
from utils import zee_news
from utils import business_standard
import os

# Define the path to the folder
folder_path = f'Assignment 3/md files/{str(date.today())}'
#Check for the folder is not present then create the folder
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f'Folder created: {folder_path}')
    

#Output is stored in zee_filename
zee_filename = 'zee_news_'+str(date.today())+'.md'
zee_file_path = os.path.join(folder_path, zee_filename)
#Output is stored in bs_filename
bs_filename = 'business_standard_'+str(date.today())+'.md'
bs_file_path = os.path.join(folder_path, bs_filename)

#Extract data from zee news
news_articles_zn = zee_news.zee_news()
utils.write_news_to_markdown(news_articles_zn, zee_file_path)

#Extract data from business standard
news_articles_bs = business_standard.business_standard()
utils.write_news_to_markdown(news_articles_bs,bs_file_path)