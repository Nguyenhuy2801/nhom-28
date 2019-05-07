#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

host = "localhost"
user = "ngocanh"
password = "nao123456"
dbname = "fshare"

def connection():
    
    db = pymysql.connect(host, user, password, dbname)
    return db
