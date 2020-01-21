#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : models.py.py
# @Author: Betafringe
# @Date  : 2020/1/17
# @Desc  : 
# @Contact : betafringe@foxmail.com

import pymysql
from collections import Counter
import json

db_info = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'Qdalone2412#',
    'db': 'master_car',
}


class DB():
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


# carname = n
# cate pos a, neg b, neral c
# cate  :  a/(a+b) [0,1]
# a 某个车型下的某个类别中的 积极评论的数量
def service_radar(carname):
    '''
    :param carname:
    :return: a dict contains each category score eg.{'价格': 0.5, '动力': 0.8, '外观': 1.0, '操控': 0.75, '油耗': 1.0}
    '''
    category_dict = {'价格': 0, '动力': 2, '外观': 4, '操控': 5, '油耗': 6 }
    ret = {}
    with DB(host=db_info['host'], user=db_info['user'], passwd=db_info['passwd'], db=db_info['db']) as db:
        for k, v in zip(category_dict.keys(), category_dict.values()):
            pos_sql = 'select count(Comment.comm_id) from comment ' \
                  'join sentiment on sentiment.comm_id = comment.comm_id ' \
                  'where car_name like \"%%%s%%\" and cate_id=%d and senti_value=2' % (carname, v)
            neg_sql = 'select count(Comment.comm_id) from comment ' \
                    'join sentiment on sentiment.comm_id = comment.comm_id ' \
                    'where car_name like \"%%%s%%\" and cate_id=%d and senti_value=0' % (carname, v)
            db.execute(pos_sql)
            pos_n = db.fetchone()['count(Comment.comm_id)']
            db.execute(neg_sql)
            neg_n = db.fetchone()['count(Comment.comm_id)']
            if pos_n + neg_n == 0:
                ret[k] = 0.3
            else:
                ret[k] = pos_n / (pos_n + neg_n)
    return ret


# carname下出现最多的aspect words
# select aspect_word from sentiment_aspect_word
# join sentiment on sentiment.senti_id = sentiment_aspect_word.senti_id
# join comment on sentiment.comm_id = comment.comm_id
# where comment.car_name like "%夏利%";
def service_hotwords(carname, topn=10):
    """
    :param carname=keywords for query:
    :param topn, topn topic should return :
    :return a dict contains word and freq eg. {'外观': 58, '刹车': 19, '加速': 19, '配置': 17, '座椅': 16}:
    """
    ret = {}
    with DB(host=db_info['host'], user=db_info['user'], passwd=db_info['passwd'], db=db_info['db']) as db:
        sql = 'select aspect_word from sentiment_aspect_word ' \
              'join sentiment on sentiment.senti_id = sentiment_aspect_word.senti_id ' \
              'join comment on sentiment.comm_id = comment.comm_id ' \
              'where comment.car_name like \"%%%s%%\";' % carname
        db.execute(sql)
        # hotwords is a list [['aspect_word':'word'], ...]
        hotwords = db.fetchall()
    h = []
    for v in hotwords:
        h.append(v['aspect_word'])
    counter_words = Counter(h)
    for word, freq in counter_words.most_common(topn):
        ret[word] = freq
    return ret

def tsql():
    pass

service_radar("奔驰")