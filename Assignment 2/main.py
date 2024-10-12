from pypdf import PdfReader
from utils import read_pdf
from utils import utils 
import os

#Path for PDF files
Tata_pdf_path = r'C:\Users\atharva.yanna\Desktop\Python\Assignment 2\Forms\Tata form.pdf'
tata_link = r'https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf'
Airtel_pdf_path = r'C:\Users\atharva.yanna\Desktop\Python\Assignment 2\Forms\Airtel form.pdf'
airtel_link = r'https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf'
page_number = 3

#Check for the pdf file exist if not then download the file
if not os.path.exists(Tata_pdf_path):
    utils.download_form(tata_link, 'Tata form.pdf')
if not os.path.exists(Airtel_pdf_path):
    utils.download_form(airtel_link, 'Airtel form.pdf')

#Reader object for the pdf
tata_reader = PdfReader(Tata_pdf_path)
airtel_reader = PdfReader(Airtel_pdf_path)

#Filtering the pages
tata_pages = utils.select_pages(tata_reader,page_number)
airtel_pages = utils.select_pages(airtel_reader,page_number)

print("\n********** Tata PDF **********\n")
read_pdf.read_data(tata_pages)
print("\n********** Airtel PDF **********\n")
read_pdf.read_data(airtel_pages)
     
