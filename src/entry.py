#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : entry.py
# @Author: Betafringe
# @Date  : 2020/1/5
# @Desc  : 
# @Contact : betafringe@foxmail.com

import sys, os, json
from flask import Flask, render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


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
@app.route('/task/v1/analyse/', methods=['GET', 'POST'])
def task_analyse():
    recv_data = request.args.get("carType")
    print(recv_data)
    return recv_data


@app.route('/charts')
@app.route('/charts/charts.html', methods=['GET', 'POST'])
def charts():
    return render_template('/charts/charts.html')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5008,
        debug=True
    )
