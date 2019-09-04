from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


def scrape():

    # 1_news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find('div',class_= 'content_title').text.strip()
    news_p = soup.find('div', class_="image_and_description_container").find('div', class_="rollover_description_inner").text.strip()
    
    # 2_feature image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = soup.find('img', class_="main_image")['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+featured_image_url 




    # 3_Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    mars_weather = soup.find('div',class_= 'content').find('div',class_= 'js-tweet-text-container').text.strip()

    #4_Mars Diameter
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Description', 'Value']
    mars_html_table = df.to_html(index = False)
    mars_html_table.replace('\n', '')

    #5_hemisphere_image
    hemisphere_image_urls = []

    url1 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    url2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    url3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    url4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    urls = [url1,url2,url3,url4]

    for i in range(4):

        url = urls[i]
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
    
        img_url = soup.find('div',class_= 'container').\
                       find('div',class_ = 'wide-image-wrapper').\
                       find_all('img')[1]['src']
    
        title = soup.find('div',class_= 'container').\
                     find('div',class_ = 'content').\
                     find('section').\
                     find('h2').text.strip()
    
        img_url = 'https://astrogeology.usgs.gov' + img_url
    
        hemisphere_image_urls.append({'title':title,'img_url':img_url})

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather":mars_weather,
        "mars_html_table":mars_html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
   
    # Return results
    return mars_data
