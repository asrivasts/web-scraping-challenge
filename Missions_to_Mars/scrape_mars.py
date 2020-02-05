# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Setup Chromedriver for Windows
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    nasaURL = 'https://mars.nasa.gov/news/'
    browser.visit(nasaURL)
    time.sleep(2)
    soupNasa = bs(browser.html, 'html.parser')

    news_title = soupNasa.find('div', class_="content_title").find('a').text.strip()
    news_p = soupNasa.find('div', class_="article_teaser_body").text.strip()
    news_date = soupNasa.find('div', class_="list_date").text.strip()

    jplURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jplURL)
    time.sleep(2)
    soupJPL = bs(browser.html, 'html.parser')
    browser.find_by_id("full_image").click()
    browser.find_link_by_partial_text("more info").click()
    soupJPL = bs(browser.html, 'html.parser')

    featured_image_url = 'https://www.jpl.nasa.gov' + soupJPL.find('figure').find('img')['src']

    twitterURL = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterURL)
    time.sleep(2)
    soupTwitter = bs(browser.html, 'html.parser')

    mars_weather = soupTwitter.find("div", {"data-testid" : "tweet"}).find('div', {"lang" : "en"}).find('span').text

    factsURL = 'https://space-facts.com/mars/'
    tables = pd.read_html(factsURL)[0]
    tables.set_index(0, inplace=True)
    marsFacts = tables.to_html(header=False)

    hemisphereURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphereBaseURL = 'https://astrogeology.usgs.gov'
    browser.visit(hemisphereURL)
    time.sleep(2)
    soupHemi = bs(browser.html, 'html.parser')

    hemisphere_image_urls = []
    hemis = soupHemi.find_all('div', class_="item")

    for h in hemis:
        tempURL = hemisphereBaseURL + h.find('a')['href']
        browser.visit(tempURL)
        time.sleep(2)
        soupSearch = bs(browser.html, 'html.parser')
        downloads = soupSearch.find("div", class_="downloads").find_all("li")
        for dl in downloads:
            if (dl.find('a').text == "Sample"):
                temp_dict = {"title": soupSearch.find("h2", class_="title").text, 
                            "img_url" : dl.find('a')['href']}
                hemisphere_image_urls.append(temp_dict)
    
    returnDictionary = {
        "news_title" : news_title,
        "news_p" : news_p,
        "news_date" : news_date,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "mars_facts_table" : marsFacts,
        "hemisphere_image_urls" : hemisphere_image_urls
    }
    browser.quit()
    return returnDictionary

    