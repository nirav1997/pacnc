#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 04:29:15 2020

@author: shaivalshah
"""

import xml.etree.ElementTree as ET
import requests
import time
import pandas as pd
from postgres import PostGres

db = PostGres().connect_db()
default_id = "202010171030"
while True:
    url = "https://github.com/wraldata/nc-covid-data/commits/master.atom"
    content = requests.get(url)
    xml = ET.fromstring(content.content)
    for child in xml.findall("{http://www.w3.org/2005/Atom}entry"):
        title = child.find("{http://www.w3.org/2005/Atom}title").text.lower().strip()
        datetime = title.split(' ')[-1]
        id_ = datetime
        if "Adding data as of" in title:
            if default_id != id_:
                default_id = id_
                data_url = "https://raw.githubusercontent.com/wraldata/nc-covid-data/master/zip_level_data/time_series_data/csv/nc_zip{}.csv".format(datetime)
                df = pd.read_csv(data_url)
                date = "{}-{}-{}".format(datetime[:4], datetime[4:6], datetime[6:8])
                data_time = datetime[8:]
                df['Date'] = date
                df['Time'] = data_time
                df = df[['Date', 'Time', 'ZIPCode', 'Cases', 'Deaths', 'TotalPop', 'Place']]
                df.columns= df.columns.str.lower()
                df.to_sql('nccoviddata', db, if_exist='append', index=False)
            break
    time.sleep(14400)