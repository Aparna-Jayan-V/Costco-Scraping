#!/usr/bin/env python
# coding: utf-8

# In[44]:


import time
import random
import requests
import regex as re
import pandas as pd
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
pd.options.mode.chained_assignment = None 
from urllib.request import urlopen as ureq
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 

driver=webdriver.Firefox()

url='https://www.costco.com/electronics.html'

driver.get(url) 

driver.find_element(By.XPATH,'//*[@id="navpills-sizing"]/a[3]').click()

html_content=driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

category_links=[]
for i in soup.find_all('div', attrs={"class": "col-xs-12 col-lg-6 col-xl-3"}):
    for b in i.find_all('a'):
         category_links.append(b['href'])
category_links = category_links[:4]

product_list=[]
driver.get(category_links[0])
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
for product_section in soup.find_all('div', {'automation-id': 'productList'}):
    for product_link in product_section.find_all('a'):
        product_list.append(product_link['href'])
product_list = set(product_list[:-1]) 

data_dic = {'Product_url': [],'Item_id':[],'Brand': [], 'Product_name': [],'Colour':[],'Model': [],'Price' :[],
            'Connection_type': [], 'Delivery_type': [],'Type_of_headphones':[], 'Description':[],'Overall_review':[],'Number_of_reviews':[]} 

df=pd.DataFrame(data_dic)

df['Product_url']=df_product_links['product_links']

df.drop(df.index[2], inplace=True)

for each_product in range(len(df)):
    product_url = df['Product_url'].iloc[each_product]
    driver.get(product_url)
    html_content=driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    dom = et.HTML(str(soup)) 
    try:                                                                                           
        product_name=(dom.xpath('//*[@id="product-page"]/div[3]/div[1]/div[2]/div[1]/span/text()'))   
        df['Product_name'].iloc[each_product] = product_name                                                     
        df[['Product_name']] = df[['Product_name']].astype(str)
        df['Product_name']=df['Product_name'].apply(lambda x: x.strip("]'["))
    except:                                                                                       
        product_name = "Product name is not available"
        df['Product_name'].iloc[each_product] = product_name 


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                           
            model=(dom.xpath('//*[@id="model-no"]/span/text()'))   
            df['Model'].iloc[each_product] = model                                                     
            df[['Model']] = df[['Model']].astype(str)
            df['Model']=df['Model'].apply(lambda x: x.strip("]'["))
        except:
            model = "model is not available"
            df['Model'].iloc[each_product] = model 

        
for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                           
            brand=(dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[2]/div[2]/text()'))   
            df['Brand'].iloc[each_product] = brand                                                     
            df[['Brand']] = df[['Brand']].astype(str) 
            df['Brand']=df['Brand'].apply(lambda x: x.strip("]'["))
        except:                                                                                        
            brand = "brand is not available"
            df['Brand'].iloc[each_product] = brand


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                           
            connection_type=(dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[4]/div[2]/text()'))   
            df['Connection_type'].iloc[each_product] = connection_type                                                    
            df[['Connection_type']] = df[['Connection_type']].astype(str) 
            df['Connection_type']=df['Connection_type'].apply(lambda x: x.strip("]'["))
        except:                                                                                       
            connection_type = "connection type is not available"
            df['Connection_type'].iloc[each_product] = connection_type 


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                         
            price=(dom.xpath('//*[@id="pull-right-price"]/span[1]/text()'))  
            df['Price'].iloc[each_product] = price 
            df[['Price']] = df[['Price']].astype(str)
            df['Price']=df['Price'].apply(lambda x: x.strip("]'["))
        except:                                                                                        
            price = "price is not available"
            df['Price'].iloc[each_product] = price


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                           
            colour=(dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[2]/div[2]/text()'))  
            df['Colour'].iloc[each_product] = colour                                                     
            df[['Colour']] = df[['Colour']].astype(str)
            df['Colour']=df['Colour'].apply(lambda x: x.strip("]'["))
        except:                                                                                       
            colour = "colour is not available"
            df['Colour'].iloc[each_product] = colour


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                         
            item_id=(dom.xpath('//*[@id="item-no"]/span/text()'))  
            df['Item_id'].iloc[each_product] = item_id                                                    
            df[['Item_id']] = df[['Item_id']].astype(str)
            df['Item_id']=df['Item_id'].apply(lambda x: x.strip("]'["))
        except:                                                                                    
            item_id = "Item Id is not available"
            df['Item_id'].iloc[each_product] = item_id   


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                        
            type_of_headphones=(dom.xpath('//*[@id="nav-pdp-tab-header-4"]/div/div[1]/div/div[4]/div[2]/text()'))  
            df['Type_of_headphones'].iloc[each_product] = type_of_headphones                                                    
            df[['Type_of_headphones']] = df[['Type_of_headphones']].astype(str)
            df['Type_of_headphones']=df['Type_of_headphones'].apply(lambda x: x.strip("]'["))
        except:                                                                                  
            type_of_headphones = "no of reviews is not available"
            df['Type_of_headphones'].iloc[each_product] = type_of_headphones


for each_product in range(len(df)):
        product_url = df['Product_url'].iloc[each_product]
        driver.get(product_url)
        html_content=driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        dom = et.HTML(str(soup)) 
        try:                                                                                           
            description=(dom.xpath('//*[@id="product-page"]/div[3]/div[1]/div[2]/div[2]/text()'))  
            df['Description'].iloc[each_product] = description                                                     
            df[['Description']] = df[['Description']].astype(str) 
            df['Description']=df['Description'].apply(lambda x: x.strip("n\]'[ "))
        except:                                                                                      
            description = "description is not available"
            df['Description'].iloc[each_product] = description

