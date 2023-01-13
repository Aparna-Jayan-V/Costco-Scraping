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
    dom = et.HTML(str(soup))
    return soup,dom

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
    content = extract_content(category_links(soup)[0])
    for product_section in content.find_all('div', {'automation-id': 'productList'}):
        for product_link in product_section.find_all('a'):
            product_urls.append(product_link['href'])
    product_urls = list(set(product_urls[:-1]))
    data['product_url'] = product_urls
    index = data[ data['product_url'] == 'https://www.costco.com/headphones.html?keyword=applecare+available'].index
    data.drop(index,inplace=True)
    return data

# Function to extract product name
def get_product_name(dom):
    try:
        name = (dom.xpath('//*[@id="product-page"]/div[3]/div[1]/div[2]/div[1]/span/text()'))
        data['product_name'].iloc[product] = name
        data[['product_name']] = data[['product_name']].astype(str)
        data['product_name'] = data['product_name'].apply(lambda x: x.strip("]'["))
        if data['product_name'].iloc[product] == '':
            name = "Product name is not available"
            data['product_name'].iloc[product] = name
    except:
        pass
    return name

# Function to extract model of the product
def get_model(dom):
    try:
        product_model = (dom.xpath('//*[@id="model-no"]/span/text()'))
        data['model'].iloc[product] = product_model
        data[['model']] = data[['model']].astype(str)
        data['model'] = data['model'].apply(lambda x: x.strip("]'["))
        if data['model'].iloc[product] == '':
            product_model = "Model is not available"
            data['model'].iloc[product] = product_model
    except:
        pass
    return product_model

# Function to extract brand of the product
def get_brand(dom):
    try:
        product_brand = (dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[2]/div[2]/text()'))
        data['brand'].iloc[product] = product_brand
        data[['brand']] = data[['brand']].astype(str)
        data['brand'] = data['brand'].apply(lambda x: x.strip("]'["))
        if data['brand'].iloc[product] == '':
            product_brand = "Brand is not available"
            data['brand'].iloc[product] = product_brand
    except:
        pass
    return product_brand

# Function to extract connection type of the product
def get_connection_type(dom):
    try:
        product_connection = (dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[4]/div[2]/text()'))
        data['connection_type'].iloc[product] = product_connection
        data[['connection_type']] = data[['connection_type']].astype(str)
        data['connection_type'] = data['connection_type'].apply(lambda x: x.strip("]'["))
        if data['connection_type'].iloc[product] == '':
            product_connection = "Connection type is not available"
            data['connection_type'].iloc[product] = product_connection
    except:
        pass
    return product_connection

# Function to extract price of the product
def get_price(dom):
    try:
        product_price = (dom.xpath('//*[@id="pull-right-price"]/span[1]/text()'))
        data['price'].iloc[product] = product_price
        data[['price']] = data[['price']].astype(str)
        data['price'] = data['price'].apply(lambda x: x.strip("]'[-"))
        if data['price'].iloc[product] == '':
            product_price = "Price is not available"
            data['price'].iloc[product] = product_price
    except:
        pass
    return product_price

# Function to extract colour of the product
def get_colour(dom):
    try:
        product_colour = (dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[2]/div[2]/text()'))
        data['colour'].iloc[product] = product_colour
        data[['colour']] = data[['colour']].astype(str)
        data['colour'] = data['colour'].apply(lambda x: x.strip("]'["))
        if data['colour'].iloc[product] == '':
            product_colour = "Colour is not available"
            data['colour'].iloc[product] = product_colour
    except:
        pass
    return product_colour

# Function to extract item id of the product
def get_item_id(dom):
    try:
        product_id = (dom.xpath('//*[@id="item-no"]/span/text()'))
        data['item_id'].iloc[product] = product_id
        data[['item_id']] = data[['item_id']].astype(str)
        data['item_id'] = data['item_id'].apply(lambda x: x.strip("]'["))
        if data['item_id'].iloc[product] == '':
            product_id = "Item Id is not available"
            data['item_id'].iloc[product] = product_id
    except:
        pass
    return product_id

# Function to extract type of the product
def get_type_of_headphones(dom):
    try:
        product_type = (dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[4]/div[2]/text()'))
        data['type_of_headphones'].iloc[product] = product_type
        data[['type_of_headphones']] = data[['type_of_headphones']].astype(str)
        data['type_of_headphones'] = data['type_of_headphones'].apply(lambda x: x.strip("]'["))
        if data['type_of_headphones'].iloc[product] == '':
            product_type = "Type of headphone is not available"
            data['type_of_headphones'].iloc[product] = product_type
    except:
        pass
    return product_type

# Function to extract description of the product
def get_description(dom):
    try:
        product_description = (dom.xpath('//*[@id="product-page"]/div[3]/div[1]/div[2]/div[2]/text()'))
        data['description'].iloc[product] = product_description
        data[['description']] = data[['description']].astype(str)
        data['description'] = data['description'].apply(lambda x: x.strip("n\]'[ "))
        if data['description'].iloc[product] == '':
            product_description = "Description is not available"
            data['description'].iloc[product] = product_description
    except:
        pass
    return product_description

# Costco electroic categories link
url = 'https://www.costco.com/electronics.html'

driver.get(url)

url_soup=click_url(driver)

# Creating a dictionary with required columns
data_dic = {'product_url': [], 'item_id': [], 'brand': [], 'product_name': [], 'colour': [], 'model': [], 'price': [],
            'connection_type': [], 'type_of_headphones': [], 'description': []}

# Creating a dataframe
data = pd.DataFrame(data_dic)

# Scraping product links and adding it to the dataframe column 'product_url'
product_links(url_soup)

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
    get_type_of_headphones(product_content)
    
    #description
    get_description(product_content)
    
    #product name
    get_product_name(product_content)

#Saving the final dataframe as a csv file
data.to_csv('costco_headphones.csv')

