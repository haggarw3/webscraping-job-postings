from bs4 import BeautifulSoup
import requests
import pandas as pd
pd.set_option('display.max_columns', 100)
# import numpy as np
import os.path
from os import path
position = 'data+analyst'
location = 'Florida'
# url = 'https://www.indeed.com/jobs?q=data+analyst&l=Florida'
url = 'https://www.indeed.com/jobs?q='+position+'&l='+location
print(url)
html = requests.get(url).content
soup = BeautifulSoup(html, "html.parser")
print(soup)
if not path.exists('jobdata.txt'):
    with open('jobdata.txt', 'w') as f:
        f.write(soup.text)
    f.close()








































#For automation: https://www.indeed.com/jobs?q=data+analyst&l=Florida&start=20
starts = [10, 20, 30, 40, 50, 60]
for page in starts:
    url = 'https://www.indeed.com/jobs?q='+position+'&l='+location+'&start='+str(page)
    print(url)