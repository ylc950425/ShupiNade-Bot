import datetime as t
import re
import json


def read_json(jsonfile: str):
    """讀取 json 檔案"""
    with open(f'jsonfile/{jsonfile}.json', 'r') as f:
        return json.load(f)

def write_json(jsonfile: str, content: dict):
    """寫入 json 檔案"""
    with open(f'jsonfile/{jsonfile}.json', 'w') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


def now_time(time_zone: int):
    """獲取目前時間的字串"""
    return str(t.datetime.now(tz=t.timezone(t.timedelta(hours=time_zone))))[:-13]

def time_print(content: str = ""):
    """列印前面加上時間標記的字串"""
    print(f'[{now_time(8)}] {content}')


def is_youtube_url(video_url: str):
    """判斷字串是否含有 YouTube 影片 URL"""
    if re.search(r"(https?://)(www\.youtube\.com|youtu?\.be)/", video_url):
        return True
    else:
        return False


def get_channel_id(url: str):
    """獲取 Discord 訊息連結中的頻道 ID"""
    url = re.split('/', url)
    url = list(reversed(url))
    channel_id = int(url[1])
    return channel_id

def get_message_id(url: str):
    """獲取 Disocrd 訊息連結中的訊息 ID"""
    url = re.split('/', url)
    url = list(reversed(url))
    message_id = int(url[0])
    return message_id
    


def is_custom_emoji(emoji_str: str):
    """
    判斷字串是否含有自訂表情符號\n
    `<:008_su_kawaii:1317099578557726770>`\n
    `<a:3a_su_blink1:1308410665664380950>`
    """
    if re.fullmatch(r"^<a?:\w+:\d{19}>$", emoji_str):
        return True
    else:
        return False