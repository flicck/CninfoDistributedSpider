from scrapy import cmdline
import datetime
import time
import shutil
import os
#爬虫任务定时设置

#这是为爬虫能够续爬而创建的目录。存储续爬需要的数据
recoderDir = r"C:/Users/stawind/Desktop/spider/cninfospider1"
#判断爬虫是否在运行的标记
checkFile = "C:/Users/stawind/Desktop/spider/isRunning.txt"

startTime = datetime.datetime.now()
print(f"startTime={startTime}")

i = 0
moniter = 0

while True:
    isRunning = os.path.isfile(checkFile)
    if not isRunning:
        #在爬虫启动之前处理一些事情，清理掉jobdir = crawls
        isExsit = os.path.isdir(recoderDir)
        print(f"cninfospider not running,ready to start.isExsit:{isExsit}")
        if isExsit:
            #删除续爬目录crawls及目录下所有文件
            removeRes = shutil.rmtree(recoderDir)
            print(f"At time:{datetime.datetime.now()}, delete res:{removeRes}")
        else:
            print(f"At time:{datetime.datetime.now()}, Dir:{recoderDir} is not exsit.")
        time.sleep(20)
        clawerTime = datetime.datetime.now()
        waitTime = clawerTime - startTime
        print(f"At time:{clawerTime}, start clawer: mySpider !!!, waitTime:{waitTime}")
        cmdline.execute('scrapy crawl cninfospider1 -s JOBDIR=C:/Users/stawind/Desktop/spider/cninfospider1/storeMyRequest'.split())
        break #爬虫结束后退出脚本
    else:
        print(f"At time:{datetime.datetime.now()}, mySpider is running, sleep to wait.")
    i += 1

    time.sleep(10)
    moniter += 10
    if moniter >= 1440:
        break

