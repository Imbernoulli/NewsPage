from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.common.by import By
 

driver = webdriver.Chrome()
driver.get('https://weibo.com/login.php')
sleep(5)
a = driver.find_element(By.XPATH, '//*[@id="pl_login_form"]/div/div[1]/div/a[2]')
a.click()
sleep(5)
dictCookies = driver.get_cookies()
with open('weibo_cookies.json', 'w') as f:
    f.write(json.dumps(dictCookies,indent=4))

