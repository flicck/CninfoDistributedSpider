# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import json
#所有的pipeline必须有return
class MyspiderPipeline(object):
    # count = 0
    counters= {}
    re = redis.Redis(host='127.0.0.1', port=6379, db=2)
    def process_item(self, item, spider):
        # print (item)
        tipster = item["com"]
        if MyspiderPipeline.counters.__contains__(tipster):
            i = MyspiderPipeline.counters.get(tipster)
            i = i + 1
            t = json.dumps(item)
            MyspiderPipeline.re.set(item["com"]+"_"+item["time"]+"_"+str(i),t)
            tmpdict = {tipster:i}
            MyspiderPipeline.counters.update(tmpdict)
        else:
            t = json.dumps(item)
            MyspiderPipeline.re.set(item["com"]+"_"+item["time"]+"_"+str(1), t)
            MyspiderPipeline.counters[tipster] = 1
        return item
