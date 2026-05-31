import discord
from discord import Interaction, ui
from discord.ext import tasks
from Define.Classes import MyBot, MyCog, MyView, MyModal
from Define.CommandsGroup import YoutubeCommandsGroup
import Define.Functions as func
import requests
import datetime as t
import pytchat
import asyncio
import re
# import filecmp
# import shutil
import os
from typing import Literal
import aiohttp
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


settings = func.read_json("settings")
youtube_data = func.read_json("youtube_data")

youtube_data_dirty = False


PLAYLIST_ID = youtube_data['playlist_id']
CHANNEL_ID = youtube_data['channel_id']


hololive_channel_id = {
    #'UC97104KkGIEPvOYABW-3I0Q', #test_YLC
    #'UCkr7uCq7BZO2perY5PqX3lw', #test_olea
    'UCp6993wxpyDPHUpavwDFqgg', #sora
    'UCDqI2jOz0weumE8s7paEk6g', #roboco
    'UC5CwaMl1eIgY8h02uZw7u8A', #suisei
    'UC-hM6YJuNYVAmUWxeIr9FeA', #miko
    'UC0TXe_LYZ4scaW2XMyi5_kw', #azki
    'UC1CfXB_kRs3C-zaeTG3oGyg', #haachama
    'UCD8HOxPs4Xvsm8H0ZxXGiBw', #mel
    'UCdn5BQ06XqgXoAxIhbqw5Rg', #fubuki
    'UCFTLzh12_nrtzqBPsTCqenA', #akiroze
    'UCQ0UDLQCjY0rmuxCDE38FGg', #matsuri
    'UC1opHUrw8rvnsadT-iGp7Cg', #aqua
    'UC1suqwovbL1kzsoaZgFZLKg', #choco
    'UC7fk0CB07ly8oSl0aqKkqFg', #ayame
    'UCvzGlP9oQwU--Y0r9id_jnA', #subaru
    'UCXTpFs_3PqI41qX2d9tL2Rw', #shion
    'UChAnqc_AY5_I3Px5dig3X1Q', #korone
    'UCp-5t9SrOQwXMU7iIjQfARg', #mio
    'UCvaTdHTWBGv3MKj3KVqJVCw', #okayu
    'UC1DCedRgGHBdm81E1llLhOQ', #pekora
    'UCCzUftO8KOVkV4wQG1vkUvg', #marine
    'UCdyqAaZDKHXg4Ahi7VENThQ', #noel
    'UCvInZx9h3jC2JzsIzoOebWg', #flare
    'UCl_gCybOJRIgOXw6Qb4qJzQ', #rushia
    'UC1uv2Oq6kNxgATlCiez59hw', #towa
    'UCa9Y57gfeY0Zro_noHRVrnw', #luna
    'UCqm3BQLlJfvkTsX_hvm0UmA', #watame
    'UCZlDXzGoo7d44bwdNObFacg', #kanata
    'UCS9uQI-jC3DE0L4IpXyvr6w', #coco
    'UCAWSyEs_Io8MtpY3m-zqILA', #nene
    'UCFKOVgVbGmX65RxO3EtH3iw', #lamy
    'UCK9V2B22uJYu3N7eR_BT9QA', #polka
    'UCUKD-uaobj9jiqB-VXt71mA', #botan
    'UCgZuwn-O7Szh9cAgHqJ6vjw', #aloe
    'UC6eWCld0KwmyHFbAqK3V-Rw', #koyori
    'UCENwRMx5Yh42zWpzURebzTw', #laplus
    'UCIBY1ollUsauvVi4hW4cumw', #chloe
    'UCs9_O1tRPMQTHQ-N_L6FU2g', #lui
    'UC_vMYWcDjmfdpH6r4TTn1MQ', #iroha
    'UCHsx4Hqa-1ORjQTh9TYDhww', #kiara
    'UCL_qhgtOy0dy1Agp8vkySQg', #calli
    'UCMwGHR0BTZuLsmjY_NT5Pwg', #ina
    'UCoSrY_IQQVpmIRZ9Xf-y93g', #gura
    'UCyl1z3jo3XHR1riLFKG5UAg', #ame
    'UC8rcEBzJSleTkf_-agPM20g', #irys
    'UC3n5uGu18FoCy23ggWWp8tA', #mumei
    'UCgmPnx-EEeOrZSg5Tiw7ZRQ', #bae
    'UCmbs8T6MWqUHP1tIQvSgKrg', #kronii
    'UCO_aKKYxn4tvrqPjcTzZ6EQ', #fauna
    'UCsUj0dszADCGbF3gNrQEuSQ', #sana
    'UC9p_lqQ0FEDz327Vgf5JwqA', #biboo
    'UCgnfPPb9JI3e9A4cXHnWbyg', #shiori
    'UC_sFNM0z0MWm9A6WlKPuMMg', #nerissa
    'UCt9H_RpQzhxzlyBxFqrdHqA', #fuwamoco
    'UCDHABijvPBnJm7F-KlNME3w', #gigi
    'UCl69AEx4MdqMZH7Jtsm7Tig', #raora
    'UCvN5h1ShZtc7nly3pezRayg', #cecilia
    'UCW5uhrG1eCBYditmhL0Ykjw', #liz
    'UCAoy6rzhSf4ydcYjJw3WoVg', #iofi
    'UCOyYb1c43VlX9rc_lT6NKQw', #risu
    'UCP0BspO_AMEe3aQqqpo89Dg', #moona
    'UC727SQYUvx5pDDGQpTICNWg', #anya
    'UChgTyjG-pdNvxxhdsXfHQ5Q', #reine
    'UCYz_5n-uDuChHtLo7My1HnQ', #ollie
    'UCjLEmnpCNeisMxy134KPwWw', #kobo
    'UCTvHWSfBZgtxE4sILOaurIQ', #zeta
    'UCZLZ8Jjx_RN2CXloOmgTHVg', #kaela
    'UC1iA6_NT4mtAcIII6ygrvCw', #hajime
    'UCdXAk5MpyLD8594lm_OvtGQ', #raden
    'UCMGfV7TVTmHhEErVJg1oHBQ', #ao
    'UCtyWhCj3AqKh2dXctLkDtng', #ririka
    'UCWQtYtq9EOB4-I5P-3fh8lA', #kanade
    'UC9LSiN9hXI55svYEBrrK-tw', #riona
    'UCGzTVXqMQHa4AgJVJIVvtDQ', #vivi
    'UCjk2nKmHzgH5Xy-C5qYRd5A', #su
    'UCKMWFR6lAstLa7Vbf5dH7ig', #chihaya
    'UCuI_opAVX6qbxZY-a-AxFuQ', #niko

    'UCt30jJgChL8qeT9VPadidSw' #ui
}


def get_thumbnail_url(video_data: dict):
    if "maxres" in video_data['snippet']['thumbnails']:
        return video_data['snippet']['thumbnails']['maxres']['url']

    elif "standard" in video_data['snippet']['thumbnails']:
        return video_data['snippet']['thumbnails']['standard']['url']

    elif "high" in video_data['snippet']['thumbnails']:
        return video_data['snippet']['thumbnails']['high']['url']

    elif "medium" in video_data['snippet']['thumbnails']:
        return video_data['snippet']['thumbnails']['medium']['url']

    elif "default" in video_data['snippet']['thumbnails']:
        return video_data['snippet']['thumbnails']['default']['url']
    
    return None
    
    # if 'maxres' in video_data['snippet']['thumbnails']:
    #     return f'https://img.youtube.com/vi/{video_data["id"]}/maxresdefault.jpg'

    # elif 'standard' in video_data['snippet']['thumbnails']:
    #     return f'https://img.youtube.com/vi/{video_data["id"]}/sddefault.jpg'

    # elif 'high' in video_data['snippet']['thumbnails']:
    #     return f'https://img.youtube.com/vi/{video_data["id"]}/hqdefault.jpg'

    # elif 'medium' in video_data['snippet']['thumbnails']:
    #     return f'https://img.youtube.com/vi/{video_data["id"]}/mqdefault.jpg'

    # elif 'default' in video_data['snippet']['thumbnails']:
    #     return f'https://img.youtube.com/vi/{video_data["id"]}/default.jpg'


# 觀看數檢查操作面板
class ViewsCheckPanelView(MyView):
    def __init__(self, *, timeout=180, user_id):
        super().__init__(timeout=timeout, user_id=user_id)
        self.embed = discord.Embed(title="影片觀看數紀錄", color=0xFF0080)
        self.page_index = 0
        self.total_page = int((len(youtube_data['views_check']) - 1) / 5) + 1

        self.prev_btn = ui.Button(label="◀上一頁", row=1, style=discord.ButtonStyle.blurple)
        self.prev_btn.callback = lambda i: self.flip_page(i, -1)
        self.prev_5_btn = ui.Button(label="◀◀上五頁", row=2, style=discord.ButtonStyle.blurple)
        self.prev_5_btn.callback = lambda i: self.flip_page(i, -5)
        self.next_btn = ui.Button(label="下一頁▶", row=1, style=discord.ButtonStyle.blurple)
        self.next_btn.callback = lambda i: self.flip_page(i, 1)
        self.next_5_btn = ui.Button(label="下五頁▶▶", row=2, style=discord.ButtonStyle.blurple)
        self.next_5_btn.callback = lambda i: self.flip_page(i, 5)
        self.add_item(self.prev_btn)
        self.add_item(self.prev_5_btn)
        self.add_item(self.next_btn)
        self.add_item(self.next_5_btn)
        self.update_page()
        

    @discord.ui.button(label="新增歌曲", row=0, style=discord.ButtonStyle.green)
    async def add_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(ViewsCheckAddModal())
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.add_video", e)
    
    @discord.ui.button(label="刪除歌曲", row=0, style=discord.ButtonStyle.red)
    async def delete_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message(view=ViewsCheckRemoveView(user_id=self.user_id))
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.delete_video", e)

    # @discord.ui.button(label="編輯歌曲", row=0, style=discord.ButtonStyle.blurple)
    # async def edit_video(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     try:
    #         await interaction.response.send_message("功能暫未啟用", ephemeral=True)
    #     except Exception as e:
    #         self.report_error(__file__, f"{self.__class__.__name__}.edit_video", e)

    async def flip_page(self, interaction: Interaction, page_num: int = 0):
        try:
            self.page_index += page_num
            self.total_page = int((len(youtube_data['views_check']) - 1) / 5) + 1
            self.update_page()
            await interaction.response.edit_message(embed=self.embed, view=self)
        
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.flip_page", e)

    def update_page(self):
        self.embed.clear_fields()
        for i in range(self.page_index * 5, self.page_index * 5 + 5):
            try:
                video = youtube_data['views_check'][i]
            except IndexError:
                break
            self.embed.add_field(
                name = video['name'],
                value = f"ID: [{video['id']}](https://youtu.be/{video['id']})\n觀看數: {video['views']:,}",
                inline = False
            )

        self.prev_btn.disabled = (self.page_index <= 0)
        self.prev_5_btn.disabled = (self.page_index <= 4)
        self.next_btn.disabled = (self.page_index + 1 >= self.total_page)
        self.next_5_btn.disabled = (self.page_index + 5 >= self.total_page)

# 觀看數檢查功能: 新增
class ViewsCheckAddModal(MyModal):
    def __init__(self, *, title = ..., timeout = None):
        super().__init__(title=title, timeout=timeout)
        self.title = "新增歌曲"

    name = discord.ui.TextInput(label="歌曲名稱", row=0)
    url = discord.ui.TextInput(label="URL/ID", row=1)
    view_count = discord.ui.TextInput(label="初始觀看數", row=2, default="0")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            name = self.name.value

            id = re.findall(r'[a-zA-Z0-9-_]{11}', self.url.value)
            if id:
                id = id[0]
            else:
                await interaction.response.send_message(content="URL/ID格式錯誤", ephemeral=True)
                return
            
            try:
                views = int(self.view_count.value)
            except:
                await interaction.response.send_message(content="觀看數格式錯誤", ephemeral=True)
                return
            
            youtube_data['views_check'].append(
                {
                    "name": name,
                    "id": id,
                    "views": views
                }
            )
            func.write_json("youtube_data", youtube_data)

            embed = discord.Embed(
                title = "新增影片",
                description = f"**曲名：**{name}\n**ID：**[{id}](https://youtu.be/{id})\n**觀看數：**{views}",
                color = 0x00BB00
            )
            await interaction.response.send_message(embed=embed, view=None)
            
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.on_submit", e)

# 觀看數檢查功能: 刪除
class ViewsCheckRemoveView(MyView):
    def __init__(self, *, timeout = 180, user_id: int):
        super().__init__(timeout=timeout, user_id=user_id)
        self.page_index = 0
        self.total_page = int((len(youtube_data['views_check']) - 1) / 25) + 1
        self.options = []
        self.delete_index: int

        self.prev_page_btn = discord.ui.Button(label="◀上一頁", row=1, style=discord.ButtonStyle.blurple)
        self.prev_page_btn.callback = lambda i: self.flip_page(i, -1)
        self.next_page_btn = discord.ui.Button(label="下一頁▶", row=1, style=discord.ButtonStyle.blurple)
        self.next_page_btn.callback = lambda i: self.flip_page(i, 1)

        self.state = "menu"
        self.update_view()

    def update_view(self):
        self.clear_items()
        self.options.clear()

        for i in range(self.page_index * 25, self.page_index * 25 + 25):
            try:
                video = youtube_data['views_check'][i]
            except IndexError:
                break
            self.options.append(
                discord.SelectOption(label=video['name'], value=i, description=f"ID: {video['id']} 觀看數: {video['views']}")
            )

        if self.state == "menu":
            (select := discord.ui.Select(placeholder="刪除對象", options=self.options, row=0)).callback = self.delete_select
            self.add_item(select)
            self.add_item(self.prev_page_btn)
            self.add_item(self.next_page_btn)

        elif self.state == "confirm":
            (cancel_btn := discord.ui.Button(label="取消", row=0, style=discord.ButtonStyle.red)).callback = lambda i: self.confirm(i, False)
            self.add_item(cancel_btn)
            (confirm_btn := discord.ui.Button(label="確定", row=0, style=discord.ButtonStyle.green)).callback = lambda i: self.confirm(i, True)
            self.add_item(confirm_btn)

        self.prev_page_btn.disabled = (self.page_index <= 0)
        self.next_page_btn.disabled = (self.page_index + 1 >= self.total_page)

    async def delete_select(self, interaction: Interaction):
        try:
            self.delete_index = int(interaction.data['values'][0])
            video = youtube_data['views_check'][self.delete_index]

            self.state = "confirm"
            self.update_view()

            embed = discord.Embed(
                title = "確定要刪除此影片嗎",
                description = f"**曲名：**{video['name']}\n**ID：**[{video['id']}](https://youtu.be/{video['id']})\n**觀看數：**{video['views']}",
                color = 0xFF0000
            )
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.delete_select", e)

    async def flip_page(self, interaction: Interaction, page_num: int):
        try:
            self.page_index += page_num
            self.update_view()
            await interaction.response.edit_message(view=self)
        
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.flip_page", e)

    async def confirm(self, interaction: Interaction, confirm: bool):
        try:
            if confirm:
                del youtube_data['views_check'][self.delete_index]
                func.write_json("youtube_data", youtube_data)

                embed = interaction.message.embeds[0]
                embed.title = "刪除影片"
                self.clear_items()

            else:
                self.state = "menu"
                self.update_view()
                embed = None
                
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.confirm", e)


# 新影片紀錄
class youtube_log:
    @property
    def guild(self):
        return self.bot.get_guild(settings['id']['guild'])

    @property
    def video_upload_channel(self):
        return self.guild.get_channel(settings['id']['channel']['youtube']['video_upload'])
    
    @property
    def oshi_chat_channel(self):
        return self.guild.get_channel(settings['id']['channel']['chat']['oshi'])
    
    @property
    def stream_chat_channel(self):
        return self.guild.get_channel(settings['id']['channel']['chat']['stream'])

    def __init__(self, bot: MyBot):
        self.bot = bot
        self.file: discord.File
        self.embed: discord.Embed


    def stream_base(self, video_data: dict):
        self.embed = discord.Embed(
            title = video_data['snippet']['title'],
            url = f"https://youtu.be/{video_data['id']}",
            timestamp = t.datetime.now()
        )
        self.embed.set_author(
            name = video_data['snippet']['channelTitle'],
            url = f"https://www.youtube.com/channel/{video_data['snippet']['channelId']}"
        )
        self.file = discord.File(f"image/{video_data['id']}.jpg", filename="thumbnail.png")
        self.embed.set_image(url="attachment://thumbnail.png")

    def video_base(self, video_data: dict):
        self.embed = discord.Embed(
            title = video_data['snippet']['title'],
            url = f"https://youtu.be/{video_data['id']}",
            timestamp = t.datetime.now()
        )
        self.embed.set_author(
            name = video_data['snippet']['channelTitle'],
            url = f"https://www.youtube.com/channel/{video_data['snippet']['channelId']}"
        )
        self.embed.set_image(url=get_thumbnail_url(video_data))
        return self.embed
            
    async def upcoming(self, video_data: dict, start_time: str):
        self.stream_base(video_data)
        text = "待機室上傳"
        start_time = str(int(t.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()))
        
        self.embed.add_field(
            name = "直播開始時間",
            value = f"<t:{start_time}:F>（<t:{start_time}:R>）",
            inline = False
        )
        self.embed.color = 0xFF5809

        await self.video_upload_channel.send(content=text, embed=self.embed, file=self.file)

    async def video(self, video_data: dict):
        self.video_base(video_data)
        text = "影片上傳"
        self.embed.color = 0xFF0000

        await self.video_upload_channel.send(content=text, embed=self.embed)
        await self.oshi_chat_channel.send(content=f"新影片上傳！\nhttps://youtu.be/{video_data['id']}")

    async def time(self, video_data: dict, old_start_time: str):
        self.stream_base(video_data)
        text = "開台時間變更"
        old_start_time = str(int(t.datetime.strptime(old_start_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()))
        new_start_time = str(int(t.datetime.strptime(video_data['liveStreamingDetails']['scheduledStartTime'], "%Y-%m-%dT%H:%M:%SZ").timestamp()))

        self.embed.add_field(
            name = "原始時間",
            value = f"<t:{old_start_time}:F>（<t:{old_start_time}:R>）",
            inline = False
        )
        self.embed.add_field(
            name = "變更時間",
            value = f"<t:{new_start_time}:F>（<t:{new_start_time}:R>）",
            inline = False
        )
        self.embed.color = 0xFF00FF

        await self.video_upload_channel.send(content=text, embed=self.embed, file=self.file)

    async def title(self, video_data: dict, old_title: str):
        self.stream_base(video_data)
        text= "標題變更"

        self.embed.add_field(name="原始標題", value=f"```{old_title}```", inline=True)
        self.embed.add_field(name="變更標題", value=f"```{video_data['snippet']['title']}```", inline=True)
        self.embed.color = 0xFF00FF

        await self.video_upload_channel.send(content=text, embed=self.embed, file=self.file)

    async def thumbnail(self, video_data: dict):
        self.stream_base(video_data)
        message = "封面圖變更"
        self.embed.color = 0xFF00FF

        await self.video_upload_channel.send(content=message, embed=self.embed, file=self.file)

    async def stream_start(self, video_data: dict):
        self.stream_base(video_data)
        # text = "開始直播"
        text = f"<@&{settings['id']['role']['stream_notice']}> 開始直播"
        start_time = t.datetime.strptime(video_data['liveStreamingDetails']['actualStartTime'], "%Y-%m-%dT%H:%M:%SZ")

        self.embed.add_field(
            name = "實際開始時間",
            value = f"<t:{int(start_time.timestamp())}:F>（<t:{int(start_time.timestamp())}:R>）",
            inline = False
        )
        self.embed.color = 0xFF0000

        await self.video_upload_channel.send(content=text, embed=self.embed, file=self.file)
        await self.stream_chat_channel.edit(name=youtube_data['channel_chat_live_title']['live'])

    async def stream_end(self, video_data: dict):
        self.stream_base(video_data)
        message = "直播結束"
        end_time = t.datetime.strptime(video_data['liveStreamingDetails']['actualEndTime'], "%Y-%m-%dT%H:%M:%SZ")
        start_time = t.datetime.strptime(video_data['liveStreamingDetails']['actualStartTime'], "%Y-%m-%dT%H:%M:%SZ")
        time_diff = end_time - start_time

        self.embed.add_field(
            name = "結束時間",
            value = f"<t:{int(end_time.timestamp())}:F>（<t:{int(end_time.timestamp())}:R>）",
            inline = False
        )
        self.embed.add_field(name="直播時長", value=str(time_diff), inline=False)
        self.embed.color = 0x101010

        await self.video_upload_channel.send(content=message, embed=self.embed, file=self.file)

        # 如果還有在進行中的直播就要保留頻道名稱
        if not any(stream['live'] for stream in youtube_data['streams']):
            await self.stream_chat_channel.edit(name=youtube_data['channel_chat_live_title']['nolive'])


class youtube(MyCog):
    @property
    def oshi_chat_channel(self):
        return self.guild.get_channel(settings['id']['channel']['chat']['oshi'])

    def __init__(self, bot):
        super().__init__(bot)
        self.log = youtube_log(bot)
        self.livechat_id_list = []
        self.livechat_check = None

    async def cog_load(self):
        try:
            # 啟動youtube頻道監控任務
            self.minutes_check.start()
            self.seconds_check.start()

            # 載入youtube.py時, 如果有直播中的台, 重新載入聊天室監測
            if youtube_data['streams']:
                self.livechat_id_list = [s['id'] for s in youtube_data['streams']]
                self.livechat_check = self.bot.loop.create_task(self.livechat(self.livechat_id_list))

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.cog_load", e)

    async def cog_unload(self):
        try:
            # 結束youtube頻道監控任務
            self.minutes_check.cancel()
            self.seconds_check.cancel()

            # 卸載youtube.py時, 如果有直播中的台, 關閉正在執行的聊天室監測
            if self.livechat_check:
                self.livechat_check.cancel()
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.cog_unload", e)


    def get_playlist_data(self):
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status,id&maxResults=10&playlistId={PLAYLIST_ID}&key={YOUTUBE_API_KEY}"
        data = requests.get(url).json()

        if "error" in data:
            return None
        else:
            return data['items']
        
    def get_video_data(self, video_id: str) -> list:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,statistics,liveStreamingDetails,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
        data = requests.get(url).json()

        if "items" in data:
            return data['items']
        else:
            return []

    def get_channel_data(self):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,status,topicDetails,brandingSettings,contentDetails&id={CHANNEL_ID}&key={YOUTUBE_API_KEY}"
        data = requests.get(url).json()

        if "error" in data:
            return None
        else:
            return data['items']

    # 檢查新影片的類型
    async def new_video_check(self, video_id: str) -> bool:
        try:
            global youtube_data_dirty

            # 如果影片已經在清單內或是為freechat台
            if video_id in youtube_data['playlist_video_id'] or video_id in youtube_data['freechat_video_id']:
                return False

            # 用 YT api 獲取影片資料
            video_data = self.get_video_data(video_id)[0]

            # 影片類型為普通影片
            if video_data['snippet']['liveBroadcastContent'] == "none" and "liveStreamingDetails" not in video_data:
                await self.log.video(video_data)
                func.time_print(f"影片上傳 https://youtu.be/{video_id}")
            
            # 影片類型為直播
            else:
                stream_item = {
                    "id": video_id,
                    "start_check": False,
                    "live": False,
                    "start_time": video_data['liveStreamingDetails']['scheduledStartTime'],
                    "title": video_data['snippet']['title'],
                    "description": video_data['snippet']['description'],
                    "thumbnail": get_thumbnail_url(video_data),
                    "thumbnail_hash": await self.get_thumbnail_hash(video_data)
                }
                await self.download_thumbnail(video_data)
                await self.livechat_create(video_id, "append")

                # 直播待機室
                if video_data['snippet']['liveBroadcastContent'] == "upcoming" and "liveStreamingDetails" in video_data:
                    await self.log.upcoming(video_data, stream_item['start_time'])
                    func.time_print(f"待機室上傳 https://youtu.be/{video_id}")

                # 已經開始的直播
                elif video_data['snippet']['liveBroadcastContent'] == "live" and "liveStreamingDetails" in video_data:
                    stream_item['live'] = True
                    await self.log.stream_start(video_data)
                    func.time_print(f"突襲直播 https://youtu.be/{video_id}")

                youtube_data['streams'].append(stream_item)

            # 將影片ID加到清單內
            youtube_data['playlist_video_id'].append(video_id)
            if len(youtube_data['playlist_video_id']) > 20:
                del youtube_data['playlist_video_id'][0]
            youtube_data_dirty = True

            return True

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.new_video_check", e)


    async def download_thumbnail(self, video_data: dict):
        try:
            thumbnail_url = get_thumbnail_url(video_data)
            request = requests.get(thumbnail_url, stream=True)
            if request.status_code == 200:
                with open(f"image/{video_data['id']}.jpg", 'wb') as file:
                    for chunk in request.iter_content(1024):
                        file.write(chunk)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.get_thumbnail", e)

    async def delete_thumbnail(self, video_id: str):
        try:
            os.remove(f"/home/container/image/{video_id}.jpg")
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.delete_thumbnail", e)

    async def get_thumbnail_hash(self, video_data: dict):
        try:
            thumbnail_url = get_thumbnail_url(video_data)
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail_url) as respone:
                    if respone.status == 200:
                        file_byte = await respone.read()
                        return hashlib.sha256(file_byte).hexdigest()
            return None
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.get_thumbnail_hash", e)

    async def get_temp_thumbnail(self, video_data: dict):
        try:
            thumbnail_url = get_thumbnail_url(video_data)
            request = requests.get(thumbnail_url, stream=True)
            if request.status_code == 200:
                with open("image/temp.jpg", 'wb+') as file:
                    for chunk in request.iter_content(1024):
                        file.write(chunk)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.get_temp_thumbnail", e)

    async def compare_thumbnail(self, video_data: dict, old_hash: str):
        try:
            # temp_file = "image/temp.jpg"
            # old_file = f"image/{video_id}.jpg"

            # await self.get_temp_thumbnail(video_data)

            # if filecmp.cmp(temp_file, old_file):
            #     return True
            # else:
            #     shutil.copyfile(temp_file, old_file)
            #     return False

            new_hash = await self.get_thumbnail_hash(video_data)

            if old_hash == new_hash:
                return None
            
            await self.download_thumbnail(video_data)
            return new_hash
        
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.compare_thumbnail", e)


    async def views_check(self):
        global youtube_data_dirty
        try:
            for list_num in range(int((len(youtube_data['views_check']) - 1) / 50) + 1):

                id_string = ",".join(video['id'] for video in youtube_data['views_check'][list_num * 50 : list_num * 50 + 50])

                video_data_list = self.get_video_data(id_string)
                
                for i, old_video_data in enumerate(youtube_data['views_check'][list_num * 50 : list_num * 50 + 50]):

                    if not (new_video_data := next((v for v in video_data_list if v['id'] == old_video_data['id']), None)):
                        continue

                    old_view = old_video_data['views']
                    new_view = int(int(new_video_data['statistics']['viewCount']) / 100000) * 100000

                    if new_view > old_view:
                        youtube_data['views_check'][i + list_num * 50]['views'] = new_view
                        youtube_data_dirty = True

                        embed = self.log.video_base(new_video_data)
                        embed.description = f"播放次數達到 {new_view:,}"
                        embed.color = 0xFF0000
                        await self.guild.get_channel(settings['id']['channel']['youtube']['video_views']).send(embed=embed)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.views_check", e)

    async def channel_check(self):
        global youtube_data_dirty
        try:
            channel_data = self.get_channel_data()[0]

            new_videoCount = int(channel_data['statistics']['videoCount'])
            old_videoCount = youtube_data['statistics']['videoCount']

            new_subscriberCount = int(channel_data['statistics']['subscriberCount'])
            old_subscriberCount = youtube_data['statistics']['subscriberCount']

            new_viewCount = int(channel_data['statistics']['viewCount'])
            old_viewCount = youtube_data['statistics']['viewCount']

            embed = discord.Embed(timestamp=t.datetime.now(), color=0xFF0000)
            embed.set_author(
                name = channel_data['snippet']['title'],
                url = f"https://www.youtube.com/channel/{channel_data['id']}",
                icon_url = channel_data['snippet']['thumbnails']['default']['url']
            )

            # 比較影片數
            if new_videoCount > old_videoCount:
                youtube_data['statistics']['videoCount'] = new_videoCount
                youtube_data_dirty = True

                new_video_milestone = int(new_videoCount / 100) * 100
                old_video_milestone = youtube_data['statistics']['milestone']['videoCount']

                if new_video_milestone > old_video_milestone:
                    youtube_data['statistics']['milestone']['videoCount'] = new_video_milestone

                    video_embed = embed.copy()
                    video_embed.title = "影片數里程"
                    video_embed.description = f"YouTube頻道影片數達到 {new_video_milestone:,}"
                    await self.oshi_chat_channel.send(embed=video_embed)

            # 比較訂閱數
            if new_subscriberCount > old_subscriberCount:
                youtube_data['statistics']['subscriberCount'] = new_subscriberCount
                youtube_data_dirty = True

                subscribe_embed = embed.copy()
                subscribe_embed.title = "訂閱數里程"
                subscribe_embed.description = f"YouTube頻道訂閱數達到 {new_subscriberCount:,}"
                await self.oshi_chat_channel.send(embed=subscribe_embed)
    
            # 比較觀看數
            if new_viewCount > old_viewCount:
                youtube_data['statistics']['viewCount'] = new_viewCount
                youtube_data_dirty = True

                new_view_milestone = int(new_viewCount / 10000000) * 10000000
                old_view_milestone = youtube_data['statistics']['milestone']['viewCount']

                if new_view_milestone > old_view_milestone:
                    youtube_data['statistics']['milestone']['viewCount'] = new_view_milestone

                    view_embed = embed.copy()
                    view_embed.title = "總觀看數里程"
                    view_embed.description = f"YouTube頻道總觀看數達到 {new_view_milestone:,}"
                    await self.oshi_chat_channel.send(embed=view_embed)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.check_channel", e)


    async def livechat(self, video_id_list: list[str]):
        live_chat_list = [pytchat.create(vid) for vid in video_id_list]
        
        while True:
            for count, video_id in enumerate(video_id_list):
                try:
                    if live_chat_list[count].is_alive():
                        chatdata = live_chat_list[count].get().sync_items()
                        if chatdata:
                            for chat in chatdata:

                                if chat.author.channelId == "UC97104KkGIEPvOYABW-3I0Q":
                                    func.time_print(f"ylc留言 https://youtu.be/{video_id}")
                                elif chat.author.channelId == "UCkr7uCq7BZO2perY5PqX3lw":
                                    func.time_print(f"olea留言 https://youtu.be/{video_id}")

                                elif chat.author.isChatModerator or chat.author.channelId in hololive_channel_id:

                                    func.time_print(f"成員留言 https://youtu.be/{video_id}")
                                    # title = get_video_data(video_id)[0]['snippet']['title']

                                    channel_chat_live = self.guild.get_channel(settings['id']['channel']['chat']['stream'])

                                    chat_message = chat.message
                                    for emoji_change in youtube_data['emoji']:

                                        chat_message = re.sub(emoji_change['yt'], emoji_change['dc'], chat_message)

                                    embed = discord.Embed(description=chat_message, color=0xFF0080, timestamp=t.datetime.now())
                                    embed.set_author(name=chat.author.name, url=chat.author.channelUrl, icon_url=chat.author.imageUrl)
                                    embed.set_footer(text=video_id)

                                    await channel_chat_live.send(embed=embed)

                    else:
                        func.time_print("live_chat不存在")
                        await asyncio.sleep(1)
                        live_chat_list[count] = pytchat.create(video_id)

                except Exception as e:
                    await self.report_error(__file__, f"{self.__class__.__name__}.livechat", e)
                    await asyncio.sleep(5)
                    live_chat_list[count] = pytchat.create(video_id)

                await asyncio.sleep(0.5)

    async def livechat_create(self, video_id: str, mode: Literal["append", "remove"]):
        try:
            if mode == "append":
                self.livechat_id_list.append(video_id)
            elif mode == "remove":
                self.livechat_id_list.remove(video_id)

            if self.livechat_check:
                self.livechat_check.cancel()

            if self.livechat_id_list:
                self.livechat_check = self.bot.loop.create_task(self.livechat(self.livechat_id_list))
                func.time_print(f"聊天室監測創建 {self.livechat_id_list}")
            else:
                self.livechat_check = None
                func.time_print(f"聊天室監測結束 {video_id}")

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.livechat_create", e)


    @tasks.loop(minutes=1)
    async def minutes_check(self):
        global youtube_data_dirty
        try:
            # 獲取頻道的全體播放清單
            playlist_data = self.get_playlist_data()

            for video in reversed(playlist_data):
                await self.new_video_check(video['contentDetails']['videoId'])

            # 如果有直播台存在
            if youtube_data['streams']:

                # 把現有的待機台ID集中在一個字串內
                stream_id_string = ",".join(stream['id'] for stream in youtube_data['streams'])

                # 取得所有待機台的資料並檢查
                video_data_list = self.get_video_data(stream_id_string)
                for count, stream in enumerate(youtube_data['streams']):
                    video_id = stream['id']
                    # 獲取對應ID的api資料
                    video_data = next((vid for vid in video_data_list if vid['id'] == video_id), {})

                    # 如果無法獲取影片資料, 判定為影片刪除
                    if not video_data:
                        youtube_data['playlist_video_id'] = [
                            vid for vid in youtube_data['playlist_video_id'] if vid != video_id
                        ]
                        del youtube_data['streams'][count]
                        youtube_data_dirty = True

                        func.time_print(f"影片刪除/私人 https://youtu.be/{video_id}")

                        await self.delete_thumbnail(video_id)
                        await self.livechat_create(video_id, "remove")
                        continue

                    # 偵測開始直播時間變更
                    if video_data['liveStreamingDetails']['scheduledStartTime'] != stream['start_time']:
                        old_start_time = youtube_data['streams'][count]['start_time']
                        youtube_data['streams'][count]['start_time'] = video_data['liveStreamingDetails']['scheduledStartTime']
                        youtube_data_dirty = True

                        await self.log.time(video_data, old_start_time)
                        func.time_print(f"開始時間變更 https://youtu.be/{video_id}")

                    # 偵測標題變更
                    if video_data['snippet']['title'] != stream['title']:
                        old_title = youtube_data['streams'][count]['title']
                        youtube_data['streams'][count]['title'] = video_data['snippet']['title']
                        youtube_data_dirty = True

                        await self.log.title(video_data, old_title)
                        func.time_print(f"標題變更 https://youtu.be/{video_id}")

                    # 偵測封面圖變更
                    if (new_hash := await self.compare_thumbnail(video_data, stream['thumbnail_hash'])):
                        youtube_data['streams'][count]['thumbnail_hash'] = new_hash
                        youtube_data_dirty = True

                        await self.log.thumbnail(video_data)
                        func.time_print(f"封面圖變更 https://youtu.be/{video_id}")

                    # 如果紀錄狀態為直播中
                    if stream['live']:
                        # 偵測直播是否結束
                        if video_data['snippet']['liveBroadcastContent'] == "none":
                            del youtube_data['streams'][count]
                            youtube_data_dirty = True

                            await self.log.stream_end(video_data)
                            func.time_print(f"直播結束 https://youtu.be/{video_id}")

                            await self.delete_thumbnail(video_id)
                            await self.livechat_create(video_id, "remove")

                    # 如果紀錄狀態為直播前
                    else:
                        start_UTCtime = t.datetime.strptime(stream['start_time'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=t.timezone.utc)
                        now_UTCtime = t.datetime.now(t.timezone.utc)
                        time_difference = start_UTCtime - now_UTCtime

                        # 如果已經開始頻繁檢查開台
                        if stream['start_check']:
                            # 如果表定開台時間1小時後還沒開台, 或是開始檢查後開台時間延後到範圍外, 停止檢查
                            if time_difference < t.timedelta(hours=-1) or time_difference > t.timedelta(minutes=30):
                                youtube_data['streams'][count]['start_check'] = False
                                youtube_data_dirty = True

                                func.time_print(f"停止頻繁檢查 https://youtu.be/{video_id}")


                        # 還沒開始頻繁檢查開台
                        else:
                            # 表定開台時間30分鐘前切換至頻繁檢查開台
                            if time_difference < t.timedelta(minutes=30) and not time_difference < t.timedelta(hours=-1):
                                youtube_data['streams'][count]['start_check'] = True
                                youtube_data_dirty = True

                                func.time_print(f"開始頻繁檢查開台 https://youtu.be/{video_id}")

                            # 如果在表定開台時間30分鐘前就開始直播, 紀錄狀態
                            elif video_data['snippet']['liveBroadcastContent'] == "live":
                                youtube_data['streams'][count]['start_check'] = False
                                youtube_data['streams'][count]['live'] = True
                                youtube_data_dirty = True

                                await self.log.stream_start(video_data)
                                func.time_print(f'直播開始 https://youtu.be/{video_id}')

            # 檢查頻道的狀態資訊
            await self.channel_check()

            # 檢查有紀錄在清單內的影片的觀看次數
            if youtube_data['views_check']:
                await self.views_check()

            # 如果資料有被變更，將變更後的資料寫入json
            if youtube_data_dirty:
                func.write_json("youtube_data", youtube_data)
                youtube_data_dirty = False

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.minutes_check", e)


    @tasks.loop(seconds=5)
    async def seconds_check(self):
        try:
            # 如果有直播台存在且為頻繁檢查狀態
            if youtube_data['streams']:
                for count, stream in enumerate(youtube_data['streams']):             
                    if stream['start_check']:

                        video_id = stream['id']
                        video_data = self.get_video_data(video_id)[0]

                        if video_data['snippet']['liveBroadcastContent'] == "live":

                            await self.log.stream_start(video_data)
                            func.time_print(f'直播開始 https://youtu.be/{video_id}')

                            youtube_data['streams'][count]['start_check'] = False
                            youtube_data['streams'][count]['live'] = True
                            func.write_json("youtube_data", youtube_data)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.seconds_check", e)
    

    youtubeCommandsGroup = YoutubeCommandsGroup()

    @youtubeCommandsGroup.command(name="add-video", description="【Admin Only】手動加入待機室/直播/影片", extras={"public": False})
    async def add_video(self, interaction: discord.Interaction, url: str):
        try:
            await interaction.response.defer(ephemeral=True)
            
            video_id = re.findall(r'[a-zA-Z0-9-_]{11}', url)[0]

            if await self.new_video_check(video_id):
                msg = "新增成功"
            else:
                msg = "本影片已經在清單內"
            await interaction.response.send_message(msg, ephemeral=True)

        except IndexError:
            await interaction.response.send_message("URL錯誤", ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.add_video", e)

    @youtubeCommandsGroup.command(name="show-streams", description="【Admin Only】顯示目前所有的直播台", extras={"public": False})
    async def show_streams(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="直播台")
            for stream in youtube_data['streams']:
                id = f"[{stream['id']}](https://youtu.be/{stream['id']})"
                status = "直播中" if stream['live'] else "等待開台"
                time = str(int(t.datetime.strptime(stream['start_time'], "%Y-%m-%dT%H:%M:%SZ").timestamp()))

                embed.add_field(
                    name = stream['title'],
                    value = f"**ID：**{id}\n**狀態：**{status}\n**開始時間：**<t:{time}:F>（<t:{time}:R>）",
                    inline = False
                )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.show_streams", e)

    @youtubeCommandsGroup.command(name="video-views", description="【Admin Only】影片觀看數紀錄設定", extras={"public": False})
    async def video_views(self, interaction: discord.Interaction):
        try:
            view = ViewsCheckPanelView(user_id=interaction.user.id)
            await interaction.response.send_message(embed=view.embed, view=view)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.video_views", e)

    @youtubeCommandsGroup.command(name="get-thumbnail", description="抓取Youtube影片的封面圖")
    async def get_thumbnail(self, interaction: discord.Interaction, url: str):
        try:
            if func.is_youtube_url(url):
                try:
                    video_id = re.findall(r'[a-zA-Z0-9-_]{11}', url)[0]
                    image_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'

                    embed = discord.Embed()
                    embed.set_image(url=image_url)

                    await interaction.response.send_message(embed=embed)
                except:
                    await interaction.response.send_message(content="抓取失敗", ephemeral=True)
                    return
            
            else:
                await interaction.response.send_message(content="URL格式錯誤", ephemeral=True)
                return

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.get_thumbnail", e)


async def setup(bot: MyBot):
    await bot.add_cog(youtube(bot))