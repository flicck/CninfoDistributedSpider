import six
import Msg_pb2
import socket
import random
import time
import queue
import threading

import action.consumer as consumer
from multiprocessing import Process
# from action.consumer import Consumer
address = ('127.0.0.1',8765)
s = socket.socket()
s.connect(address)
q = queue.Queue()
def DecodeVarint(buffer):
    mask = (1 << 32) - 1
    result_type = int
    result = 0
    shift = 0
    for b in buffer:
        result |= ((b & 0x7f) << shift)
        shift += 7
        if shift >= 64:
            raise Exception('Too many bytes when decoding varint.')
    result &= mask
    result = result_type(result)
    return result

#收到消息封装成item类，扔到队列里
class item():
    def __init__(self,tmpstr,retry_time):
        self.tmpstr = tmpstr
        self.retry_time = retry_time

max_retry_time = 3
class pythonClient(threading.Thread):
    def run(self):
        global q
        reply = b''
        count = 0
        flag = True
        while True:
            len_signal = 0
            len_buffer = b""
            data_buffer = b""

            if flag:
                msg1 = Msg_pb2.Msg()
                msg1.name = 'hello java,please give me some data,thanks'
                send_str = msg1.SerializeToString()
    # 实测拿数据实在是太快了，压一点速度，另外由于消费端消费速度其实不快（要下载公告，取决于网络速度） 可以多压一点
                time.sleep(random.randint(0, 9) / 30.0)
                s.send(send_str)


                reply = reply+s.recv(1024*1024)
            #这里判断长度头的字节数有几个，目前设置了最大4个，也就是支持int的最大上限的2倍的单个数据传输
            if reply.__len__()>=2 and reply[1] == 10:
                len_signal=1
            elif reply.__len__()>=3 and reply[2] == 10:
                len_signal=2
            elif reply.__len__()>=4 and reply[3] == 10:
                len_signal=3
            elif reply.__len__()>=5 and reply[4] == 10:
                len_signal=4
            for k in range(0,len_signal):
                len_buffer = len_buffer + six.int2byte(reply[k])
            len = DecodeVarint(len_buffer)

            for i in range(len_signal,len+len_signal):
                #长度不够，说明半包,把flag改为True，继续接收
                if(reply.__len__()<len+len_signal):
                    flag =True
                #长度足够，说明整包或粘包
                else:
                    data_buffer = data_buffer + six.int2byte(reply[i])
                    #取出data_buffer后需要去除在reply里面的这一部分内容
            reply1 = b''
            if reply.__len__()>=len+len_signal:
                for j in range(len+len_signal,reply.__len__()):
                    reply1 = reply1 + six.int2byte(reply[j])

                reply = reply1
                #大于等于len_signal且实际长度大于指示长度加len_signal说明足够获取下一个数据，将flag改为False,小于则改为True
            len_buffer1 = b''
            if reply.__len__()>=len_signal:
                for m in range(0, len_signal):
                    len_buffer1 = len_buffer1 + six.int2byte(reply[m])
                len1 = DecodeVarint(len_buffer1)
                if reply.__len__()>=len1+len_signal:
                    flag = False
            else:
                flag = True
            # print(data_buffer)
            if  data_buffer != b"":
        #注意:这里根据自己protobuf生成文件改一下
                msg3 = Msg_pb2.Msg.FromString(data_buffer)
                tmpitem = item(msg3.name,max_retry_time)
                # print(msg3.name)
                q.put(tmpitem)
                count = count +1
            # if data_buffer != b"":
            #     print (count)

if __name__ == "__main__":
    t1 = pythonClient()
    # t1.setDaemon()
    c1 = consumer.Consumer(q,"公告")
    c2 = consumer.Consumer(q, "公告")
    c3 = consumer.Consumer(q, "公告")
    c4 = consumer.Consumer(q, "公告")
    t1.start()
    c1.start()
    c2.start()
    c3.start()
    c4.start()
    print()
    # while True:
    #     time.sleep(1)
    #     print (q.qsize())
# pc = pythonClient()
# q1 = queue.Queue
# pc.startparse(q1)