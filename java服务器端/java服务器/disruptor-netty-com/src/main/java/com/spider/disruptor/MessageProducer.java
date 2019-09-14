package com.spider.disruptor;



import com.lmax.disruptor.RingBuffer;
import com.spider.codec.MsgSerial;
import com.spider.codec.MsgSerialWapper;

import io.netty.channel.ChannelHandlerContext;

public class MessageProducer {
	protected String producerId;
	private RingBuffer<MsgSerialWapper> ringBuffer;
	public MessageProducer(String producerId,RingBuffer<MsgSerialWapper> ringBuffer){
		this.ringBuffer = ringBuffer;
		this.producerId = producerId;
	}
	//生产一个wapper
	public void onData(MsgSerial.Msg msg,ChannelHandlerContext ctx){
		long sequence = ringBuffer.next();
		try {
			MsgSerialWapper wapper = ringBuffer.get(sequence);
			wapper.setMsg(msg);
			wapper.setCtx(ctx);
		} finally {
			ringBuffer.publish(sequence);
		}
	}
}
