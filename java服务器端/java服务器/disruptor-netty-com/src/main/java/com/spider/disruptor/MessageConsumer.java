package com.spider.disruptor;

import com.lmax.disruptor.WorkHandler;
import com.spider.codec.MsgSerialWapper;

public abstract class MessageConsumer implements WorkHandler<MsgSerialWapper>{
	protected String ConsumerId;
	public MessageConsumer(String ConsumerId){
		this.ConsumerId = ConsumerId;
	}
	public String getConsumerId() {
		return ConsumerId;
	}
	public void setConsumerId(String consumerId) {
		ConsumerId = consumerId;
	}
	
}
