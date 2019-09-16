# CninfoDistributedSpider
针对巨潮资讯网上市公司公告的分布式爬虫，创新的采用了java服务器和python客户端的分布式架构，而不
是传统的redis分布式（redis分布式对集群性能要求高、容易丢失数据、大量使用不必要的网络传输）  
支持按时间段和条数查询公告，采用抓包爬取，速度非常快。但为爬虫的友好性，在多处设置了睡眠时间，可根据情况删除。  
支持windows和linux平台，linux使用的是centos7，需根据需要的库安装相应的库，修改相应的目录为linux目录，同时需要开启virtualenv，
否则centos7自带的python2.7.5会和需要安装的python3.7.4相冲突
