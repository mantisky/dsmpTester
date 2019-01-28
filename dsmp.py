#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：dsmp上使用requests实现接口测试
作者：陈晨
时间：201901211121
"""

import requests
import json

requests.packages.urllib3.disable_warnings()


class DsmpRequest():
    def __init__(self, login_url, login_data):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }

        try:
            resp_login = requests.post(login_url, data=login_data, headers=self.headers,
                                       verify=False)
            assert resp_login.status_code == 200
        except:
            print("登录失败!")
        else:
            cookie = resp_login.headers['Set-Cookie'].split('; ')[0]
            self.headers['cookie'] = cookie
            print("headers: ", self.headers)
            print("登录成功!")

    def request(self, go_url, method, go_data):
        if method == 'GET':
            resp = requests.get(go_url, params=go_data, headers=self.headers, verify=False)
        elif method == 'POST':
            resp = requests.post(go_url, data=go_data, headers=self.headers, verify=False)

        return resp


if __name__ == "__main__":
    base_url = 'https://172.16.140.147:8443/dsmp'

    login_url = base_url + "/login/login.do?fp=1"
    login_data = {
        "username": "admin",
        "pwd": "Admin123"
    }

    dsmp = DsmpRequest(base_url, login_data)

    go_url = base_url + "/uidevicemonitor/queryListByCondition.do"
    method = "POST"
    go_data = {
        "area": "II区",
        "ip":"172.16.140.22",
        "corpname":"500kV兆和测试电厂",
        "page": 1,
        "rows": 50
    }

    resp = dsmp.request(go_url, method, go_data)
    print(resp.text)
