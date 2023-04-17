from bs4 import BeautifulSoup
from datetime import datetime
from sys import platform
import os.path
import requests
import csv
import time
import os
import shutil
import random
import sys

#Searches for articles related to user input
def search(input):
    for news in news_list:
        if input.lower() not in news[0].lower():
            news_list.remove(news)
            search(input)

#Checks for duplicate articles in the list
def checkDuplicates(list):
    for i in list:
        if i not in newList:
            newList.append(i)

def abcNews():
    source = requests.get('https://www.abc.net.au/news/').text
    soup = BeautifulSoup(source, 'html.parser')
    headlines = soup.find_all(class_ = '_37gvg u0kBv _3CtDL _1_pW8 _3Fvo9 VjkbJ')

    for headline in headlines:
        news_list.append([headline.text, "https://abc.net.au" + headline['href']])

def theGuardian():
    source = requests.get('https://www.theguardian.com/au/').text
    soup = BeautifulSoup(source, 'html.parser')
    headlines = soup.find_all(class_ = 'u-faux-block-link__overlay js-headline-text')

    for headline in headlines:
        news_list.append([headline.text, headline['href']])

def nineNews():
    source = requests.get('https://www.9news.com.au/').text
    soup = BeautifulSoup(source, 'html.parser')
    headlines = soup.find_all(class_ = 'story__link story__wrapper')

    for headline in headlines:
        news_list.append([headline.text, headline['href']])

def newscom():
    source = requests.get('https://www.news.com.au/').text
    soup = BeautifulSoup(source, 'html.parser')
    headlines = soup.find_all(class_ = 'storyblock_title_link')

    for headline in headlines:
        news_list.append([headline.text, headline['href']])

def perthnow():
    source = requests.get('https://www.perthnow.com.au/news').text
    soup = BeautifulSoup(source, 'html.parser')
    headlines = soup.find_all(class_ = 'Card-Header css-nio7fb-StyledHeader egbh3fx1')

    for headline in headlines:
        news_list.append([headline.text, "https://www.perthnow.com.au" + headline['href']])

#Populates array with news
def populate():
    abcNews()
    theGuardian()
    nineNews()
    newscom()
    perthnow()
    
#csv contents
headers = ["Headline", "URL"]
news_list = []

input1 = input("What news do you want to see today? ")

populate()

search(input1)

newList = []
checkDuplicates(news_list)
news_list = newList
random.shuffle(news_list)

today = datetime.today()
name = "todays_news_list.csv"
new_path = today.strftime("%d-%m-%Y %Hh%Mm") + ".csv"

#Checks if its first-time setup. Creates Archives folder.
if os.path.exists(name) == False:
    with open(name, "w") as news:
        news_articles = csv.writer(news)
        news_articles.writerow(headers)
        news_articles.writerows(news_list)
    os.mkdir('Archives')
    print("Searching for articles...")
    time.sleep(2)
    print("File Created.")
    print("Opening File...")
    time.sleep(1)
    if platform == "linux" or platform == "linux2":
	    os.system("xdg-open todays_news_list.csv")
    else:
    	os.system("start EXCEL.exe todays_news_list.csv")
    
#Archives old csv file. Deletes duplicates otherwise doesnt execute.
else:
    os.rename("todays_news_list.csv", new_path)
    try:
        shutil.move(new_path, "Archives")
    except shutil.Error:
        input2 = input("There is a duplicate file in the 'Archives' folder. Would you like to overwrite? (Y/N or Yes/No) ")
        if (input2.lower() == "yes" or input2.lower() == 'y'):
            os.remove("Archives/" + new_path)
            shutil.move(new_path, "Archives")
        else:
            os.rename(new_path, "todays_news_list.csv")
            print("Please rerun program in 1 minute.")
            time.sleep(1)
            sys.exit()

    #Creates current csv file and opens it.
    with open(name, "w") as news:
        news_articles = csv.writer(news)
        news_articles.writerow(headers)
        news_articles.writerows(news_list)
    print("Searching for articles...")
    time.sleep(2)
    print("File Created.")
    print("Opening File...")
    time.sleep(1)
    if platform == "linux" or platform == "linux2":
	    os.system("xdg-open todays_news_list.csv")
    else:
	    os.system("start EXCEL.exe todays_news_list.csv")
