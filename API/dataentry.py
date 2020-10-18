#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 16:28:50 2020

@author: shaivalshah
"""

import os
from postgres import PostGres
from google.cloud import storage
from io import BytesIO
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "My_First_Project-88a396c2c3f0.json"
def create_table():
    db = PostGres().connect_db()
    with db.connect() as conn:
        query = "CREATE TABLE IF NOT EXISTS nccoviddata (Date date, \
                                                        Time varchar(4), \
                                                        ZIPCode varchar(5), \
                                                        Cases integer, \
                                                        TotalPop integer, \
                                                        Place varchar(50), \
                                                        PRIMARY KEY (Date, Time, ZipCode))"
        conn.execute(query)
def populate_data():
    db = PostGres().connect_db()
    client = storage.Client()
    bucket = client.get_bucket('hacknc_covid_data')
    files = bucket.list_blobs()
    fileList = [file.name for file in files if '.' in file.name]
    for file in fileList:
        blob = storage.blob.Blob(file, bucket)
        content = blob.download_as_string()
        df = pd.read_csv(BytesIO(content))
        date = "{}-{}-{}".format(file[6:10], file[10:12], file[12:14])
        time = file[14:18]
        df['Date'] = date
        df['Time'] = time
        df = df[['Date', 'Time', 'ZIPCode', 'Cases', 'TotalPop', 'Place']]
        df.columns = df.columns.str.lower()
        df.to_sql('nccoviddata', db, if_exists='append',  index=False)
    
create_table()
populate_data()