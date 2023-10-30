# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:55:03 2021

@author: krishnan
"""
import pandas as pd
import numpy as np
import re

jabalpur = pd.read_csv('G:/Shubhangi/Internships 2021/Jabalpur.csv')

stopwords = {"उर्फ","उम्र","साल","वर्ष","पिता","जाति","चालक"}

jabalpur['Name'] = jabalpur['Name'].str.replace('\d+', '')
jabalpur['Name'] = jabalpur['Name'].str.replace(r'[-()\"#/@;:<>{}`+=~|.!?,]','')
jabalpur['Name'] = jabalpur['Name'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
jabalpur['LastName'] = jabalpur['Name'].apply(lambda x: x.split()[-1])

jabalpur.to_csv('G:/Shubhangi/Internships 2021/Jabalpur.csv')
