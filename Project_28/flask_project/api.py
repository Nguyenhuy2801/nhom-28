#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for
import pymysql
from flask_sqlalchemy import SQLAlchemy
from qb import connection, host, user, password, dbname


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost:3306/{}'.format(user, password, dbname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sqldb = SQLAlchemy(app)

def getlinkstatic():

    getLink=[{
        "linkTrangchu": url_for('my_home'),
        "linkMua": url_for('itemCT', donviCT="_mua", category = 'all'),
        "linkCachchebien": url_for('itemCT', donviCT="cach_cb", category = 'all'),
        "linkThanhphan": url_for('itemCT', donviCT="thanh_phan", category = 'all'),
        "linkVanhoa": url_for('itemCT', donviCT="van_hoa", category = 'all'),
        "linkMeovaobep": url_for('meovat')
    }]
    
    return getLink

def getListDishes(results):
    listData = []
    for result in results:
        jsonData = {
            "tenmon": result[0],
            "linkImg": result[1], 
            "linkMon": url_for('monan', tenmon=result[0])
        }
        listData.append(jsonData)
    connection().close()
    return listData

def getTitle(donviCT):
    switcher = {
        "_mua": "Món ăn theo mùa".decode('utf-8'),
        "cach_cb": "Món ăn theo cách chế biến".decode('utf-8'),
        "thanh_phan": "Món ăn theo thành phần".decode('utf-8'),
        "van_hoa": "Món ăn theo văn hóa".decode('utf-8'),
    }
    return switcher.get(donviCT, "Trang chủ".decode('utf-8'))

def model(donviCT):
    switcher = {
        "_mua": _mua,
        "cach_cb": Cach_cb,
        "thanh_phan": Thanh_phan,
        "van_hoa": Van_hoa,
    }
    return switcher.get(donviCT)

# Trang chủ
@app.route('/home')
def my_home():
    cursor = connection().cursor()
    query = "SELECT ten_mon, image from mon_an order by ma_mon limit 10"
    cursor.execute(query)
    results = cursor.fetchall()
    listData = []
    for result in results:
        jsonData = {
            "tenmon": result[0].decode('utf-8'),
            "linkImg": result[1], 
            "linkMon": url_for('monan', tenmon=result[0])
        }
        listData.append(jsonData)
    connection().close()
    return render_template('trangchu.html', getLink=getlinkstatic(), listmonan=listData)

# giao diện các công thức đơn vị
@app.route('/home/<donviCT>')
def itemCT(donviCT):
    
    return render_template('itemcongthuc.html', getLink=getlinkstatic(), title=donviCT)

# giao diện mẹo vào bếp
@app.route('/home/meovaobep')
def meovat():
    return render_template('meovaobep.html', getLink=getlinkstatic())

# giao diện công thức món ăn cụ thể
@app.route('/home/congthucnauan/<tenmon>')
def monan(tenmon):
    
    return render_template('app_nauan.html', getLink=getlinkstatic())

# giao diện mẹo vặt cụ thể
@app.route('/home/meo_vao_bep/<tenmeovat>')
def meovaobep(tenmeovat):
    return render_template('app_meovat.html', getLink=getlinkstatic(), title = tenmeovat)
