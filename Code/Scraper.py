import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#import scrapy
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree

#python Scraper.py CO2 concentration table

def main():
    input = sys.argv[1:]
    text = ' '.join(input)
    scraper(text)

def scraper(text):
    global corpus
    global dict_href_links

    options = Options()
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com/search?q=' + text)
    try:
        driver.find_element(By.ID, "L2AGLb").click()
    except:
        pass
    URL = driver.current_url
    #driver.save_screenshot('screenshot.png')
    corpus = (driver.find_element(By.XPATH, "/html/body").text)

    links = urls(driver)
    print(links)
    
    for i in links:
        driver.get(i)
        html_source = driver.page_source
        table = []
        soup = BeautifulSoup(html_source, 'html.parser')
        mini = []
        print(driver.current_url)
        for i in soup.find_all('table'):
            for child in i.children:
                for td in child:
                    #html_source.find(">", start_index_number, end_index_number)
                    #print(td)
                    if td != " " and td != "":
                        mini.append(str(td))
        whole = []
        for i in mini:
            sp = BeautifulSoup(i, 'html.parser')
            tag = sp('span')
            temp = []
            for a in tag:
                try:
                    temp2 = str(a.contents[0])
                    if "<" not in temp2 and "" != temp2:
                        temp.append(a.contents[0])
                except:
                    pass
            if temp != []:
                whole.append(temp)
        if whole != []:
            print(whole)
    #print((driver.find_element(By.XPATH, "/html/body").text))



def urls(driver):
    links = [] # Initiate empty list to capture final results
    # Specify number of pages on google search, each page contains 10 #links
    n_pages = 20 
    for page in range(1, n_pages):
        #url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
        #driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # soup = BeautifulSoup(r.text, 'html.parser')

        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            if h.a.get('href') not in links:
                links.append(h.a.get('href'))
    
    return links



if __name__ == "__main__":
    main()