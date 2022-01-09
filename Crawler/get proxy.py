# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 22:50:43 2020

@author: Jerry
"""
from bs4 import BeautifulSoup
import requests
def get_soup(url):
    proxies = {
      "http": "40.121.198.48:80",
      "https": "69.195.157.162:8100"
     }
    #headers = {'user-agent': UA.random}
    response = requests.get(url,proxies=proxies)
    soup = BeautifulSoup(response.text,features="html.parser")
    response.close()
    return soup

url = "https://medium.com/qiubingcheng/%E5%A6%82%E4%BD%95%E5%AE%89%E8%A3%9Danaconda-%E4%B8%A6%E4%B8%94%E5%8C%AF%E5%85%A5conda%E8%99%9B%E6%93%AC%E7%92%B0%E5%A2%83-ba2e140706a3"
soup = get_soup(url)

requests.get(url)
