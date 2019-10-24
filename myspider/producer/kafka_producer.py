# -*- coding: UTF-8 -*-
"""
Created on 2018年2月7日
@author: Leo
@file: kafka_consumer.py
"""

from pykafka import KafkaClient

client = KafkaClient(hosts="localhost:9092")
# 要用字节形式

producer = client.topics[b'newtest'].get_producer()

for i in range(0, 100):
    data = "Message: %s" % str(i)
    producer.produce(data.encode(encoding="UTF-8"))
    print(data)
producer.stop()
