# Import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    
    # set up path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    fact_table, hemisphere_image_urls = mars_facts(browser)

    # run all scraping functions and store results in a dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': fact_table,
        'last_modified': dt.datetime.now(),
        'hemisphere_image_urls': hemisphere_image_urls
    }
    
    # stop webdriver and return data
    browser.quit()
    return data

# making news scraping function
def mars_news(browser):
    
    # visit nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # add try/except before scraping for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # scrape article title
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # scrape summary text for article
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None    
    
    return news_title, news_p


# Featured Images function
def featured_image(browser):

    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # try/except to catch errors
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    
    # use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# mars facts function
def mars_facts(browser):

    try:
        # scrape table from mars facts
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    fact_table = df.to_html(classes='table table-striped')

    # grab hemisphere photos
    # visit url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for x in range(4):
        # scrape name of hemisphere
        html = browser.html
        mars_soup = soup(html, 'html.parser')

        # Get the title of the images
        hemi = mars_soup.find_all('h3')[x].get_text()
            
        # navigate to img page
        full_img_link = browser.find_by_tag('img')[x+3]
        full_img_link.click()
    
        # scrape relative url
        html = browser.html
        mars_img_soup = soup(html, 'html.parser')
        img_elem = mars_img_soup.select_one('ul')
    
        img_url_rel = img_elem.find('a', target='_blank').get('href')
        
        # get absolute url
        img_url = f'https://marshemispheres.com/{img_url_rel}'
        
        browser.back()
    
        # make dictionary of titles and image urls
        hemispheres = {}
        hemispheres['img_url'] = img_url
        hemispheres['title'] = hemi
        hemisphere_image_urls.append(hemispheres)

    return fact_table, hemisphere_image_urls

if __name__ == '__main__':
    # if running as code, print scraped data
    print(scrape_all())
