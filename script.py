from selenium import webdriver as wd
from selenium.webdriver import ActionChains as ac
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from utils import Utils

BASE_URL = Utils().getBaseUrl()

# cr_usr = input('enter your login => ')
# cr_pwd = input('enter your pass => ')
# acc = input('enter profile to search => ')

cr_usr = Utils().getCreds()['usr']
cr_pwd = Utils().getCreds()['pwd']
acc = Utils().getAcc()

driver = wd.Chrome('/Users/ionglobe/Downloads/chromium-browser/chromedriver')

driver.get(BASE_URL + 'login')

driver.implicitly_wait(20)

## Authentication process
usr = driver.find_element_by_id('username')
pwd = driver.find_element_by_id('password')
sbmt = driver.find_element_by_xpath('//button[@type="submit"]')

usr.send_keys(cr_usr)
pwd.send_keys(cr_pwd)

ac(driver).click(sbmt).perform()

driver.get(BASE_URL + 'in/' + acc)


## Scrapping process
sName = ''
sJTitle = []
sCompany = []
sYear = []
sDescr = []

content = driver.page_source
soup = bs(content, features='html.parser')

sName = soup.select_one('ul.pv-top-card--list > li').text

for li in soup.findAll('li', attrs={'class':'pv-entity__position-group-pager'}):
    jt = li.find('h3')
    c = li.find('p', attrs={'class':'pv-entity__secondary-title'})
    y = li.find('h4', attrs={'class':'pv-entity__date-range'})
    sJTitle.append(jt.text)
    sCompany.append(c.text.split('\n')[1])
    sYear.append(y.text.split('\n')[2])


## How many times the 'WORD' being found in the profile
def findTheWord(str):
    return

def countTheWord(arr):
    return


## Save to file
df = pd.DataFrame({'Job Title': sJTitle, 'Company': sCompany, 'Year': sYear})

filename = re.sub(r'(\w)([A-Z])', r'\1 \2', sName.replace(' ', '')).lower().replace(' ', '_').replace('\n', '') + '.csv'

df.to_csv(filename, index = False, encoding = 'utf-8')

## return
# Name, Job title, Company, Year at company, description
# first job
# quantity of 'marketing' word usage