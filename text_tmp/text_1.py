#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests     #获取网页信息
import traceback
import re           #正则表达式
import random
import time

import sys
sys.path.append("../../library/service")
from HeaderInfo import *

#----------------------------------------

ip_list=[]  #获取的ip列表
page=20     #设置爬取页数

#----------------------------------------


#获取html的正则匹配内容
def GetHtml( url, pattrens, proxy = {}):
    try:
        header={
            'User-Agent':random.choice(user_agent_list), 
            'Referer':random.choice(referer_list)
        }
        #print(proxy)
        html=requests.get(url, headers=header, proxies = proxy, timeout=(3,7))
        #print(html)
        if html.status_code == 200:
            return re.findall(pattrens, html.text, re.S) #忽略大小写
    except:
        return [] #无匹配内容返回空列表


#通过正则表达式，获取爬取的ip
def GetIP(url):
    try:
        pattrens = r'alt="Cn" /></td>[\s]*?<td>([\d\D]*?)</td>[\s]*?<td>([\d\D]*?)</td>'
        root=GetHtml(url, pattrens)
        #print(len(root))   当返回值为503的时候，root 的长度为0，可能是代理ip出现了问题，更换ip即可.
        for i in range(len(root)):
            #设置代理过滤方式 不获取端口号为9999的IP地址
            print(i)
            if(root[i][1]!='9999'and TestProxy(root[i])):
                print(root[i][0]+':'+root[i][1])
                ip_list.append(root[i][0]+':'+root[i][1])
                write_text(root[i][0]+':'+root[i][1]+'\n')
    except:
        print('正则匹配错误！')
        #traceback.print_exc()   #打印异常

#测试可用IP
def TestProxy(ip):
    try:
        url = 'http://www.httpbin.org/get'
        proxy_ip = 'http://' + ip[0] + ':' + ip[1]
        proxy_ips = 'https://' + ip[0] + ':' + ip[1]
        proxy = {'https': proxy_ips, 'http': proxy_ip}
        pattrens = r'"origin": "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"'
        res = GetHtml(url, pattrens, proxy)
        print(111111)
        print(res)
        print(ip)
        print(res[0]+' '+ip[0])
        if(res[0] == ip[0]):
            return 1
    except:
        print('测试IP错误！')
        return 0

def write_text(ip):
    file = open("Data.txt",'a') #打开文件，并在文件尾添加内容
    file.write(ip)              #写入文件
    file.flush()                #刷新缓冲区 
    file.close()                #关闭文件


if __name__ == '__main__':
    for i in range(page):
        print("-----"+str(i+1)+"-----")
        url ='https://www.xicidaili.com/nn/'+str(i+1)
        GetIP(url)
        time.sleep(5)
