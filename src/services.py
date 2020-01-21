#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : services.py
# @Author: Betafringe
# @Date  : 2020/1/21
# @Desc  : 
# @Contact : betafringe@foxmail.com
import models
import time

data = {
  "code": "",
  "message": "car analyse created",
  "carName": "",
  "options": {
    "service_hotwords": {
      "message": "hotwords req",
      "data": {
      }
    },
    "service_radar": {
      "message": "radar req",
      "data": {
      }
    }
  },
  "time": "utc-time"
}


def ret_radar(carname):
    data["carName"] = carname
    data["options"]["service_radar"]["data"] = models.service_radar(carname)
    data["time"] = time.asctime()
    return data

