#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : conn_sql.py
# @Author: Betafringe
# @Date  : 2020/1/10
# @Desc  : 
# @Contact : betafringe@foxmail.com


import pymysql
import os
import pandas as pd

# 打开数据库连接
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


category_dict = {'价格': 0, '内饰': 1, '动力': 2, '外观': 3, '安全性': 4, '操控': 5, '油耗': 6, '空间': 7, '舒适性': 8, '配置': 9}
path = '../../data/final_sql'

def insert_category(db):
    for c in category_dict:
        sql_category = "INSERT INTO `category` (cate_id, cate_name) VALUES (%d, \"%s\")" % (category_dict[c], c)
        db.execute(sql_category)


def creat_sql(db, file):

    car = file.strip('.csv')

    df = pd.read_csv(os.path.join(path, file))
    comment = df['all_comment']
    category = df['aspects']
    sentiment = df['sentiment']
    aspect_words = df['aspect_words']

    for com_i, com in enumerate(comment):
        com = com.replace('\"','')

        comment_exist = db.execute('select comm_id from comment where content=\"%s\";'% com)
        #判断该评论是否已经被存储过,0:数据库中不存在，>0:数据库中已经存在
        #当数据库中不存在该评论时，将该评论存入数据库
        if comment_exist == 0:
            # 当前评论条数
            db.execute('select count(comm_id) from `comment`')
            comment_num = db.fetchone()['count(comm_id)']

            # 当前评论条数就是新加入评论的id
            sql_comment = "INSERT INTO `Comment` (content, car_name) VALUES (\"%s\", \"%s\")" % (
            com[:511], car)
            #print(sql_comment)
            db.execute(sql_comment)
        else:
            db.execute('select comm_id from comment where content=\"%s\";' % com)
            comment_id = db.fetchone()['comm_id']
            comment_num = comment_id

        db.execute('select count(senti_id) from `sentiment`')
        sentiment_num = db.fetchone()['count(senti_id)']

        sql_sentiment = "INSERT INTO `Sentiment` (comm_id, cate_id, senti_value) VALUES (%d, %d, %d)" %\
                        (comment_num, category_dict[category[com_i]], sentiment[com_i])
        #print(sql_sentiment)
        db.execute(sql_sentiment)

        if type(aspect_words[com_i]) is str:
            for word in aspect_words[com_i].split('#'):
                sql_sentiment_aspect_word = "INSERT INTO `Sentiment_Aspect_word` (senti_id, aspect_word) VALUES (%d, \"%s\")" % (sentiment_num, word)
                #print(sql_sentiment_aspect_word)
                db.execute(sql_sentiment_aspect_word)


# Unnamed: 0,uid,all_comment,score,aspects,aspect_words,segs,sentiment
if __name__ == '__main__':
    # db_info = {
    #     'host': 'rm-2ze12jwa5a242g11lmo.mysql.rds.aliyuncs.com',
    #     'user': 'ycf',
    #     'passwd': 'Cjb77xxh!',
    #     'db': 'ycf',
    # }
    db_info = {
        'host': 'localhost',
        'user': 'root',
        'passwd': 'Qdalone2412#',
        'db': 'master_car',
    }
    file_list = os.listdir(path)
    for idx, file in enumerate(file_list):
        print(">" * 15, file, idx+1, len(file_list))
        try:
            with DB(host=db_info['host'], user=db_info['user'], passwd=db_info['passwd'], db=db_info['db']) as db:
                creat_sql(db, file)
        finally:
            pass
