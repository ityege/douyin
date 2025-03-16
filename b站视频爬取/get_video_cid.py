import requests


def get_video_cids(work, headers, logger):
    bvid = work[1]
    response = requests.get("https://api.bilibili.com/x/player/pagelist?bvid=" + bvid, headers=headers)
    response = response.json()
    cids = []
    for i in response['data']:
        cids.append(str(i['cid']))
    if len(cids) > 1:
        print(f"作品有多个cid:{work}:{cids}")
        logger.info(f"作品有多个cid:{work}:{cids}")
        # raise Exception(f"视频有多个cid,目前没有处理这个逻辑,程序停止:{work}:{cids}")
    cids = ",".join(cids)
    return work[0], work[1], work[2], cids
