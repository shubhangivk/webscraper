#Importing all the necessary packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from tqdm import tqdm
import urllib3

# Ignoring all warnings
import warnings
warnings.filterwarnings('ignore')

# Decrease security level for SSL
urllib3.disable_warnings()
urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'


# In[2]:


#Ignoring all warnings
import warnings
warnings.filterwarnings('ignore')


# In[3]:


url = 'https://citizen.mppolice.gov.in/Custom_Arrested_Person.aspx'


# In[4]:


list_days = list(range(1,32))
days = ["{:02}".format(num) for num in list_days]


# In[5]:


list_months = list(range(1,13))
months = ["{:02}".format(num) for num in list_months]


# In[18]:


#Enter range of required years here 
list_years = list(range(2022,2024))
years = ["{:02}".format(num) for num in list_years]


# In[19]:

#DON'T CHANGE!
#Function to scrape the first page of every day in a given year
def all_days(url, month, year, district):
    with requests.Session() as req:
        req.headers['user-agent'] = 'Mozilla/5.0'
        r = req.get(url, verify=False)
        soup = BeautifulSoup(r.content, 'lxml')
        df = None
        for day in days:
            date = '{}/{}/{}'.format(day, month, year)
            payload = {
            #     "__LASTFOCUS": ""
                "__EVENTTARGET": "",
                '__EVENTARGUMENT': '',
                "ctl00$hdnSessionIdleTime": "",
                "ctl00$hdnUserUniqueId": "",
                "ctl00$ContentPlaceHolder1$ddlDistrict": "{}".format(district),
                "ctl00$ContentPlaceHolder1$ddlPoliceStation": "",
                "ctl00$ContentPlaceHolder1$txtStartDate": "{}".format(date),
                "ctl00$ContentPlaceHolder1$meeSecurityAnswer1_ClientState": "",
                "ctl00$ContentPlaceHolder1$txtEndDate": "{}".format(date),
                "ctl00$ContentPlaceHolder1$txtEndDate_MaskedEditExtender_ClientState": "",
                "ctl00$ContentPlaceHolder1$txtmissing_name":"",
                "ctl00$ContentPlaceHolder1$btnSearch": "खोजें"

            }
            payload['__VIEWSTATE'] = soup.find("input", id="__VIEWSTATE").get("value")
            payload['__EVENTVALIDATION'] = soup.find(
            "input", id="__EVENTVALIDATION").get("value")
            r = req.post(url, data=payload)
            try:
                df1 = pd.read_html(r.content, attrs={
                              'id': 'ContentPlaceHolder1_GrdFoundPS'})[0]
                df1['date'] = date
                df1['year'] = year  
                if df is None:
                    df = df1
                else:
                    df = df._append(df1)
            except:
                pass 
        return df


# In[20]:


#DON'T CHANGE!
def missing_days(url, district, page, missing_dates):
    with requests.Session() as req:
        req.headers['user-agent'] = 'Mozilla/5.0'
        r = req.get(url, verify=False)
        soup = BeautifulSoup(r.content, 'lxml')
        df = None
        for day in tqdm(missing_dates):
            payload = {
            #     "__LASTFOCUS": ""
                "__EVENTTARGET": "ctl00$ContentPlaceHolder1$GrdFoundPS",
                '__EVENTARGUMENT': 'Page${}'.format(page), #Change to 3 when required
                "ctl00$hdnSessionIdleTime": "",
                "ctl00$hdnUserUniqueId": "",
                "ctl00$ContentPlaceHolder1$ddlDistrict": "{}".format(district),
                "ctl00$ContentPlaceHolder1$ddlPoliceStation": "",
                "ctl00$ContentPlaceHolder1$txtStartDate": "{}".format(day),
                "ctl00$ContentPlaceHolder1$meeSecurityAnswer1_ClientState": "",
                "ctl00$ContentPlaceHolder1$txtEndDate": "{}".format(day),
                "ctl00$ContentPlaceHolder1$txtEndDate_MaskedEditExtender_ClientState": "",
                "ctl00$ContentPlaceHolder1$txtmissing_name":"",
#                 "ctl00$ContentPlaceHolder1$btnSearch": "खोजें"

            }
            payload['__VIEWSTATE'] = soup.find("input", id="__VIEWSTATE").get("value")
            payload['__EVENTVALIDATION'] = soup.find(
            "input", id="__EVENTVALIDATION").get("value")
            r = req.post(url, data=payload)
            try:
                df1 = pd.read_html(r.content, attrs={
                              'id': 'ContentPlaceHolder1_GrdFoundPS'})[0]
                df1['date'] = day
                year = re.findall(r'\d+/\d+/(.+)', day)
                df1['year'] = year[0] 
                if df is None:
                    df = df1
                else:
                    df = df._append(df1)
            except:
                pass
#         df['year'] = year    
        return df


# In[21]:


def p_ones(district_no):
    district = None
    for year in tqdm(years):
        for month in tqdm(months):
            df = all_days(url, month, year, district_no) #Enter district code here
            if district is None:
                district = df
            else:
                district = district._append(df)
    return district


# In[22]:


def p_rest(district, district_no):
    zila = district.जिला.values[0]            
    missing_dates_df = district[district.जिला != zila]
    missing_dates = missing_dates_df.date.values
    p_t = missing_dates_df.जिला.unique()
    p_n = sorted(p_t, key = len)
    sage = 2
    md = None
    for i in range(len(p_n)):
        df_2 = missing_days(url, district_no, sage, missing_dates)
        missing_dates_df = missing_dates_df[missing_dates_df.जिला != p_n[i]]
#         print(len(missing_dates_df))
#         print(p_n[i])
        missing_dates = missing_dates_df.date.values
#         print(len(missing_dates))
        sage += 1
#         print(sage)
        if md is None:
                md = df_2
        else:
                md = md._append(df_2)
    return md


# In[23]:


def autoscraper(district_no):
    o = p_ones(district_no)
    m = p_rest(o, district_no)
    om = o._append(m)
    z = om.जिला.values[0]
    om = om[om.जिला == z]
    return om


# In[16]:
stopwords = {"उर्फ","उम्र","साल","वर्ष","पिता","जाति","चालक"}

list_of_districts = ['21370','21350','21351','21326','21359','21362','21352','21347','21737','21346','21734','21349','21353','21348','21307','21329'] #'21314,'21730','21320','21733','21731','21303','21330','21970','21356','21371','21364','21333','21334','21327','21328','21318','21319','21331','21332','21355','21306','21322','21321','21323','21324','21338','21736','21971','21369','21339','21304','21732','21312','21315','21316','21735','21335','21336','21337','21344','21343','21342','21345','21738','21357','21370','21350','21351','21326','21359','21362','21352','21347','21737','21346','21734','21349','21353','21348','21307','21329'
for jj in list_of_districts:
    dd = autoscraper(jj)

    # cleanup
    dd.drop_duplicates()
    dd = dd.rename(columns={
        'जिला': 'District',
        'थाना': 'PS',
        'गिरफ्तार व्यक्ति का नाम': 'Name',
        'धारा एबं अधिनियम': 'Offence',
        'पूछताछ अधिकारी के नाम': 'IO',
        'पूछताछ अधिकारी के पद': 'Designation'
    })
    dd.drop('क्र.सं.', axis=1, inplace=True)
    dd['Name'] = dd['Name'].str.replace('\d+', '', regex=True)
    dd['Name'] = dd['Name'].str.replace(r'[-()\"#/@;:<>{}`+=~|.!?,]','', regex=True)
    dd['Name'] = dd['Name'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
    dd['LastName'] = dd['Name'].apply(lambda x: x.split()[-1])
    dd.to_excel('df_{}.xlsx'.format(jj), index = False)
    #dd.to_csv('df_{}.csv'.format(jj), index = False)


# In[17]:


print(len(list_of_districts))
print(dd.columns)

