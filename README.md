# Mission-to-Mars
## Overview
Create a website that gathers new articles and images about and from Mars, as well as data and pictures about the neighboring planet.
## Details
This was a project built in 3 parts: Gather necessary resources, build python program and Flask server, and finally clean HTML with bootstrap
#### Gather Necessary Resources
The main challenge here was making sure the featured image and news articles were getting properly updated, as well as gathering the hemisphere photos. For the news articles and featured image, we could make a short cut in the code because only the top article needed to be gathered. The hemispheres pictures don't need updating, but it did need a for loop to scrape through the site:
```python
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
```
Honestly, I could've made this cleaner by having the hemisphere title be scraped from the image page, instead of scraping two different pages. the `[x+3]` to get the full image link was needed as there were three previous pictures in the site that all had the same tag.
#### Build Python and Flask server
This was fairly straightforward given the power of Mongo to store the resources we scraped and Flask to build a webpage. This step is where app.py and the `scrape_all()` function do their work
#### Clean HTML with Bootstrap
The final step is building the website. Important steps were to make the webpage responsive to all screen sizes, as well as changing some of the default elements to something more you're liking. The changes I made were to make the hemisphere photos much smaller on extra-small screens to fit easier on the page, as well as making those same photos circles, changing the button to be bigger and green, and finally rounding the edges of the featured image picture.
## Review and Possible Updates
There's obviously a lot more powerful customizations on Bootstrap that I barely scratched the surface of. Making the page match the theme of Mars or Space exploration would definitely catch more people's eyes. A functionality update would be to add a last-modified element. The code is already written in, so all it needs is a home in the HTML.
