#! /usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
作者：陈晨
时间：2018-12-10
功能：构建测试用例数据，提取变量值
'''

from .testCase import TestCase
import re
import json

class TestSuite():
    def __init__(self,suite_json):
        for case_json in suite_json:
            if 'config' in case_json:
                self.config = case_json['config']
                print(self.config['name'])

            elif 'setup' in case_json:
                case = self.caseAnalyze(case_json)['setup']
                go_test = TestCase(case, self.config)
                self.config['variables'] = go_test.variables

            elif 'test' in case_json:
                case_status = case_json['test']['status']
                if case_status:
                    case = self.caseAnalyze(case_json)['test']
                    go_test = TestCase(case, self.config)
                    self.config['variables'] = go_test.variables
                else:
                    pass


    ## 解析测试用例
    def caseAnalyze(self,case_json):
        case_str = json.dumps(case_json)
        case_re = re.findall(r"[\'\"]\$(.+?)[\"\']", case_str)

        out = case_str
        for ii in case_re:

            repl = "\${ii}".format(ii=ii)
            string = self.config['variables'][ii]

            out = re.sub(repl, string, out)

        return json.loads(out)


if __name__ == '__main__':
    pass