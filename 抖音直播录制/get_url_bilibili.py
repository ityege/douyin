import requests


# 参考
# https://github.com/SocialSisterYi/bilibili-API-collect/blob/feb0087e6c3efd743f86437529d047cb252959ce/docs/live/info.md
# https://github.com/SocialSisterYi/bilibili-API-collect/blob/feb0087e6c3efd743f86437529d047cb252959ce/docs/live/live_stream.md
def get_url(room_id):
    url = f"https://api.live.bilibili.com/room/v1/Room/get_info?id={room_id}&from=room"
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    json_obj = res.json()
    live_status = json_obj["data"]["live_status"]
    # 直播中
    if live_status == 1:
        url = f"https://api.live.bilibili.com/room/v1/Room/playUrl?cid={room_id}&quality=4&platform=web"
        res = requests.get(url, headers=headers)
        json_obj = res.json()
        return json_obj["data"]["durl"][0]["url"]
    return None

if __name__ == "__main__":
    print(get_url("25304523"))
