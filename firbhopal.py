# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, codecs, os
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from datetime import timedelta, date

dates = []
start_date = date(2017,9,29)
end_date = date(2018,1,1)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def parse_html(html,date_value):
    soup = BeautifulSoup(html,"lxml")
    table = soup.find("table", { "id" : "ContentPlaceHolder1_GrdFoundPS" })
    lightrows = table.findAll("tr", { "class" : "lightrow" })
    darkrows = table.findAll("tr", { "class" : "darkrow" })
    for row in lightrows:
        columns = row.findAll("span")
        out='"'+date_value+'",'
        for column in columns:
            out=out+'"'+column.text+'",'
        print (out)
    for row in darkrows:
        columns = row.findAll("span")
        out='"'+date_value+'",'
        for column in columns:
            out=out+'"'+column.text+'",'
        print (out)

for single_date in daterange(start_date, end_date):
    date_value = single_date.strftime("%d/%m/%Y")
    dates.append(date_value)

class TsCrawler(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'G:\Shubhangi\Internships 2021\CPA\chromedriver')
        self.driver.implicitly_wait(1)
        self.base_url = "https://citizen.mppolice.gov.in"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_ts_crawler(self):
        driver = self.driver
        driver.get(self.base_url + "/Custom_Arrested_Person.aspx")
        time.sleep(2)
        select = Select(driver.find_elements_by_id('ContentPlaceHolder1_ddlDistrict')[0])
        select.select_by_value('21323')
        time.sleep(10)
        for date_value in dates:
            driver.execute_script("document.getElementById('ContentPlaceHolder1_txtStartDate').value ='"+date_value+"'")
            driver.execute_script("document.getElementById('ContentPlaceHolder1_txtEndDate').value = '"+date_value+"'")
            driver.find_elements_by_id('ContentPlaceHolder1_btnSearch')[0].click()
            time.sleep(7)
            html = driver.page_source
            name = date_value.replace("/","-")+"-"+str(1)
            ofile = codecs.open("G:/Shubhangi/Internships 2021/CPA/devas/" + name + ".html", "w", "utf-8")
            ofile.write(html)
            ofile.close()
            parse_html(html, date_value)
            try:
                for i in range(2,10):
                    driver.execute_script("javascript:__doPostBack('ctl00$ContentPlaceHolder1$GrdFoundPS','Page$"+str(i)+"')")
                    time.sleep(10)
                    html = driver.page_source
                    name = date_value.replace("/","-")+"-"+str(i)
                    ofile = codecs.open("G:/Shubhangi/Internships 2021/CPA/devas/"+name+".html","w","utf-8")
                    ofile.write(html)
                    ofile.close()
                    parse_html(html,date_value)
            except:
                pass
            driver.get(self.base_url + "/Custom_Arrested_Person.aspx")
            time.sleep(2)
            select = Select(driver.find_elements_by_id('ContentPlaceHolder1_ddlDistrict')[0])
            select.select_by_value('21323')
            time.sleep(2)
        
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
