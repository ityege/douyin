import time

from bs4 import BeautifulSoup
import json
import requests
import traceback
import tools
import re


# 本人没有系统的学习过爬虫,这个推流地址的提取存在些问题，出现问题见招拆招
def get_url(uid,name,logger_info,cur):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://live.douyin.com/',
    }
    # 删除视频
    cur.execute(
        "select value from luzhi.conf where program='douyin_record' and key  = 'cookie' ")
    cookie = cur.fetchone()[0]
    headers["Cookie"]=cookie
    cur.execute(
        "select value from luzhi.conf where program='record' and key  = 'iscache'")
    iscache = cur.fetchone()[0]

    response = requests.get(f"https://live.douyin.com/{uid}", headers=headers, timeout=30)
    html_str = response.text
    if iscache == "1":
        cache = open(f"record_tmp_path/{int(time.time())}_douyin_{uid}.html", "w")
        cache.write(html_str)
        cache.flush()
        cache.close()
    soup = BeautifulSoup(html_str, 'lxml')
    scripts = soup.find_all('script')
    for script in scripts:
        if "h265" in script.text and "origin" in script.text:
            finds=re.findall(r"self.__pace_f.push\(\[1,(.*?)\]\)",script.text)
            json_obj=json.loads(finds[0])
            finds=re.findall(r"\"origin\":\{\"main\":\{\"flv\":\"(.*?)\"",json_obj)
            if len(finds)==0:
                return None
            else:
                return finds[0]
    return None

if __name__ == '__main__':
    conn=tools.connect_db(True)
    cur=conn.cursor()
    # with open("input/input.txt","r") as f:
    #     for line in f:
    #         line=line.strip()
    #         if line=="":
    #             continue
    #         print(line)
    #         print(get_url(line,"","",cur))
    print(get_url("527431879652","","",cur))