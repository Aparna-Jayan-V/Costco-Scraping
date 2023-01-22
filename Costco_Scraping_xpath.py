# Importing necessary libraries
import pandas as pd
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# Function to extract content from page
def extract_content(url):
    driver.get(url)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'lxml')
    dom = et.HTML(str(soup))
    return dom

# Function to click the electronic cateory 'Audio/Video' and extract content from the page
def click_url(driver):
    driver.find_element(By.XPATH, '//*[@id="navpills-sizing"]/a[3]').click()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'lxml')
    dom = et.HTML(str(soup))
    return dom

# Function to get the urls of sub categories under Audio/Video
def category_links(dom):
    category_link = []
    links = dom.xpath('//*[@class="categoryclist_v2"]//a/@href')
    for link in links:
        category_link.append(link)
    return category_link

# Function to extract urls of products and adding it to the dataframe
def product_links(dom):
    product_urls = []
    for link in category_links(dom):
        content=extract_content(link)
        for product_link in content.xpath('//*[@automation-id="productList"]//a[substring(@href, string-length(@href) - 4) = ".html"]/@href'):
            product_urls.append(product_link)
    product_urls = list(set(product_urls))
    data['product_url'] = product_urls
    return data

# Function to extract product name
def get_product_name(dom):
    try:
        name = dom.xpath('//*[@class="product-title"]/text()')
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
        product_model = dom.xpath('//*[@id="model-no"]/span/text()')
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
        product_brand = dom.xpath('//*[@itemprop="brand"]/text()')
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
        product_connection = dom.xpath('//div[text()="Connection Type"]/following::div[1]/text()')[0]
        data['connection_type'].iloc[product] = product_connection
    except:
        product_connection = "Connection type is not available"
        data['connection_type'].iloc[product] = product_connection
    return product_connection

# Function to extract price of the product
def get_price(dom):
    try:
        product_price = dom.xpath('//span[@automation-id="productPriceOutput"]/text()')
        data['price'].iloc[product] = product_price
        data[['price']] = data[['price']].astype(str)
        data['price'] = data['price'].apply(lambda x: x.strip("]'[-."))
        if data['price'].iloc[product] == '':
            product_price = "Price is not available"
            data['price'].iloc[product] = product_price
    except:
        pass
    return product_price  

# Function to extract colour of the product
def get_colour(dom):
    try:
        product_colour = dom.xpath('//*[text()="Color"]/following::div[1]/text()')[0]
        data['colour'].iloc[product] = product_colour
    except:
        product_colour = "Colour is not available"
        data['colour'].iloc[product] = product_colour
    return product_colour

# Function to extract item id of the product
def get_item_id(dom):
    try:
        product_id = dom.xpath('//*[@id="item-no"]/span/text()')
        data['item_id'].iloc[product] = product_id
        data[['item_id']] = data[['item_id']].astype(str)
        data['item_id'] = data['item_id'].apply(lambda x: x.strip("]'["))
        if data['item_id'].iloc[product] == '':
            product_id = "Item Id is not available"
            data['item_id'].iloc[product] = product_id
    except:
        pass
    return product_id 

# Function to extract description of the product
def get_description(dom):
    try:
        product_description = dom.xpath('//*[@automation-id="productDetailsOutput"]/text()')
        data['description'].iloc[product] = product_description
        data[['description']] = data[['description']].astype(str)
        data['description'] = data['description'].apply(lambda x: x.strip("n\]'[ "))
        if data['description'].iloc[product] == '':
            product_description = "Description is not available"
            data['description'].iloc[product] = product_description
    except:
        pass
    return product_description

# Function to extract category type of the product
def get_category(dom):
    try:
        product_category = dom.xpath('(//*[@itemprop="name"]/text())[10]')
        data['category'].iloc[product] = product_category
        data[['category']] = data[['category']].astype(str)
        data['category'] = data['category'].apply(lambda x: x.strip("]'["))
        if data['category'].iloc[product] == '':
            product_category = "Category is not available"
            data['category'].iloc[product] = product_category
    except:
        pass
    return product_category

# Costco electroic categories link
url = 'https://www.costco.com/electronics.html'

driver.get(url)

url_content=click_url(driver)

# Creating a dictionary with required columns
data_dic = {'product_url': [], 'item_id': [], 'brand': [], 'product_name': [], 'category': [], 'model': [], 'price': [], 'colour': [], 'connection_type': [], 'description': []}

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
    
    #category type 
    get_category(product_content)
    
    #description
    get_description(product_content)
    
    #product name
    get_product_name(product_content)
    
        
data.to_csv('costco_data.csv')


