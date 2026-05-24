import datetime as t
import re
import json
import discord
from pathlib import Path


# 讀取/寫入檔案
def read_json(jsonfile: str):
    with open(f'jsonfile/{jsonfile}.json', 'r') as f:
        return json.load(f)

def write_json(jsonfile: str, content):
    with open(f'jsonfile/{jsonfile}.json', 'w') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


settings = read_json("settings")


# 時間相關
def now_time():
    return str(t.datetime.now(tz=t.timezone(t.timedelta(hours=8))))[:-13]

def time_print(content: str=''):
    print(f'[{now_time()}] {content}')


# 判斷是否為Youtube影片URL
def is_youtube_url(video_url: str):
    if re.search(r'(https?://)(www\.youtube\.com|youtu?\.be)/', video_url):
        return True
    else:
        return False


# 管理員檢查
def is_admin(member: discord.Member):
    for role in member.roles:
        if role.id == settings['id']['role']['admin'] or role.id == settings['id']['role']['sub_admin']:
            return True
    return False


# 獲取訊息連結中的特定ID
def get_channel_id(url: str):
    url = re.split('/', url)
    url = list(reversed(url))
    channel_id = int(url[1])
    return channel_id

def get_message_id(url: str):
    url = re.split('/', url)
    url = list(reversed(url))
    message_id = int(url[0])
    return message_id
    

# 判斷字串是否為自訂表情符號
# <:008_su_kawaii:1317099578557726770>
# <a:3a_su_blink1:1308410665664380950>
def is_custom_emoji(emoji_str: str):
    if re.fullmatch(r"^<a?:\w+:\d{19}>$", emoji_str):
        return True
    else:
        return False