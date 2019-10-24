# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import json,hashlib
# Scrapy

from scrapy.conf import settings

# PyKafka
from pykafka import KafkaClient
#所有的pipeline必须有return
class MyspiderPipeline(object):
    # section1 这里是导入redis的代码
    # counters= {}
    # re = redis.Redis(host='127.0.0.1', port=6379, db=2)
    # def process_item(self, item, spider):
    #
    #     tipster = item["com"]
    #     if MyspiderPipeline.counters.__contains__(tipster):
    #         i = MyspiderPipeline.counters.get(tipster)
    #         i = i + 1
    #         t = json.dumps(item)
    #         MyspiderPipeline.re.set(item["com"]+"_"+item["time"]+"_"+str(i),t)
    #         tmpdict = {tipster:i}
    #         MyspiderPipeline.counters.update(tmpdict)
    #     else:
    #         t = json.dumps(item)
    #         MyspiderPipeline.re.set(item["com"]+"_"+item["time"]+"_"+str(1), t)
    #         MyspiderPipeline.counters[tipster] = 1
    #     return item


    # section2 这里是导入到kafka的代码
    def __init__(self):
        # 判断下配置里面个给的是啥
        # 1. 如果长度等于1, list只有一个数据, 如果是字符肯定大于1
        # 2. 否则, 判断类型是否是list, 是的话用 逗号分隔
        # 3. 否则就是一个字符串
        kafka_ip_port = settings['KAFKA_IP_PORT']
        if len(kafka_ip_port) == 1:
            kafka_ip_port = kafka_ip_port[0]
        else:
            if isinstance(kafka_ip_port, list):
                kafka_ip_port = ",".join(kafka_ip_port)
            else:
                kafka_ip_port = kafka_ip_port

        # 初始化client
        self._client = KafkaClient(hosts=kafka_ip_port)

        # 初始化Producer 需要把topic name变成字节的形式
        self._producer = \
            self._client.topics[
                settings['KAFKA_TOPIC_NAME'].encode(encoding="UTF-8")
            ].get_producer()
    # 自动读取文件创建topic
    # def create_topic(self, brokers,topic='topic', num_partitions=3, configs=None, timeout_ms=3000):
    #
    #     client = KafkaClient(hosts=brokers)
    #
    #     if topic not in client.cluster.topics(exclude_internal_topics=True):  # Topic不存在
    #
    #         request = admin.CreateTopicsRequest_v0(
    #             create_topic_requests=[(
    #                 topic,
    #                 num_partitions,
    #                 -1,  # replication unset.
    #                 [],  # Partition assignment.
    #                 [(key, value) for key, value in configs.items()],  # Configs
    #             )],
    #             timeout=timeout_ms
    #         )
    #
    #         future = client.send(2, request)  # 2是Controller,发送给其他Node都创建失败。
    #         client.poll(timeout_ms=timeout_ms, future=future, sleep=False)  # 这里
    #
    #         result = future.value
    #         # error_code = result.topic_error_codes[0][1]
    #         print("CREATE TOPIC RESPONSE: ", result)  # 0 success, 41 NOT_CONTROLLER, 36 ALREADY_EXISTS
    #         client.close()
    #     else:  # Topic已经存在
    #         print("Topic already exists!")
    #         return

    def process_item(self, item, spider):
        if spider.name == "cninfospider1":
            t = json.dumps(item)
            self._producer.produce(t.encode(encoding="UTF-8"))

            #获得t的md5存放到mysql数据库中
            md5_data = self.md5(t)
            print(md5_data)
            #将这个md5值存放到mysql数据库去重

            print(item['title'])
            print(item['time'])
            print(item['page'])

            #如果
            return item

    #数据也能获取md5指纹
    def md5(self,t):
        obj = hashlib.md5()
        obj.update(bytes(t,encoding="utf-8"))
        return obj.hexdigest()

    def close_spider(self,spider):
        if spider.name == "cninfospider1":
            self._producer.stop()

