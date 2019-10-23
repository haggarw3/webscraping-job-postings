import requests
from bs4 import BeautifulSoup
url = 'https://www.flalottery.com/exptkt/p2.htm'
html = requests.get(url).content
soup = BeautifulSoup(html, "lxml")
soup
tags = ['td']
text = [element.text for element in soup.find_all(tags)]
text
content = []
for element in soup.find_all(tags):
    text = element.text
    if text != '':
        print(text)
        content.append(text)

pattern = '\d*/\d*/\d*'
dates = []
alphabets = []
number1 = []
number2 = []
for i, item in enumerate(content):
    if re.search(pattern, item) is not None:
        dates.append(item)
        alphabets.append(re.findall('[A-Z]',content[i+1]))
        number1.append(re.findall('[0-9]',content[i+2]))
        number2.append(re.findall('[0-9]',content[i+4]))


# pattern = '\d*/\d*/\d*'
# string = '10/21/19'
# re.search(pattern, string)
import pandas as pd
data = pd.DataFrame([dates,alphabets, number1, number2])
data=data.T
data.head(100)
