import requests
import get_erification_token


def get_all_videos(mid, headers):
    works = []
    pn = 1
    while True:
        params = {
            "mid": mid,
            "order": "pubdate",
            "tid": 0,
            "pn": pn,
            "ps": 40,

        }
        query = get_erification_token.get_token(params)
        response = requests.get(
            'https://api.bilibili.com/x/space/wbi/arc/search?' + query, headers=headers
        )
        response = response.json()
        work_list = response["data"]["list"]["vlist"]
        # with open('test.json', 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(work_list, ensure_ascii=False))
        if len(work_list) == 0:
            break
        for work in work_list:
            works.append((work["aid"], work["bvid"], work["title"]))
        pn += 1
    return works
