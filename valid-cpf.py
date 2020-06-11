import time
import traceback
from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

client = MongoClient('localhost', 27017)
db = client.miningNames
tablesNames = db.names
tablesUsers = db.users


def get_cpf_site(url):
    try:
        req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
        html = urlopen(req).read()
    except HTTPError as e:
        print(e, traceback.format_exc())
        return None
    try:
        html = BeautifulSoup(html, "html.parser")
        print(html)
    except AttributeError as e:
        print(e, traceback.format_exc())
        return None
    # return title


def format_name(s):
    l = s.split()
    new = ""

    for i in range(1, len(l) - 1):
        s = l[i]
        new += (s[0].upper() + '. ')

    new += l[-1].title()
    return l[0] + " " + new


# get_cpf_site("https://www.situacao-cadastral.com/")

sleep = 30

driver = webdriver.Firefox()
driver.get("https://www.situacao-cadastral.com/")
driver.execute_script("document.getElementById('doc').value = '03715447184';")
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="consultar"]')))
time.sleep(sleep)
element.click()

element_cpf = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="dados documento"]')))
element_name = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="dados nome"]')))

print(element_cpf.text, element_name.text)
driver.close()

# for user in list(tablesNames.find({})):
#     name = user.get('name')
#     cpfs = user.get('cpf')
#
#     for cpf in cpfs:
#         get_cpf_site("https://www.situacao-cadastral.com/")
# print(name, format_name(name), cpf)
