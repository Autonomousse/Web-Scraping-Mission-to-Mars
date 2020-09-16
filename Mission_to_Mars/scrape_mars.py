# Import dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # Set the path for chromedriver (include chromdriver.exe in the same folder)
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    # Intialize the browser
    browser = init_browser()


    ''' -------------- '''
    ''' NASA MARS NEWS '''
    ''' -------------- '''

    # Set the URL for the browser to open and visit the website
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)

    # Wait 5 seconds so the browser can fully load, otherwise an empty HTML object may be created
    time.sleep(5)

    # Create an HTML object from the web page
    news_html = browser.html

    # Use BeautifulSoup to parse through the HTML object and store it in a variable
    news_soup = BeautifulSoup(news_html, 'html.parser')

    # Scrape and collect the latest News Article Title, also get the link for the article
    article_title = news_soup.find('ul', class_='item_list').find('div', class_='content_title').find('a').text
    title_link = news_soup.find('ul', class_='item_list').find('div', class_='content_title').find('a')['href']
    article_link = news_url + title_link

    # Scrape and collect the News Article Teaser, right below the News Article Title
    teaser = news_soup.find('ul', class_='item_list').find('div', class_='article_teaser_body').text


    ''' -------------------------------------- '''
    ''' JPL Mars Space Images - Featured Image '''
    ''' -------------------------------------- '''

    # Set the URL for the browser to open and visit the website
    # Save the URL for the home page as we need it to append the route of the featured image later
    home_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Wait 5 seconds so the browser can fully load, otherwise an empty HTML object may be created
    # time.sleep(5)

    # Create an HTML object from the web page
    image_html = browser.html

    # Use BeautifulSoup to parse through the HTML object and store it in a variable
    image_soup = BeautifulSoup(image_html, 'html.parser')

    # Scrape and collect the URL for the full sized Featured Image
    featured = image_soup.find('section', class_='primary_media_feature').find('div', class_='carousel_items').find('article')['style']

    # Split the inline CSS Style attribute object returned to capture the route to the full sized image
    featured_image = featured.split("'")[1]

    # Append the route to the home URL to get the full link
    featured_image_url = home_url + featured_image


    ''' ---------- '''
    ''' MARS FACTS '''
    ''' ---------- '''

    # Set the URL for pandas to read into a table
    facts_url = 'https://space-facts.com/mars/'

    # Visit the page to grab the name of the table so we can insert it as a header
    browser.visit(facts_url)

    # Wait 5 seconds so the browser can fully load, otherwise an empty HTML object may be created
    # time.sleep(5)

    table_html = browser.html
    table_soup = BeautifulSoup(table_html, 'html.parser')
    table_name = table_soup.find('section', class_='widget-area').find('div', class_='widget-header').find('h3').text

    # Read the tables into pandas
    tables = pd.read_html(facts_url)

    # Display the table with facts about Mars
    facts_table = tables[0]

    # Rename the columns
    facts_table.columns = [table_name, '']

    # Convert the data to a HTML table string and remove the index
    html_facts_table = facts_table.to_html(index=False)
    html_facts_table = html_facts_table

    ''' ---------------- '''
    ''' MARS HEMISPHERES '''
    ''' ---------------- '''

    # Set the URL for the image path, visit the page, create an HTML object, pass it to the parser
    base_url = 'https://astrogeology.usgs.gov'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    # Find the number of H3 tags because those are the title tags for each hemisphere
    title_location = hemisphere_soup.find('div', class_='collapsible results')
    titles = title_location.find_all('h3')

    # Create a list to store the dictionaries from the for loop
    hemisphere_list = []

    for title in titles:

        # New dictionary for each entry
        hemisphere_dict = {}

        # Get the title from the h3 tag and strip off the last word and any leading or trailing whitespaces
        name = title.text
        hemisphere_name = name.strip('Enhanced').strip()
        hemisphere_dict['title'] = hemisphere_name

        # Click the link in the anchor tag that the h3 tag is encapsulated in to find the link to the full image
        browser.click_link_by_partial_text(name)

        # On the page with the full image, create an HTML object and find the image URL
        img_link_html = browser.html
        img_link_soup = BeautifulSoup(img_link_html, 'html.parser')
        img_link_route = img_link_soup.find('img', class_='wide-image')['src']
        img_link = base_url + img_link_route

        # Add the URL to the dictionary
        hemisphere_dict['img_url'] = img_link

        # Append the dictionary to the list
        hemisphere_list.append(hemisphere_dict)

        # Go back to the previous page to get the rest of the image links and titles
        browser.back()

    
    ''' -------------------- '''
    ''' Dictionary to return '''
    ''' -------------------- '''

    mars_data = {
        "latest_article_title": article_title,
        "latest_article_link": article_link,
        "latest_article_teaser": teaser,
        "featured_image": featured_image_url,
        "facts_table": html_facts_table,
        "hemisphere_images": hemisphere_list
    }

    # Close the browser
    browser.quit()

    # Return the dictionary with the scraped data
    return mars_data