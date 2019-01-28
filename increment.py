#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：提取替换文件
作者：陈晨
时间：20190123
"""

import os
import pdb

class Increment():
    def __init__(self):
        unzip_dict = {
            "proxyserver":"""
                cd /media/cjd/increment &&
                rm -rf dsmp* &&
                cp /home/dsmp2.0/proxyserver/webapps/dsmp.war . &&
                unzip -o dsmp.war -d dsmp
            """,
            "consumer":"""
                cd /media/cjd/increment &&
                rm -rf DSMP2.0-cluster-consumer* &&
                cp /home/dsmp2.0/consumer/DSMP2.0-cluster-consumer.jar . &&
                unzip -o DSMP2.0-cluster-consumer.jar -d DSMP2.0-cluster-consumer
            """
        }

        pdb.set_trace()

        st = """
            cd /media/cjd/increment &&
            rm -rf change* &&
            mkdir change &&
            touch change.txt
        """
        os.system(st)

        while True:
            model = raw_input("请输入需要更新的模块(proxyserver,consumer)：")
            if model in unzip_dict:
                os.system(unzip_dict[model])
                self.copyFile(model)
            else:
                print("输入的模块不支持替换！")

            go_state = raw_input("是否继续替换(y/n):")
            if go_state == 'y':
                pass
            else:
                break

    def copyFile(self, model):
        file = raw_input("请输入需要更换的文件路径：")
        go_code = """
            cd /media/cjd/increment &&
            cp {type}/{file} change &&
            echo {typename}/{file} >> change.txt
        """
        if model == "proxyserver":
            go_code = go_code.format(type='dsmp', typename='dsmp.war', file=file)
        elif model == "consumer":
            go_code = go_code.format(type='DSMP2.0-cluster-consumer', typename='DSMP2.0-cluster-consumer.jar', file=file)

        os.system(go_code)


if __name__ == "__main__":
    chge = Increment()