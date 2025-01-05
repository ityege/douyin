import time

from bs4 import BeautifulSoup
import json
import requests
import tools
import re


# 本人没有系统的学习过爬虫,这个推流地址的提取存在些问题，出现问题见招拆招
# https://live.douyin.com/webcast/room/web/enter/?aid=6383&app_name=douyin_web&live_id=1&device_platform=web&language=zh-CN&web_rid=49839037432
def get_url(uid, name, logger_info, cur):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://live.douyin.com/',
    }
    # 删除视频
    cur.execute(
        "select value from luzhi.conf where program='douyin_record' and key  = 'cookie' ")
    cookie = cur.fetchone()[0]
    headers["Cookie"] = cookie
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
        script_text = script.text
        if "h265" in script_text and "origin" in script_text and "main" in script_text and "flv" in script_text and "status" in script_text:
            finds = re.findall(r"self.__pace_f.push\(\[1,(.*?)\]\)", script.text)
            json_obj = json.loads(finds[0])
            # print(json_obj)
            json_obj = json.loads(json_obj[2:])
            live_status = json_obj[3]["state"]["roomStore"]["roomInfo"]["room"]["status"]
            # 状态2是正在直播
            if live_status == 2:
                # 获取画质
                # state.cameraStore.cameraInfoList[0].h265Stream.flv_pull_url
                flv_pull_url = json_obj[3]["state"]["cameraStore"]["cameraInfoList"][0]["h265Stream"]["flv_pull_url"]
                # print(flv_pull_url)
                if "FULL_HD1" in flv_pull_url:
                    return flv_pull_url["FULL_HD1"]
                if "HD1" in flv_pull_url:
                    return flv_pull_url["HD1"]
            else:
                return None
    return None


if __name__ == '__main__':
    conn = tools.connect_db(True)
    cur = conn.cursor()
    # with open("input/input.txt","r") as f:
    #     for line in f:
    #         line=line.strip()
    #         if line=="":
    #             continue
    #         print(line)
    #         print(get_url(line,"","",cur))

    print(get_url("", "", "", cur))
