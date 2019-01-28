#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：代码迁移到git后，重新设计发布脚本
作者：陈晨
时间：2019-01-04
"""

import os
## import pdb

env_ip = "172.16.140.71"
git_get = "/media/cjd/git-get"

mode_dict = {
    "proxyserver": {
        "dir": "dsmp2.0_web_framework",
        "update_code": """
            cd {gitget}/dsmp2.0/dsmp2.0_web_framework/ &&
            sed -i "s/172.16.140.147/{env_ip}/g" $(grep 172.16.140.147 -rl .) &&
            mv ./build.xml ./buildBak.xml &&
            cp /media/cjd/proxyBuildGit.xml ./build.xml &&
            echo '#####--build proxyserver--######'
            ant &&
            echo '#####--update proxyserver--######'
            /home/scripts/servicectl stop proxyserver &&
            cd /home/dsmp2.0/proxyserver/webapps/ &&
            rm -rf dsmp dsmp.war.bak1 &&
            rm -rf ../work/Catalina &&
            mv dsmp.war dsmp.war.bak1 &&
            cp {gitget}/bak/proxyserver/webapps/dsmp.war /home/dsmp2.0/proxyserver/webapps/  &&
            /home/scripts/servicectl start proxyserver &&
            /home/scripts/servicectl status
            echo '######--backup--######'
            mv {gitget}/bak/proxyserver/webapps/dsmp.war {gitget}/bak/proxyserver/dsmp.war`date +%Y%m%d%H%M%S` 
        """.format(env_ip=env_ip, gitget=git_get)
    },
    "consumer": {
        "dir": "dsmp2.0-cluster-consumer",
        "update_code": """
            cd {gitget}/dsmp2.0/dsmp2.0-cluster-consumer &&
            sed -i "s/172.16.140.147/{env_ip}/g" $(grep 172.16.140.147 -rl .) &&
            mv ./build.xml ./buildBak.xml &&
            cp /media/cjd/consumerBuildGit.xml ./build.xml &&
            echo '#####--build consumer--#####'
            ant &&
            echo '#####--update consumer--#####'
            /home/scripts/servicectl stop consumer &&
            cp {gitget}/bak/consumer/DSMP2.0-cluster-consumer.jar /home/dsmp2.0/consumer/ &&
            /home/scripts/servicectl start consumer &&
            /home/scripts/servicectl status
            echo '#####--backup consumer--#####'
            mv {gitget}/bak/consumer/DSMP2.0-cluster-consumer.jar {gitget}/bak/consumer/DSMP2.0-cluster-consumer.jar`date +%Y%m%d%H%M%S`
        """.format(env_ip=env_ip, gitget=git_get)
    },
    "rpc": {
        "dir": "dsmp2.0-rpc-n",
        "update_code": """
            cd {gitget}/dsmp2.0/dsmp2.0-rpc-n &&
            sed -i "s/172.16.140.77/{env_ip}/g" $(grep 172.16.140.77 -rl .) &&
            sed -i "s/192.168.1.250/{env_ip}/g" $(grep 192.168.1.250 -rl .) &&
            mv ./build.xml ./buildBak.xml &&
            cp /media/cjd/rpcBuildGit.xml ./build.xml &&
            echo '#####--build rpc--#####'
            ant &&
            echo '#####--update rpc--#####'
            /home/scripts/servicectl stop rpc &&
            cp {gitget}/bak/rpc/DSMP2.0-RPC.jar /home/dsmp2.0/rpc/ &&
            /home/scripts/servicectl start rpc &&
            /home/scripts/servicectl status
            echo '#####--backup rpc--#####'
            mv {gitget}/bak/rpc/DSMP2.0-RPC.jar {gitget}/bak/rpc/DSMP2.0-RPC.jar`date +%Y%m%d%H%M%S`
        """.format(env_ip=env_ip, gitget=git_get)
    },
    "stationnsync": {
        "dir": "dsmp2.0-station-nsync",
        "update_code": """
            cd {gitget}/dsmp2.0/dsmp2.0-station-nsync/ &&
            mv ./build.xml ./buildBak.xml &&
            cp /media/cjd/station-nsyncBuildGit.xml ./build.xml &&
            ant &&
            ps -ef |grep DSMP2.0-StationNsync |grep -v grep |awk '{{print $2}}'|xargs kill -9 &&
            cp {gitget}/bak/StationNsync/stationnsync/DSMP2.0-StationNsync.jar /home/dsmp2.0/stationnsync/ &&
            
            mv {gitget}/bak/StationNsync/stationnsync/DSMP2.0-StationNsync.jar {gitget}/bak/StationNsync/stationnsync/DSMP2.0-StationNsync.jar`date +%Y%m%d%H%M%S` &&
            nohup java -jar /home/dsmp2.0/stationnsync/DSMP2.0-StationNsync.jar &
            ps -ef |grep DSMP2.0-StationNsync.jar |grep -v grep
        """.format(gitget=git_get)
    }
}

class DsmpUpdate():

    def __init__(self):
        try:
            print("可更新的模块：proxyserver, consumer, rpc, stationnsync")
            mode = raw_input("请输入需要更新的模块：")
            #mode = input("请输入需要更新的模块：")

            all_branch = "cd {gitget}/dsmp2.0 && git fetch && git branch -a".format(gitget=git_get)
            os.system(all_branch)
            branch = raw_input("请输入需要更新的分支：")
            #branch = input("请输入需要更新的分支：")
        except Exception as e:
            print("Error massge: ", e)
        else:
            git_log = """
                cd {gitget}/dsmp2.0 && 
                git reset --hard HEAD &&
                git checkout {branch} && 
                git pull origin {branch} && 
                echo '输出Git日志—{dir}' &&
                git log {branch} -3 -- {dir} 
            """.format(
                gitget=git_get,
                branch=branch,
                dir=mode_dict[mode]['dir']
            )

            os.system(git_log)

            ## 发布版本
            ## pdb.set_trace()
            version = raw_input("请输入需要更新的版本号：")
            print("Git checkout verison {version}".format(version=version))
            checkout_version = "cd {gitget}/dsmp2.0 && git checkout {version}".format(gitget=git_get, version=version)
            checkout_status = os.system(checkout_version)
            update = raw_input("是否发布(y/n)：")
            #update = input("是否发布(y/n)：")
            if update == 'y':
                os.system("{update_code}".format(update_code=mode_dict[mode]['update_code']))
            else:
                pass

if __name__ == "__main__":
    ud = DsmpUpdate()
