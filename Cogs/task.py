import discord
from discord.ext import commands, tasks
from Define.Classes import MyBot, MyCog
import Define.Functions as func
import datetime as t
import random


settings = func.read_json("settings")

first_person = settings['function']['first_person']

guild = settings['guild']


class task(MyCog):
    @property
    def lobby_channel(self):
        return self.guild.get_channel(settings['id']['channel']['chat']['lobby'])
    
    async def cog_load(self):
        self.random_song.start()
        if guild['kanade']:
            self.monday_guild.start()
            self.monday.start()

    async def cog_unload(self):
        self.random_song.cancel()
        if guild['kanade']:
            self.monday_guild.cancel()
            self.monday.cancel()


    # 每日隨機推薦歌曲
    @tasks.loop(time=t.time(hour=8, minute=0, tzinfo=t.timezone(t.timedelta(hours=8))))
    async def random_song(self):
        try:
            song_list = func.read_json('youtube_data')['views_check']
            song = random.choice(song_list)
            # 跳過LIVE
            while song['id'] in {"mt8AyISL9Ig", "zZ2Ce3eDamU"}:
                song = random.choice(song_list)

            await self.lobby_channel.send(content=f"## 每日隨機{first_person}歌曲推薦：[{song['name']}](https://youtu.be/{song['id']})")
            
            
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.random_song", e)


    # 星期一將伺服器改名
    @tasks.loop(time=t.time(hour=0, minute=0, tzinfo=t.timezone(t.timedelta(hours=8))))
    async def monday_guild(self):
        try:
            now_time = t.datetime.now(tz=t.timezone(t.timedelta(hours=8)))

            if now_time.isoweekday() == 1:
                await self.guild.edit(name="奏的月曜工坊")

            elif now_time.isoweekday() == 2:
                await self.guild.edit(name="奏的樂音工坊")

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.monday_guild", e)


    # 星期一嘲諷
    @tasks.loop(time=t.time(hour=23, minute=30, tzinfo=t.timezone(t.timedelta(hours=8))))
    async def monday(self):
        try:
            now_time = t.datetime.now(tz=t.timezone(t.timedelta(hours=8)))

            if now_time.isoweekday() == 7:
                
                sticker = await self.guild.fetch_sticker(1363951780332961933)
                await self.lobby_channel.send(stickers=[sticker])
                await self.lobby_channel.send(content="<:6_knd_monday2:1317852457619034173>")
                # await channel_chat.send(content="明日は月曜日～♫ 月曜日～♫\nるんるん♪ るんるん♪ 月曜日♫")

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.monday", e)


async def setup(bot: MyBot):
    await bot.add_cog(task(bot))