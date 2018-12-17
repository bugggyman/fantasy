#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import csv
import time
from collections import defaultdict, OrderedDict

ALLTHEDAMNPLAYERS={}
BaseUrl='https://www.myscore.com.ua/football/europe/europa-league/fixtures/'
binary = FirefoxBinary()
browser = webdriver.Firefox(firefox_binary = binary)
browser.set_window_size(1300, 900)
browser.get(BaseUrl)
time.sleep(3)

content = browser.page_source
soup = BeautifulSoup(''.join(content), 'lxml')
records=soup.find_all("tr")
print(len(records))
i=0
c=0
index=1
while i<len(records):
	matches = records[i].findAll("td")
	if len(matches)==6:
		try:
			Home_Team=matches[2].get_text()
			Guest_Team=matches[3].get_text()
			
			ALLTHEDAMNPLAYERS[index] = []
			ALLTHEDAMNPLAYERS[index].append(Home_Team)
			ALLTHEDAMNPLAYERS[index].append(Guest_Team+u"(Д)")
			
			ALLTHEDAMNPLAYERS[index+1] = []
			ALLTHEDAMNPLAYERS[index+1].append(Guest_Team)
			ALLTHEDAMNPLAYERS[index+1].append(Home_Team+u"(Г)")
			
			index+=2
		except AttributeError:
			print('error')
		
	i+=1

browser.close()


Summary_Table={}
d = defaultdict(list)
for value in ALLTHEDAMNPLAYERS.values():
	d[value[0]].extend(value[1:])
	
Final_Dictionary=OrderedDict(sorted(d.items(), key=lambda t: t[0]))




with open('ENG_calendar.csv', 'w', newline='', encoding='utf-16') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow([u"Команда",u"Typ 1",u"Typ 2",u"Typ 3",u"Typ 4",u"Typ 5",u"Typ 6",u"Typ 7",u"Typ 8",u"Typ 9",u"Typ 10",
		u"Typ 11",u"Typ 12",u"Typ 13",u"Typ 14",u"Typ 15",u"Typ 16",u"Typ 17",u"Typ 18",u"Typ 19",u"Typ 20",u"Typ 21",u"Typ 22",
		u"Typ 23",u"Typ 24",u"Typ 25",u"Typ 26",u"Typ 27",u"Typ 28",u"Typ 29",u"Typ 30",u"Typ 31",u"Typ 32",u"Typ 33",u"Typ 34"])
	for key, val in Final_Dictionary.items():
			writer.writerow([key]+ val)