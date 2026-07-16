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
    
class MessageLogList:
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.log_list: list[MessageLog] = []
        self.penalty = Penalty(bot)

    async def add_log(self, message: discord.Message):
        """將新訊息加入到紀錄清單"""
        # 計算附件檔案的 hash
        attachments_hash = [
            hashlib.sha256(await attachment.read()).hexdigest()
            for attachment in message.attachments
        ]
        # 訊息紀錄物件
        new_log = MessageLog(message, attachments_hash)
        # 加入清單
        self.log_list.insert(0, new_log)
        if len(self.log_list) > 500:
            self.log_list.pop()

        return new_log
    
    def delete_log(self, log: MessageLog):
        """從紀錄清單中刪除指定的紀錄"""
        self.log_list.remove(log)

    async def spam_check(self):
        """檢查最新的訊息是否為洗頻訊息"""

        if len(self.log_list) < 1:
            return
        
        message_spam = False
        author_spam = False
        trapped = False
        
        new_log = self.log_list[0]

        if new_log.channel_id == settings['id']['channel']['trap']:
            trapped = True
        else:
            message_repeat_count = 0
            author_repeat_count = 0

            # 檢查過去10秒是否有完全相同的訊息
            for past_log in self.log_list[1:]:
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

        #刪除判定為洗頻的訊息
        if message_spam or author_spam or trapped:
            if trapped:
                violations = ["觸發陷阱"]
                delete_sec = 5
            elif message_spam:
                violations = ["重複訊息洗頻"]
                delete_sec = 10
            elif author_spam:
                violations = ["大量訊息洗頻"]
                delete_sec = 10

            # 移除基本身份組
            await self.penalty.remove_basic_role(new_log.author_id, violations, ["刪除訊息", "移除基本身份組"])
            
            to_remove: list[MessageLog] = []

            for log in self.log_list:
                if new_log.timestamp - log.timestamp > delete_sec:
                    break
                if log.author_id == new_log.author_id:
                    to_remove.append(log)

            for target in to_remove:
                # 從紀錄清單移除
                self.delete_log(target)
                # 刪除訊息
                try:
                    target_message = await self.bot.guild.get_channel(target.channel_id).fetch_message(target.message_id)
                    await target_message.delete()
                except discord.NotFound:
                    pass


class Penalty:
    def __init__(self, bot: MyBot):
        self.bot = bot

    @property
    def penalty_channel(self):
        return self.bot.guild.get_channel(settings['id']['channel']['penalty'])
    
    @property
    def trap_channel(self):
        return self.bot.get_channel(settings['id']['channel']['trap'])
    
    async def remove_basic_role(self, member_id: int, violations: list[str], penalties: list[str]):
        """移除基礎身份組"""
        if member := self.bot.guild.get_member(member_id):
            basic_role = self.bot.guild.get_role(settings['id']['role']['basic'])
            # 成員是有基本身份組的狀態才做懲處並發送紀錄
            if basic_role in member.roles:
                await member.remove_roles(basic_role)
                if "觸發陷阱" in violations:
                    await self.trap_channel.send(f"<@{member_id}> 觸發了陷阱💥")
                else:
                    await self._send_log(member, violations, penalties)
    
    async def _send_log(self, member: discord.Member, violations: list[str], penalties: list[str]):
        """發送懲處紀錄"""
        violations_str = "\n".join(f"- {v}" for v in violations)
        penalty_str = "\n".join(f"- {p}" for p in penalties)
        embed = discord.Embed(title="懲處紀錄", description=member.mention, color=0xFF0000)
        embed.add_field(name="使用者名稱", value=f"`{member.name}`")
        embed.add_field(name="ID", value=f"`{member.id}`")
        embed.add_field(name="違規事項", value=violations_str, inline=False)
        embed.add_field(name="處置", value=penalty_str)
        embed.set_thumbnail(url=member.display_avatar.url)
        await self.penalty_channel.send(embed=embed)


class message(MyCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.message_log_list = MessageLogList(bot)

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
            
            # 將訊息加入紀錄清單，檢查是否為洗頻訊息
            await self.message_log_list.add_log(message)
            await self.message_log_list.spam_check()

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