import os
import shutil
import sys
import time
import uuid
import csv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import requests

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from tqdm import tqdm

import tools


# 接口有验证,我们就用最简单的方法
def parse_response(response, cur, conn, user_id, logger, id_1, download_list):
    # 获取所有的列表
    aweme_list = response["aweme_list"]
    # 遍历每一个aweme
    count = 0
    for aweme in aweme_list:
        images = aweme["images"]
        video = aweme["video"]
        # 这个是文案
        desc = aweme["desc"]
        aweme_id = aweme["aweme_id"]
        # 这个是视频
        if images == None:
            # 遍历码率
            bit_rate_1 = video["bit_rate"]
            # 获取到码率最高的视频链接
            max_bit_rate = max(bit_rate_1, key=lambda x: x["bit_rate"])
            max_bit_rate = max_bit_rate["bit_rate"]
            for bit_rate_2 in bit_rate_1:
                if bit_rate_2["bit_rate"] == max_bit_rate:
                    videao_download_url = bit_rate_2["play_addr"]["url_list"][0]
                    element_id = str(uuid.uuid4())
                    cur.execute(
                        "INSERT INTO paqu.film_status (id,film_up_id,download_url,type1,download_id,status,desc1,aweme_id) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                        (element_id, user_id, videao_download_url, "视频", id_1, "未下载", desc, aweme_id))
                    download_list.append((element_id, videao_download_url, "视频", desc, aweme_id))
                    # 提交事务

                    # logger.info(f"添加下载任务成功,id:{element_id},up主id:{user_id},url:{videao_download_url}")


        # 这个是图片
        else:
            for image in images:
                image_download_url = image["download_url_list"][0]
                element_id = str(uuid.uuid4())
                cur.execute(
                    "INSERT INTO paqu.film_status (id,film_up_id,download_url,type1,download_id,status,desc1,aweme_id) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (element_id, user_id, image_download_url, "图片", id_1, "未下载", desc, aweme_id))
                download_list.append((element_id, image_download_url, "图片", desc, aweme_id))
                # logger.info(f"添加下载任务成功,id:{element_id},up主id:{user_id},url:{image_download_url}")


def download_video(url, download_path, user_id, logger, cur, conn, id_1, film_up_name):
    service = Service('C:/devtools/chrome/chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=D:/code/pythontest/data")
    cur.execute("SELECT value FROM paqu.conf WHERE program='douyin_paqu' and key='is_headless'")
    headless = cur.fetchone()[0]
    if headless == '1':
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    # 打开抖音，博主主页
    driver.get(url)
    time.sleep(30)
    cookies = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    url = None
    headers = None
    # 获取请求地址
    print("开始获取资源列表地址")
    logger.info("开始获取资源列表地址")
    for request in driver.requests:
        request_url = request.url
        # 获取作者作品的url
        if request_url.startswith('https://www.douyin.com/aweme/v1/web/aweme/post/'):
            url = request.url
            headers = request.headers
    driver.quit()
    response_list = []
    if url is not None and headers is not None:
        print("获取资源列表地址成功")
        logger.info("获取资源列表地址成功")
        print("开始获取资源列表")
        logger.info("开始获取资源列表")
        min_cursor = 0

        while True:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            query_params['max_cursor'] = [min_cursor]
            new_query = urlencode(query_params, doseq=True)
            new_url = urlunparse(parsed_url._replace(query=new_query))
            logger.info(f"获取资源列表请求url{new_url}")
            response = requests.get(new_url, headers=headers, cookies=cookies_dict, timeout=10)
            response = response.json()
            min_cursor = response["max_cursor"]
            has_more = response["has_more"]
            # 将响应结果写入文件
            # logger.info(f"响应结果:{response}")
            response_list.append(response)
            if has_more == 0:
                break
            time.sleep(4)
        print("获取资源列表成功")
        logger.info("获取资源列表成功")

    else:
        print('获取资源列表地址失败')
        logger.info('获取资源列表地址失败')
        sys.exit(-100)
    # 开始解析返回列表

    print("开始解析返回结果")
    logger.info("开始解析返回结果")
    count = 0
    download_list = []
    for response in response_list:
        aweme_list = response["aweme_list"]
        count += len(aweme_list)
        parse_response(response, cur, conn, user_id, logger, id_1, download_list)
    print(f"解析返回结果完成获取到资源的数量:{count}")
    logger.info(f"解析返回结果完成获取到资源的数量:{count}")
    #     开始下载元素
    print("开始下载视频和图片")
    logger.info("开始下载视频和图片")
    sub_path = film_up_name + "_" + tools.get_current_time0()
    download_path_sub = os.path.join(download_path, sub_path)
    if not os.path.exists(download_path_sub):
        os.makedirs(download_path_sub)
    for element in tqdm(download_list, desc='下载视频和图片中', unit='视频/图片'):
        element_id = element[0]
        download_url = element[1]
        type1 = element[2]

        headers = {
            # 可能需要添加额外的headers，如User-Agent等
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            'referer': "https://www.douyin.com/",
            'origin': "https://www.douyin.com"
        }
        if type1 == "视频":
            download_path_sub_sub = os.path.join(str(download_path_sub), element_id + ".mp4")
            is_download_success = False
            ex = None
            for i in range(5):
                if is_download_success:
                    break
                try:
                    response = requests.get(download_url, stream=True, timeout=30, headers=headers)
                    if response.status_code == 200:
                        with open(download_path_sub_sub, "wb") as f:
                            response.raw.decode_content = True
                            shutil.copyfileobj(response.raw, f)
                        is_download_success = True
                except Exception as e:
                    is_download_success = False
                    ex = e
            if is_download_success:
                cur.execute(
                    "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s,is_download_success=%s,status=%s WHERE id=%s",
                    (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 1, "已下载",
                     element_id))

                # logger.info(f"下载视频成功,id:{element_id},url:{download_url},path:{download_path_sub_sub}")
            else:
                cur.execute(
                    "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s,is_download_success=%s,status=%s WHERE id=%s",
                    (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 0, "未下载",
                     element_id))

                print(f"下载视频失败,id:{element_id},url:{download_url},原因:{ex}")
                # logger.error(f"下载视频失败,id:{element_id},url:{download_url},原因:{ex}")


        elif type1 == "图片":
            download_path_sub_sub = os.path.join(str(download_path_sub), element_id + ".webp")
            is_download_success = False
            ex = None
            for i in range(5):
                if is_download_success:
                    break
                try:
                    response = requests.get(download_url, stream=True, timeout=30, headers=headers)
                    if response.status_code == 200:
                        with open(download_path_sub_sub, "wb") as f:
                            response.raw.decode_content = True
                            shutil.copyfileobj(response.raw, f)

                        is_download_success = True
                except Exception as e:
                    is_download_success = False
                    ex = e
            if is_download_success:
                cur.execute(
                    "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s ,is_download_success=%s ,status=%s WHERE id=%s",
                    (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 1, "已下载",
                     element_id))

                # logger.info(f"下载图片成功,id:{element_id},url:{download_url},path:{download_path_sub_sub}")
            else:
                cur.execute(
                    "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s ,is_download_success=%s ,status=%s WHERE id=%s",
                    (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 0, "未下载",
                     element_id))

                # print(f"下载图片失败,id:{element_id},url:{download_url},原因:{ex}")

    print("下载视频和图片结束")
    logger.info("下载视频和图片结束")
    print("开始保存文案")
    logger.info("开始保存文案")
    with open(os.path.join(str(download_path_sub), '文案.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(("视频id", "文案", "抖音资源标识"))
        # 假设我们只想将集合中的每个元素作为单独的一行写入
        for element in download_list:
            element_id = element[0]
            desc = element[3]
            aweme_id = element[4]
            writer.writerow((element_id, desc, "aweme_id:"+aweme_id))
    print("保存文案结束")
    logger.info("保存文案结束")
