from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from datetime import date, datetime
import time
# driver = webdriver.Chrome(executable_path='/Users/himanshuaggarwal/PycharmProjects/webscraping/chromedriver')
driver = webdriver.Firefox(executable_path='/Users/himanshuaggarwal/PycharmProjects/webscraping/geckodriver')
# job_filter = input('enter the job type filter')
# flag = True
# while flag:
#     print('You have entered', job_filter)
#     print('If this is correct press 1')
#     choice = int(input('Enter Choice'))
#     if choice == 1:
#         flag = False
#     else:
#         print('Your Choice was', choice)
#         job_filter = input('enter the job type filter')


def get_data(link):
    # This is to close a pop up window if it appears on the screen
    time.sleep(6)
    try:
        if driver.find_elements_by_class_name('popover-foreground') is not None:
            if len(driver.find_elements_by_class_name('popover-foreground')) > 0:
                driver.find_elements_by_id('popover-link-x')[0].click()
    finally:
        html = requests.get(link).content
        soup = BeautifulSoup(html, 'html.parser')
        jobpostings = soup.find_all('div', {'data-tn-component': 'organicJob'})
        title = []
        company = []
        location = []
        summary = []
        salary_snippet = []
        day_posted = []
        for posting in jobpostings:
            if posting.find('div', {'class': 'title'}) is not None:
                title.append(posting.find('div', {'class': 'title'}).text.strip())
                if posting.find('div', {'class': 'sjcl'}) is not None:
                    temp = posting.find('div', {'class': 'sjcl'}).text.strip().split('\n')
                    sjcl = []
                    for item in temp:
                        if item != '':
                            sjcl.append(item)
                    company.append(sjcl[0])
                    location.append(sjcl[-1])
                else:
                    company.append('NA')
                    location.append('NA')
                if posting.find('div', {'class': 'summary'}) is not None:
                    summary.append(posting.find('div', {'class': 'summary'}).text.strip())
                else:
                    summary.append('NA')
                if posting.find('div', {'class': 'salarysnippet'}) is not None:
                    salary_snippet.append(posting.find('div', {'class': 'salarysnippet'}))
                else:
                    salary_snippet.append('NA')
                if posting.find('div', {'class': 'jobsearch-SerpJobCard-footerActions'}) is not None:
                    day_posted.append(
                        posting.find('div', {'class': 'jobsearch-SerpJobCard-footerActions'}).text.strip().split(' -')[
                            0].strip())
                else:
                    day_posted.append('NA')
        temp_df = pd.DataFrame()
        temp_df['Title'] = title
        temp_df['Company'] = company
        temp_df['Summary'] = summary
        temp_df['Location'] = location
        temp_df['DayPosted'] = day_posted
    return temp_df


jobs = ['Data Analysis', 'Data Analyst', 'Developer', 'Software Engineer', 'UX', 'Product Designer', 'UX/UI']
for job in jobs:
    driver.get('https://www.indeed.com')
    # Deleting anything that might be there in the cell and input new values for Job Type
    driver.find_element_by_id('text-input-what').send_keys(Keys.COMMAND + "a")
    driver.find_element_by_id('text-input-what').send_keys(Keys.DELETE)
    driver.find_elements_by_id('text-input-what')[0].send_keys(job)
    time.sleep(6)
    # location = input('enter the location filter')
    # flag = True
    # while flag:
    #     print('You have entered', location)
    #     print('If this is correct press 1')
    #     choice = int(input('Enter Choice'))
    #     if choice == 1:
    #         flag = False
    #     else:
    #         print('Your Choice was', choice)
    #         location = input('enter the location filter')

    # Deleting anything that might be there in the cell and input new values for Location
    driver.find_element_by_id('text-input-where').send_keys(Keys.COMMAND + "a")
    driver.find_element_by_id('text-input-where').send_keys(Keys.DELETE)
    driver.find_elements_by_id('text-input-where')[0].send_keys('Miami, FL')
    # time.sleep(3)
    # Since the clicks was not working. We used the return key in the same cell
    # driver.find_elements_by_class_name('icl-WhatWhere-buttonWrapper')[0].click()
    driver.find_elements_by_id('text-input-where')[0].send_keys(Keys.RETURN)
    data = pd.DataFrame(columns=['Title', 'Company', 'Summary', 'Location', 'DayPosted'])
    # time.sleep(3)
    try:
        if driver.find_elements_by_class_name('popover-foreground') is not None:
            if len(driver.find_elements_by_class_name('popover-foreground')) > 0:
                driver.find_elements_by_id('popover-link-x')[0].click()
                print('PopOver Eliminated')
    finally:
        print('Starting Scraping')

    FLAG = True
    counter = 1
    while FLAG:
        if driver.current_url is not None:
            print(driver.current_url)
            print(counter)
            counter += 1
            # Go to the next page. We are using find_element instead of elements so that we only go to the next page
            url = driver.current_url
            scraped_page_df = get_data(url)
            data = pd.concat([data, scraped_page_df], axis=0)
            try:
                time.sleep(3)
                driver.find_element_by_class_name('pn').click()
            except KeyError:
                print('Next page was not found or click did not word')
                FLAG = False
        else:
            FLAG = False
            print('Exit - url not found')
        if data.shape[0] > 100:
            FLAG = False
            print('Exit - Got 100 rows')

    data['Cohort'] = job
    data['Date'] = date.today()
    data['Date & Time'] = datetime.now()
    data['DayPosted'] = list(map(lambda x: x[0:11], data['DayPosted']))
    print(data)
    # Saving to a csv file
    if 'UX' in job:
        data.to_csv('Results for UX')
    else:
        data.to_csv('Results for' + job)


