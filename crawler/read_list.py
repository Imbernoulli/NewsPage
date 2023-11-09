import random
import re
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from threading import Thread, Lock
import pandas as panda
import datetime
from datetime import date, timedelta

date1 = datetime.datetime(2022, 1, 1)
date2 = datetime.datetime(2022, 12, 31)

current_date=date1

option=ChromeOptions()
option.add_argument("--headless")

while current_date<=date2:
    browser = webdriver.Chrome(options=option)
    for i in range(1,5):
        try:
            browser.get("https://news.sina.com.cn/roll/?from=wap#pageid=153&lid=2515&etime=1693238400&stime=1693324800&ctime=1693324800&date="+current_date.strftime("%Y-%m-%d")+"&k=&num=50&page="+str(i))
            links=re.findall(r"<span class=\"c_tit\"><a href=\"(.+?)\" target=\"_blank\">",browser.page_source)
            browser.close()
            with open("sina_links.txt","a") as f:
                for link in links:
                    f.write(str(link)+"\n")
        except:
            break
    current_date+=timedelta(days=1)
