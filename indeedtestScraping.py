from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
pd.set_option('display.max_columns', None)
import numpy as np
from datetime import date, datetime
import time
import os
# driver = webdriver.Chrome(executable_path='/Users/himanshuaggarwal/PycharmProjects/webscraping/chromedriver')
driver = webdriver.Firefox(executable_path='/Users/himanshuaggarwal/PycharmProjects/webscraping/geckodriver')
files = os.listdir()
for file in files:
    if 'Results for UX' in file or 'Results for Data' in file or 'Results for Web Devs' in file:
        os.remove(file)
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
    except:
        pass
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
        job_posting_link = []
        for posting in jobpostings:
            temp = posting.find('a', {'class': 'jobtitle turnstileLink'})['href']
            if posting.find('div', {'class': 'title'}) is not None and len(re.findall('jk.*', temp)) > 0:
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
                if posting.find('a', {'class':'jobtitle turnstileLink'}) is not None:
                    temp = posting.find('a', {'class':'jobtitle turnstileLink'})['href']
                    try:
                        temp = 'https://www.indeed.com/viewjob?' + re.findall('jk.*', temp)[0]
                        job_posting_link.append(temp)
                    except:
                        pass
                else:
                    job_posting_link.append('NA')
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
        temp_df['JobPostingLink'] = job_posting_link
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
    time.sleep(3)
    # Since the clicks was not working. We used the return key in the same cell
    # driver.find_elements_by_class_name('icl-WhatWhere-buttonWrapper')[0].click()
    driver.find_elements_by_id('text-input-where')[0].send_keys(Keys.RETURN)
    time.sleep(3)
    driver.find_elements_by_partial_link_text('Advanced Job Search')[0].click()
    select = Select(driver.find_element_by_id('radius'))
    # select by visible text
    # select.select_by_visible_text('within 50 miles of')
    # select by value
    select.select_by_value('50')
    select = Select(driver.find_element_by_id('fromage'))
    select.select_by_value('7')
    select = Select(driver.find_element_by_id('limit'))
    select.select_by_value('50')
    time.sleep(2)
    driver.find_element_by_id('fj').click()

    data = pd.DataFrame(columns=['Title', 'Company', 'Summary', 'Location', 'DayPosted', 'JobPostingLink'])
    time.sleep(3)
    try:
        if driver.find_elements_by_class_name('popover-foreground') is not None:
            if len(driver.find_elements_by_class_name('popover-foreground')) > 0:
                driver.find_elements_by_id('popover-link-x')[0].click()
                print('PopOver Eliminated')
                time.sleep(4)
    finally:
        print('Starting Scraping')

    FLAG = True
    counter = 1
    while FLAG:
        try:
            if driver.find_elements_by_class_name('popover-foreground') is not None:
                if len(driver.find_elements_by_class_name('popover-foreground')) > 0:
                    driver.find_elements_by_id('popover-link-x')[0].click()
                    print('PopOver Eliminated')
                    time.sleep(4)
        except:
            pass
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
            except:
                print('Next page was not found or click did not word')
                FLAG = False
        else:
            FLAG = False
            print('Exit - url not found')
        if data.shape[0] > 150:
            FLAG = False
            print('Exit - Got 100 rows')

    data['Cohort'] = job
    data['Date'] = date.today()
    data['Date & Time'] = datetime.now()
    data['DayPosted'] = list(map(lambda x: x[0:11], data['DayPosted']))
    data = data.reset_index()
    print(data)
    # Saving to a csv file

    if 'ux' in job.lower():
        if '/' in job:
            data.to_excel('Results for UXUI.xlsx', sheet_name='Sheet')
        else:
            data.to_excel('Results for UX.xlsx', sheet_name=job)
    elif 'designer' in job.lower():
        data.to_excel('Results for Product Designer.xlsx', sheet_name=job)
    elif 'analysis' in job.lower():
        data.to_excel('Results for Data Analysis.xlsx', sheet_name=job)
    elif 'analyst' in job.lower():
        data.to_excel('Results for Data Analyst.xlsx', sheet_name=job)
    elif 'developer' in job.lower():
        data.to_excel('Results for Web Developers.xlsx', sheet_name=job)
    elif 'software' in job.lower():
        data.to_excel('Results for Software Engineer.xlsx', sheet_name=job)


