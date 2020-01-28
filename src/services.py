#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : services.py
# @Author: Betafringe
# @Date  : 2020/1/21
# @Desc  : 
# @Contact : betafringe@foxmail.com
from models import service_radar, service_hotwords, service_hot_pos_topics, service_hot_neg_topics
import time

data = {
  "code": 200,
  "message": "car analyse created",
  "carName": "奔驰",
  "time": "utc-time",
  "options": {
    "service_hotwords": {
      "message": "hotwords req",
      "data": {
      }
    },
    "service_hot_neg_topics": {
      "message": "service_hot_neg_topics req",
      "data": {
      }
    },
    "service_hot_pos_topics": {
      "message": "service_hot_pos_topics req",
      "data": {
      }
    },
    "service_radar": {
      "message": "radar req",
      "data": {
      }
    }
  }
}


def ret_r(carname):
    data["carName"] = carname
    data["options"]["service_radar"]["data"] = service_radar(carname)
    data["options"]["service_hotwords"]["data"] = service_hotwords(carname)
    data["options"]["service_hot_pos_topics"]["data"] = service_hot_pos_topics(carname)
    data["options"]["service_hot_neg_topics"]["data"] = service_hot_neg_topics(carname)
    data["time"] = time.asctime()
    return data

