import csv
from bs4 import BeautifulSoup
import requests

import pandas as pd

import json

csv_url="https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM/edit?usp=sharing"
csv_path ='/'.join(csv_url.split('/')[:-1])+"/export?format=csv"
#print(path)

df=pd.read_csv(csv_path)
#print(df)
#print(len(df))

page_details={}

list_of_details=[]

for i in range(len(df)):
    data=df.loc[i]
    asin=data['Asin']
    country=data['country']
    #print(asin,"-----",country)
    
    page_url=f"https://www.amazon.{country}/dp/{asin}"
    #print(page_url)
    source=requests.get(page_url)
    #print(source.status_code)
    
    #if source.status_code==404:
        #print(f"The {page_url} not available")
        
        
    if source.status_code>=200 and source.status_code<300:
        
        #print('The Page URL is :',page_url)
        
        soup=BeautifulSoup(source.text,'lxml')
        #print(soup.prettify())
        title=soup.find('span',id="productTitle").text
        #print("Product Title is :",title)
        
        img_url=soup.find('div',id="dp")
        img_url=soup.find('div',id="dp-container")
        img_url=soup.find('div',id="main-image-container")
        img_url=soup.find('img')['src']
        #print("Product Image URL is :",img_url)
        
        if soup.find('span',id="price")==None:
            prod_price=soup.find('span',id="price")
            #print('Product price is :',prod_price)
        else:
            prod_price=soup.find('span',id="price").text
            #print('Product price is :',prod_price)
            
        prod_details=soup.find('div',id="detailBullets_feature_div")
        prod_details=prod_details.find('div',id="detailBullets_feature_div")
        prod_details=prod_details.find('ul').find_all('li')
        
        #detailBulletsWrapper_feature_div
        
        
        pdetails=''
        for li in prod_details:
           
            d1=li.text.split('\n')
            
            pdetails=pdetails+f"{d1[0]} : {d1[-1].strip()}\n"
        
        #print('Product details is :',pdetails)
    
        page_details["Product Title"]=title
        page_details["Product Image URL"]=img_url
        page_details["Product Price"]=prod_price
        page_details["Product Details"]=pdetails
        
        #print('All details of product :',page_details)
        
        list_of_details.append(page_details)
        
with open("json_file.json",'a+') as jf:
    json.dumps(list_of_details, jf)

