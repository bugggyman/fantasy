    #! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import csv
import re
from datetime import datetime
from collections import defaultdict, OrderedDict
import json

time_start=datetime.now()
Start_number = int(input('''
Select champ to start: 
Turkey - 0
Eredivisie - 1
Championship - 2
France - 3
- Russia - 4
Germany - 4
Italy - 5
La Liga - 6
England - 7
     '''))

end_number = int(input("Number to finish:"))
BaseUrl='https://www.whoscored.com'
ALLTHEDAMNPLAYERS = {}

with open("LeaguesWR.json") as json_file:  
    json_data = json.load(json_file)
    while Start_number <= end_number:
        index = 0
        ALLTHEDAMNPLAYERS = {}
        Teams=list(json_data.values())[Start_number]['TeamData']
        Country=list(json_data.values())[Start_number]['Country']
        League=list(json_data.keys())[Start_number]
        for team in Teams:
            
            if team[0] in {'Cardiff','Swansea'}:
                Team_Page_URL = BaseUrl + '/Teams/' + team[1] + '/Show/Wales-' + team[0]
            else:
               Team_Page_URL =  BaseUrl + '/Teams/' + team[1] + '/Show/%s-' %(Country) + team[0]
            # Connect webdriver
            options = Options()
            options.headless = True
            binary = FirefoxBinary()
            browser = webdriver.Firefox(firefox_binary = binary, options = options)
            browser.set_window_size(1300, 900) # browser has default resolution 400X300 is executable element outside might cause problem
            try:
                browser.get(Team_Page_URL)
                time.sleep(3)
            except:
                print("page refresh-----------------")
                browser.refresh()
                browser.get(Team_Page_URL)
                time.sleep(30)
            # Get content
            content = browser.page_source
            soup = BeautifulSoup(''.join(content), 'lxml')

            #parse team page to get urls to last 6 matches

            links=soup.find_all(class_ = "match-link match-report rc")
            if len(links) <= 5:
                last_match = 0
            else:
                last_match = 1
            m_number = len(links) - 1
            
            while m_number >= last_match:
                        
                MatchPartUrl = links[m_number].get('href').replace('MatchReport', 'LiveStatistics', 1)
                
                
                FinalURL = BaseUrl + MatchPartUrl
                try:
                    browser.get(FinalURL)
                    time.sleep(3)
                except:
                    print("page refresh-----------------")
                    browser.refresh()
                    browser.get(FinalURL)
                    time.sleep(30)


                try:
                    element = WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='live-player-home-summary\']")))
                    time.sleep(3)

                    content = browser.page_source
                    soup = BeautifulSoup(''.join(content), 'lxml')
                    Temp_Teams = soup.findAll("div", {"id": "match-header"})

                    
                    for Find_Teams in Temp_Teams:
                        HomeTeam = Find_Teams.findAll("td", {"class": "team"})[0].get_text()
                        
                        AwayTeam = Find_Teams.findAll("td", {"class": "team"})[1].get_text()
                        print(HomeTeam + " - " + AwayTeam)
                    if HomeTeam == team[2]:

                        AwayTeamStat = []
                        HomeTeamStat = [soup.find("div", {"id": "statistics-table-home-summary"}).find("tbody", {"id": "player-table-statistics-body"})]

                        m_number-=1
                        print('Hometeam stats reading')
                        
                    elif AwayTeam == team[2]:
                        AwayTeamStat = [soup.find("div", {"id": "statistics-table-away-summary"}).find("tbody", {"id": "player-table-statistics-body"})]
                        HomeTeamStat = []
                        m_number-=1
                        print('AwayTeam stats reading')
                        
                    else:
                        print("Something went wrong with Team on page", team[0], AwayTeam,HomeTeam)
                        



                    # if HomeTeam in Teamlist and AwayTeam in Teamlist:

                    #     AwayTeamStat = [soup.find("div", {"id": "statistics-table-away-summary"}).find("tbody", {"id": "player-table-statistics-body"})]
                    #     HomeTeamStat = [soup.find("div", {"id": "statistics-table-home-summary"}).find("tbody", {"id": "player-table-statistics-body"})]
                    #     m_number-=1
                    #     print('Both Teams in EPL')


                    # elif HomeTeam in Teamlist and AwayTeam not in Teamlist:
                    #     AwayTeamStat = []
                    #     HomeTeamStat = [soup.find("div", {"id": "statistics-table-home-summary"}).find("tbody", {"id": "player-table-statistics-body"})]
                    #     m_number-=1
                    #     print('AwayTeam not in EPL')

                    # elif AwayTeam in Teamlist and HomeTeam not in Teamlist:
                    #     AwayTeamStat = [soup.find("div", {"id": "statistics-table-away-summary"}).find("tbody", {"id": "player-table-statistics-body"})]
                    #     HomeTeamStat = []
                    #     m_number-=1
                    #     print('HomeTeam not in EPL')
                    # else:
                    #     print('Bulshit')

                    for data in HomeTeamStat:

                        # Get players
                        players = data.findAll("tr")

                            
                        #Get stats
                        i = 0
                        count_of_players=len(players)
                        
                        
                        while i < len(players):
                            
                            stats = players[i].findAll("td")
                            Player_Id1= stats[2].find('a').get('href').split('/')[2]
                            #count length of first column to parse it correctly
                            Col_length=len(stats[2].findChildren())
                            #Get values for each field
                            Shots_on_Target = int(stats[4].get_text().strip())
                            Shots_Off_Target = int(stats[3].get_text().strip())-Shots_on_Target
                            Key_passes = int(stats[5].get_text().strip())
                            Rating = str(stats[9].get_text().strip())
                            #defining last column, where goals, assists,cards and other data stored
                            Match_Data =str(stats[10])  
                            
                            Penalties=len(re.findall('data-event-satisfier-penaltyscored=', Match_Data))
                            Goals=len(re.findall('data-event-satisfier-goalnormal=', Match_Data))+Penalties
                            Assists=len(re.findall('data-event-satisfier-assist=', Match_Data))
                            Red_Cards=len(re.findall('data-event-satisfier-redcard=', Match_Data))
                            Yellow_Cards=len(re.findall('data-event-satisfier-voidyellowcard=', Match_Data))+len(re.findall('data-event-satisfier-yellowcard=', Match_Data))
                            Sec_Yellow_Card=len(re.findall('data-event-satisfier-secondyellow=', Match_Data))
                            Penalty_Saved=len(re.findall('data-event-satisfier-keeperpenaltysaved=', Match_Data))
                            Shot_on_Post=len(re.findall('data-event-satisfier-shotonpost=', Match_Data))
                            Penalty_Miss=len(re.findall('data-event-satisfier-penaltymissed=', Match_Data))
                            Name = unidecode(stats[2].findChildren()[0].get_text().rstrip(' 01234567890()′'))
                            Position = stats[2].findChildren()[Col_length-1].get_text().strip(', ')
                            Age = stats[2].findChildren()[Col_length-2].get_text()
                            Sub_on = len(re.findall('data-event-satisfier-subon=', str(stats[2])))==1
                            Sub_off = len(re.findall('data-event-satisfier-suboff=', str(stats[2])))==1
                            if Name == "Wanderson" and HomeTeam == "FC Krasnodar":
                                Name = (Name+("1"))
                            elif Name == "Maicon" and HomeTeam == "Galatasaray":
                                Name=(Name+("1"))
                            elif Name=="Hakan Arslan" and HomeTeam=="Rizespor":
                                Name=(Name+("1"))
                            elif Name=="Gokhan Akkan" and HomeTeam=="Rizespor":
                                Name=(Name+("1"))
                            elif Name=="Juanfran" and HomeTeam=="Leganes":
                                Name=(Name+("1"))
                            elif Name=="Raul Garcia" and AwayTeam=="Leganes":
                                Name=(Name+("1"))
                            elif Name=="Sergio Alvarez" and AwayTeam=="Eibar":
                                Name=(Name+("1"))
                            elif Name=="Danny Ward" and AwayTeam=="Cardiff":
                                Name=(Name+("1"))
                            elif Name=="Josue" and AwayTeam=="Kasimpasa":
                                Name=(Name+("1"))
                            else:
                                Name=Name

                            if Rating=='-':
                                Minutes_Played=0
                                Rating='0'
                            elif not Sub_on and not Sub_off:
                                Minutes_Played=93
                            elif  Sub_on and not Sub_off:
                                Minutes_Played=95-int(stats[2].find("span", {"class": "player-meta-data"}).get_text().strip('′)('))
                            elif Sub_off and not Sub_on:
                                Minutes_Played=int(stats[2].find("span", {"class": "player-meta-data"}).get_text().strip('′)('))
                            elif Sub_on and Sub_off:
                                Minutes=int(stats[2].findAll("span", {"class": "player-meta-data"})[1].get_text().strip('′)('))-int(stats[2].findAll("span", {"class": "player-meta-data"})[0].get_text().strip('′)('))
                            
                            
                            i+=1
                            ALLTHEDAMNPLAYERS[index] = []
                            ALLTHEDAMNPLAYERS[index].append(Name)
                            ALLTHEDAMNPLAYERS[index].append(HomeTeam)
                            ALLTHEDAMNPLAYERS[index].append(Age)
                            ALLTHEDAMNPLAYERS[index].append(Shots_Off_Target)
                            ALLTHEDAMNPLAYERS[index].append(Shots_on_Target)
                            ALLTHEDAMNPLAYERS[index].append(Key_passes)
                            ALLTHEDAMNPLAYERS[index].append(Rating)
                            ALLTHEDAMNPLAYERS[index].append(Goals)
                            ALLTHEDAMNPLAYERS[index].append(Assists)
                            ALLTHEDAMNPLAYERS[index].append(Penalties)
                            ALLTHEDAMNPLAYERS[index].append(Shot_on_Post)
                            ALLTHEDAMNPLAYERS[index].append(Penalty_Miss)
                            ALLTHEDAMNPLAYERS[index].append(Minutes_Played)
                            ALLTHEDAMNPLAYERS[index].append(Position)
                            index += 1

                            
                    for data in AwayTeamStat:

                        # Get players
                        players = data.findAll("tr")

                            
                        #Get stats
                        i = 0
                        
                        while i < len(players):
                            
                            stats = players[i].findAll("td")
                            Player_Id1 = stats[2].find('a').get('href').split('/')[2]
                            
                            #count length of first column to parse it correctly
                            Col_length = len(stats[2].findChildren())
                            #Get values for each field
                            #index = stats[0].get_text()
                            Shots_on_Target = int(stats[4].get_text().strip())
                            Shots_Off_Target = int(stats[3].get_text().strip()) - Shots_on_Target
                            Key_passes = int(stats[5].get_text().strip())
                            Rating = str((stats[9].get_text().strip()))
                            #defining last column, where goals, assists,cards and other data stored
                            Match_Data = str(stats[10])
                            
                            Penalties=len(re.findall('data-event-satisfier-penaltyscored=', Match_Data))
                            Goals=len(re.findall('data-event-satisfier-goalnormal=', Match_Data))+Penalties
                            Assists=len(re.findall('data-event-satisfier-assist=', Match_Data))
                            Red_Cards=len(re.findall('data-event-satisfier-redcard=', Match_Data))
                            Yellow_Cards=len(re.findall('data-event-satisfier-voidyellowcard=', Match_Data))+len(re.findall('data-event-satisfier-yellowcard=', Match_Data))
                            Sec_Yellow_Card=len(re.findall('data-event-satisfier-secondyellow=', Match_Data))
                            Penalty_Saved=len(re.findall('data-event-satisfier-keeperpenaltysaved=', Match_Data))
                            Shot_on_Post=len(re.findall('data-event-satisfier-shotonpost=', Match_Data))
                            Penalty_Miss=len(re.findall('data-event-satisfier-penaltymissed=', Match_Data))
                            Name = unidecode(stats[2].findChildren()[0].get_text().rstrip(' 01234567890()′'))
                            Position = stats[2].findChildren()[Col_length-1].get_text().strip(', ')
                            Age = stats[2].findChildren()[Col_length-2].get_text()
                            Sub_on=len(re.findall('data-event-satisfier-subon=', str(stats[2])))==1
                            Sub_off=len(re.findall('data-event-satisfier-suboff=', str(stats[2])))==1
                            if Rating=='-':
                                Rating='0'
                                Minutes_Played=0
                            elif not Sub_on and not Sub_off:
                                Minutes_Played=93
                            elif  Sub_on and not Sub_off:
                                Minutes_Played=95-int(stats[2].find("span", {"class": "player-meta-data"}).get_text().strip('′)('))
                            elif Sub_off and not Sub_on:
                                Minutes_Played=int(stats[2].find("span", {"class": "player-meta-data"}).get_text().strip('′)('))
                            elif Sub_on and Sub_off:
                                Minutes=int(stats[2].findAll("span", {"class": "player-meta-data"})[1].get_text().strip('′)('))-int(stats[2].findAll("span", {"class": "player-meta-data"})[0].get_text().strip('′)('))
                            stats_list=[Name,Age,Shots_Off_Target,Shots_on_Target,Key_passes,Rating,Goals,Assists,Penalties,Shot_on_Post,Penalty_Miss,Minutes_Played]
                                
                            if Name=="Wanderson" and AwayTeam=="FC Krasnodar":
                                Name=(Name+("1"))
                            elif Name=="Maicon" and AwayTeam=="Galatasaray":
                                Name=(Name+("1"))
                            elif Name=="Hakan Arslan" and AwayTeam=="Rizespor":
                                Name=(Name+("1"))
                            elif Name=="Gokhan Akkan" and AwayTeam=="Rizespor":
                                Name=(Name+("1"))
                            elif Name=="Juanfran" and AwayTeam=="Leganes":
                                Name=(Name+("1"))
                            elif Name=="Raul Garcia" and AwayTeam=="Leganes":
                                Name=(Name+("1"))
                            elif Name=="Sergio Alvarez" and AwayTeam=="Eibar":
                                Name=(Name+("1"))
                            elif Name=="Josue" and AwayTeam=="Kasimpasa":
                                Name=(Name+("1"))
                            elif Name=="Danny Ward" and AwayTeam=="Cardiff":
                                Name=(Name+("1"))
                           
                            else:
                                Name=Name

                            i+=1
                            ALLTHEDAMNPLAYERS[index] = []
                            ALLTHEDAMNPLAYERS[index].append(Name)
                            ALLTHEDAMNPLAYERS[index].append(AwayTeam)
                            ALLTHEDAMNPLAYERS[index].append(Age)
                            ALLTHEDAMNPLAYERS[index].append(Shots_Off_Target)
                            ALLTHEDAMNPLAYERS[index].append(Shots_on_Target)
                            ALLTHEDAMNPLAYERS[index].append(Key_passes)
                            ALLTHEDAMNPLAYERS[index].append(Rating)
                            ALLTHEDAMNPLAYERS[index].append(Goals)
                            ALLTHEDAMNPLAYERS[index].append(Assists)
                            ALLTHEDAMNPLAYERS[index].append(Penalties)
                            ALLTHEDAMNPLAYERS[index].append(Shot_on_Post)
                            ALLTHEDAMNPLAYERS[index].append(Penalty_Miss)
                            ALLTHEDAMNPLAYERS[index].append(Minutes_Played)
                            ALLTHEDAMNPLAYERS[index].append(Position)
                            index+=1
                            
                except ZeroDivisionError:
                    m_number-=1
                    print ('Error page without data', FinalURL)

            browser.quit()
       
        
        ln=13
        Summary_Table={}
        d = defaultdict(list)
        for value in ALLTHEDAMNPLAYERS.values():
            d[value[0]].extend(value[1:])
        
            
        Final_Dictionary=OrderedDict(sorted(d.items(), key=lambda t: t[1]))
        for key1, value1 in Final_Dictionary.items():
            if len(value1)>65:
                print(key1, len(value1), "  ****************************************************")
        excel_index = 2
        for key, val in Final_Dictionary.items():
            Summary_Table[key]=[]
            Summary_Table[key].append(val[0])
            Summary_Table[key].append(int(val[1]))
            Summary_Table[key].append(val[12])
            if len(val)==ln:
                Sum_Shots_Off_target=val[2]
                Sum_Shots_On_target=val[3]
                Sum_Key_passes=val[4]
                Sum_Goals=val[6]
                Sum_Assists=val[7]
                Sum_Penalties_scored=val[8]
                Sum_Shot_on_Post=val[9]
                Sum_Penalty_Miss=val[10]
                Sum_Minutes_Played=val[11]

                
                
                try:
                    Koef_Full_Match=Sum_Minutes_Played/93.0
                    Aver_Shots_Off_target=Sum_Shots_Off_target/Koef_Full_Match
                    Aver_Shots_On_target=Sum_Shots_On_target/Koef_Full_Match
                    Aver_Key_passes=Sum_Key_passes/Koef_Full_Match
                    Aver_Goals=Sum_Goals/Koef_Full_Match
                    Aver_Assists=Sum_Assists/Koef_Full_Match
                    Aver_Penalties_scored=Sum_Penalties_scored/Koef_Full_Match    
                    Aver_Minutes_Played=Sum_Minutes_Played/(len(val)/ln)
                    Average_Rating=float(val[5])/(len(val)/ln)




                    if Sum_Penalties_scored!=0 or Sum_Penalty_Miss!=0:
                        Penalty_Success_Rate=("%.2f" %((Sum_Penalties_scored/(Sum_Penalties_scored+Sum_Penalty_Miss)) * 100))
                    else:
                        Penalty_Success_Rate=0
                except ZeroDivisionError:
                    # print('Error - Zero div error(matches played-1) for player ', key)
                    Aver_Shots_Off_target=0
                    Aver_Shots_On_target=0
                    Aver_Key_passes=0
                    Aver_Goals=0
                    Aver_Assists=0
                    Aver_Penalties_scored=0    
                    Penalty_Success_Rate=0
                    Aver_Minutes_Played=0
                    Average_Rating=0
                
                Formula_za_5 = (Sum_Shots_On_target * 0.9 + Sum_Shot_on_Post + (Sum_Shots_Off_target - Sum_Shot_on_Post) * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists) + (Sum_Shots_On_target * 0.9 +  Sum_Shots_Off_target  * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists)
                Formula_za_3 = (Sum_Shots_On_target * 0.9 +  Sum_Shots_Off_target  * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists)
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!A$2:B$575;2;0)" % excel_index))
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!C$2:D$575;2;0)"% excel_index))
                excel_index+=1
                Summary_Table[key].append("%.2f" % Formula_za_5)
                Summary_Table[key].append("%.2f" % Formula_za_3)
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)
                Summary_Table[key].append(Sum_Shot_on_Post)
                Summary_Table[key].append(Sum_Penalties_scored)
                Summary_Table[key].append(str(Penalty_Success_Rate) + '%')
                
                #data for last 3 matches
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" %Average_Rating)

                #append data for last match Shotsoff, Shotson, KeyPasses, Goals, Assists, Minutes Played, Rating
                Summary_Table[key].append(val[3])
                Summary_Table[key].append(val[2])
                Summary_Table[key].append(val[4])
                Summary_Table[key].append(val[6])
                Summary_Table[key].append(val[7])
                Summary_Table[key].append(val[11])
                Summary_Table[key].append(val[5])

                
            elif len(val)==2*ln:
                Sum_Shots_Off_target=val[2+ln]+val[2]
                Sum_Shots_On_target=val[3]+val[3+ln]
                Sum_Key_passes=val[4]+val[4+ln]
                Sum_Goals=val[6]+val[6+ln]
                Sum_Assists=val[7]+val[7+ln]
                Sum_Penalties_scored=val[8]+val[8+ln]
                Sum_Shot_on_Post=val[9]+val[9+ln]
                Sum_Penalty_Miss=val[10]+val[10+ln]
                Sum_Minutes_Played=val[11]+val[11+ln]


                Sum3_Shots_Off_target=Sum_Shots_Off_target
                Sum3_Shots_On_target=Sum_Shots_On_target
                Sum3_Key_passes=Sum_Key_passes
                Sum3_Goals=Sum_Goals
                Sum3_Assists=Sum_Assists
                Sum3_Minutes_Played=Sum_Minutes_Played
                try:
                    Koef_Full_Match=Sum_Minutes_Played/93
                    Aver_Shots_Off_target=Sum_Shots_Off_target/Koef_Full_Match
                    Aver_Shots_On_target=Sum_Shots_On_target/Koef_Full_Match
                    Aver_Key_passes=Sum_Key_passes/Koef_Full_Match
                    Aver_Goals=Sum_Goals/Koef_Full_Match
                    Aver_Assists=Sum_Assists/Koef_Full_Match
                    Aver_Penalties_scored=Sum_Penalties_scored/Koef_Full_Match    
                    Aver_Minutes_Played=Sum_Minutes_Played/(len(val)/ln)
                    Average_Rating=(float(val[5])+float(val[5]))/(len(val)/ln)
                    if Sum_Penalties_scored!=0 or Sum_Penalty_Miss!=0:
                        Penalty_Success_Rate= ("%.2f" %((Sum_Penalties_scored/(Sum_Penalties_scored+Sum_Penalty_Miss))*100))
                    else:
                        Penalty_Success_Rate=0
                except ZeroDivisionError:
                    # print('Error Zero div error(matches played-2) for player ', key)
                    Aver_Shots_Off_target=0
                    Aver_Shots_On_target=0
                    Aver_Key_passes=0
                    Aver_Goals=0
                    Aver_Assists=0
                    Aver_Penalties_scored=0    
                    Penalty_Success_Rate=0
                    Aver_Minutes_Played=0
                    Average_Rating=0
                
                Formula_za_5 = (Sum_Shots_On_target * 0.9 + Sum_Shot_on_Post + (Sum_Shots_Off_target - Sum_Shot_on_Post) * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists) + (Sum_Shots_On_target * 0.9 + Sum_Shots_Off_target  * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists)
                Formula_za_3 = (Sum_Shots_On_target * 0.9 + Sum_Shots_Off_target  * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists)
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!A$2:B$575;2;0)" % excel_index))
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!C$2:D$575;2;0)"% excel_index))
                excel_index+=1
                Summary_Table[key].append("%.2f" % Formula_za_5)
                Summary_Table[key].append("%.2f" % Formula_za_3)
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)
                Summary_Table[key].append(Sum_Shot_on_Post)
                Summary_Table[key].append(Sum_Penalties_scored)
                Summary_Table[key].append(str(Penalty_Success_Rate)+'%')

                #data for last 3 matches
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)

                #append data for last match Shotsoff, Shotson, KeyPasses, Goals, Assists, Minutes Played, Rating
                Summary_Table[key].append(val[3])
                Summary_Table[key].append(val[2])
                Summary_Table[key].append(val[4])
                Summary_Table[key].append(val[6])
                Summary_Table[key].append(val[7])
                Summary_Table[key].append(val[11])
                Summary_Table[key].append(val[5])

                
                
            elif len(val)==3*ln:
                Sum_Shots_Off_target=val[2+ln]+val[2]+val[2+2*ln]
                Sum_Shots_On_target=val[3]+val[3+ln]+val[3+2*ln]
                Sum_Key_passes=val[4]+val[4+ln]+val[4+2*ln]
                Sum_Goals=val[6]+val[6+ln]+val[6+2*ln]
                Sum_Assists=val[7]+val[7+ln]+val[7+2*ln]
                Sum_Penalties_scored=val[8]+val[8+ln]+val[8+2*ln]
                Sum_Shot_on_Post=val[9]+val[9+ln]+val[9+2*ln]
                Sum_Penalty_Miss=val[10]+val[10+ln]+val[10+2*ln]
                Sum_Minutes_Played=val[11]+val[11+ln]+val[11+2*ln]


                Sum3_Shots_Off_target=Sum_Shots_Off_target
                Sum3_Shots_On_target=Sum_Shots_On_target
                Sum3_Key_passes=Sum_Key_passes
                Sum3_Goals=Sum_Goals
                Sum3_Assists=Sum_Assists
                Sum3_Minutes_Played=Sum_Minutes_Played
                try:    
                    Koef_Full_Match=Sum_Minutes_Played/93
                    Aver_Shots_Off_target=Sum_Shots_Off_target/Koef_Full_Match
                    Aver_Shots_On_target=Sum_Shots_On_target/Koef_Full_Match
                    Aver_Key_passes=Sum_Key_passes/Koef_Full_Match
                    Aver_Goals=Sum_Goals/Koef_Full_Match
                    Aver_Assists=Sum_Assists/Koef_Full_Match
                    Aver_Penalties_scored=Sum_Penalties_scored/Koef_Full_Match    
                    Aver_Shot_on_Post=Sum_Shot_on_Post/Koef_Full_Match
                    
                    Aver_Minutes_Played=Sum_Minutes_Played/(len(val)/ln)
                    Average_Rating=(float(val[5])+float(val[5+ln])+float(val[5+2*ln]))/(len(val)/ln)
                    if Sum_Penalties_scored!=0 or Sum_Penalty_Miss!=0:
                        Penalty_Success_Rate=("%.2f" %((Sum_Penalties_scored/(Sum_Penalties_scored+Sum_Penalty_Miss))*100))
                    else:
                        Penalty_Success_Rate=0

                except ZeroDivisionError:
                    # print('Error Zero div error(matches played-3) for player ', key)
                    Aver_Shots_Off_target=0
                    Aver_Shots_On_target=0
                    Aver_Key_passes=0
                    Aver_Goals=0
                    Aver_Assists=0
                    Aver_Penalties_scored=0    
                    Aver_Shot_on_Post=0
                    Penalty_Success_Rate=0
                    Aver_Minutes_Played=0
                    Average_Rating=0
                
                Formula_za_5 = (Sum_Shots_On_target * 0.9 + Sum_Shot_on_Post + (Sum_Shots_Off_target - Sum_Shot_on_Post) * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists) + (Sum_Shots_On_target * 0.9 + Sum_Shots_Off_target * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists)
                Formula_za_3 = (Sum_Shots_On_target * 0.9 +  Sum_Shots_Off_target  * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists)
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!A$2:B$575;2;0)" % excel_index))
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!C$2:D$575;2;0)"% excel_index))
                excel_index+=1
                Summary_Table[key].append("%.2f" % Formula_za_5)
                Summary_Table[key].append("%.2f" % Formula_za_3)
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)
                Summary_Table[key].append(Sum_Shot_on_Post)
                Summary_Table[key].append(Sum_Penalties_scored)
                Summary_Table[key].append(str(Penalty_Success_Rate)+'%')

                #data for last 3 matches
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)

                #append data for last match Shotsoff, Shotson, KeyPasses, Goals, Assists, Minutes Played, Rating
                Summary_Table[key].append(val[3])
                Summary_Table[key].append(val[2])
                Summary_Table[key].append(val[4])
                Summary_Table[key].append(val[6])
                Summary_Table[key].append(val[7])
                Summary_Table[key].append(val[11])
                Summary_Table[key].append(val[5])

                
            elif len(val)==4*ln:
                Sum_Shots_Off_target=val[2+ln]+val[2]+val[2+2*ln]+val[2+3*ln]
                Sum_Shots_On_target=val[3]+val[3+ln]+val[3+2*ln]+val[3+3*ln]
                Sum_Key_passes=val[4]+val[4+ln]+val[4+2*ln]+val[4+3*ln]
                Sum_Goals=val[6]+val[6+ln]+val[6+2*ln]+val[6+3*ln]
                Sum_Assists=val[7]+val[7+ln]+val[7+2*ln]+val[7+3*ln]
                Sum_Penalties_scored=val[8]+val[8+ln]+val[8+2*ln]+val[8+3*ln]
                Sum_Shot_on_Post=val[9]+val[9+ln]+val[9+2*ln]+val[9+3*ln]
                Sum_Penalty_Miss=val[10]+val[10+ln]+val[10+2*ln]+val[10+3*ln]
                Sum_Minutes_Played=val[11]+val[11+ln]+val[11+2*ln]+val[11+3*ln]

                Sum3_Shots_Off_target=val[2+ln]+val[2]+val[2+2*ln]
                Sum3_Shots_On_target=val[3]+val[3+ln]+val[3+2*ln]
                Sum3_Key_passes=val[4]+val[4+ln]+val[4+2*ln]
                Sum3_Goals=val[6]+val[6+ln]+val[6+2*ln]
                Sum3_Assists=val[7]+val[7+ln]+val[7+2*ln]
                Sum3_Minutes_Played=val[11]+val[11+ln]+val[11+2*ln]

                try:
                    Koef3_Full_Match=Sum3_Minutes_Played/93
                    Aver3_Shots_Off_target=Sum3_Shots_Off_target/Koef3_Full_Match
                    Aver3_Shots_On_target=Sum3_Shots_On_target/Koef3_Full_Match
                    Aver3_Key_passes=Sum3_Key_passes/Koef3_Full_Match
                    Aver3_Goals=Sum3_Goals/Koef3_Full_Match
                    Aver3_Assists=Sum3_Assists/Koef3_Full_Match
                    Aver3_Minutes_Played=Sum3_Minutes_Played/3
                    Average3_Rating=(float(val[5])+float(val[5+ln])+float(val[5+2*ln]))/3
                except ZeroDivisionError:
                    # print("Error Player not played last3 matches", key)
                    Aver3_Shots_Off_target=0
                    Aver3_Shots_On_target=0
                    Aver3_Key_passes=0
                    Aver3_Goals=0
                    Aver3_Assists=0
                    Aver3_Minutes_Played=0
                    Average3_Rating=0
                try:    
                    Koef_Full_Match=Sum_Minutes_Played/93
                    Aver_Shots_Off_target=Sum_Shots_Off_target/Koef_Full_Match
                    Aver_Shots_On_target=Sum_Shots_On_target/Koef_Full_Match
                    Aver_Key_passes=Sum_Key_passes/Koef_Full_Match
                    Aver_Goals=Sum_Goals/Koef_Full_Match
                    Aver_Assists=Sum_Assists/Koef_Full_Match
                    Aver_Penalties_scored=Sum_Penalties_scored/Koef_Full_Match    
                    Aver_Shot_on_Post=Sum_Shot_on_Post/Koef_Full_Match
                    Aver_Minutes_Played=Sum_Minutes_Played/(len(val)/ln)
                    Average_Rating=(float(val[5])+float(val[5+ln])+float(val[5+2*ln])+float(val[5+3*ln]))/(len(val)/ln)

                    if Sum_Penalties_scored!=0 or Sum_Penalty_Miss!=0:
                        Penalty_Success_Rate=("%.2f" %((Sum_Penalties_scored/(Sum_Penalties_scored+Sum_Penalty_Miss))*100))
                    else:
                        Penalty_Success_Rate=0

                except ZeroDivisionError:
                    # print('error Zero div error(matches played-4) for player ', key)
                    Aver_Shots_Off_target=0
                    Aver_Shots_On_target=0
                    Aver_Key_passes=0
                    Aver_Goals=0
                    Aver_Assists=0
                    Aver_Penalties_scored=0    
                    Aver_Shot_on_Post=0
                    Penalty_Success_Rate=0
                    Aver_Minutes_Played=0
                    Average_Rating=0
                
                Formula_za_5 = (Sum_Shots_On_target * 0.9 + Sum_Shot_on_Post + (Sum_Shots_Off_target - Sum_Shot_on_Post) * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists) + (Sum3_Shots_On_target * 0.9  + Sum3_Shots_Off_target * 0.7 + Sum3_Key_passes * 0.54 + Sum3_Goals * 1.5 + Sum3_Assists)
                Formula_za_3 = (Sum3_Shots_On_target * 0.9 +  Sum3_Shots_Off_target * 0.7 + Sum3_Key_passes * 0.54 + Sum3_Goals * 1.5 + Sum3_Assists)
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!A$2:B$575;2;0)" % excel_index))
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!C$2:D$575;2;0)"% excel_index))
                excel_index+=1
                Summary_Table[key].append("%.2f" % Formula_za_5)
                Summary_Table[key].append("%.2f" % Formula_za_3)
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)
                Summary_Table[key].append(Sum_Shot_on_Post)
                Summary_Table[key].append(Sum_Penalties_scored)
                Summary_Table[key].append(str(Penalty_Success_Rate)+'%')

                #data for last 3 matches
                Summary_Table[key].append(Sum3_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver3_Shots_On_target)
                Summary_Table[key].append(Sum3_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver3_Shots_Off_target)
                Summary_Table[key].append(Sum3_Key_passes)
                Summary_Table[key].append("%.2f" % Aver3_Key_passes)
                Summary_Table[key].append(Sum3_Goals)
                Summary_Table[key].append("%.2f" % Aver3_Goals)
                Summary_Table[key].append(Sum3_Assists)
                Summary_Table[key].append("%.2f" % Aver3_Assists)
                Summary_Table[key].append(Sum3_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver3_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average3_Rating)

                #append data for last match Shotsoff, Shotson, KeyPasses, Goals, Assists, Minutes Played, Rating
                Summary_Table[key].append(val[3])
                Summary_Table[key].append(val[2])
                Summary_Table[key].append(val[4])
                Summary_Table[key].append(val[6])
                Summary_Table[key].append(val[7])
                Summary_Table[key].append(val[11])
                Summary_Table[key].append(val[5])

            else:
                Sum_Shots_Off_target=val[2+ln]+val[2]+val[2+2*ln]+val[2+3*ln]+val[2+4*ln]
                Sum_Shots_On_target=val[3]+val[3+ln]+val[3+2*ln]+val[3+3*ln]+val[3+4*ln]
                Sum_Key_passes=val[4]+val[4+ln]+val[4+2*ln]+val[4+3*ln]+val[4+4*ln]
                Sum_Goals=val[6]+val[6+ln]+val[6+2*ln]+val[6+3*ln]+val[6+4*ln]
                Sum_Assists=val[7]+val[7+ln]+val[7+2*ln]+val[7+3*ln]+val[7+4*ln]
                Sum_Penalties_scored=val[8]+val[8+ln]+val[8+2*ln]+val[8+3*ln]+val[8+4*ln]
                Sum_Shot_on_Post=val[9]+val[9+ln]+val[9+2*ln]+val[9+3*ln]+val[9+4*ln]
                Sum_Penalty_Miss=val[10]+val[10+ln]+val[10+2*ln]+val[10+3*ln]+val[10+4*ln]
                Sum_Minutes_Played=val[11]+val[11+ln]+val[11+2*ln]+val[11+3*ln]+val[11+4*ln]

                Sum3_Shots_Off_target=val[2+ln]+val[2]+val[2+2*ln]
                Sum3_Shots_On_target=val[3]+val[3+ln]+val[3+2*ln]
                Sum3_Key_passes=val[4]+val[4+ln]+val[4+2*ln]
                Sum3_Goals=val[6]+val[6+ln]+val[6+2*ln]
                Sum3_Assists=val[7]+val[7+ln]+val[7+2*ln]
                Sum3_Penalties_scored=val[8]+val[8+ln]+val[8+2*ln]
                Sum3_Minutes_Played=val[11]+val[11+ln]+val[11+2*ln]
                try:
                    Koef3_Full_Match=Sum3_Minutes_Played/93
                    Aver3_Shots_Off_target=Sum3_Shots_Off_target/Koef3_Full_Match
                    Aver3_Shots_On_target=Sum3_Shots_On_target/Koef3_Full_Match
                    Aver3_Key_passes=Sum3_Key_passes/Koef3_Full_Match
                    Aver3_Goals=Sum3_Goals/Koef3_Full_Match
                    Aver3_Assists=Sum3_Assists/Koef3_Full_Match
                    Aver3_Minutes_Played=Sum3_Minutes_Played/3
                    Average3_Rating=(float(val[5])+float(val[5+ln])+float(val[5+2*ln]))/3
                except ZeroDivisionError:
                    # print("Error Player not played last3 matches", key)
                    Aver3_Shots_Off_target=0
                    Aver3_Shots_On_target=0
                    Aver3_Key_passes=0
                    Aver3_Goals=0
                    Aver3_Assists=0
                    Aver3_Minutes_Played=0
                    Average3_Rating=0

                try:    
                    Koef_Full_Match=Sum_Minutes_Played/93
                    Aver_Shots_Off_target=Sum_Shots_Off_target/Koef_Full_Match
                    Aver_Shots_On_target=Sum_Shots_On_target/Koef_Full_Match
                    Aver_Key_passes=Sum_Key_passes/Koef_Full_Match
                    Aver_Goals=Sum_Goals/Koef_Full_Match
                    Aver_Assists=Sum_Assists/Koef_Full_Match
                    Aver_Penalties_scored=Sum_Penalties_scored/Koef_Full_Match    
                    Aver_Shot_on_Post=Sum_Shot_on_Post/Koef_Full_Match
                    Aver_Minutes_Played=Sum_Minutes_Played/(len(val)/ln)
                    Average_Rating=(float(val[5])+float(val[5+ln])+float(val[5+2*ln])+float(val[5+3*ln])+float(val[5+4*ln]))/(len(val)/ln)

                    if Sum_Penalties_scored!=0 or Sum_Penalty_Miss!=0:
                        Penalty_Success_Rate=("%.2f" %((Sum_Penalties_scored/(Sum_Penalties_scored+Sum_Penalty_Miss))*100))
                    else:
                        Penalty_Success_Rate=0

                except ZeroDivisionError:
                    # print('Error Zero div error(matches played-5 or more) for player ', key)
                    Aver_Shots_Off_target=0
                    Aver_Shots_On_target=0
                    Aver_Key_passes=0
                    Aver_Goals=0
                    Aver_Assists=0
                    Aver_Penalties_scored=0    
                    Aver_Shot_on_Post=0
                    Penalty_Success_Rate=0
                    Aver_Minutes_Played=0
                    Average_Rating=0

                Formula_za_5 = (Sum_Shots_On_target * 0.9 + Sum_Shot_on_Post + (Sum_Shots_Off_target - Sum_Shot_on_Post) * 0.7 + Sum_Key_passes * 0.54 + Sum_Goals * 1.5 + Sum_Assists) + (Sum3_Shots_On_target * 0.9 + Sum3_Shots_Off_target * 0.7 + Sum3_Key_passes * 0.54 + Sum3_Goals * 1.5 + Sum3_Assists)
                Formula_za_3 = (Sum3_Shots_On_target * 0.9 +  Sum3_Shots_Off_target * 0.7 + Sum3_Key_passes * 0.54 + Sum3_Goals * 1.5 + Sum3_Assists)
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!A$2:B$575;2;0)" % excel_index))
                Summary_Table[key].append(("55=VLOOKUP(A%s;Sports!C$2:D$575;2;0)"% excel_index))
                excel_index+=1
                Summary_Table[key].append("%.2f" % Formula_za_5)
                Summary_Table[key].append("%.2f" % Formula_za_3)
                Summary_Table[key].append(Sum_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_On_target)
                Summary_Table[key].append(Sum_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver_Shots_Off_target)
                Summary_Table[key].append(Sum_Key_passes)
                Summary_Table[key].append("%.2f" % Aver_Key_passes)
                Summary_Table[key].append(Sum_Goals)
                Summary_Table[key].append("%.2f" % Aver_Goals)
                Summary_Table[key].append(Sum_Assists)
                Summary_Table[key].append("%.2f" % Aver_Assists)
                Summary_Table[key].append(Sum_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average_Rating)
                Summary_Table[key].append(Sum_Shot_on_Post)
                Summary_Table[key].append(Sum_Penalties_scored)
                Summary_Table[key].append(str(Penalty_Success_Rate)+'%')

                #data for last 3 matches
                Summary_Table[key].append(Sum3_Shots_On_target)
                Summary_Table[key].append("%.2f" % Aver3_Shots_On_target)
                Summary_Table[key].append(Sum3_Shots_Off_target)
                Summary_Table[key].append("%.2f" % Aver3_Shots_Off_target)
                Summary_Table[key].append(Sum3_Key_passes)
                Summary_Table[key].append("%.2f" % Aver3_Key_passes)
                Summary_Table[key].append(Sum3_Goals)
                Summary_Table[key].append("%.2f" % Aver3_Goals)
                Summary_Table[key].append(Sum3_Assists)
                Summary_Table[key].append("%.2f" % Aver3_Assists)
                Summary_Table[key].append(Sum3_Minutes_Played)
                Summary_Table[key].append("%.2f" % Aver3_Minutes_Played)
                Summary_Table[key].append("%.2f" % Average3_Rating)

                #append data for last match Shotsoff, Shotson, KeyPasses, Goals, Assists, Minutes Played, Rating
                Summary_Table[key].append(val[3])
                Summary_Table[key].append(val[2])
                Summary_Table[key].append(val[4])
                Summary_Table[key].append(val[6])
                Summary_Table[key].append(val[7])
                Summary_Table[key].append(val[11])
                Summary_Table[key].append(val[5])
        # replacing all dots on commas for googedocs
        Fin_Dict={}
        for key, value in Summary_Table.items():
            value_sec = [str(w).replace('.', ',') for w in value[5:]]
            value = value[0:5] + value_sec
            Fin_Dict[key] = value
            
        
        with open('%s_LAST5.csv' % League, 'w', newline='', encoding='utf-16') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([u"Имя",u"Команда",u"Возраст", u"Позиция", u"Цена Sports", u"Позиция Sports", u"Формула5",  u"Формула3", u"Cтвор5", u"Створ/Матч5", u"Уд.Мимо5", u"Мимо/Матч5",u"Кл.пасы5",u"Кл.пасы/Матч5",u"Голы5",
             u"Гол/Матч5",u"Ассисты5",u"Ассисты/Матч5",u"Минут5",u"Минут/Матч5", u"Ср.рейтинг5", u"Штанг5",u"Пенал", u"% Усп.Пен",u"Cтвор3",u"Створ/Матч3",u"ΣУд.Мимо3",u"Мимо/Матч3",u"Кл.пасы3",u"Кл.пасы/Матч3",u"Голы3",
             u"Гол/Матч3",u"Ассисты3",u"Ассисты/Матч3",u"Минут3",u"Минут/Матч3", u"Ср.рейтинг3",u"CтворПосл", u"Уд.Мимо Посл",u"Кл.пасыПосл",u"ГолыПосл",
             u"АссистыПосл",u"МинутПосл",u"РейтингПосл",])
            for key, val in Fin_Dict.items():
                    writer.writerow([key]+ val)

        Start_number+=1

        
time_end=datetime.now()
print(time_end - time_start)        

    

