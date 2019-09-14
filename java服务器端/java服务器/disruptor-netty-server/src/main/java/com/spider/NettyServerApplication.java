package com.spider;



import com.lmax.disruptor.BlockingWaitStrategy;
import com.lmax.disruptor.dsl.ProducerType;
import com.spider.disruptor.MessageConsumer;
import com.spider.disruptor.RingBufferWorkerPoolFactory;
import com.spider.server.MessageConsumerForServer;
import com.spider.server.NettyServer;


public class NettyServerApplication {
	public static void main(String[] args) {
		MessageConsumer[] consumers=new MessageConsumer[4];
		for(int i =0;i<consumers.length;i++){
			String id ="ServerConsumer:"+i;
			MessageConsumer messageConsumer = new MessageConsumerForServer(id);
			consumers[i] = messageConsumer;
		}
		RingBufferWorkerPoolFactory.getInstance().initAndStart(ProducerType.MULTI
				, 1024*1024,
				new BlockingWaitStrategy(), consumers);
		new NettyServer();
		
	}
	
}
