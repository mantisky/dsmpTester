#! /usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
作者：陈晨
时间：2018-12-24
功能：提供简易接口
'''

from flask import Flask, request
import sqlite3
import json


db_address = "db/mock.db"

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

## 测试接口
@app.route('/test/', methods=['POST','GET'])
def test():
    if request.method =="GET":
        getData = request.args
        return '获取的GET数据为：{}'.format(getData)
    elif request.method == 'POST':
        postData = request.form
        return '获取的POST数据为：{}'.format(postData)

## 联接sqlite3
@app.route('/sqlite',methods=['GET'])
def connect_db():
    conn = sqlite3.connect(db_address)
    c = conn.cursor()

    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    ls = []
    for row in cursor:
        user = (row[0], row[1], row[2], row[3])
        ls.append(user)
    conn.close()

    return json.dumps(ls)


## 执行sqlite3语句
def execute_sql(sql):
    conn = sqlite3.connect(db_address)
    cursor = conn.cursor()

    if sql.upper().startswith("SELECT"):
        cursor.execute(sql)
        values = cursor.fetchall()
        cursor.close()
    else:
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        values = {"status":"执行成功！"}

    conn.close()

    return json.dumps(values)


## 模拟下单
@app.route("/addOrder",methods=["POST"])
def addOrder():
    addOrder_sql = request.form['sql']
    status = execute_sql(addOrder_sql)

    return status

## 模拟查询订单信息
@app.route("/orderInfo",methods=["GET"])
def orderInfo():
    ## 通过cookie查询用户订单信息,通过order_no查询订单信息
    cookie = request.args['cookie']
    order_no = request.args['order_no']

    sql = "select user_id from user where cookie = '{}'".format(cookie)
    user_id = json.loads(execute_sql(sql))
    print(user_id)

    return_list = []
    if user_id and order_no:
        for ii in user_id:
            order_sql = "select * from order_info where user_id = '{id}' and order_no = '{order_no}'".format(
                id=ii[0],
                order_no=order_no
            )
            order_info = json.loads(execute_sql(order_sql))
            return_list.append(order_info)

    return json.dumps(return_list)


## 模拟登录，校验账号密码并返回cookie
@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    sql = "select * from user where user_name = '{}' limit 1".format(username)
    user_info = json.loads(execute_sql(sql))

    for ii in user_info:
        if ii[1] == username and ii[2] == password:
            cookie = ii[3]
        else:
            cookie = ""

    return cookie

## 模拟直接返回数据
@app.route('/note',methods=['POST','GET'])
def note():
    if request.method == 'GET':
        note_id = request.args['note_id']
    elif request.method == 'POST':
        note_id = request.form['note_id']

    sql = "select text from note where note_id = {note_id} limit 1".format(note_id=note_id)
    text = json.loads(execute_sql(sql))

    return json.dumps(text[0][0])

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=8808,
        debug=True
    )