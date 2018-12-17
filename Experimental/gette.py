#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import os
from unidecode import unidecode
def parsing(s, number):
 #   s = re.sub(r'\\x5Cu00e1', 'a', s)
 #   s = re.sub(r'\\x5Cu00d6', 'O', s)
  #  s = re.sub(r'\\x5Cu00e9', 'e', s)
   # s = re.sub(r'\\x5Cu00df', 's', s)
    #s = re.sub(r'\\x5Cu00fc', 'u', s)
#    s = re.sub(r'\\x5Cu00f6', 'o', s)
 #   s = re.sub(r'\\x5Cu00c1', 'A', s)
  #  s = re.sub(r'\\x5Cu00f8', 'o', s)
   # s = re.sub(r'\\x5Cu00ed', 'i', s)c
    #s = re.sub(r'\\x5Cu00f3', 'o', s)
#    s = re.sub(r'\\x5Cu00e3', 'a', s)
    
    s = s.replace(',', ';')
    s = s.replace('.', ',')

    s = re.sub(r'\\x..', ' ', s)
    s = re.sub(r'\s*<.*>', '', s)

    for i in range(1,5):
        s = s.replace('  ', ' ')

    s = re.sub(r'(.... id )', '\nid ', s)
    s = s.replace(' ; ', ';')
    s = s.replace(';\n', '\n')
    s = re.sub(r'par\nid', '', s)
    s = re.sub(r""" \'\)""", '', s)
    s = re.sub(r'\t.*', '\n', s)
    s = re.sub(r'\n\n', '', s)
    s = re.sub(r'a\n' , '\n', s)
    s = re.sub(r'\Z' , '\n', s)
    
    s = re.sub(r';.*? ',';', s) #заголовки
    s = re.sub(r'\n',';' + str(number) + '\n', s) # номер матча

    return s

def open_file(fname):
    f = open(str(fname) + '.html','r')
    s = f.read()
    f.close()
    return s

def del_file(fname):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(fname) + '.html')
    os.remove(path)

def get_site(start, end):
    for i in range(start, end):
        url = 'https://understat.com/match/' + str(i)
        r = requests.get(url)
        s = unidecode(r.text)
        s1 = s.encode('utf-8')

        f = open (str(i) + '.html', 'wb')
        f.write(s1) 
        f.close() 

start_game = 10693  # с какого номера скачать матчи
end_game = 10702  # по какой 

end_game = end_game + 1

f = open('End.csv', 'w')    #обнуление итоговой страницы
f.close()                   #

get_site(start_game, end_game)

f = open('End.csv', 'a')

f_top = open('top.txt', 'r')
s_top = str(f_top.read())
f_top.close()

f.write(s_top)

for i in range(start_game, end_game):
    f.write(parsing(open_file(i), i))
    # del_file(i) #удаление html файлов

f.close()
