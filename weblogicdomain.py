#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''
import requests
from multiprocessing import Pool, Manager

headers = {'user-agent': 'ceshi/0.0.1'}
filename1='domain.txt'
filename2='domainresult.txt'
filename3='domainalive.txt'
filename4='domainlog.txt'

def islive(url):
    if 'http' not in url:
        url = 'http://' + url
    try:
        r = requests.get(url, timeout=5,headers=headers)
        fwlog = open(filename4, 'a')
        fwlog.write("当前站点：{}\t状态码：{}\n".format(url,r.status_code))
        fwlog.close()
        print("当前站点：{}\t状态码：{}".format(url,r.status_code))
        return r.status_code
    except:
        fwlog = open(filename4, 'a')
        fwlog.write("当前站点：{}\t响应超时\n".format(url))
        fwlog.close()
        print("当前站点：{}\t响应超时\n".format(url))

#Weblogic模糊识别模块
def isweblogic(url):
    if 'http' not in url:
        url = 'http://' + url
    try:
        url1=url+'/console/login/LoginForm.jsp'
        r1 = requests.get(url1,timeout=5,headers=headers)
        fwlog = open(filename4, 'a')
        fwlog.write("当前站点：{}\t状态码：{}\n".format(url1,r1.status_code))
        fwlog.close()
        print("当前站点：{}\t状态码：{}".format(url1,r1.status_code))
        url2=url+'/wls-wsat/CoordinatorPortType'
        r2 = requests.get(url2,timeout=5, headers=headers)
        fwlog = open(filename4, 'a')
        fwlog.write("当前站点：{}\t状态码：{}\n".format(url2,r2.status_code))
        fwlog.close()
        print("当前站点：{}\t状态码：{}".format(url2,r2.status_code))
        return r1.status_code,r2.status_code
    except:
        fwlog = open(filename4, 'a')
        fwlog.write("当前站点：{}\t响应超时\n".format(url))
        fwlog.close()

def readtxt(url,i,q):
    if islive(url)==200:
        fwa = open(filename3, 'a')
        fwa.write(url + '\n')
        fwa.close()
        r1,r2=isweblogic(url)
        if r1 == 200 or r2 == 200:
            fw = open(filename2, 'a')
            fw.write(url + '\n')
            fw.close()
    q.put(i)

# 进程池管理模块
def poolmana():
    p = Pool(20)
    q = Manager().Queue()
    fr = open(filename1, 'r')
    urls=fr.readlines()
    fr.close()
    for i in range(len(urls)):
        url = urls[i]
        url = url.replace("\n", '')
        p.apply_async(readtxt, args=(url,i,q))
    p.close()
    p.join()
    print('>>>>>任务结束\n')

def main():
    poolmana()

if "__main__" == __name__:
    main()