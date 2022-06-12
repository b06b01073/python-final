from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service


import time



def crawler(urls):
    driver = webdriver.Chrome('./chromedriver')

    dict = {}

    for url in urls:
        # crawl the page by selenium
        # try:

        # change url to scientific name
        dict.setdefault(url, [])
        driver.get(url)

        # sleep for 3 secs to make sure the page is loaded completely
        time.sleep(2)

        html = driver.page_source

        # pass the crawled page to beautifulsoup
        soup = BeautifulSoup(html, "html.parser")

        # select the <div> with id "threats-details"
        result = soup.find("div", {"id": "threats-details"})

        for row in result.tbody.find_all('tr', recursive=False):
            threat = row.find('td').text
            if len(threat) != 0:
                dict[url].append(threat)

    return dict
