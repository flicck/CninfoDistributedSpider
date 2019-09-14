package com.spider.code;

import java.nio.ByteOrder;

import com.spider.codec.MsgSerial;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.LengthFieldBasedFrameDecoder;

public class NettyMsgDecoder extends LengthFieldBasedFrameDecoder {
	public NettyMsgDecoder(ByteOrder byteOrder, int maxFrameLength, int lengthFieldOffset, int lengthFieldLength, int lengthAdjustment, int initialBytesToStrip, boolean failFast) {
		super(byteOrder, maxFrameLength, lengthFieldOffset, lengthFieldLength, lengthAdjustment, initialBytesToStrip, failFast);
		}
	public NettyMsgDecoder() {
		this(ByteOrder.BIG_ENDIAN, 100000, 0, 4, 2, 4, true);
		}
	@Override
	protected Object decode(ChannelHandlerContext ctx, ByteBuf byteBuf) throws Exception {
	if (byteBuf != null && byteBuf.readableBytes()>0){
	int len = byteBuf.readableBytes();
	byte[] data = new byte[len];
	byteBuf.readBytes(data);
	MsgSerial.Msg msg = MsgSerial.Msg.parseFrom(data);
	return msg;
	}
	return null;
	}
}
