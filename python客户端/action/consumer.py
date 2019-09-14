

count = 0
data_out_dir = "C:/Users/stawind/Desktop/data_out"
#设置请求头
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
mutex = threading.Lock()

class Consumer(threading.Thread):
    def __init__(self,queue,name):
        """
        :param queue:           队列对象, 这个要和生产线程用同一个
        :param name:            队列名称
        :return:
        """
        super(self.__class__, self).__init__()
        self.queue = queue
        self.name = name
        self.logger = LogUtil().get_logger("consumer_%s" % self.name, "consumer_%s" % self.name)


    #消费逻辑
    def Consume(self,item):
        data = json.loads(item.tmpstr)
    #创建公司名文件夹
        mutex.acquire()
        if os.path.exists(data_out_dir+"/"+data["com"]):
            pass
        else:
            os.makedirs(data_out_dir+"/"+data["com"])

    #创建日期文件夹
        if os.path.exists(data_out_dir+"/"+data["com"]+"/"+data["time"]):
            pass
        else:
            os.makedirs(data_out_dir+"/"+data["com"]+"/"+data["time"])
        mutex.release()
    #创建pdf文件，pdf文件的名称就是title
        urllib.request.urlretrieve(data["url"],data_out_dir+"/"+data["com"]+"/"+data["time"]+"/"+data["title"]+".pdf")
        if os.path.exists(data_out_dir+"/"+data["com"]+"/"+data["time"]+"/"+data["title"]+".pdf"):
            pass
        else:
    #说明没有下载到，返回失败，重爬
            return False
        return  True

    def run(self):
        global count
        '''
        线程体
        '''
        while True:
            try:
                # 从队列里取出
                item = self.queue.get()
                # 获取开始时间
                start_time = time.time()
                # 校验 c_action 的有效性
                # if not isinstance(c_action, ConsumerAction):
                #     raise Exception("%s is not ConsumerAction instance" % c_action)
                # 消费action
                result = self.Consume(item)

                # 获取结束时间
                end_time = time.time()
                run_time = end_time - start_time
                # 计算随机睡眠时间
                # random_sleep_time = round(random.uniform(0.5, self.max_sleep_time),2)
                is_success = result

                if is_success:
                    count = count+1
                # 打印日志
                self.logger.info("queue.name=【comsumer_%s】, success_count=%d,  "
                                 "remain_retry_times=%d, result=%s" %
                                 (self.name, count,item.retry_time,
                                  "SUCCESS" if is_success else "FAIL"))
                if count !=0 and count % 50 == 0:
                # 爬虫友好性：每下载50个休息一下5到8秒的睡眠时间
                    time.sleep(random.randint(3, 9))
                # 重试机制，如果不是0的话还有重试的机会
                if  is_success is False and item.retry_time > 0:
                    #让剩余重试次数减1
                    item.retry_time = item.retry_time-1


                    # 把c_action 还回队列
                    self.queue.put(item)
                # 标记队列消费成功
                self.queue.task_done()
                # # 随机睡眠
                # time.sleep(random_sleep_time)
            except Exception as e:
                self.logger.exception(e)



