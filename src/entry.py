#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : entry.py
# @Author: Betafringe
# @Date  : 2020/1/5
# @Desc  : 
# @Contact : betafringe@foxmail.com

import sys, os, json
from flask import Flask, render_template, request, Response
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from services import ret_radar
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "4037e9565e69cc2668f0d95fe1899621"
app.config['JSON_AS_ASCII'] = False
# app.config['SQLCHEMY_DATABASE_URI'] = '_sqlite:///site.db'
# # db = SQLAlchemy(app)

@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')


# task/v1/analyse/?carType=name
@app.route('/task/v1/analyse/', methods=['GET'])
def task_analyse():
    ret_data = {}
    if request.method == 'GET':
        car_name = request.args.get("carType")
        ret_data = ret_radar(car_name)
    else:
        pass
    return jsonify(ret_data)


@app.route('/charts/charts.html')
def charts():
    return render_template('charts/charts.html')


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5008,
        debug=True
    )
