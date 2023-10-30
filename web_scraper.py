# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 16:08:39 2021

@author: krishnan
"""

import unittest, time, re, codecs, os
from bs4 import BeautifulSoup
from datetime import timedelta, date

path = "jabalpur/"

dates = []
start_date = date(2022,1,1)
end_date = date(2023,10,20)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

for single_date in daterange(start_date, end_date):
    date_value = single_date.strftime("%d/%m/%Y")
    dates.append(date_value)

for date_value in dates:
    data=date_value.split("/")
    directory = path+data[2]+"/"+data[0]+"-"+data[1]+"-"+data[2]+"/"
    for file in os.listdir(directory):
        f = open(directory+file,"r")
        soup = BeautifulSoup(f.read(),"lxml")
        table = soup.find("table", { "id" : "ContentPlaceHolder1_GrdFoundPS" })
        try:
            lightrows = table.findAll("tr")
            for k in range(1,len(lightrows)-2):
                columns = lightrows[k].findAll("span")
                date_format =  file.split(".")[0].split("-")
                out='"'+date_format[0]+"-"+date_format[1]+"-"+date_format[2]+'",'
                for column in columns:
                    out=out+'"'+column.text+'",'
                print(out)
        except:
            pass