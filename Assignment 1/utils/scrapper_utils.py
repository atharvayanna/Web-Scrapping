import json
from bs4 import BeautifulSoup
import csv
import requests



def read_config(file_path):
    """This function takes file path as input, reads the following json file and returns a dictionary"""
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data
    
def write_json(file_path, data):
    """This function takes file path, dictionary data as input and over write the file with the data"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

#Get date from meta data of the link
def extract_date_from_meta(link):
    """Extracts the date from the meta tags of the given URL."""
    try:
        response = requests.get(link)
        
        # Get the page source and parse it with BeautifulSoup
        if response.status_code == 200:
            source = response.content
            date_soup = BeautifulSoup(source, 'html.parser')
            
            # Extract date from meta tags
            meta_tag = date_soup.find('meta', {'property': 'article:published_time'})
            if meta_tag:
                return meta_tag.get('content')
            
            meta_tag = date_soup.find('meta', {'itemprop': 'article:published_time'})
            if meta_tag:
                return meta_tag.get('content')
        
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def dict_to_csv(data_dict, csv_file_path):
    """This function takes data(ditionary) and csv file path as input and writes the data to csv file"""
    try:
        # Prepare the CSV file for writing
        with open(csv_file_path, 'w', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header row (column names)
            header = data_dict.keys()
            writer.writerow(header)

            # Determine the maximum length of lists for proper row count
            max_len = max(len(v) for v in data_dict.values())

            # Write data rows
            for i in range(max_len):
                row = [data_dict[key][i] if i < len(data_dict[key]) else '' for key in header]
                writer.writerow(row)

    except Exception as e:
        raise Exception('Unable to write file',e)


