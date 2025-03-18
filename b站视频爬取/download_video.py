import shutil

import requests

import get_erification_token

# 这个接口会报请求频繁,目前解决办法就是更加频繁请求,让他返回数据
def download_video(download_path_sub, bvid, cid, title, headers, logger):
    params = {
        "cid": cid,
        "bvid": bvid,
        "qn": 80,
        "fnval": 1,
        "fourk": 0,
        "otype": "json",

    }
    query = get_erification_token.get_token(params)
    is_query_success = False
    ex = None
    download_url = None
    for i in range(10):
        if is_query_success:
            break
        try:
            response = requests.get("https://api.bilibili.com/x/player/wbi/playurl?" + query, headers=headers)
            response = response.json()
            # 请求成功了
            if response["code"] == 0:
                download_url = response["data"]["durl"][0]["url"]
                is_query_success = True
        except Exception as e:
            is_query_success = False
            ex = e
            logger.error(f"download_video:查询失败: {str(e)}", exc_info=True)
    if not is_query_success:
        print(f"{query}:download_video查询失败:{ex}")
        logger.error(f"{query}:download_video:查询失败{ex}")
    is_download_success = False
    for i in range(5):
        if is_download_success:
            break
        try:
            response = requests.get(download_url, stream=True, timeout=30, headers=headers)
            if response.status_code == 200:
                with open(f"{download_path_sub}\\{bvid}_{cid}.mp4", "wb") as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                is_download_success = True
        except Exception as e:
            is_download_success = False
            ex = e
            logger.error(f"download_video:下载失败: {str(e)}", exc_info=True)

    if not is_download_success:
        print(f"{bvid}_{cid}:download_video:下载失败{ex}")
        logger.error(f"{bvid}_{cid}:download_video:下载失败{ex}")
