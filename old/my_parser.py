# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 11:46:42 2021

@author: krishnan
"""
import pandas as pd
import unittest, time, re, codecs, os
from bs4 import BeautifulSoup
from datetime import timedelta, date

path = "devas/"

dates = []
start_date = date(2022,1,1)
end_date = date(2023,10,21)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

for single_date in daterange(start_date, end_date):
    date_value = single_date.strftime("%d/%m/%Y")
    dates.append(date_value)

for date_value in dates:
    data=date_value.split("/")
    directory = path
    for file in os.listdir('C:/Users/Shubhangi/CPA Project/CPA 2023/devas/'):
        f = open(directory+file,"r",encoding="UTF-8")
        outfile = codecs.open('C:/Users/Shubhangi/CPA Project/CPA 2021/d.csv','a','utf-8')
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
                outfile.write(out+"\n")
        except:
            pass