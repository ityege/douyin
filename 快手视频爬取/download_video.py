import shutil
import requests


def download_video(download_path_sub, download_url, id1, logger):
    is_download_success = False
    ex = None
    for i in range(5):
        if is_download_success:
            break
        try:
            # 快手视频的证书都验证不通过,快手干什么吃的
            response = requests.get(download_url, stream=True, timeout=30, verify=False)
            if response.status_code == 200:
                with open(f"{download_path_sub}\\{id1}.mp4", "wb") as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                is_download_success = True
        except Exception as e:
            is_download_success = False
            ex = e
            logger.error(f"操作失败: {str(e)}", exc_info=True)

    if not is_download_success:
        print(f"{id1}下载失败{ex}")
        logger.error(f"{id1}下载失败{ex}")


if __name__ == '__main__':
    download_video(".",
                   "",
                   "test", "")
