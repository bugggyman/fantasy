#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import csv
from collections import defaultdict, OrderedDict
from unidecode import unidecode
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import json
time_start=datetime.now()

ALLTHEDAMNPLAYERS={}

login_url = "https://www.sports.ru/logon.html"
BaseUrl='https://www.sports.ru/fantasy/football/team/transfers/1829209.html'

browser =  webdriver.Chrome()
browser.set_window_size(1920, 1280) # PhantomJS default to 400X300 is executable element outside might cause problem
browser.get(login_url)
time.sleep(1)

inputElement = browser.find_element_by_id("login")
inputElement.send_keys("mrtaylorchuk@gmail.com")
inputElement = browser.find_element_by_id("password")
inputElement.send_keys("sadass1")
inputElement.send_keys(Keys.ENTER)


browser.get(BaseUrl)
time.sleep(1)
content = browser.page_source
soup = BeautifulSoup(''.join(content), 'lxml')

table = soup.find("table", {"class": "transfer-table"})

records=table.find_all("tr")

i=1

# c=0
# index=1
while i<len(records):
	Price=records[i].attrs["data-price"]
	Position_id=records[i].attrs["data-amplua"].strip()
	print(Position_id)
	Rus_name=records[i].attrs["data-name"]
	Points=records[i].attrs["data-points"]
	Name=unidecode(Rus_name)
	
	params=records[i].find_all("td")
	Team=unidecode(params[1].attrs['title'])
	print(Team)
	if int(Position_id)==1:
		Position="GK"
	elif int(Position_id)==2:
		Position="DEF"
	elif int(Position_id)==3:
		Position="MID"
	elif int(Position_id)==4:
		Position="FOR"	
	else:
		Position='Not defined'
	ALLTHEDAMNPLAYERS[Name] = []
	ALLTHEDAMNPLAYERS[Name].append(Position)
	ALLTHEDAMNPLAYERS[Name].append(Price)
	ALLTHEDAMNPLAYERS[Name].append(Points)
	ALLTHEDAMNPLAYERS[Name].append(Team)
	i+=1



	

browser.close()
json = json.dumps(ALLTHEDAMNPLAYERS,indent=0)
with open("dict.json","w") as f:
	f.write(json)
	f.close()



time_end=datetime.now()
print(time_end - time_start)  


# Summary_Table={}
# d = defaultdict(list)
# for value in ALLTHEDAMNPLAYERS.values():
# 	d[value[0]].extend(value[1:])
	
# Final_Dictionary=OrderedDict(sorted(d.items(), key=lambda t: t[0]))




# with open('ENG_calendar.csv', 'w', newline='', encoding='utf-16') as csv_file:
# 	writer = csv.writer(csv_file)
# 	writer.writerow([u"Команда",u"Typ 1",u"Typ 2",u"Typ 3",u"Typ 4",u"Typ 5",u"Typ 6",u"Typ 7",u"Typ 8",u"Typ 9",u"Typ 10",
# 		u"Typ 11",u"Typ 12",u"Typ 13",u"Typ 14",u"Typ 15",u"Typ 16",u"Typ 17",u"Typ 18",u"Typ 19",u"Typ 20",u"Typ 21",u"Typ 22",
# 		u"Typ 23",u"Typ 24",u"Typ 25",u"Typ 26",u"Typ 27",u"Typ 28",u"Typ 29",u"Typ 30",u"Typ 31",u"Typ 32",u"Typ 33",u"Typ 34"])
# 	for key, val in Final_Dictionary.items():
# 			writer.writerow([key]+ val)
