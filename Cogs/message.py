import discord
from discord.ext import commands
from Define.Classes import MyBot, MyCog
import Define.Functions as func
import random
import re
import datetime as t
import hashlib


settings = func.read_json("settings")

message_react: dict = settings['functions']['message_react']
sticker_react: dict = settings['functions']['sticker_react']

dm_reply = settings['functions']['dm_reply']

first_person = settings['functions']['first_person']


class MessageLog:
    def __init__(self, message: discord.Message, attachments_hash: list):
        self.content = message.content
        self.author_id = message.author.id
        self.channel_id = message.channel.id
        self.message_id = message.id
        self.attachments_hash = attachments_hash
        self.timestamp = message.created_at.timestamp()
                
    @classmethod
    async def create(cls, message: discord.Message):
        attachments_hash = []
        if message.attachments:
            for attachment in message.attachments:
                attachments_hash.append(hashlib.sha256(await attachment.read()).hexdigest())
        return cls(message, attachments_hash)
    

class SpamCheck:
    @property
    def penalty_channel(self):
        return self.guild.get_channel(settings['id']['channel']['penalty'])
    
    @property
    def guild(self):
        return self.bot.guild

    def __init__(self, bot: MyBot):
        self.message_log_list: list[MessageLog] = []
        self.bot = bot

    async def check(self, message: discord.Message):
        new_log = await MessageLog.create(message)

        message_repeat_count = 0
        author_repeat_count = 0
        message_spam = False
        author_spam = False

        # 檢查過去10秒是否有完全相同的訊息
        for past_log in self.message_log_list:
            if new_log.timestamp - past_log.timestamp > 10:
                break

            if past_log.author_id == new_log.author_id:
                author_repeat_count += 1

                if (past_log.content == new_log.content) and (past_log.attachments_hash == new_log.attachments_hash):
                    message_repeat_count += 1

            if message_repeat_count >= 3:
                message_spam = True
                break
            elif author_repeat_count >= 10:
                author_spam = True
                break

        # 將新訊息加入紀錄清單
        self.message_log_list.insert(0, new_log)
        if len(self.message_log_list) > 500:
            self.message_log_list.pop()

        # 判定為洗頻訊息
        if message_spam or author_spam:
            if message_spam:
                violations = "- 重複訊息洗頻"
            elif author_spam:
                violations = "- 大量訊息洗頻"
            
            # 刪除基本身份組，發送懲處紀錄
            if author := self.guild.get_member(new_log.author_id):
                await author.remove_roles(self.guild.get_role(settings['id']['role']['basic']))
                embed = discord.Embed(title="違規紀錄", description=author.mention, color=0xFF0000)
                embed.add_field(name="使用者名稱", value=f"`{author.name}`")
                embed.add_field(name="ID", value=f"`{author.id}`")
                embed.add_field(name="違規事項", value=violations, inline=False)
                embed.add_field(name="處置", value="- 刪除訊息\n- 移除基本身份組")
                embed.set_thumbnail(url=author.display_avatar.url)
                await self.penalty_channel.send(embed=embed)

            # 刪除過去10秒所有來自此使用者的訊息
            to_remove: list[MessageLog] = []
            for log in self.message_log_list:
                if new_log.timestamp - log.timestamp > 10:
                    break
                if log.author_id == new_log.author_id:
                    to_remove.append(log)
                    try:
                        target_message = await self.guild.get_channel(log.channel_id).fetch_message(log.message_id)
                        await target_message.delete()
                    except discord.NotFound:
                        pass
                    
            # 從訊息紀錄清單中移除 bot 刪除的訊息
            for log in to_remove:
                self.message_log_list.remove(log)
    

class message(MyCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.spamCheck = SpamCheck(self.bot)

    async def dm(self, message: discord.Message):
        try:
            embed = discord.Embed(title="有人無聊去私訊bot", description=message.author.mention, timestamp=t.datetime.now(), color=0xFF0080)
            files = []
            
            if message.content:
                member = message.author
                embed.set_author(name=member, icon_url=member.display_avatar)
                embed.add_field(name="訊息", value=message.content, inline=False)

            if message.attachments:
                embed.add_field(name="附檔", value="", inline=False)
                for attachment in message.attachments:
                    files.append(await attachment.to_file())

            if message.stickers:
                embed.add_field(name="貼圖", value="", inline=False)

            await self.panel_channel.send(embed=embed, files=files)

            if dm_reply['enable']:
                await message.channel.send(dm_reply['message'])

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.dm", e)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            # 忽略任何bot發的訊息
            if message.author.bot:
                return
            
            # 檢查洗頻
            await self.spamCheck.check(message)

            # 對特定訊息做出反應
            for target, react in message_react.items():
                # @bot的訊息
                target = target.format(mention_self=f"<@{self.bot.user.id}>")

                if re.search(target, message.content):
                    for r in react['reaction']:
                        await message.add_reaction(r)
                    for r in react['reply']:
                        await message.reply(r)
                    for s in react['send']:
                        await message.channel.send(s)

            # 對特定貼圖做出反應
            for target, react in sticker_react.items():
                if any(int(target) == sticker.id for sticker in message.stickers):
                    for r in react['reaction']:
                        await message.add_reaction(r)
                    for r in react['reply']:
                        await message.reply(r)
                    for s in react['send']:
                        await message.channel.send(s)

            # 對話功能
            if message.channel.id == settings['id']['channel']['bot']['chat'] or message.channel.id == settings['id']['channel']['bot']['panel']:
                answer = ""
                embed = None

                # 「是、否」問答
                if re.search(r"是.*(嗎|吗|吧|不是)", message.content):
                    answer = random.choice(["不是", "是"])

                # 「可以、不可以」問答
                elif re.search(r"(可以.*(嗎|吗|吧))|可不可以", message.content):
                    answer = random.choice(["可以", "不可以"])

                # 「會、不會」問答
                elif re.search(r"((會|会).*(嗎|吗|吧))|(會|会)不(會|会)", message.content):
                    answer = random.choice(["會", "不會"])
                
                # 求籤
                elif re.search(r"求.*籤", message.content):
                    omikuji = random.choice(settings['image']['omikuji'])
                    embed = discord.Embed(title="【求籤結果】")
                    embed.set_image(url=f"{omikuji['url']}.png")

                # 機率
                elif re.search(r"率", message.content):
                    percentage = random.randint(0, 100)
                    sentence = re.findall(r".*率", message.content)[0]
                    answer = f"{sentence}是**{percentage}%**"

                # 選擇
                elif re.search(r"(選|选).*(:|：)", message.content):
                    choices = re.split(r"(:|：)", message.content, maxsplit=1)[2]
                    choices = re.findall(r"[\S]+", choices)
                    answer = f"{first_person}幫你選的是**{random.choice(choices)}**"

                # 傳送結果
                if answer or embed:
                    await message.reply(content=answer, embed=embed)

            # 私訊
            elif isinstance(message.channel, discord.DMChannel):
                await self.dm(message)
        
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_message", e)


async def setup(bot: MyBot):
    await bot.add_cog(message(bot))