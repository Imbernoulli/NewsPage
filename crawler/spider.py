import random
import re
import json
import requests
import threading
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread, Lock

line="https://www.fastcompany.com/90944322/how-did-cotton-become-the-fabric-of-our-lives-a-logo-and-that-damn-song"
# response = requests.get(line)
# response=response.text
option=ChromeOptions()
option.add_argument("--headless")
browser = webdriver.Chrome(options=option)
browser.get(line)
response = browser.page_source
# browser = webdriver.Chrome(options=option)
# browser.get(line.strip("\n"))
# response=browser.page_source
soup=BeautifulSoup(response,"lxml")
# Extract article title
with open("debug1.txt", "w") as f:
    f.write(response)
# title = soup.select_one('.main-title').text

# Extract author 
# author = soup.select_one('.article-editor').text
# print("Author:", author)


# option = ChromeOptions()
# option.add_argument("--headless")
# browser = webdriver.Chrome(options=option)
# browser.get('https://weibo.com/login.php')
# with open('微博_cookies.txt', 'r', encoding='utf8') as f:
#     listCookies = json.loads(f.read())
# for cookie in listCookies:
#     cookie_dict = {
#         'domain': '.weibo.com',
#         'name': cookie.get('name'),
#         'value': cookie.get('value'),
#         "expires": '',
#         'path': '/',
#         'httpOnly': False,
#         'HostOnly': False,
#         'Secure': False
#     }
#     browser.add_cookie(cookie_dict)
# sleep(1)
# browser.get(url)
# response=browser.page_source
# fans=re.findall("粉丝<span>(.+?)</span>",response)[0]
# print(fans)

# weibolink=re.findall(r"作者：.+?<a href=\"(.+?)\" target=\"_blank\">.+?</a>",response,re.DOTALL)[0]
# author=re.findall(r"作者：.+?<a href=\".+?\" target=\"_blank\">(.+?)</a>",response,re.DOTALL)[0]
# fans=get_weibo_fans(weibolink)
# source = soup.find('a', rel='nofollow').text
# print(source)

# print('\"'in"sha\"sd")
# source = soup.select_one('.source').text
# # source = soup.find('a', rel='nofollow').text
# print("Source:", source)
# browser = webdriver.Chrome()
# browser.maximize_window()
# browser.get('https://weibo.com/login.php')
# with open('微博_cookies.txt', 'r', encoding='utf8') as f:
#     listCookies = json.loads(f.read())

# # 往browser里添加cookies
# for cookie in listCookies:
#     cookie_dict = {
#         'domain': '.weibo.com',
#         'name': cookie.get('name'),
#         'value': cookie.get('value'),
#         "expires": '',
#         'path': '/',
#         'httpOnly': False,
#         'HostOnly': False,
#         'Secure': False
#     }
#     browser.add_cookie(cookie_dict)
# sleep(1)
# browser.get('https://weibo.com/u/6468040956')



# for i in range(1,51):
#     browser=webdriver.Safari()
#     browser.get("https://news.sina.com.cn/roll/?from=wap#pageid=153&lid=2515&k=&num=50&page="+str(i))
#     links=re.findall(r"<span class=\"c_tit\"><a href=\"(.+?)\" target=\"_blank\">",browser.page_source)
#     browser.close()
#     with open("sina_links.txt","a") as f:
#         for link in links:
#             f.write(str(link)+"\n")


# browser=webdriver.Safari()
# browser.get("http://finance.sina.com.cn/tech/csj/2022-09-22/doc-imqqsmrp0103050.shtml")
# response = browser.page_source
# print(re.findall("<a target=\"_blank\" href=\".+?\">(.+?)</a>",response,re.DOTALL))
# browser.close()
# with open("debug.txt", "w") as f:
#     f.write(response)

# def get_weibo_fans(url):
#     browser = webdriver.Chrome()
#     browser.maximize_window()
#     browser.get('https://weibo.com/login.php')
#     with open('微博_cookies.txt', 'r', encoding='utf8') as f:
#         listCookies = json.loads(f.read())
#     for cookie in listCookies:
#         cookie_dict = {
#             'domain': '.weibo.com',
#             'name': cookie.get('name'),
#             'value': cookie.get('value'),
#             "expires": '',
#             'path': '/',
#             'httpOnly': False,
#             'HostOnly': False,
#             'Secure': False
#         }
#         browser.add_cookie(cookie_dict)
#     sleep(1)
#     browser.get(url)
#     response=browser.page_source
#     with open("debug.txt", "w") as f:
#         f.write(response)
#     fans=re.findall("粉丝<span>(.+?)</span>",response)[0]
#     return fans

# line="http://finance.sina.com.cn/tech/csj/2022-07-08/doc-imizirav2517173.shtml"
# option=ChromeOptions()
# option.add_argument("--headless")
# browser = webdriver.Chrome(options=option)
# browser.get(line)
# response = browser.page_source
# browser.close()
# weibolink=re.findall(r"作者：.+?<a href=\"(.+?)\" target=\"_blank\">.+?</a>",response,re.DOTALL)[0]
# author=re.findall(r"作者：.+?<a href=\".+?\" target=\"_blank\">(.+?)</a>",response,re.DOTALL)[0]
# maincontent=re.findall(r"techsina</span></p> -->(.+?)<!-- 正文页广告 -->",response,re.DOTALL)[0]
# keywords=["网络文化"]
# public_time=re.findall(r"/tech/csj/(.+?)/",line)[0]