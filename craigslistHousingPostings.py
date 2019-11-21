import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', None)
import re
import urllib
import os
os.makedirs('Image Data')  # for storing the images for each listing
import numpy as np
from datetime import date, datetime
import time
housinglink = 'https://miami.craigslist.org/d/housing/search/hhh'
current_link = housinglink
links = []
while len(links) < 200:
    html = requests.get(current_link).content
    soup = BeautifulSoup(html, 'html.parser')
    postings = soup.find_all('a', {'class': 'result-image gallery'})
    temp = [posting['href'] for posting in postings]
    next_link_end = re.findall('\?.*', soup.find('a', {'class': 'button next'})['href'])
    current_link = current_link + next_link_end[0]
    for item in temp:
        links.append(item)
# Now we have all the links , we can scrape them one at a time and store the data
for link in links[0:2]:
    print(link)
    if requests.get(link).status_code == 200:
        html = requests.get(link).content
        soup = BeautifulSoup(html, 'html.parser')
        image_link = soup.find_all('img')[0]['src'].lstrip('/')
        current_path = os.getcwd()
        image_storage_path = current_path + '/Image Data'
        os.chdir(image_storage_path)
        urllib.request.urlretrieve(image_link, os.path.basename(image_link))
        os.chdir(current_path)
        # imgData = requests.get(image_link).content
