# -*- coding: utf-8 -*-
import json
import scrapy
import re
import logging
import threading
import time
import random
import datetime
import copy
class Company_List:
    #这里需要放公司文件的绝对路径
    # f = open("C:/Users/stawind/Desktop/list/WaitSearchCompanyList.txt", "r", encoding='UTF-8')
    f = open("/tmp/scrapyApp/WaitSearchCompanyList.txt", "r", encoding='UTF-8')
    def get_company_list(self):
        companyList=[]
        while True:
            line = Company_List.f.readline().strip()
            if len(line) == 0:
                break
            companyList.append(line)
        # line = line.strip()
        return companyList
current_cursor = -1
mutex = threading.Lock()
mutex1 = threading.Lock()
mutex2 = threading.Lock()
# page_thread_sequence = 0
#注意scrapy是异步多线程框架，yield方法不会阻塞，如果需要对request和response进行修改，需要区middlewares中间件进行修改
class Cninfospider1Spider(scrapy.Spider):
    name = 'cninfospider1'
    allowed_domains = ['cninfo.com.cn']
    reader = Company_List()
    # start_company = reader.get_next_line()
    start_urls = ['http://www.cninfo.com.cn/']
    company_list = reader.get_company_list()

    # 查询的page限制，和timeLimitBound同一优先级
    pageLimit = 100000
    # 查询的时间限制，和pageLimit同一优先级,左闭右开
    timeLimitBound =["2019-06-04","2019-6-27"]
    time_limit_list = [pageLimit] * company_list.__len__()
    pre = datetime.date(int(timeLimitBound[0].split("-")[0]), int(timeLimitBound[0].split("-")[1]), int(timeLimitBound[0].split("-")[2]))
    post = datetime.date(int(timeLimitBound[1].split("-")[0]), int(timeLimitBound[1].split("-")[1]), int(timeLimitBound[1].split("-")[2]))
    page_thread_sequence = 0
    page_thread_sequence1 = 0
    def parse(self, response):
        global current_cursor
        global page_thread_sequence
        while current_cursor+1 <=  Cninfospider1Spider.company_list.__len__():
            #scrapy是使用多线程的，所以注意加锁增加原子性
            mutex.acquire()
            current_cursor = current_cursor + 1
#爬虫友好性，设置爬取一个公司的间隔时间
            time.sleep(random.randint(0,9)/5.0)
            if current_cursor+1 >  Cninfospider1Spider.company_list.__len__():
                break
            company = Cninfospider1Spider.company_list[current_cursor]
            Cninfospider1Spider.current_company = company
            # 通过meta传递当前company数据--》由于scrapy是异步的，所以全局变量很容易被覆盖
            request = scrapy.Request(
                url="http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=" + company + "&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1",
                callback=self.parse0, meta={"company": company}, dont_filter=True)
            yield request
            mutex.release()

    #翻页
    def parse0(self, response):
        list1 =[]
        company = response.meta["company"]
        print (company)
        dic = json.loads(response.body.decode(response.encoding))
        num = int(dic.get("totalAnnouncement"))
        page = int((num / 10))+1 if num % 10 != 0 else int((num/10))

        # 如果没有页数说明公司不存在，需要报警告
        if page == 0:
            logger = logging.getLogger(__name__)
            logger.warn(company + "不存在")

        # 如果公共页数大于页数限制，就请求页数限制的的全部信息
        if page >=Cninfospider1Spider.pageLimit:
            for i in range(Cninfospider1Spider.pageLimit,0,-1):
                request = scrapy.Request(url = "http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey="+company+"&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum="+str(i),callback=self.parse1,meta={"company":company,"page":copy.deepcopy(i)}, dont_filter=True)
                list1.append(request)
                # yield request
        else:
            for k in range(page,0,-1):
                request = scrapy.Request(
                    url="http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey="+company+"&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=" + str(
                        k), callback=self.parse1, meta={"company":company,"page":copy.deepcopy(k)},dont_filter=True)
                list1.append(request)
                # yield  request
        return list1
    #把每一页的数据放到item里面
    def parse1(self, response):
        if response.body != b'':

            company = response.meta["company"]
            page = response.meta["page"]
            dic = json.loads(response.body.decode(response.encoding))

            for j in range(0, dic.get("announcements").__len__()):
                item = {}
                #确实是存在没有命名的公告的
                titles = "未命名"
                if dic.get("announcements")[j]["announcementTitle"] is not None:
                    titles = re.split('[:：]',dic.get("announcements")[j]["announcementTitle"],1)
                if titles.__len__() == 2:
                    title = titles[1]
                else:
                    title = titles[0]
                adjuntUrl = dic.get("announcements")[j]["adjunctUrl"]
                adjuntUrl_time = adjuntUrl.split("/")[1]
                #防止拿不到time
                try:
                    current_time = datetime.date(int(adjuntUrl_time.split("-")[0]), int(adjuntUrl_time.split("-")[1]), int(adjuntUrl_time.split("-")[2]))
                except Exception as e:
                    print (e.__traceback__)
                    continue
                else:
                    if current_time >= Cninfospider1Spider.post:
                        pass

                    else:
                        if current_time < Cninfospider1Spider.pre:
                            index = Cninfospider1Spider.company_list.index(company)
                            #及时更新应爬取的page的范围给parse0知道,不要再多爬了
                            #加锁，只允许第一个达到这个page的进入修改Cninfospider1Spider.time_limit_list[index]
                            #否则数会不对
                            mutex1.acquire()
                            if(Cninfospider1Spider.page_thread_sequence == 0):
                                Cninfospider1Spider.page_thread_sequence = 1
                                if Cninfospider1Spider.time_limit_list[index] == Cninfospider1Spider.pageLimit:
                                    Cninfospider1Spider.time_limit_list[index] = page+1
                            else:
                                pass
                            mutex1.release()
                        else:
                            item["com"] = company
                            item["time"] = adjuntUrl_time
                            item["title"] = title.replace('<em>', '').replace('</em>','')
                            item["url"] = "http://static.cninfo.com.cn/" + adjuntUrl
                            yield item
