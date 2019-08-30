import requests
from bs4 import BeautifulSoup
import random
import re
import os
import hashlib
import time
import threading
from multiprocessing import Pool #进程池
from concurrent.futures import ThreadPoolExecutor
import json
import pandas as pd
from datetime import datetime

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]
START_URL = 'http://bb.ergeduoduo.com/baby/bb.php?type=getvideos&collectid=29&interver=8&page={}&pagesize=30&grade=1_3&user=863064010482414&prod=childstory_ar_4.3.5.0&corp=duoduo&source=childstory_ar_4.3.5.0_pp&srcver=story&ver=1&imei=863064010482414&sdkv=22&androidid=48f17fedaf991418&protect=1'
STORAGE_DIR = r'C:\STORAGE\ergeduoduo'


def get_md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def download_picture(future):
    '''
    根据url，下载图片，保存到指定位置
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':random.choice(USER_AGENT_LIST),
    }
    urls = future.result()
    for url in urls:
        try:
            r  = requests.get(url,headers=headers,timeout=3)
        except:
            continue
        filepath = os.path.join(STORAGE_DIR,get_md5(url)+'.mp4')
        time.sleep(random.randint(1,4))
        if r.status_code == 200 and not os.path.exists(filepath):
            f = open(filepath,'wb')
            f.write(r.content)
            f.close()
            print('{} download success'.format(filepath))

def get_content(url):
    '''
    返回url的html内容
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':random.choice(USER_AGENT_LIST),
    }
    try:
        r = requests.get(url,headers=headers,timeout=2)
    except:
        return {}
    if r.status_code == 200:
        return r.json()

def ergeduoduo(url):
    dic_data = get_content(url)
    urls = []
    for dic in dic_data.get('list'):
        if 'downurl' in dic.keys():
            url = dic.get('downurl')
            urls.append(url)
    return urls

if __name__ == '__main__':
    excutor = ThreadPoolExecutor()
    for i in range(1,15):
        url = START_URL.format(i)
        excutor.submit(ergeduoduo,url).add_done_callback(download_picture)
    excutor.shutdown()

    print('-----------------------END--------------------------')






