package com.spider.server;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import com.spider.codec.MsgSerial;
import com.spider.companyReader.CompanyReader;
import com.spider.disruptor.MessageProducer;
import com.spider.disruptor.RingBufferWorkerPoolFactory;
import com.spider.redisConn.RedisConnector;

import io.netty.channel.Channel;
import io.netty.channel.ChannelHandler;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;
import io.netty.channel.group.ChannelGroup;
import io.netty.channel.group.DefaultChannelGroup;
import io.netty.util.ReferenceCountUtil;
import io.netty.util.concurrent.GlobalEventExecutor;
//这里可能有数据持久化操作-->很影响workgroup的性能-->交给一个线程池去异步的调用执行
public class ServerHandler extends ChannelInboundHandlerAdapter {
	public static ChannelGroup channelGroup = new DefaultChannelGroup(GlobalEventExecutor.INSTANCE);
	//获得公司列表
	public static List<String> companyList = CompanyReader.getCompanyList();
	//公司查询游标-->需线程安全，不然会重复查询给多个客户端
	public static AtomicInteger listcursor =new AtomicInteger(0);
	@Override
	public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
		try{
			//实现Discard
		}finally{
			ReferenceCountUtil.release(msg);
		}
		 MsgSerial.Msg.Builder builder = MsgSerial.Msg.newBuilder();
		 	int index = listcursor.getAndIncrement();
		 	String company = null;
		 	boolean flag = true;
		 	if((index+1)>companyList.size()){
		 		flag = false;
		 		
		 	}else{
		 		company = companyList.get(index);
		 	}
		 	if(flag){
			 	//去redis里面查询数据
			 	List<String> data =	new ArrayList<>();
			 	while(data.size() == 0 && company !=null){
			 
			 		data = RedisConnector.getData(company);
			 		/**
				 	 * 如果数据为0条的话，说明大爬虫还没爬到，睡一会-->这里应当改成是大爬虫没爬到后，将没爬到的写入日志
				 	 * 这里读取日志，直接跳过当前公司，爬下一个-->后面改
				 	 * 
				 	 */
			 		if(data.size()==0){
			 			Thread.sleep(5000);
			 		}
			 		/**
				 	 * 如果数据不为50条的话，有可能只拿到了一部分数据，也可能本身数据就不到50，
				 	 * 不管如何，睡一会，确保大爬虫拿到该字段全部数据的时候再往下走
				 	 */
				 		
			 		if(data.size()!=50){
			 			Thread.sleep(5000);
			 		}
			 	}
				int count =0;
				for(String tmpstr:data){
					count ++;
					builder.setName(tmpstr);
					MsgSerial.Msg request = builder.build();
					//自己的应用服务应该有一个id生成规则
					String producerId = "ServerProducer:"+ctx.channel().remoteAddress();
					System.out.println(producerId);
					//生成一个producer
					MessageProducer messageProducer = RingBufferWorkerPoolFactory.getInstance().getMessageProducer(producerId);
					
				
					//把数据扔进去，让生产者生产数据
					messageProducer.onData(request, ctx);
				}
				System.out.println(count);
		 	}
		
	}
	@Override
	public void handlerAdded(ChannelHandlerContext ctx) throws Exception {
		 Channel channel = ctx.channel();
		 channelGroup.add(channel);
	}
}


