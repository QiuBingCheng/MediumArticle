# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 10:40:15 2020

@author: Jerry
"""

# =============================================================================
# import 
# =============================================================================
import requests
from bs4 import BeautifulSoup,element
import pandas as pd
from selenium import webdriver
import re
import time
import sys, json
import urllib

url = "https://www.ubereats.com/tw"
url = "https://www.ubereats.com/api/getFeedV1?localeCode=tw"


response = requests.get(url)
soup = BeautifulSoup(response.text)

soup.find_all("a")
# =============================================================================
#   
# =============================================================================
url = "https://www.ubereats.com/api/getFeedV1?localeCode=tw"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
params = {"cacheKey":"JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNSU4RiVCMCVFNSU4QyU5NyUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUptUXJpdkhLc1FqUVI0TUlLM2M0MWFqOCUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wMzI5Njk0JTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjU2NTQxNzclN0Q=/DELIVERY///0/0//JTVCJTVE///","feedSessionCount":{"announcementCount":0,"announcementLabel":""},"userQuery":"","date":"","startTime":0,"endTime":0,"carouselId":"","sortAndFilters":[],"marketingFeedType":"","billboardUuid":"","feedProvider":""}

data = urllib.parse.urlencode(params)
data = data.encode('ascii') # data should be bytes

headers = {'User-Agent': user_agent,
           'Connection': 'Keep-Alive',
           'Accept-Encoding': 'gzip, deflate',
           "cookie":"IDE=AHWqTUlq-9ImvjFT2zojJO2geKK1XjTcP1XGK4E9maflv898hp5VV6itR5ZetcNB"
           ,"x-uber-xps":"%7B%22eats_web_expand_search_by_default%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_payments_select_preload%22%3A%7B%22name%22%3A%22prefetch%22%7D%2C%22eats_web_local_chains%22%3A%7B%22name%22%3A%22enabled%22%7D%2C%22eats_pickup_mvp_rtapi%22%3A%7B%22name%22%3A%22pickup_enabled%22%7D%2C%22eats_web_xlb_pinned_items_2%22%3A%7B%22name%22%3A%22treatment%22%2C%22inclusionLoggingToken%22%3A%22eyJ0cmVhdG1lbnRHcm91cCI6eyJpZCI6MTIyMTE4NywibmFtZSI6InRyZWF0bWVudCIsInNlZ21lbnRVVUlEIjoiNTg5MTFjNWEtM2QyOC00ZWM5LTg3NjMtYTM5Y2RhNzMzMmFjIiwiZXhwZXJpbWVudElEIjo0NDMxOTgzLCJleHBlcmltZW50TmFtZSI6ImVhdHNfd2ViX3hsYl9waW5uZWRfaXRlbXNfMiIsImxvZ1RyZWF0bWVudHMiOjEsInNlZ21lbnRLZXkiOiJwdWJsaWNfcm9sbG91dCIsInV1aWQiOiJiNTEwZTA2Zi0zYmU5LTQwNDQtOGNjNi0yYzM1NGNlZjIxNzkiLCJidWNrZXRCeSI6IiR1c2VyIiwic2VnbWVudElEIjoxMjI5MjI1LCJtb3Jsb2dBY3RpdmF0ZWQiOmZhbHNlLCJleHBlcmltZW50VmVyc2lvbiI6MH0sImNvbnRleHQiOnsiY2l0eUlEIjo5NCwiYXBwIjoidWJlcmVhdHNfY29tIiwiYXBwVmVyc2lvbiI6IjMuMC4wIiwiZGV2aWNlIjoid2luZG93c3Bob25lIiwiZGV2aWNlSUQiOiIyYTJlYTEzNS1kYjBjLTQ4N2EtYjM1OC02ZWEwMGM3ZjBhNmUiLCJ1c2VySUQiOiI3NmUzM2VjZC0zNTRmLTQxZjAtYjBlOC0zZTNlYThiNzFkODciLCJjb29raWVJRCI6Ijc2ZTMzZWNkLTM1NGYtNDFmMC1iMGU4LTNlM2VhOGI3MWQ4NyIsInNlc3Npb25JRCI6ImM4ZDVjZjg3LWIzOTEtNDJkMS04ZDc2LTU2NmFkOWRjODQ3MiJ9LCJ0cnVuY2F0ZWRUb2tlbiI6dHJ1ZX0%3D%22%7D%2C%22eats_web_cro_home_fullbleed%22%3A%7B%22name%22%3A%22t_fullbleed%22%7D%2C%22eats_web_cro_m_search_shortcuts%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_cro_mw_h_ext_blocks%22%3A%7B%22name%22%3A%22control%22%7D%2C%22eats_web_payments_arrears_enable%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22payments_hub_wpe_event_transport_enable%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22payments_web_select_business%22%3A%7B%22name%22%3A%22personal_business%22%7D%2C%22eats_web_promo_manager%22%3A%7B%22name%22%3A%22enabled%22%7D%2C%22eats_web_promo_entry%22%3A%7B%22name%22%3A%22enabled%22%7D%2C%22eats_web_sort_filters%22%3A%7B%22name%22%3A%22enabled%22%7D%2C%22eats_web_bandwagon%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_interim_billboards%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_chain_landing%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_payments_pre_checkout_enable%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_cro_seo_destination_pages%22%3A%7B%22name%22%3A%22t_cuisinesrp%22%7D%2C%22eats_web_cro_rest_addr_maintain%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_web_cro_store_sticky_address_entry%22%3A%7B%22name%22%3A%22control%22%7D%2C%22eats_payments_title_replacement_wallet%22%3A%7B%22name%22%3A%22treatment%22%7D%2C%22eats_payments_wallet_new_home%22%3A%7B%22name%22%3A%22treatment%22%7D%7D"}
req = urllib.request.Request(url, data,headers)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
   
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}

result = urllib.urlopen('https://www.ubereats.com/api/getFeedV1?localeCode=tw',params=params)
resultJson = json.loads(result.read())


# =============================================================================
#  ubereat
# =============================================================================
url = "https://www.ubereats.com/tw/feed?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFOCU4NyVCQSVFNSU4QyU5NyVFOCVCQiU4QSVFNyVBQiU5OSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpVWi1XZlhLcFFqUVIwajRnZ1RvRDg5QSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wNDc2MzMzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjUxNjIzMjQlN0Q%3D"
driver = webdriver.Chrome(r"C:\Users\Jerry\chromedriver.exe")
driver.get(url)

my_data = {"cacheKey":"JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNSU4RiVCMCVFNSU4QyU5NyUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUptUXJpdkhLc1FqUVI0TUlLM2M0MWFqOCUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wMzI5Njk0JTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjU2NTQxNzclN0Q=/DELIVERY///0/0//JTVCJTVE///","feedSessionCount":{"announcementCount":0,"announcementLabel":""},"userQuery":"","date":"","startTime":0,"endTime":0,"carouselId":"","sortAndFilters":[],"marketingFeedType":"","billboardUuid":"","feedProvider":""}
driver.post(url,my_data)

soup = BeautifulSoup(driver.page_source)
soup.find_all("h3")
soup.find_all("img")

driver.find_element_by_css_selector('input[TEXT=myCheckBox]').click()

url = "https://www.ubereats.com/tw/feed?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFOCU4NyVCQSVFNSU4QyU5NyVFOCVCQiU4QSVFNyVBQiU5OSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpVWi1XZlhLcFFqUVIwajRnZ1RvRDg5QSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wNDc2MzMzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjUxNjIzMjQlN0Q%3D"
response = requests.get(url)
soup = BeautifulSoup(response.text)
soup

soup.find("div",class_="e8 g2 g3").find("img").find("img").get("src")
soup.find_all(class_="e8 g2 g3")

soup.find_all("h3")
soup.find_all("img")

# =============================================================================
# 
# =============================================================================
url = "https://www.ubereats.com/tw/taipei/food-delivery/%E8%80%81%E8%B3%B4%E8%8C%B6%E6%A3%A7-%E5%8F%B0%E5%8C%97%E6%9D%BE%E5%B1%B1%E5%BA%97/pe-58e0bTC2RMb0othzLYQ"
response = requests.get(url)
soup = BeautifulSoup(response.text)
soup.find_all("a")[15]
