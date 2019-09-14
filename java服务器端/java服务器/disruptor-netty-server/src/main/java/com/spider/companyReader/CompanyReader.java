package com.spider.companyReader;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class CompanyReader {
	public static List<String> getCompanyList(){
		List<String> li = new ArrayList<String>();
		BufferedReader br = null;
		try {
			br = new BufferedReader(new InputStreamReader(new FileInputStream("C:/Users/stawind/Desktop/list/WaitSearchCompanyList.txt")));
			String tmp = null;
			while((tmp=br.readLine())!=null){
				li.add(tmp);
			}
		} catch (Exception e) {
		
			e.printStackTrace();
		}finally{
			try {
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return li;
	}
	public static void main(String[] args) {
		List<String> companyList = CompanyReader.getCompanyList();
		System.out.println(companyList);
	}
}
