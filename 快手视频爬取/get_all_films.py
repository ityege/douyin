import requests
import json


# 快手的网页端请求参数没有验证机制,不同于b站和抖音,这点相对好爬,但是不支持图片,只能爬取视频


def get_all_films(userId, headers):
    pcursor = ""
    index = 1
    result1 = []
    while True:
        json_data = {
            'operationName': 'visionProfilePhotoList',
            'variables': {
                'userId': userId,
                'pcursor': pcursor,
                'page': 'profile',
            },
            'query': 'fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContentWithLiveInfo on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    livingInfo\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContentWithLiveInfo\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://www.kuaishou.com/graphql', headers=headers, json=json_data).json()
        for feed in response["data"]["visionProfilePhotoList"]["feeds"]:
            if feed["photo"]["photoH265Url"]:
                result1.append((feed["photo"]["id"], feed["photo"]["caption"], feed["photo"]["photoH265Url"]))
            else:
                result1.append((feed["photo"]["id"], feed["photo"]["caption"], feed["photo"]["photoUrl"]))
        # with open(f"{index}.json", "w") as f:
        #     f.write(json.dumps(response, ensure_ascii=False))
        index += 1
        pcursor = response["data"]["visionProfilePhotoList"]["pcursor"]
        if "no_more" == response["data"]["visionProfilePhotoList"]["pcursor"]:
            break
    return result1


if __name__ == '__main__':
    # 全是视频
    result = get_all_films(userId="")
    print(result)
