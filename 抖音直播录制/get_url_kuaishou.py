# 本人没有系统的学习过爬虫,这个推流地址的提取存在些问题，出现问题见招拆招
import random

import requests, re, json, time, tools, sys
import traceback
from bs4 import BeautifulSoup


def call_api(url, headers, logger_error):
    try:
        response = requests.get(url, headers=headers)
        # print(response.headers)
        return response.text
    except requests.exceptions.RequestException as e:
        # 使用traceback模块获取堆栈跟踪信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 格式化堆栈跟踪信息
        tb_info = ''.join(traceback.format_tb(exc_traceback))
        # 记录错误和堆栈跟踪信息到日志
        logger_error.error("请求失败: %s\n%s", e, tb_info)
        print(e, tb_info, file=sys.stderr)
        return None


def get_url(short_id, logger_error, cur):
    url = "https://live.kuaishou.com/u/" + short_id
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'live.kuaishou.com',
        'Referer': 'https://live.kuaishou.com/my-follow/living',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    cur.execute(
        "select value from luzhi.conf where program='kuaishou_record' and key  = 'cookie' ")
    headers['Cookie'] = cur.fetchone()[0]
    cur.execute(
        "select value from luzhi.conf where program='record' and key  = 'iscache'")
    iscache = cur.fetchone()[0]
    # 这个接口会请求失败，需要重试
    html = ""
    for i in range(10):
        response = call_api(url, headers, logger_error)
        if response is not None:
            html = response
            break
        time.sleep(random.randint(5, 10))
    # 保存html
    if iscache == '1':
        cache = open(f"record_tmp_path/{int(time.time())}_kuaishou_{short_id}.html", "w")
        cache.write(html)
        cache.flush()
        cache.close()
    soup = BeautifulSoup(html, 'lxml')
    scripts = soup.find_all('script')
    for index, script in enumerate(scripts):
        if "window.__INITIAL_STATE__" in script.text:
            finds = re.findall("window.__INITIAL_STATE__=(.*?);\(function", script.text)
            find = finds[0].replace("undefined", "null")
            json_obj = json.loads(find)
            liveStream = json_obj["liveroom"]["playList"][0]["liveStream"]
            if "playUrls" in liveStream:
                playUrls = liveStream["playUrls"]
            else:
                return None
            # 保证主播开播
            if len(playUrls) > 0:
                representation = playUrls[0]["adaptationSet"]["representation"]
                # 找到最高画质
                max_bitrate = max([element["bitrate"] for element in representation])
                for element in representation:
                    if element["bitrate"] == max_bitrate:
                        return element["url"]
    return None


if __name__ == "__main__":
    logger = tools.get_transcode_log_conf("debug.log")
    conn = tools.connect_db(True)
    cur = conn.cursor()
    print(get_url("zhangmingyang88888", logger, cur))
    # print(get_url("3xuvrfygnh45ajc", logger, cur))

