#! /usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
作者：陈晨
时间：2018-12-10
功能：执行测试用例
'''

import requests
import re
import json
import pdb

requests.packages.urllib3.disable_warnings()


class TestCase():

    def __init__(self, case_json, config):
        self.case_json = case_json
        self.headers = config['headers']
        self.base_url = config['base_url']
        try:
            self.variables = config['variables']
        except:
            self.variables = {}

        if case_json['status'] :
            print("## 执行请求 ##")
            self.requestsBase()

            print("## 提取变量 ##")
            self.extractBase()

            print("## 断言 ##")
            self.validateBase()

            print("## 输出到日志 ##")
            self.outBase()

        else:
            pass

    ## 执行requests请求
    def requestsBase(self):
        case_json = self.case_json
        print("######-CaseName: {}-######".format(case_json['name']))
        print("TestCase: ", case_json)
        case_request = case_json['request']

        url = self.base_url + case_request['url']
        method = case_request['method']
        headers = self.headers

        try:
            case_headers = case_request['headers']
            for key, value in case_headers.items():
                exec("headers['{key}'] = '{value}'".format(key=key, value=value))
        except KeyError:
            headers = self.headers

        try:
            if 'data' in case_request:
                data = case_request['data']
                json_dumps = False
            else:
                data = case_request['json']
                json_dumps = True
        except:
            data = None
            json_dumps = False


        if method == 'GET':
            self.response = requests.request(method, url, params=data, headers=headers, verify=False)
        elif method == 'POST':
            # print('In requestsBase!')
            if json_dumps:
                data = json.dumps(data)
            self.response = requests.request(method, url, data=data, headers=headers, verify=False)

    ## 断言
    def validateBase(self):
        response = self.response
        # print(self.case_json['validate'])
        try:
            validate = self.case_json['validate']
            ## 目前只支持‘eq’
            eq_list = [ii['eq'] for ii in validate if 'eq' in ii]
        except KeyError:
            print('Validate parameter is empty!')

        else:
            ## 判断
            try:
                for ss in eq_list:
                    key = ss[0]
                    value = ss[1]
                    test_key = self.executeCode('{key}'.format(key=key))

                    assert test_key == value
                print("断言成功！")
            except AssertionError:
                print('断言失败！')
                print("test_key: ", test_key)
                print("test_value: ", value)



    ## 提取变量
    def extractBase(self):
        response = self.response
        # pdb.set_trace()
        try:
            extract = self.case_json['extract']

        except KeyError:
            print('Extract parameter is empty!')

        else:
            for ii in extract:
                for key, value in ii.items():
                    value = re.findall(r'\{\{(.*)\}\}', value)
                    self.variables['{}'.format(key)] = self.executeCode("{}".format(value[0]))
                    #print('variables: ',self.variables)

    ## 输出到日志
    def outBase(self):
        response = self.response
        try:
            output = self.case_json['output']
        except KeyError:
            print('Output parameter is empty!')
        else:
            for ii in output:
                for key, value in ii.items():
                    value = self.executeCode("response.{value}".format(value=value))
                    print("{key}: {value}".format(key=key, value=value))

    ## 执行python代码
    def executeCode(self, code):
        response = self.response
        try:
            resp = eval(code)
            return resp
        except Exception as err:
            raise ExecuteError(err)


class ExecuteError(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return self.msg