from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import pymongo

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_="content_title")[0].text.strip()
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text.strip()
    

    #JPL Mars Space Images - Featured Image
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html2 = browser.html
    image_soup = BeautifulSoup(html2, "html.parser")
    relative_image_path = image_soup.find('img', class_='fancybox-image')["src"]
    featured_img_url = img_url + relative_image_path

    #Mars Facts
    facts_url = 'https://galaxyfacts-mars.com'
    facts_table = pd.read_html(facts_url)[1]
    facts_table.columns = ["Description", "Mars"]
    facts_table = facts_table.to_html(index=False)

    #Mars Hemispheres
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    hemisphere_image_urls = []
    for hemi in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemi].click()
    
        html3 = browser.html
        hemi_soup = BeautifulSoup(html3, "html.parser")

        title = hemi_soup.find('h2', class_='title').text.strip()
        img_url = hemi_soup.find('li').a.get('href')
    
        hemis = {}
        hemis['title'] = title
        hemis['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemisphere_image_urls.append(hemis)

        browser.back()

    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_img_url': featured_img_url,
        'facts_table': facts_table,
        'hemispheres': hemisphere_image_urls
        }
    return mars_data