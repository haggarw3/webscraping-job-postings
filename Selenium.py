# https://selenium-python.readthedocs.io/locating-elements.html
# https://devhints.io/xpath
from selenium import webdriver
driver = webdriver.Chrome(executable_path='/Users/himanshuaggarwal/PycharmProjects/webscraping/chromedriver')
driver.get('https://www.overbuff.com')
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/div[2]/a').click()
table = driver.find_element_by_tag_name('table')
tabla_contents = table.find_element_by_tag_name('thead')
print(tabla_contents)
columns = tabla_contents.find_element_by_tag_name('tr')
print(columns)
tbody = driver.find_element_by_tag_name('tbody')
tr_body = driver.find_elements_by_tag_name('tr')
tr = [i.text for i in tr_body]
tr_complete= tr[1:]
tr_clean= [i.split('\n')for i in tr_complete]
print(tr_clean)
import pandas as pd
df = pd.DataFrame(tr_clean, columns= (['Hero', 'Position', 'Pick Rate', 'Win Rate', 'Tie Rate', 'On Fire']))
for i in tr_clean:
    df = df.append(i)
print(df)






