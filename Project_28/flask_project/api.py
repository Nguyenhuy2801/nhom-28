#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for
import pymysql
from db import connection

app = Flask(__name__)

def getlinkstatic():

    getLink=[{
        "linkTrangchu": url_for('my_home'),
        "linkMua": url_for('itemCT', donviCT="_mua"),
        "linkCachchebien": url_for('itemCT', donviCT="cach_cb"),
        "linkThanhphan": url_for('itemCT', donviCT="thanh_phan"),
        "linkVanhoa": url_for('itemCT', donviCT="van_hoa"),
        "linkMeovaobep": url_for('meovat')
    }]
    
    return getLink


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
