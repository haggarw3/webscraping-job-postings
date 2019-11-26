import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', None)
import re
import json
import urllib
import os
# os.makedirs('Image Data')  # for storing the images for each listing
import numpy as np
from datetime import date, datetime
import time
housinglink = 'https://miami.craigslist.org/d/housing/search/hhh'
current_link = housinglink
links = []
while len(links) < 1000:
    html = requests.get(current_link).content
    soup = BeautifulSoup(html, 'html.parser')
    postings = soup.find_all('a', {'class': 'result-image gallery'})
    temp = [posting['href'] for posting in postings]
    next_link_end = re.findall('\?.*', soup.find('a', {'class': 'button next'})['href'])
    current_link = current_link + next_link_end[0]
    for item in temp:
        links.append(item)
# Now we have all the links , we can scrape them one at a time and store the data
data = pd.DataFrame()
for link in links:
    title = []
    image_links = []
    description = []

    if requests.get(link).status_code == 200:
        html = requests.get(link).content
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('img'):
            image_links.append(i['src'])
        title_text = soup.find('span', {'class', 'postingtitletext'}).text.strip()
        description = [i for i in soup.find('section', {'id':'postingbody'}).text.strip().split('\n') if i != ""]
        temp_df = pd.DataFrame([title_text, link, description, image_links]).T
        data = pd.concat([data, temp_df], axis=0)



data.columns = ['Title', 'Link for Listing', 'Description', 'Image Links ']
data = data.reset_index()
data_acquired = data.to_dict('records')
f = open('DATA ACQUIRED 1', 'w')
f.write(json.dumps(data_acquired))
f.close()

        # current_path = os.getcwd()
        # image_storage_path = current_path + '/Image Data'
        # os.chdir(image_storage_path)
        # urllib.request.urlretrieve(image_link, os.path.basename(image_link))
        # os.chdir(current_path)
        # imgData = requests.get(image_link).content
