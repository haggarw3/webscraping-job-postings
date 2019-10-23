import requests
import pandas as pd
pd.set_option('display.max_columns', 100)
# url = 'http://www.miamidade.gov/transit/WebServices/Buses/?BusID'
# html = requests.get(url).content
# print(html)
# This is not the best option as the output is not in the right format
from bs4 import BeautifulSoup
url = 'http://www.miamidade.gov/transit/WebServices/Buses/?BusID'
html = requests.get(url).content
soup = BeautifulSoup(html, "lxml")
print(soup)
soup = BeautifulSoup(html, "html.parser")
print(soup)
soup = BeautifulSoup(html, "xml")
print(soup)
tags = ['BusID', 'BusName', 'Latitude', 'Longitude', 'RouteID', 'TripID', 'Direction', 'ServiceDirection', 'Service', 'ServiceName', 'TripHeadsign', 'LocationUpdated']
text = [element.text for element in soup.find_all(tags)]
print(text)
data = pd.DataFrame(columns=['BusID', 'BusName', 'Latitude', 'Longitude', 'RouteID', 'TripID', 'Direction', 'ServiceDirection', 'Service', 'ServiceName', 'TripHeadsign', 'LocationUpdated'])
data_list = []
data_dict = {}
print(len(tags))
for item in text:
    if (text.index(item) % 12 == 0) or (text.index(item) == 0):
        data_dict['BusID'] = item
    elif (text.index(item) % 12 == 1) or (text.index(item) == 1):
        data_dict['BusName'] = item
    elif (text.index(item) % 12 == 2) or (text.index(item) == 2):
        data_dict['Latitude'] = item
    elif (text.index(item) % 12 == 3) or (text.index(item) == 3):
        data_dict['Longitude'] = item
    elif (text.index(item) % 12 == 4) or (text.index(item) == 4):
        data_dict['RouteID'] = item
    elif (text.index(item) % 12 == 5) or (text.index(item) == 5):
        data_dict['TripID'] = item
    elif (text.index(item) % 12 == 6) or (text.index(item) == 6):
        data_dict['Direction'] = item
    elif (text.index(item) % 12 == 7) or (text.index(item) == 7):
        data_dict['ServiceDirection'] = item
    elif (text.index(item) % 12 == 8) or (text.index(item) == 8):
        data_dict['Service'] = item
    elif (text.index(item) % 12 == 9) or (text.index(item) == 9):
        data_dict['ServiceName'] = item
    elif (text.index(item) % 12 == 10) or (text.index(item) == 10):
        data_dict['TripHeadsign'] = item
    elif (text.index(item) % 12 == 11) or (text.index(item) == 11):
        data_dict['LocationUpdated'] = item
        data_list.append((data_dict))
        data_dict = {}

print(data_list)
data = pd.DataFrame(data_list)
print(data.head())
print(data.shape)