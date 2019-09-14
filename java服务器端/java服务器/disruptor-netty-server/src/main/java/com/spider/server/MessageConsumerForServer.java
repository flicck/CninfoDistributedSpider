package com.spider.server;
import java.util.List;

import com.spider.codec.MsgSerial;
import com.spider.codec.MsgSerialWapper;
import com.spider.disruptor.MessageConsumer;
import com.spider.redisConn.RedisConnector;

import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelFutureListener;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.group.ChannelGroup;
public class MessageConsumerForServer extends MessageConsumer{
	public static ChannelGroup channelGroup = ServerHandler.channelGroup;
	public MessageConsumerForServer(String ConsumerId) {
		super(ConsumerId);
	}

	@Override
	public void onEvent(MsgSerialWapper event) throws Exception {
		//实际业务处理
		MsgSerial.Msg request = event.getMsg();
		ChannelHandlerContext ctx = event.getCtx();
		Channel channel = ctx.channel();
		if(channelGroup.contains(channel)){
				event.getCtx().writeAndFlush(request.getName());
		}
	}

}
