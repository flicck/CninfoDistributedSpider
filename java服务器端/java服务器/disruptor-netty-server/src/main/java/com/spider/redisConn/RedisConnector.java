package com.spider.redisConn;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import redis.clients.jedis.Jedis;

public class RedisConnector {
	public static Jedis jedis = new Jedis("localhost", 6379);
	static {
		jedis.select(2);
	}
	public static List<String> getData(String str) {
		List<String> li = new ArrayList<>();
		Set<String> set = jedis.keys(str+"*");
		for (String key : set) {
			String tmpstr = jedis.get(key);
			li.add(tmpstr);
		}
		return li;
	}
	public static void main(String[] args) {
		List<String> data = getData("中原高速");
		
		System.out.println(data);
		System.out.println(data.size());
		if(data.size()==0){
			System.out.println("yes");
		}
	}
	
}
