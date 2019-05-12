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
def searching(search):
    results = search_mon(search)
    listData =[]
    for result in results:
        jsonData = {
            "tenmon": result["_source"]["ten_mon"],
            "linkImg": result["_source"]["image"], 
            "linkMon": url_for('monan', tenmon=result["_source"]["ten_mon"])
        }
        listData.append(jsonData)
    return listData

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
@app.route('/home/<donviCT>', methods =["GET","POST"])
def itemCT(donviCT):
    timkiem = ""
    category = request.args.get('category')
    class_name = model(donviCT)
    results = class_name.query.with_entities(class_name.name).all()
    congthucnauan = []
    for result in results:
        jsonData = {
            "link": url_for('itemCT', donviCT = donviCT, category = result[0]),
            "name": result[0]
        }
        congthucnauan.append(jsonData)
    if request.method == 'POST':
        search = request.form.get("search")
        listmonan = searching(search)
        timkiem = "Kết quả tìm kiếm: "
    else:
        res = query(donviCT, category)
        listmonan = getListDishes(res)

    return render_template('itemcongthuc.html', timkiem = timkiem, getLink=getlinkstatic(), title = getTitle(donviCT), congthucnauan = congthucnauan, listmonan = listmonan)


# giao diện mẹo vào bếp
@app.route('/home/meovaobep')
def meovat():
    return render_template('meovaobep.html', getLink=getlinkstatic())

# giao diện công thức món ăn cụ thể
@app.route('/home/congthucnauan/<tenmon>', methods = ["GET", "POST"])
def monan(tenmon):
    timkiem = ""
    if request.method == 'POST':
        timkiem = "Kết quả tìm kiếm: "
        search = request.form.get("search")
        listData = searching(search)
        return render_template('trangchu.html', timkiem = timkiem, getLink=getlinkstatic(), listmonan=listData, menu=getlinkstatic())
    else:
        results = Mon_an.query.\
            with_entities(Mon_an.ten_mon, Mon_an.cong_thuc, Mon_an.nguyen_lieu, Mon_an.image, Mon_an.video).\
            filter(Mon_an.ten_mon == tenmon).order_by(Mon_an.ma_mon.desc()).all()
        mon = []
        for result in results:
            if(len(result[4]) != 0):
                video = result[4]
            else :
                video = "#"
            jsonData = {"ten_mon": result[0], 
                        "cong_thuc": result[1], 
                        "nguyen_lieu": result[2], 
                        "image": result[3],
                        "linkVideo": video
                        }
            mon.append(jsonData)
        title= tenmon
    return render_template('app_nauan.html', timkiem = timkiem, getLink=getlinkstatic(), title=title,mon=mon, menu=getlinkstatic())


# giao diện mẹo vặt cụ thể
@app.route('/home/meo_vao_bep/<tenmeovat>')
def meovaobep(tenmeovat):
    return render_template('app_meovat.html', getLink=getlinkstatic(), title = tenmeovat)
