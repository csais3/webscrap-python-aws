from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://mx.indeed.com/')

df = pd.DataFrame({'link': [''], 'job_title': [''], 'company': [''],
                   'date_posted': [''], 'location': ['']})

while True:
    soup = BeautifulSoup(driver.page_source, 'lxml')

    boxes = soup.find_all('div', class_='job_seen_beacon')
    
    for box in boxes:
        # Get link
        link = box.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        # Get job title
        job_title = box.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').text
        # get company
        try:
            company = box.find('span', class_='companyName').text
        except:
            company = 'N/A'
        # get date posted
        date_posted = box.find('span', class_='date').text
        # get location
        location = box.find('div', class_='companyLocation').text
        # append to dataframe
        df = df.append({'link': link, 'job_title': job_title, 'company': company,
                           'date_posted': date_posted, 'location': location}, ignore_index=True)
        
        next_page = soup.find('a', {'aria-label': 'Next Page'}).get('href')
        next_page = 'https://mx.indeed.com'+next_page
        driver.get(next_page)
        time.sleep(3)
     
############################ Data Cleaning ####################################
# Add link main domain to column link in dataframe
df['link'] = 'https://mx.indeed.com'+df['link']
# replacing elements from date posted
df.iloc[1:,:]
def posted(x):
    x = x.replace('PostedPublicado hace ', '').strip()
    try:
        x = x.replace('más de ', '').strip()
    except:
        pass
    try:
        x = x.replace(' días', '').strip()
    except:
        pass
    try:
        x = x.replace('EmployerActivo hace ', '').strip()
    except:
        pass
    return float(x)
    
df['date_posted'] = df[1:]['date_posted'].apply(posted)

############################ Send email #####################################
        
        
        
        
        
        
        
        