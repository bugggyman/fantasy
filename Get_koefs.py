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

		
team_dictionary = {"Basaksehir" : "Istanbul Basaksehir",
				   "Akhisar": "Akhisarspor",
				   "Akhisar Genclik Spor" : "Akhisarspor",
				   "Malatyaspor" : "Yeni Malatyaspor",
				   "Sheffield Utd" : "Sheffield United",
				   "Sheffield Wed" : "Sheffield Wednesday",
				   "West Brom" : "West Bromwich Albion",
				   "Hull City" : "Hull",
				   "Nottingham" : "Nottingham Forest",
				   "Paris Saint-Germain" : "Paris Saint Germain",
				   "Paris SG" : "Paris Saint Germain",
				   "FK Anzi Makhackala" : "Anzhi Makhachkala",
				   "Anzhi" : "Anzhi Makhachkala",
				   "Dynamo Moscow" : "Dinamo Moscow",
				   "Krasnodar" : "FC Krasnodar",
				   "Orenburg" : "FC Orenburg",
				   "FK Rostov": "FC Rostov",
				   "Rostov": "FC Rostov",
				   "FK Krylya Sovetov Samara": "Krylya Sovetov Samara",
				   "Krylya Sovetov": "Krylya Sovetov Samara",
				   "Ufa" : "FC Ufa",
				   "Yenisey" : "FC Yenisey Krasnoyarsk",
				   "Akhmat Grozny" : "FK Akhmat",
				   "Lok. Moscow" : "Lokomotiv Moscow",
				   "Zenit Petersburg": "Zenit St. Petersburg",
				   "Zenit" : "Zenit St. Petersburg",
				   "AS Roma" : "Roma",
				   "Parma" : "Parma Calcio 1913",
				   "Spal" : "SPAL 2013",
				   "Athletic Bilbao": "Athletic Club",
				   "Ath Bilbao": "Athletic Club",
				   "Atl. Madrid" : "Atletico Madrid",
				   "Betis" : "Real Betis",
				   "Valladolid" : "Real Valladolid",
				   "Huesca" : "SD Huesca",
				   "Den Haag" : "ADO Den Haag",
				   "Graafschap" : "De Graafschap",
				   "Emmen" : "FC Emmen",
				   "Groningen" : "FC Groningen",
				   "Utrecht" : "FC Utrecht",
				   "Sittard" : "Fortuna Sittard",
				   "Breda" : "NAC Breda",
				   "Zwolle" : "PEC Zwolle",
				   "PSV" : "PSV Eindhoven",
				   "Heerenveen" : "SC Heerenveen",
				   "Venlo" : "VVV-Venlo",
				   "Leverkusen" : "Bayer Leverkusen",
				   "Dortmund" : "Borussia Dortmund",
				   "B. Monchengladbach": "Borussia M.Gladbach",
					"M'gladbach"  : "Borussia M.Gladbach",
				   "Frankfurt" : "Eintracht Frankfurt",
				   "Fortuna" : "Fortuna Duesseldorf",
           "Dusseldorf" : "Fortuna Duesseldorf",           
				   "Mainz" : "Mainz 05",
				   "Nurnberg" : "Nuernberg",
				   "RB Leipzig": "RasenBallsport Leipzig",
				   "Leipzig" : "RasenBallsport Leipzig",
				   "Schalke" : "Schalke 04",
				   "Stuttgart" : "VfB Stuttgart",
				   "Man City" : "Manchester City",
				   "Man Utd" : "Manchester United",
				   "Wolves" : "Wolverhampton Wanderers",
				   "BB Erzurumspor" : "Erzurum BB",
				   "Vallecano":"Rayo Vallecano"
		}

time_start=datetime.now()
champs = [["English Premier League", "http://sports.williamhill.com/bet/en-gb/betting/t/295/English+Premier+League.html", "http://www.oddsportal.com/soccer/england/premier-league/"], 
["Championship", "http://sports.williamhill.com/bet/en-gb/betting/t/292/English+Championship.html", "http://www.oddsportal.com/soccer/england/championship/"], 
["Serie A", "http://sports.williamhill.com/bet/en-gb/betting/t/321/Italian+Serie+A.html", "http://www.oddsportal.com/soccer/italy/serie-a/"], 
["BundesLiga", "http://sports.williamhill.com/bet/en-gb/betting/t/315/German+Bundesliga.html", "http://www.oddsportal.com/soccer/germany/bundesliga/"], 
["France","http://sports.williamhill.com/bet/en-gb/betting/t/312/French+Ligue+1.html", "http://www.oddsportal.com/soccer/france/ligue-1/"], 
["Eredivisie","http://sports.williamhill.com/bet/en-gb/betting/t/306/Dutch+Eredivisie.html", "http://www.oddsportal.com/soccer/netherlands/eredivisie/"], 
["Turkey","http://sports.williamhill.com/bet/en-gb/betting/t/325/Turkish+Super+Lig.html", "http://www.oddsportal.com/soccer/turkey/super-lig/"], 
["La Liga","http://sports.williamhill.com/bet/en-gb/betting/t/338/Spanish+La+Liga+Primera.html", "http://www.oddsportal.com/soccer/spain/laliga/"], 
["Russia","http://sports.williamhill.com/bet/en-gb/betting/t/334/Russian+Premier+League.html", "http://www.oddsportal.com/soccer/russia/premier-league/"]]

start_number = int(input('''
Select champ to start: 
England - 0
Championship - 1
Serie A - 2
Bundesliga - 3
France - 4
Eredivisie - 5
Turkey - 6
La Liga - 7
Russia - 8
'''))
end_number = int(input("Number to finish:"))
ALLTHEDAMNPLAYERS={}

index=0
BaseUrl = 'http://sports.williamhill.com/bet/en-gb/betting/t/295/English+Premier+League.html'
binary = FirefoxBinary()
browser = webdriver.Firefox(firefox_binary = binary)
browser.set_window_size(1300, 900)
browser.get('http://sports.williamhill.com/bet/en-gb/betting/')
time.sleep(5)
more_matches = browser.find_element_by_id('yesBtn')
more_matches.click()
odds_element = WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.ID, "oddsSelect")))
select = Select(odds_element)
select.select_by_visible_text("Decimal")


while start_number <= end_number:
	champ_name = champs[start_number][0]
	browser.get(champs[start_number][1])
	time.sleep(5)
	content = browser.page_source
	soup = BeautifulSoup(''.join(content), 'lxml')
	links = soup.find_all(title="More markets", class_="")


	m_number = len(links) - 1
	match = 0
	while match <= m_number:

		MatchtUrl = links[match].get('href')
		   
		try:
			browser.get(MatchtUrl)
			time.sleep(4)
			more_matches = browser.find_element_by_link_text('Goals')
			more_matches.click()
			time.sleep(5)
		except Exception as e:
			print(e)
			try:
				browser.close()
				browser.get(MatchtUrl)
				time.sleep(7)
				more_matches = browser.find_element_by_id('yesBtn')
				more_matches.click()
				odds_element = WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.ID, "oddsSelect")))
				select = Select(odds_element)
				select.select_by_visible_text("Decimal")
				more_matches = browser.find_element_by_link_text('Goals')
				more_matches.click()
				time.sleep(9)
			except:
				print("Can't get ceffs for", MatchtUrl )

			
		else:

			content = browser.page_source
			soup = BeautifulSoup(''.join(content), 'lxml')
			team_link = MatchtUrl.split("/")
			Home_Team = team_link[len(team_link) - 1 ].split("+v+")[0].replace("+", " ").replace("%27", "'").replace("%2d", "-").replace("%2e", ".")
			Guest_Team = team_link[len(team_link) - 1 ].split("+v+")[1].strip("html").replace("+", " ").strip(".").replace("%27", "'").replace("%2d", "-").replace("%2e", ".")

			print(Home_Team, Guest_Team)
			cl_sheet = "This table shows " + Home_Team + ' v ' + Guest_Team + " - To Keep A Clean Sheet"
			cleansheet = soup.find("table", { "summary" : cl_sheet})
			try:
				home_cs = cleansheet.find_all(class_= "eventprice")[0].get_text().strip().replace(".", ",")
				guest_cs = cleansheet.find_all(class_= "eventprice")[1].get_text().strip().replace(".", ",")          
				home_over_summary = "This table shows " + Home_Team + ' v ' + Guest_Team + " - " +  Home_Team + " Under/Over 1.5 Goals"
				home_over_table = soup.find("table", { "summary" : home_over_summary})
				home_over = home_over_table.find_all(class_= "eventprice")[1].get_text().strip().replace(".", ",")
					
				guest_over_summary = "This table shows " + Home_Team + ' v ' + Guest_Team + " - " +  Guest_Team + " Under/Over 1.5 Goals"
				guest_over_table = soup.find("table", { "summary" : guest_over_summary})
				guest_over = guest_over_table.find_all(class_= "eventprice")[1].get_text().strip().replace(".", ",")
			except AttributeError as attribute:
				print(attribute)
				home_cs = "-"
				guest_cs = "-"
				home_over = "-"
				guest_over = "-"
			except TimeoutException as timeout:
				print(timeout)
				home_cs = "-"
				guest_cs = "-"
				home_over = "-"
				guest_over = "-"
				print("timeout error")
			except WebDriverException as er:
				print(er)
			#Replace team names to one unified Whoscore-like names
			if Guest_Team in team_dictionary.keys():
				Guest_Team = team_dictionary[Guest_Team]
			if Home_Team in team_dictionary.keys():
				Home_Team = team_dictionary[Home_Team]
			
			ALLTHEDAMNPLAYERS[index] = []
			ALLTHEDAMNPLAYERS[index].append(Home_Team)
			ALLTHEDAMNPLAYERS[index].append(champ_name)
			ALLTHEDAMNPLAYERS[index].append(Guest_Team + u"(Дом)")
			ALLTHEDAMNPLAYERS[index].append(u"Клиншит")
			ALLTHEDAMNPLAYERS[index].append(home_cs)
			ALLTHEDAMNPLAYERS[index].append(datetime.now().date())
			
			ALLTHEDAMNPLAYERS[index+1] = []
			ALLTHEDAMNPLAYERS[index+1].append(Home_Team)
			ALLTHEDAMNPLAYERS[index+1].append(champ_name)
			ALLTHEDAMNPLAYERS[index+1].append(Guest_Team + u"(Дом)")
			ALLTHEDAMNPLAYERS[index+1].append(u"ИТБ")
			ALLTHEDAMNPLAYERS[index+1].append(home_over)
			ALLTHEDAMNPLAYERS[index+1].append(datetime.now().date())

			ALLTHEDAMNPLAYERS[index+2] = []
			ALLTHEDAMNPLAYERS[index+2].append(Guest_Team)
			ALLTHEDAMNPLAYERS[index+2].append(champ_name)
			ALLTHEDAMNPLAYERS[index+2].append(Home_Team + u"(Гост)")
			ALLTHEDAMNPLAYERS[index+2].append(u"Клиншит")
			ALLTHEDAMNPLAYERS[index+2].append(guest_cs)
			ALLTHEDAMNPLAYERS[index+2].append(datetime.now().date())
			
			ALLTHEDAMNPLAYERS[index+3] = []
			ALLTHEDAMNPLAYERS[index+3].append(Guest_Team)
			ALLTHEDAMNPLAYERS[index+3].append(champ_name)
			ALLTHEDAMNPLAYERS[index+3].append(Home_Team + u"(Гост)")
			ALLTHEDAMNPLAYERS[index+3].append(u"ИТБ")
			ALLTHEDAMNPLAYERS[index+3].append(guest_over)
			ALLTHEDAMNPLAYERS[index+3].append(datetime.now().date())
			index+=4
		
		match+=1

	#go to oddsportal to get match winner odds
	try:
		browser.get(champs[start_number][2])
		time.sleep(3)
	except WebDriverException:
		print("restarting browser....")
		browser =  webdriver.Chrome()
		browser.set_window_size(1920, 1280)
		browser.get(champs[start_number][2])
		time.sleep(5)

   
	#clicking to view all available matches
	try:
		all_matches = browser.find_element_by_id('show-all-link')
		all_matches.click()
	except:
		print("no addiitional coefs")
	# Get content

	content = browser.page_source
	soup = BeautifulSoup(''.join(content), 'lxml')
	link_odds = soup.find_all("tr")
	i=0
	while i<len(link_odds):
		stats = link_odds[i].findAll("td")
		
		if len(stats) == 6:
			try:
				Team_Name=stats[1].findAll("a")
				
				if len(Team_Name)==1:
					Teamlist=Team_Name[0].get_text().split('-')
					
				elif len(Team_Name)==2:
					Teamlist=Team_Name[1].get_text().split('-')
				Home_Team=Teamlist[0].rstrip()
				Guest_Team=Teamlist[1].strip()
				
				
				Bet_Win=stats[2].get_text().replace(".", ",")
				Bet_Lose=stats[4].get_text().replace(".", ",")
				if Home_Team in team_dictionary.keys():
					Home_Team = team_dictionary[Home_Team]
				if Guest_Team in team_dictionary.keys():
					Guest_Team = team_dictionary[Guest_Team] 

				ALLTHEDAMNPLAYERS[index] = []
				ALLTHEDAMNPLAYERS[index].append(Home_Team)
				ALLTHEDAMNPLAYERS[index].append(champ_name)
				ALLTHEDAMNPLAYERS[index].append(Guest_Team+u"(Дом)")
				ALLTHEDAMNPLAYERS[index].append(u"Победа")
				ALLTHEDAMNPLAYERS[index].append(Bet_Win)
				ALLTHEDAMNPLAYERS[index].append(datetime.now().date())
				ALLTHEDAMNPLAYERS[index+1] = []
				ALLTHEDAMNPLAYERS[index+1].append(Guest_Team)
				ALLTHEDAMNPLAYERS[index+1].append(champ_name)
				ALLTHEDAMNPLAYERS[index+1].append(Home_Team+u"(Гост)")
				ALLTHEDAMNPLAYERS[index+1].append(u"Победа")
				ALLTHEDAMNPLAYERS[index+1].append(Bet_Lose)
				ALLTHEDAMNPLAYERS[index+1].append(datetime.now().date())
				index+=2
			except (AttributeError, TimeoutException):
				print('attribute error')
		i+=1
	start_number+=1

	 


browser.close()



# Summary_Table={}
# d = defaultdict(list)
# for value in ALLTHEDAMNPLAYERS.values():
#     d[value[0]].extend(value[1:])
	
# Final_Dictionary=OrderedDict(sorted(d.items(), key=lambda t: t[0]))

newDict = {}
for key in sorted(ALLTHEDAMNPLAYERS):
	value = ALLTHEDAMNPLAYERS[key]
	valuesExist = False

	for newValue in newDict.values():
		if value[0] == newValue[0]  and value[3] == newValue[3]:
			valuesExist = True

	if not valuesExist:
		newDict[key] = value
	else:
		updated_value = value[3] + "2"
		newDict[key] = [value[0],value[1],value[2],updated_value,value[4],datetime.now().date()]

newDict1 = {}
for key in sorted(newDict):
	value = newDict[key]
	valuesExist = False

	for newValue in newDict1.values():
		if value[0] == newValue[0]  and value[3] == newValue[3]:
			valuesExist = True

	if not valuesExist:
		newDict1[key] = value
	else:
		updated_value = value[3].rstrip("2") + "3"
		newDict1[key] = [value[0],value[1],value[2],updated_value,value[4],datetime.now().date()]

with open('Koeffs.csv', 'w', newline='', encoding='utf-16') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow([u"ID", u"Команда",u"Чемпионат",u"Соперник1",u"Тип",u"Кэф",u"Дата"])
	for key, val in newDict1.items():
			writer.writerow([key]+ val)



time_end=datetime.now()
print(time_end - time_start)  