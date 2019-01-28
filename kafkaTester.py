#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：操作kafka生产者
作者：陈晨
时间：2019-01-08
"""

from kafka import KafkaProducer
import json
import re


class Producer():
    def __init__(self, dir):
        ##读取message.json
        with open(dir, 'r', encoding='utf-8') as case:
            self.case_json = json.load(case)

    def send_msg(self):
        msg_config = self.case_json[0]["config"]
        ip = msg_config['ip']
        port = msg_config['port']
        variables = msg_config['variables']

        producer = KafkaProducer(bootstrap_servers=[
            '{ip}:{port}'.format(ip=ip, port=port)])  # 此处ip可以是多个['0.0.0.1:9092','0.0.0.2:9092','0.0.0.3:9092' ]

        case = self.case_json[1:]
        for test in case:
            test = test['test']

            topic = test['topic']
            msg = json.dumps(test['value'])
            status = test['status']
            tms = test['times']

            if status:
                var = re.findall(r'\$([a-zA-Z\_]*)', msg)
                for code in var:
                    msg = re.sub(r'\${code}'.format(code=code), variables['{code}'.format(code=code)], msg)

                print(test["name"])
                msg = msg.strip('"')

                i = 0
                while True:
                    i += 1
                    if i > tms:
                        break
                    else:
                        print(msg)
                        producer.send(topic, msg.encode('utf-8'))  # 参数为主题和bytes数据

        producer.close()


if __name__ == "__main__":
    json_dir = "./json/kafkaMsg.json"
    producer = Producer(json_dir)
    producer.send_msg()