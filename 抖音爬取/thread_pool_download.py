import os
import requests
import shutil
import time


def thread_pool_download(element_id, download_url, type1, download_path_sub, logger):
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
            pass
            # cur.execute(
            #     "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s,is_download_success=%s,status=%s WHERE id=%s",
            #     (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 1, "已下载",
            #      element_id))

            # logger.info(f"下载视频成功,id:{element_id},url:{download_url},path:{download_path_sub_sub}")
        else:
            # cur.execute(
            #     "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s,is_download_success=%s,status=%s WHERE id=%s",
            #     (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 0, "未下载",
            #      element_id))

            print(f"下载视频失败,id:{element_id},url:{download_url},原因:{ex}")
            logger.error(f"下载视频失败,id:{element_id},url:{download_url},原因:{ex}")
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
            pass
            # cur.execute(
            #     "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s ,is_download_success=%s ,status=%s WHERE id=%s",
            #     (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 1, "已下载",
            #      element_id))

            # logger.info(f"下载图片成功,id:{element_id},url:{download_url},path:{download_path_sub_sub}")
        else:
            # cur.execute(
            #     "UPDATE paqu.film_status SET download_path=%s,download_time_unix=%s,download_time_string=%s ,is_download_success=%s ,status=%s WHERE id=%s",
            #     (download_path_sub_sub, tools.get_current_time2(), tools.get_current_time3(), 0, "未下载",
            #      element_id))

            print(f"下载图片失败,id:{element_id},url:{download_url},原因:{ex}")
            logger.error(f"下载图片成功,id:{element_id},url:{download_url},path:{download_path_sub_sub}")


def monitor_remaining_tasks(futures):
    """每秒打印剩余任务数"""
    total = len(futures)
    while True:
        completed = sum(1 for f in futures if f.done())
        remaining = total - completed
        print(f"\r剩余下载数: {remaining:3d}", end="", flush=True)
        if remaining <= 0:
            break
        time.sleep(1)
