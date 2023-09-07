import json
import random
import re
import threading
from tqdm import tqdm
from threading import Lock, Thread
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

pages = []
bugs = []

def get_weibo_fans(url):
    option = ChromeOptions()
    option.add_argument("--headless")
    browser = webdriver.Chrome(options=option)
    browser.get('https://weibo.com/login.php')
    with open('weibo_cookies.json', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie['name'],
            'value': cookie['value'],
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        browser.add_cookie(cookie_dict)
    sleep(1)
    browser.get(url)
    response = browser.page_source
    fans = re.findall("粉丝<span>(.+?)</span>", response)[0]
    return fans


def getpage(i):
    global pages
    global bugs
    option = ChromeOptions()
    option.add_argument("--headless")
    with open("/Users/bernoulli_hermes/projects/python_summer/sina_links.txt", "r") as f:
        lines = f.readlines()
        for line in tqdm(lines[24000+20*i:24000+20*i+20]):
            links = [content["link"] for content in pages]
            if line.replace("\n", "") in links or line.replace("\n", "") in bugs:
                # if line.replace("\n", "") in links:
                continue
            # print("Start to catch:", line.replace("\n", ""))
            singlepage = {}
            # browser = webdriver.Chrome(options=option)
            # browser.get(line.strip("\n"))
            # response = browser.page_source
            response = requests.get(line.strip("\n"))
            response.encoding = 'UTF-8'
            response = str(response.text)
            soup = BeautifulSoup(response, "html.parser")
            public_time = re.findall(r"/(20.+?)/doc", line)[0]
            # browser.close()
            # try:
            #     title = soup.select('.main-title')[0].text
            #     source = soup.select('.source')[0].text
            #     author = source
            # except:
            if "/tech/csj/" in line:
                try:
                    weibolink = re.findall(
                        r"作者：.+?<a href=\"(.+?)\" target=\"_blank\">.+?</a>", response, re.DOTALL)[0]
                    author = re.findall(
                        r"作者：.+?<a href=\".+?\" target=\"_blank\">(.+?)</a>", response, re.DOTALL)[0]
                    if author in [page["author"] for page in pages]:
                        for page in pages:
                            if page["author"] == author:
                                fans = page["author_fans"]
                                break
                    else:
                        # fans = get_weibo_fans(weibolink)
                        fans=""
                    keywords = ["网络文化"]
                    source = "创世纪"
                except:
                    with open("bug.txt", "a") as f:
                        f.write("Failed in 1:"+line)
                    continue
            else:
                weibolink = ""
                fans = ""
                keywords = [kw.text for kw in soup.select('.keywords a')]
                try:
                    try:
                        author = soup.select_one(
                            '.article-editor').text.split("：")[1]
                    except:
                        author = soup.select_one('.article-editor').text
                    source = soup.select_one('.source').text
                except:
                    try:
                        source = soup.find('a', rel='nofollow').text
                        author = source
                    except:
                        with open("bug.txt", "a") as f:
                            f.write("Failed in 2:"+line)
                        continue
            try:
                maincontent = []
                keywords = [kw.text for kw in soup.select('.keywords a')]
                matches = re.findall(r'<p.*?>(.*?)</p>|<div class="img_wrapper"><img .*? src="(.*?)".+?</div>', str(
                    soup.select_one('#artibody')), re.DOTALL)
                for match in matches:
                    p_content, img_link = match
                    if p_content:
                        result = p_content.strip().replace('\n', "").replace("\t", "")
                        maincontent.append(result)
                    if img_link:
                        if "//n" in img_link and "://n" not in img_link:
                            result = img_link.replace("//n", "https://n")
                        else:
                            result = img_link
                        maincontent.append(result)
                title = soup.select_one('meta[property="og:title"]')['content']
                comments = []
                comment_user = re.findall(
                    r"userLnk=(.+?)&amp;cont=.+?\"", response)
                comment_content = re.findall(
                    r"userLnk=.+?&amp;cont=(.+?)\"", response)
            except:
                with open("bug.txt", "a") as f:
                    f.write("Failed in 4:"+line)
                continue
            for i in range(len(comment_content)):
                singlecontent = {}
                p = 0
                if i >= 1:
                    for j in range(i):
                        if comment_content[i] == comment_content[j]:
                            p += 1
                if (p != 0):
                    continue
                singlecontent["user"] = comment_user[i]
                singlecontent["content"] = comment_content[i]
                comments.append(singlecontent)
            singlepage["index"] = len(pages)+1
            singlepage["title"] = title
            singlepage["link"] = line.strip("\n")
            singlepage["date"] = public_time
            singlepage["source"] = source
            singlepage["author"] = author
            singlepage["author_fans"] = fans
            singlepage["author_weibo_link"] = weibolink
            singlepage["content"] = maincontent
            singlepage["keywords"] = keywords
            singlepage["comments"] = comments
            pages.append(singlepage)
            with open("/Users/bernoulli_hermes/projects/python_summer/sina_pages.json", "w") as f:
                f.write(json.dumps(pages, indent=4, ensure_ascii=False))


def main():
    global pages
    global bugs
    
    try:
        with open("/Users/bernoulli_hermes/projects/python_summer/bug.txt", "r") as f:
            kugs = f.readlines()
            for kug in kugs:
                bugs.append(kug.split(":")[1]+":" +
                            kug.split(":")[2].replace("\n", ""))
    except:
        pass
    
    with open("/Users/bernoulli_hermes/projects/python_summer/sina_pages.json", "r") as f:
        pages = json.loads(f.read())
        
    for i in range(40):
        t = threading.Thread(target=getpage, args=(i,))
        t.start()


if __name__ == "__main__":
    main()
