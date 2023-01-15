# Importing necessary libraries
import pandas as pd
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

# Function to extract content from page
def extract_content(url):
    driver.get(url)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup

# Function to click the electronic cateory 'Audio/Video' and extract content from the page
def click_url(driver):
    driver.find_element(By.XPATH, '//*[@id="navpills-sizing"]/a[3]').click()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Function to get the urls of sub categories under Audio/Video
def category_links(soup):
    category_link = []
    for div in soup.find_all('div', attrs={"class": "col-xs-12 col-lg-6 col-xl-3"}):
        for links in div.find_all('a'):
            category_link.append(links['href'])
    category_link = category_link[:4]
    return category_link

# Function to extract urls of products and adding it to the dataframe
def product_links(soup):
    product_urls = []
    for links in category_links(soup):
        content=extract_content(links)
        for product_section in content.find_all('div', {'automation-id': 'productList'}):
            for product_link in product_section.find_all('a'):
                product_urls.append(product_link['href'])
    product_urls = list(set(product_urls))
    valid_urls = [url for url in product_urls if url.endswith('.html')]
    data['product_url'] = valid_urls
    return data

# Function to extract product name
def get_product_name(soup):
    try:
        name = soup.find('h1',{'automation-id':'productName'}).text
        data['product_name'].iloc[product] = name
    except:
        name = "Product name is not available"
        data['product_name'].iloc[product] = name
    return name

# Function to extract model of the product
def get_model(soup):
    try:
        keys=soup.find_all('div',{'class':'spec-name col-xs-6 col-md-5 col-lg-4'})
        values=soup.find_all('div',{'class':'col-xs-6 col-md-7 col-lg-8'})    
        for item in range(len(keys)):
            if keys[item].text=='Model':
                product_model=values[item].text
        data['model'].iloc[product] = product_model
    except:
        product_model = "Model is not available"
        data['model'].iloc[product] = product_model
    return product_model 

# Function to extract brand of the product
def get_brand(soup):
    try:
        product_brand = soup.find('div',{'itemprop':'brand'}).text
        data['brand'].iloc[product] = product_brand
    except:
        product_brand = "Brand is not available"
        data['brand'].iloc[product] = product_brand
    return product_brand

# Function to extract connection type of the product
def get_connection_type(soup):
    try:
        keys=soup.find_all('div',{'class':'spec-name col-xs-6 col-md-5 col-lg-4'})
        values=soup.find_all('div',{'class':'col-xs-6 col-md-7 col-lg-8'})
        for item in range(len(keys)):
            if keys[item].text=='Connection Type':
                product_connection=values[item].text
        data['connection_type'].iloc[product] = product_connection
    except:
        product_connection = "Connection type is not available"
        data['connection_type'].iloc[product] = product_connection
    return product_connection

# Function to extract price of the product
def get_price(soup):
    try:
        product_price = soup.find('span',{'automation-id':'productPriceOutput'}).text
        data['price'].iloc[product] = product_price
        data[['price']] = data[['price']].astype(str)
        data['price'] = data['price'].apply(lambda x: x.strip("-."))
        if data['price'].iloc[product] == '':
            product_price = "Price is not available"
            data['price'].iloc[product] = product_price
    except:
        pass
    return product_price  

# Function to extract colour of the product
def get_colour(soup):
    try:
        keys=soup.find_all('div',{'class':'spec-name col-xs-6 col-md-5 col-lg-4'})
        values=soup.find_all('div',{'class':'col-xs-6 col-md-7 col-lg-8'})
        for item in range(len(keys)):
            if keys[item].text=='Color':
                product_colour=values[item].text
        data['colour'].iloc[product] = product_colour
    except:
        product_colour = "Colour is not available"
        data['colour'].iloc[product] = product_colour
    return product_colour

# Function to extract item id of the product
def get_item_id(soup):
    try:
        product_id = soup.find('input',{'name':'addedItem'})['value']   
        data['item_id'].iloc[product] = product_id
    except:
        product_id = "Item Id is not available"
        data['item_id'].iloc[product] = product_id
    return product_id

# Function to extract type of the product
def get_product_type(soup):  
    try:
        keys=soup.find_all('div',{'class':'spec-name col-xs-6 col-md-5 col-lg-4'})
        values=soup.find_all('div',{'class':'col-xs-6 col-md-7 col-lg-8'})    
        for item in range(len(keys)):
            if keys[item].text=='Type of Headphones':
                product_types=values[item].text
        data['product_type'].iloc[product] = product_types
    except:
        product_types = "Product type is not available"
        data['product_type'].iloc[product] = product_types
    return product_types  

# Function to extract description of the product
def get_description(soup):
    try:
        product_description = soup.find('div',{'itemprop':'description'}).text
        data['description'].iloc[product] = product_description
        data['description'] = data['description'].astype(str)
        data['description'] = data['description'].apply(lambda x: x.strip('\n '))
        if data['description'].iloc[product] == '':
            product_description = "Description is not available"
            data['description'].iloc[product] = product_description
    except:
        pass
    return product_description  

# Costco electroic categories link
url = 'https://www.costco.com/electronics.html'

driver.get(url)

driver.implicitly_wait(5)

url_content=click_url(driver)

# Creating a dictionary with required columns
data_dic = {'product_url': [], 'item_id': [], 'brand': [], 'product_name': [], 'colour': [], 'model': [], 'price': [],
            'connection_type': [], 'product_type': [], 'description': []}

# Creating a dataframe
data = pd.DataFrame(data_dic)

# Scraping product links and adding it to the dataframe column 'product_url'
product_links(url_content)

# Scraping all the required features of each product
for product in range(len(data)):
    product_url = data['product_url'].iloc[product]
    product_content = extract_content(product_url)

    #model
    get_model(product_content)
    
    #brand
    get_brand(product_content)
    
    #connection type
    get_connection_type(product_content)
    
    #price
    get_price(product_content)
    
    #colour
    get_colour(product_content)
    
    #item id
    get_item_id(product_content)
    
    #type of headphones
    get_product_type(product_content)
    
    #description
    get_description(product_content)
    
    #product name
    get_product_name(product_content)
        
data.to_csv('costco_Audio&Video.csv')

