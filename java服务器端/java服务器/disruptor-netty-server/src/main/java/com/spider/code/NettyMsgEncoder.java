package com.spider.code;

import com.spider.codec.MsgSerial;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.MessageToByteEncoder;

public class NettyMsgEncoder extends MessageToByteEncoder<String> {

	@Override
	protected void encode(ChannelHandlerContext ctx, String msg, ByteBuf out) throws Exception {
		MsgSerial.Msg.Builder builder = MsgSerial.Msg.newBuilder();
		builder.setName(msg);
		MsgSerial.Msg outmsg = builder.build();
		out.writeBytes(outmsg.toByteArray());
	}

}
