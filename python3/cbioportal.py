#!/usr/bin/env python
#install selenium with pip
#add the geckodriver into environment path
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import urllib2
import time,re

#1. Extract all the studies ID
#url = "http://www.cbioportal.org/study?id=brca_tcga#clinical"
url = "http://www.cbioportal.org/data_sets.jsp"
response = urllib2.urlopen(url)
htmlfile = response.read()

#compile the specific area
#1.1 extract the ID part
pattern0 = re.compile("<tbody>(.*?)</tbody>",re.S)
databody = re.findall(pattern0,htmlfile)

#1.2 get a full list of all the IDs
pattern1 = re.compile("study\?id=(.*?)'>",re.S)
cancerlist = re.findall(pattern1,databody[0])

#2. selenium for data download one by one
browser = webdriver.Firefox() # Get local session of firefox(geckodriver)
#2.1
cancerstudy = ignore_list[0]#First one as am example and to set the default download options in Firefox
#clinical_url = "http://www.cbioportal.org/study?id="+cancertudy+"#clinical"
url = "http://www.cbioportal.org/study?id="+cancerstudy+"#summary"
browser.get(url)
#button = browser.find_element_by_class_name('EFDT-download-btn')
button = browser.find_element_by_id('iviz-header-left-case-download')
button.click()

#2.2
for i in range(len(ignore_list)):
    cancerstudy = ignore_list[i]
    url = "http://www.cbioportal.org/study?id="+cancerstudy+"#summary"
    print i,cancerstudy
    browser.get(url) # Load page
    # wait for the page to load
    #WebDriverWait(browser, timeout=10).until(
    #    lambda x: x.find_element_by_class_name('EFDT-download-btn'))
    time.sleep(20)#Wait for 28s for page loading
    button = browser.find_element_by_id('iviz-header-left-case-download')
    button.click()
    time.sleep(5)
# page_source = browser.page_source
browser.close()

ignore = open("./studies_ignore.txt","r")
ignore_list = []
for line in ignore.readlines():
    ignore_list.append(line.strip())
ignore.close()