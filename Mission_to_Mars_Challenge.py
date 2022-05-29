#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time


# # Deliverable 1

# In[16]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Featured News Article

# In[17]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)


# In[18]:


# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[19]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')


# In[20]:


slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# In[21]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[22]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Image

# In[23]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[24]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[26]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[27]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts Table

# In[28]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[29]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[30]:


df.to_html()


# ### Hemisphere Images

# In[31]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[32]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[33]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(4):
    # scrape name of hemisphere
    html = browser.html
    mars_soup = soup(html, 'html.parser')

    # Get the title of the images
    hemi = mars_soup.find_all('h3')[x].get_text()
    print(hemi)

    
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
    print(img_url)

    browser.back()
    
    # make dictionary of titles and image urls
    hemispheres = {}
    hemispheres['img_url'] = img_url
    hemispheres['title'] = hemi
    hemisphere_image_urls.append(hemispheres)
    


# In[34]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[35]:


# 5. Quit the browser
browser.quit()


# In[ ]:




