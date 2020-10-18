#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 00:21:05 2020

@author: shaivalshah
"""

import pandas as pd
import json
from postgres import PostGres


def getResponse(zipcode):
    db = PostGres().connect_db()
    with db.connect() as conn:
        query = "SELECT Date, Time, Cases, TotalPop from nccoviddata where ZIPCode={} and Date > current_date - interval '7' day".format(zipcode)
        df = pd.read_sql_query(query, conn).dropna()
        df = df.sort_values(['Date', 'Time'])
        avg_total_pop = df['TotalPop'].mean()
        cases = df['Cases'].values
        response = {"cases": cases,
                    "AverageTotalPop": avg_total_pop}
    return json.dumps(response)



     