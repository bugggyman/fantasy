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

		
team_dictionary = {"Basaksehir" : "İstanbul",
				   "Malatyaspor" : "Yeni Malatyaspor",
				   "Kasimpasa" : "Kasımpaşa",
				   "Goztepe" : "Göztepe",
				   "Ankaragucu" : "Ankaragücü",
				   "Gaziantep" : "Gaziantep BB",
				   "Genclerbirligi" : "Gençlerbirliği",

				   
				   "Sheffield Utd" : "Sheffield United",
				   "Sheffield Wed" : "Sheffield Wednesday",
				   "West Brom" : "West Bromwich Albion",
				   "Hull" : "Hull City",
				   "Nottingham" : "Nottingham Forest",
				   "Birmingham" : "Birmingham City",
				   "Blackburn" : "Blackburn Rovers",
				   "Cardiff" : "Cardiff City",
				   "Charlton" : "Charlton Athletic",
				   "Derby" : "Derby County",
				   "Huddersfield" : "Huddersfield Town",
				   "Leeds" : "Leeds United",
				   "Luton" : "Luton Town",
				   "Preston" : "Preston North End",
				   "QPR" : "Queens Park Rangers",
				   "Stoke" : "Stoke City",
				   "Swansea" : "Swansea City",
				   "Wigan" : "Wigan Athletic",
				   
				   "Paris Saint Germain" : "PSG",
				   "Amiens" : "Amiens SC",
				   "Nimes" : "Nîmes",
				   "Lyon" : "Olympique Lyonnais",
				   "Marseille" : "Olympique Marseille",
				   "St Etienne" : "Saint-Étienne",
				   "St. Etienne" : "Saint-Étienne",

				   "CSKA Moscow" : "CSKA",
				   "Din. Moscow" : "Dinamo",
				   "Dynamo Moscow" : "Dinamo",
				   "Akhmat Grozny" : "Akhmat",
				   "Lok. Moscow" : "Lokomotiv",
				   "FK Rostov": "Rostov",
				   "Lokomotiv Moscow": "Lokomotiv",
				   "Spartak Moscow": "Spartak",
				   "FK Krylya Sovetov Samara": "Krylya Sovetov",
				   "Rubin Kazan" : "Rubin",
				   "Lok. Moscow" : "Lokomotiv",
				   "Zenit Petersburg": "Zenit",

				   "AS Roma" : "Roma",
				   "Spal" : "SPAL",
				   "AC Milan" : "Milan",
				   "Inter Milan" : "Internazionale",
				   "Inter" : "Internazionale",
				   "Verona" : "Hellas Verona",

				   "Athletic Bilbao": "Athletic Club",
				   "Ath Bilbao": "Athletic Club",
				   "Atl. Madrid" : "Atletico Madrid",
				   "Betis" : "Real Betis",
				   "Valladolid" : "Real Valladolid",
				   "Huesca" : "SD Huesca",
				   "Vallecano":"Rayo Vallecano",
				   "Ath. Bilbao" : "Athletic Club",
				   "Atletico Madrid" : "Atlético Madrid",
				   "Celta Vigo" : "Celta de Vigo",
				   "Alaves" : "Deportivo Alavés",
				   "Granada CF" : "Granada",
				   "Leganes" : "Leganés",

				   "Den Haag" : "ADO Den Haag",
				   "Graafschap" : "De Graafschap",
				   "FC Emmen" : "Emmen",
				   "FC Groningen" : "Groningen",
				   "FC Utrecht" : "Utrecht",
				   "Sittard" : "Fortuna Sittard",
				   "Waalwijk" : "RKC Waalwijk",
				   "Zwolle" : "PEC Zwolle",
				   "PSV" : "PSV Eindhoven",
				   "SC Heerenveen" : "Heerenveen",
				   "Venlo" : "VVV",
				   "AZ Alkmaar" : "AZ",
				   "PSV Eindhoven" : "PSV",

				   "Leverkusen" : "Bayer Leverkusen",
				   "Dortmund" : "Borussia Dortmund",
				   "B. Monchengladbach": "Borussia M'gladbach",
					"M\'gladbach"  : "Borussia M\'gladbach",
				   "Frankfurt" : "Eintracht Frankfurt",
				   "Fortuna" : "Fortuna Düsseldorf",
          		   "Dusseldorf" : "Fortuna Düsseldorf",           
				   "Mainz" : "Mainz 05",
				   "Leipzig" : "RB Leipzig",
				   "Schalke" : "Schalke 04",
				   "Fort. Dusseldorf" : "Fortuna Düsseldorf",
				   "FC Koln" : "Köln",
				   "Koln" : "Köln",
				   "Hertha Berlin" : "Hertha BSC",
				   "Bayern Munich" : "Bayern München",

				   "Man City" : "Manchester City",
				   "Man Utd" : "Manchester United",
				   "Wolves" : "Wolverhampton Wanderers",
				   "Bournemouth" : "AFC Bournemouth",
				   "Brighton" : "Brighton & Hove Albion",
				   "Leicester" : "Leicester City",
				   "Manchester Utd" : "Manchester United",
				   "Newcastle" : "Newcastle United",
				   "Norwich" : "Norwich City",
				   "Tottenham" : "Tottenham Hotspur",
				   "West Ham" : "West Ham United",

				   "Aves" : "Desportivo Aves",
				   "Famalicao" : "Famalicão",
				   "Ferreira" : "Paços de Ferreira",
				   "Pacos Ferreira" : "Paços de Ferreira",
				   "FC Porto" : "Porto",
				   "Braga" : "Sporting Braga",
				   "Nurnberg" : "Sporting CP",
				   "Sporting Lisbon" : "Sporting CP",
				   "Guimaraes" : "Vitória Guimarães",
				   "Setubal" : "Vitória Setúbal",
				   "Sporting" : "Sporting CP",
				   "Nurnberg" : "Nuernberg",
				   "Nurnberg" : "Nuernberg",
				   "Nurnberg" : "Nuernberg",
		}

time_start=datetime.now()
champs = [["English Premier League", "https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY295/English-Premier-League/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/england/premier-league/"], 
["Championship", "https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY292/English-Championship/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/england/championship/"], 
["Serie A", "https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY321/Italian-Serie-A/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/italy/serie-a/"], 
["BundesLiga", "https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY315/German-Bundesliga/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/germany/bundesliga/"], 
["France","https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY312/French-Ligue-1/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/france/ligue-1/"], 
["Eredivisie","https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY306/Dutch-Eredivisie/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/netherlands/eredivisie/"], 
["Turkey","https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY325/Turkish-Super-Lig/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/turkey/super-lig/"], 
["La Liga","https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY338/Spanish-La-Liga-Primera/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/spain/laliga/"], 
["Russia","https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY334/Russian-Premier-League/matches/OB_MGMB/Match-Betting", "http://www.oddsportal.com/soccer/russia/premier-league/"],
["Portugal", "https://sports.williamhill.com/betting/en-gb/football/competitions/OB_TY331/Portuguese-Primeira-Liga/matches/OB_MGMB/Match-Betting", "https://www.oddsportal.com/soccer/portugal/primeira-liga/"]]

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
Portugal - 9
'''))
end_number = int(input("Number to finish:"))
ALLTHEDAMNPLAYERS={}

index=0
BaseUrl = 'https://sports.williamhill.com'
binary = FirefoxBinary()
browser = webdriver.Firefox(firefox_binary = binary)
browser.set_window_size(1300, 900)

while start_number <= end_number:
	champ_name = champs[start_number][0]
	browser.get(champs[start_number][1])
	myElem = WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'wh-global-overlay')))
	time.sleep(2)
	content = browser.page_source
	soup = BeautifulSoup(''.join(content), 'lxml')
	select_type = browser.find_element_by_link_text('Odds Format').click()
	decimal_select = browser.find_element_by_link_text('Decimal').click()
	links = soup.find_all(class_="sp-o-market__more")
	m_number = len(links) - 1
	match = 0
	while match <= m_number:
		MatchtUrl = BaseUrl + links[match].find('a').get('href')
		try:
			browser.get(MatchtUrl)
			myElem = WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'wh-global-overlay')))
			time.sleep(2)
			Goals_tab = browser.find_element_by_link_text('Team Goals').click()
			myElem = WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'wh-global-overlay')))
			time.sleep(2)
		except Exception as e:
			# print(e)
			print( "----------Error loading page---------")
			browser.refresh()
			time.sleep(15)
			
			try:
				browser.get(MatchtUrl)
				myElem = WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'wh-global-overlay')))
				time.sleep(2)
				Goals_tab = browser.find_element_by_link_text('Team Goals').click()
				myElem = WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'wh-global-overlay')))
				time.sleep(2)
			except:
				print("Can't get ceffs for", MatchtUrl )
				browser.refresh()
				time.sleep(15)

			
		else:

			content = browser.page_source
			soup = BeautifulSoup(''.join(content), 'lxml')
			Home_Team = soup.find('h1', class_="header-panel__title").get_text().split(" vs ")[0]
			Guest_Team = soup.find('h1', class_="header-panel__title").get_text().split(" vs ")[1]
			print(Home_Team, Guest_Team)

			cl_sheet = "To Keep A Clean Sheet"
			Search_text = Home_Team + ' Over/Under 1.5 Goals'
			Search_text2 = Guest_Team + ' Over/Under 1.5 Goals' 
			
			try:
				home_cs = soup.find('h2', string = cl_sheet).findParent().findParent().find_all('span',class_="betbutton__odds")[0].get_text().replace(".", ",")
				guest_cs = soup.find('h2', string = cl_sheet).findParent().findParent().find_all('span',class_="betbutton__odds")[1].get_text().replace(".", ",")          
				home_over = soup.find('h2', string = Search_text).findParent().findParent().find_all('span',class_="betbutton__odds")[1].get_text().replace(".", ",")
				guest_over = soup.find('h2', string = Search_text2).findParent().findParent().find_all('span',class_="betbutton__odds")[1].get_text().replace(".", ",")
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
				home_cs = "-"
				guest_cs = "-"
				home_over = "-"
				guest_over = "-"
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
