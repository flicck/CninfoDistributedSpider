# -*- coding: UTF-8 -*-
"""
Created on 2018年2月7日
@author: Leo
@file: kafka_consumer.py
"""

# Zookeeper启动命令: zkServer
# Kafka启动命令: kafka-server-start F:\Kafka_zookeeper\kafka_2.12-1.0.0\config\server.properties

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType

client = KafkaClient(hosts="192.168.88.196:9092")
# 要用字节形式
topic = client.topics[b'wanghan15-post']
#topic = client.topics[b'testTopic']
# 用的是get_simple_consumer做测试
consumer = topic.get_simple_consumer(
    consumer_group=b"wanghan15",
    auto_offset_reset=OffsetType.EARLIEST,
    reset_offset_on_start=False,
    auto_commit_enable=True,
    #默认自动提交时间为5000ms
    auto_commit_interval_ms=100
)
for x in consumer:
    if x is not None:
        # print(json.loads(x.value.decode('utf-8')))
        print(x.value.decode('utf-8'))
