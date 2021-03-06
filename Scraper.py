from typing import final
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
import pandas as pd

START_URL="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome(r"C:/Users/ALLEN DSILVA/Downloads/Phyton codes/P127/chromedriver_win32/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers=["Proper name","Distance","Mass","Radius","hyperlink"]
planet_data=[]
new_planet_data=[]

def scrape():
    
    for i in range(0,489):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index,li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    
def scrape_more_data(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content,"html.parser")
    templist=[]
    for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
        td_tags=tr_tag.find_all("td")
        for td_tag in td_tags:
            try:
                templist.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                templist.append("")
    new_planet_data.append(templist)


scrape()

for data in planet_data:
    scrape_more_data(data[5])
final_planet_data=[]
for index,data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])
with open("final.csv","w")as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)




