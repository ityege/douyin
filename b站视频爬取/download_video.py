import shutil

import requests

import get_erification_token


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
    response = requests.get("https://api.bilibili.com/x/player/wbi/playurl?" + query, headers=headers)
    response = response.json()
    download_url = response["data"]["durl"][0]["url"]
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
            print(e)
            logger.error(f"操作失败: {str(e)}", exc_info=True)

    if not is_download_success:
        print(f"{bvid}_{cid}下载失败")
        logger.error(f"{bvid}_{cid}下载失败")
