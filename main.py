#! /usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
作者：陈晨
时间：2018-12-10
功能：配合pytest接口测试执行
'''

from apiRunner.testSuite import TestSuite
import os
import re
import json


## 读取用例json,执行用例
class TestGroup():
    def __init__(self, json_dir):
        dir_ls = os.listdir(json_dir)
        case_dir_list = [
            "{json_dir}/{case}".format(json_dir=json_dir, case=ii) for ii in dir_ls if re.match(r'test_.*.json', ii)
        ]

        for case_dir in case_dir_list:
            with open(case_dir, 'r', encoding='utf-8') as case_str:
                case_json = json.load(case_str)

            exec("def test_0{index}():TestSuite({casejson})".format(index=case_dir_list.index(case_dir),
                                                                    casejson=case_json))
            exec('test_0{index}()'.format(index=case_dir_list.index(case_dir)))


if __name__ == '__main__':
    json_dir = './json'
    testgroup = TestGroup(json_dir)
