#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 11:04:53 2017

@author: chih
"""

from bs4 import BeautifulSoup
import requests
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = 'http://sigmod2017.org/sigmod-accepted-papers/'

class SigmodCrawler:

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def fetch_download_link(self):
        page = requests.get(BASE_URL)
        a = BeautifulSoup(page.text, "lxml").find(id="DLcontent").findAll('a')
        pdf_map = dict(map(lambda i: {i.text.strip(),'http:' + i.attrs['href']}, a))
        
        print(pdf_map)

#        for item in pdf_map:
#            if ".pdf" in pdf_map[item] and "www.vldb.org" in pdf_map[item]:
#                pdf_r = requests.get(pdf_map[item])
#                with open(item + ".pdf", "wb") as pdf_file:
#                    pdf_file.write(pdf_r.content)

    def run(self):
        self.fetch_download_link()


if __name__ == '__main__':
    sc = SigmodCrawler()
    sc.run() 
