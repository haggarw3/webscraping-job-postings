from selenium import webdriver
from pyvirtualdisplay import Display
import time 
url='https://threatbutt.com/map/'

# remove pictures and display

display=Display(visible=0)
#display.start()


# In[ ]:


# Selenium Firefox driver

driver=webdriver.Firefox()


# In[ ]:


# start scrap

while 1:

    driver.get(url)

    time.sleep(3)

    count=0
    while count<1000:

        elemento=driver.find_element_by_id('attackdiv')
        t=elemento.text.split('\n')[-1]

        
        predator=(t.split('('))[0]
        ip_pred=(t.split('('))[1].split(')')[0]
        
        prey=(t.split('('))[1].split(')')[1][-4:]
        ip_prey=(t.split('('))[2].split(')')[0]
        
        print({'timestamp':time.time(), 'predator': predator, 'ip_pred': ip_pred,
               'prey': prey, 'ip_prey': ip_prey})
        
        
        count+=1


# In[ ]:




