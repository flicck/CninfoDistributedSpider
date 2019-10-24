# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import urllib

from scrapy.http import Response
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
import re
import sys
import urllib.parse
sys.path.append("D:\pythonWorkBase\mySpider\myspider\myspider\spiders\cninfospider1.py")

import requests
from myspider.spiders.cninfospider1 import Cninfospider1Spider
class MyspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
#中间件---功能：将page超出时间范围的请求筛选掉
        t = re.search(r'pageNum=(.*)',request.url)
        if t is not None:
            page = t.group(0).split("=")[1]
            company = re.search(r'searchkey=(.*)&',request.url).group(0).split("&")[0].split("=")[1]
            company = urllib.parse.unquote(company)
            # print("拿到的"+str(Cninfospider1Spider.time_limit_list[Cninfospider1Spider.company_list.index(company)]))
            if int(page) > Cninfospider1Spider.time_limit_list[Cninfospider1Spider.company_list.index(company)]:
                #请求出界，不要请求了
                r1 = Response("www.baidu.com")
                return r1
            else:
                return None
        else:
            return None

    #PHantomJs的设置
        # # if 'PhantomJS' in request.meta:
        #     driver = webdriver.PhantomJS()
        #     driver.get(request.url)
        #     content = driver.page_source.encode('utf-8')
        #     driver.quit()
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
