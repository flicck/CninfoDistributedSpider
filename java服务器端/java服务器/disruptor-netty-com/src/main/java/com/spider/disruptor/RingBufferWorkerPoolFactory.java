package com.spider.disruptor;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;

import com.lmax.disruptor.EventFactory;
import com.lmax.disruptor.ExceptionHandler;
import com.lmax.disruptor.RingBuffer;
import com.lmax.disruptor.SequenceBarrier;
import com.lmax.disruptor.WaitStrategy;
import com.lmax.disruptor.WorkerPool;
import com.lmax.disruptor.dsl.ProducerType;
import com.spider.codec.MsgSerial;
import com.spider.codec.MsgSerialWapper;
//池化
//整一个单例模式
public class RingBufferWorkerPoolFactory {
	private static class SingletonHolder{
		static final RingBufferWorkerPoolFactory instance  = new RingBufferWorkerPoolFactory();
	}
	private RingBufferWorkerPoolFactory(){	
	}
	public static RingBufferWorkerPoolFactory getInstance(){
		return SingletonHolder.instance;
	}
	private static Map<String,MessageProducer> producers = new ConcurrentHashMap<>();
	private static Map<String,MessageConsumer> consumers = new ConcurrentHashMap<>();
	
	private RingBuffer<MsgSerialWapper> ringBuffer;
	private SequenceBarrier sequenceBarrier;
	private WorkerPool<MsgSerialWapper> workerPool;
	//1.创建ringbuffer
	public void initAndStart(ProducerType type,int bufferSize,WaitStrategy ws,MessageConsumer[] mcs){
		this.ringBuffer = RingBuffer.create(
				type, 
				new EventFactory<MsgSerialWapper>(){
					@Override
					public MsgSerialWapper newInstance() {
						return new MsgSerialWapper();
					}			
				},bufferSize,
				ws);
	//2.创建生产者序号栅栏
		this.sequenceBarrier = this.ringBuffer.newBarrier();
	//3.设置消费者工作池
		this.workerPool = new WorkerPool<MsgSerialWapper>(this.ringBuffer
				,this.sequenceBarrier,new EventExceptionHandler(),mcs);
	//4.把所构建的消费者置入池中
		for(MessageConsumer mc:mcs){
			this.consumers.put(mc.getConsumerId(), mc);
		}
	//5.创建消费者的序号栅栏
		this.ringBuffer.addGatingSequences(this.workerPool.getWorkerSequences());
	//6.启动我们的工作池
		this.workerPool.start(Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors()));
	}
	//7.构建生产者获得方法
	public MessageProducer getMessageProducer(String id){
		MessageProducer mp = this.producers.get(id);
		if(null == mp){
			mp = new MessageProducer(id,this.ringBuffer);
			this.producers.put(id,mp);
		}
		return mp;
		
	}
	//异常静态类
	static class EventExceptionHandler implements ExceptionHandler<MsgSerialWapper>{

		@Override
		public void handleEventException(Throwable ex, long sequence, MsgSerialWapper event) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void handleOnStartException(Throwable ex) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void handleOnShutdownException(Throwable ex) {
			// TODO Auto-generated method stub
			
		}
		
	}
}

