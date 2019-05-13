#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

host = "foodforfamilyf3.mysql.pythonanywhere-services.com"
user = "foodforfamilyf3"
password = "ngocanh2512"
dbname = "fshare"

def connection():

    db = pymysql.connect(host, user, password, dbname)
    return db

if __name__  == '__main__':
    cursor = connection().cursor()
    query = "select ten_mon from mon_an limit 5"
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        print(result)
