#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : models.py.py
# @Author: Betafringe
# @Date  : 2020/1/17
# @Desc  : 
# @Contact : betafringe@foxmail.com

from entry import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"
