#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

def connection():
    host = "localhost"
    user = "ngocanh"
    password = "nao123456"
    dbname = "fshare"
    db = pymysql.connect(host, user, password, dbname)
    return db
