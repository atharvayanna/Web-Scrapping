from selenium  import webdriver
import time
import re

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import time
import os

def download_form(link, file_name):
    """This function takes link as input and downloads the pdf"""
    # Set the path to the correct geckodriver executable
    service = Service(executable_path=r'C:\Users\atharva.yanna\Desktop\Python\geckodriver.exe')

    # Configure Firefox options
    options = Options()
    options.set_preference("browser.download.folderList", 2)  # Use custom download path
    options.set_preference("browser.download.manager.showWhenStarting", False)  # Disable the download dialog
    options.set_preference("browser.download.dir", r"C:\Users\atharva.yanna\Desktop\Python\Assignment 2\Forms")  # Set the download path
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # MIME type for PDF
    options.set_preference("pdfjs.disabled", True)  # Disable PDF viewer to ensure the file is downloaded

    # Create a WebDriver service and instance with the options
    driver = webdriver.Firefox(options=options, service=service)

    try:
        # Navigate to the PDF URL
        if '.pdf' in link:
            driver.get(link)
            time.sleep(1)  
            driver.close()

        driver.quit()

    except Exception as e:
        print("Error to close the driver after download",e)

    finally:
        if driver:
            #Search for file name that is downloaded
            pattern = r'[^/]+\.pdf$'
            match  = re.search(pattern,link)
            download_file = match.group()
            # print(download_file, "Download file Name")
            
            # Define the download directory and new file name
            download_dir = r"C:\Users\atharva.yanna\Desktop\Python\Assignment 2\Forms"
            time.sleep(2) 

            # Rename the file
            downloaded_file_path = os.path.join(download_dir, download_file)
            new_file_path = os.path.join(download_dir, file_name)
            
            if os.path.exists(downloaded_file_path):
                os.rename(downloaded_file_path, new_file_path)
                print(f"File renamed to {file_name}")
            else:
                print("Downloaded file not found.")
            driver.quit()

def select_pages(reader,page_no):
    """This function takes pdf reader object and page_no as input and returns list of pages specified"""
    pages = []
    for i in range(0,page_no):
        pages.append(reader.pages[i])

    return pages

def find_cin(cin:list , page):
    """This function takes list and page object as input and returns the list of CIN numbers as output"""
    match = re.findall(r'([A-Z][0-9]+[A-Z]+[0-9]+[A-Z]+[0-9]+)', page.extract_text())
    if match:
        for e in match:
            cin.append(e)
    
    return cin

def table_cin(cin: list,page):
    """This function takes list and page object as input and returns only CIN number from the table only"""
    pattern = r'([0-9]+)+( )+([A-Z]+.*) ([0-9]+)+'
    match = re.findall(pattern, page.extract_text())
    if match:
        for e in match:
            match  = re.search(r'[A-Z]([0-9]+).+[A-Z]+[0-9]+', e[2])
            if match:
                cin.append(match.group())
    
    return cin
    
def find_mailid(mail_id:list,page):
    """This function takes list and page no as input and return list with all mail in page"""

    pattern = r'([\w]+@[\w]+.[\w]+)'
    match = re.findall(pattern, page.extract_text())
    for e in match:
        mail_id.append(e)

    return mail_id

def find_PAN(pan,page):
    """This function search's for Pan number and return list of pan numbers"""
    pattern = r'[A-Z]{5}[0-9]{4}[A-Z]'
    match = re.findall(pattern, page.extract_text())
    for e in match:
        pan.append(e)
    
    return pan

def find_date(date:list,page):
    """This function search for date and returns list of all dates"""
    pattern = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'

    match = re.findall(pattern,page.extract_text())
    for e in match:
        date.append(e)

    return date

def find_website(website:list, page):
    """This function searchs for website and returns list of all website"""
    pattern = r'www.[\w]+.[\w]+'

    match = re.findall(pattern,page.extract_text())
    for e in match:
        website.append(e)

    return website

def find_phone(phone, page):
    """This Function is used to get the phone no from the pdf"""
    pattern = r'Telephone number with STD code ((\+)?[0-9]+(-)?[0-9]+)'

    match = re.findall(pattern, page.extract_text())
    # print(match[0][0])
    for e in match:
        phone.append(e[0])

    return phone

