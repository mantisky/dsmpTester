#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：测试用
作者：陈晨
时间：20190124
"""
import coverage

try:
    raise KeyError("erwrw")
except KeyError as e:
    print(e)

if __name__ == "__main__":
    pass