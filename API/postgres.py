#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 00:20:04 2020

@author: shaivalshah
"""

import sqlalchemy

class PostGres:
    
    def __init__(self):
        self.db_config = {
            "pool_size": 5,
            "max_overflow": 2,
            "pool_timeout": 30,
            "pool_recycle": 1800
        }
        self.db_user = "postgres"
        self.db_pass = "hacknc2512"
        self.db_name = "coviddata"
        self.db_host = "34.68.174.224"
        self.db_port = 5432
        
    def connect_db(self):
        pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
        drivername="postgres+psycopg2",
        username=self.db_user, 
        password=self.db_pass, 
        host=self.db_host, 
        port=self.db_port,
        database=self.db_name
                ),
        **self.db_config
        )
        return pool