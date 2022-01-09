# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:44:21 2020

@author: Jerry
"""


# =============================================================================
# import 
# =============================================================================
import requests
from bs4 import BeautifulSoup,element
import pandas as pd
from re import search
import time
# =============================================================================
#   find the homepage of each city
# =============================================================================
HOME_URL = "https://www.foodpanda.com.tw"

def get_all_city_link():
    """取得所有城市的連結"""
    response = requests.get(HOME_URL)
    soup = BeautifulSoup(response.text)
    all_a = soup.find_all("a",class_="city-tile")
    all_link = [HOME_URL+a.get("href") for a in all_a ]
    
    return all_link

# =============================================================================
#   foodpanda-find all vendor
# =============================================================================
#Take Taipei as an example
def get_restaurant_info(url):  
    response = requests.get(url)
    soup = BeautifulSoup(response.text)   
    all_li = soup.find("ul",class_="vendor-list").children

    all_restaurant = []
    for v in all_li:
        if isinstance(v,element.Tag):
            all_restaurant.append(v)
            
    restaurants_info = []
    for restaurant in all_restaurant:
        v = {}
        #restaurant name
        v["name"] = restaurant.find("span",class_="name fn").text
        #restaurant link
        v["link"] = HOME_URL+restaurant.find("a").get('href')
        #restaurant photo
        pic_url = restaurant.find("div").get("data-src")
        v["pic_url"] = pic_url[:pic_url.find("?")]
       
        #restaurant star
        try:
            v["rating"] = restaurant.find("span",class_="rating").find("strong").text
            v["count"] = restaurant.find("span",class_="count").text.strip()
        except:
            v["rating"] = "NA"
            v["count"] = 0
        
        try:
            v["tag"] = restaurant.find("span",class_="multi-tag").text
        except:
            v["tag"] = "NA"
            
        restaurants_info.append(v)
    return pd.DataFrame(restaurants_info)
    

cities_link = get_all_city_link()
restaurants_info =  get_restaurant_info(cities_link[0]) 
restaurants_info["id"] = [i for i in range(1,len(restaurants_info)+1)]
# =============================================================================
#  foodpanda - find menu
# =============================================================================
def get_restaurant_menu(url):
    """return the menu of the restaurant"""
    menu = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    dishes_section = soup.find_all("div",class_="dish-category-section")
    for section in dishes_section:
        #restaurant menu-category
        category = section.find("h2",class_="dish-category-title").text
        dishes = section.find("ul",class_="dish-list").find_all("li")
        for dish in dishes:
            m = {}
            m["category"] = category
            #dish name
            m["name"] = dish.find("h3").find("span").text
            #dish description
            try:
                m["description"] = dish.find("p").text.strip()
            except:
                m["description"] = "NA"
            #dis price
            m["price"] = dish.find("span",class_="price p-price").text.strip()
            menu.append(m)
    return menu

res_url = restaurants_info.link[0]
menu = get_restaurant_menu(res_url)

#get all restaurant menu
sleep = 0.5
menu_list = []
for id_, link in zip(restaurants_info["id"].values,
                     restaurants_info["link"].values):
    print(link)
    menu = get_restaurant_menu(link)
    #add restaurant ID
    for i in range(len(menu)):
        menu[i]["id"] = id_
    menu_list.extend(menu)
    time.sleep(sleep)
     
restaurants_menu = pd.DataFrame(menu_list)

# =============================================================================
# clean data
# =============================================================================
def extract_number(str_num):
    pattern = "[\d,]+.[\d]{2}"
    return search(pattern, str_num).group(0)

restaurants_menu.price = restaurants_menu.price.apply(extract_number)
restaurants_menu.price = restaurants_menu.price.apply(lambda price:price.replace(",",""))

#remove unnessary category
unwanted_category = ["注意事項","營養標示"]
unwanted_index = []
for category in unwanted_category:
    index = restaurants_menu[restaurants_menu.category.str.contains(category)].index
    if len(index)>1:
        unwanted_index.extend(index)
restaurants_menu.drop(unwanted_index, axis=0,inplace=True)

restaurants_info.count = restaurants_info["count"].astype(int)
restaurants_menu.price = restaurants_menu["price"].astype(float)
# =============================================================================
#  save data
# =============================================================================
path = "food-panda.xlsx"
with pd.ExcelWriter(path) as writer:
    restaurants_info.to_excel(writer,sheet_name="店家評分",index=False)
    restaurants_menu.to_excel(writer,sheet_name="店家菜單",index=False)
    