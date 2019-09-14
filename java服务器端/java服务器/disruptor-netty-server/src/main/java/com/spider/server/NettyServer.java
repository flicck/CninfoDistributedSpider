package com.spider.server;

import com.spider.code.NettyMsgDecoder;
import com.spider.code.NettyMsgEncoder;
import com.spider.codec.MarshallingCodeCFactory;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.buffer.PooledByteBufAllocator;
import io.netty.channel.AdaptiveRecvByteBufAllocator;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.protobuf.ProtobufVarint32FrameDecoder;
import io.netty.handler.codec.protobuf.ProtobufVarint32LengthFieldPrepender;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;

public class NettyServer {
	public NettyServer(){
		//1.创建两个工作线程组，一个用于接收网络请求（sync队列），一个用于实际处理业务的（accept之后做一些其他的事情）
		EventLoopGroup bossGroup = new NioEventLoopGroup();
		EventLoopGroup workGroup = new NioEventLoopGroup();
		//2.建立辅助类-->类似disruptor类
		ServerBootstrap serverBootstrap = new ServerBootstrap();
		try {
			serverBootstrap.group(bossGroup,workGroup)
			.channel(NioServerSocketChannel.class)
			.option(ChannelOption.SO_BACKLOG,1024) //两个队列的合计长度
			.option(ChannelOption.RCVBUF_ALLOCATOR, AdaptiveRecvByteBufAllocator.DEFAULT)  //自适应每次的数据的大小
			.option(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT)     //表示缓冲池--用到buffer直接从池里取-->提升性能
			.handler(new LoggingHandler(LogLevel.INFO))			//配置日志
			.childHandler(new ChannelInitializer<SocketChannel>() {	//处理实际的数据--》接收到数据并异步处理,但是不要在这里写业务逻辑代码，会影响性能
				@Override
				protected void initChannel(SocketChannel sc) throws Exception {	
					//和python通信的话采取delimited的分包逻辑好了
					sc.pipeline().addLast(new ProtobufVarint32LengthFieldPrepender());
					//python发消息过来就不用解码啦
				//	sc.pipeline().addLast(new ProtobufVarint32FrameDecoder());
					sc.pipeline().addLast("decoder", new NettyMsgDecoder());
					sc.pipeline().addLast("encoder", new NettyMsgEncoder());
					sc.pipeline().addLast(new ServerHandler());//如果业务很复杂会影响netty的性能
				}		
			});		
			
			//3.绑定端口，同时等待请求连接
			ChannelFuture cf = serverBootstrap.bind(8765).sync();
			System.err.println("Server startup...");
			
			cf.channel().closeFuture().sync();  //异步的关闭
		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally{
			//优雅停机
			bossGroup.shutdownGracefully();
			workGroup.shutdownGracefully();
			System.out.println("Server shutDown");
		}
		
	}
}
