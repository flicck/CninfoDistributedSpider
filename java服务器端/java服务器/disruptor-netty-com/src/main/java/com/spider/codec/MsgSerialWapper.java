package com.spider.codec;

import io.netty.channel.ChannelHandlerContext;

public class MsgSerialWapper {
	private MsgSerial.Msg msg;
	private ChannelHandlerContext ctx;
	public MsgSerial.Msg getMsg() {
		return msg;
	}
	public void setMsg(MsgSerial.Msg msg) {
		this.msg = msg;
	}
	public ChannelHandlerContext getCtx() {
		return ctx;
	}
	public void setCtx(ChannelHandlerContext ctx) {
		this.ctx = ctx;
	}
	
}
