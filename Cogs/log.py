import discord
from discord.ext import commands
from Define.Classes import MyBot, MyCog
import Define.Functions as func
import datetime as t


settings = func.read_json("settings")


class log(MyCog):
    @property
    def message_log_channel(self):
        return self.guild.get_channel(settings['id']['channel']['log']['message'])
    
    @property
    def member_log_channel(self):
        return self.guild.get_channel(settings['id']['channel']['log']['member'])
    
    @property
    def guild_log_channel(self):
        return self.guild.get_channel(settings['id']['channel']['log']['guild'])
    

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        try:
            if payload.channel_id == None:
                return
            
            try:
                channel = self.guild.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
            except:
                return
            
            member = message.author

            if member.bot:
                return

            if payload.cached_message:
                before = payload.cached_message.content
            else:
                before = '-'
            after = payload.data['content']

            if before == after:
                return
            
            # 訊息長度超過1024
            if len(before) > 1024:
                before = before[:1022] + "……"
            if len(after) > 1024:
                after = after[:1022] + "……"

            embed = discord.Embed(title="訊息編輯", description=member.mention, timestamp=t.datetime.now(), color=0xFF8000)
            embed.set_author(name=member, icon_url=member.display_avatar)
            embed.add_field(name="位置", value=message.jump_url, inline=False)
            embed.add_field(name="原始訊息", value=before, inline=False)
            embed.add_field(name="更新訊息", value=after, inline=False)

            await self.message_log_channel.send(embed=embed)

        except Exception as e:
            message_url = f"https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}"
            await func.report_error(f"log.on_raw_message_edit\n{message_url}", e, self.panel_channel)
            await self.report_error(__file__, f"{self.__class__.__name__}.on_raw_message_edit", e)


    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        try:
            url = f"https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}"
            message = payload.cached_message

            embed = discord.Embed(title="訊息刪除", timestamp=t.datetime.now(), color=0xff0000)
            embed.add_field(name="位置", value=url, inline=False)
            files = []

            if message:
                if message.content:
                    content = message.content
                    if len(content) > 1024:
                        content = content[:1022] + "……"
                    embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
                    embed.add_field(name="訊息", value=content, inline=False)

                if message.attachments:
                    embed.add_field(name="附檔", value="", inline=False)
                    for attachment in message.attachments:
                        try:
                            files.append(await attachment.to_file())
                        except:
                            continue

                if message.stickers:
                    embed.add_field(name="貼圖", value="", inline=False)
                
                embed.description = message.author.mention
                
            else:
                embed.add_field(name="訊息", value="-", inline=False)

            await self.message_log_channel.send(embed=embed, files=files)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_raw_message_delete", e)


    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        try:
            inviter = invite.inviter
            channel = invite.channel

            if invite.max_age == 0:
                age = "∞"
            else:
                age = t.timedelta(seconds=invite.max_age)

            if invite.max_uses == 0:
                uses = "∞"
            else:
                uses = invite.uses

            embed = discord.Embed(title="邀請連結創建",description=inviter.mention, timestamp=t.datetime.now(), color=0xFFDC35)
            embed.set_author(name=inviter, icon_url=inviter.display_avatar)
            embed.add_field(name="頻道", value=channel.mention, inline=True)
            embed.add_field(name="ID", value=invite.id, inline=True)
            embed.add_field(name="有效期限", value=age, inline=True)
            embed.add_field(name="最大使用次數", value=uses, inline=True)

            func.time_print(f"邀請連結創建 位置:{channel} 成員:{inviter}")
            await self.guild_log_channel.send(embed=embed)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_invite_create", e)


    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji]):
        try:
            for aft in after:
                if aft not in before:

                    embed = discord.Embed(title="表符新增", description=f"# {aft}", timestamp=t.datetime.now(), color=0x00DB00)
                    embed.add_field(name="名稱", value=aft.name, inline=False)
                    embed.add_field(name="ID", value=aft.id, inline=False)
                    
                    func.time_print("表符新增")
                    await self.guild_log_channel.send(embed=embed)
                    return

            for bef in before:
                if bef not in after:

                    embed = discord.Embed(title="表符刪除", timestamp=t.datetime.now(), color=0x00DB00)
                    embed.add_field(name="名稱", value=bef.name, inline=False)
                    embed.add_field(name="ID", value=bef.id, inline=False)

                    if bef.animated:
                        embed.add_field(name="GIF", value="True", inline=False)
                    else:
                        embed.add_field(name="GIF", value="False", inline=False)

                    func.time_print("表符刪除")
                    await self.guild_log_channel.send(embed=embed)
                    return
                
            for bef, aft in zip(before, after):
                if bef.name != aft.name:

                    embed = discord.Embed(title="表符編輯", description=f"# {aft}", timestamp=t.datetime.now(), color=0x00DB00)
                    embed.add_field(name="原始名稱", value=bef.name, inline=False)
                    embed.add_field(name="更新名稱", value=aft.name, inline=False)

                    func.time_print("表符編輯")
                    await self.guild_log_channel.send(embed=embed)
                    return

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_guild_emojis_update", e)


    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild: discord.Guild, before: list[discord.GuildSticker], after: list[discord.GuildSticker]):
        try:
            for aft in after:
                if aft not in before:

                    emoji = self.guild.get_emoji(int(aft.emoji))

                    embed = discord.Embed(title="貼圖新增", timestamp=t.datetime.now(), color=0x00DB00)
                    embed.add_field(name="名稱", value=aft.name, inline=True)
                    embed.add_field(name="相關表符", value=emoji, inline=True)
                    embed.add_field(name="簡介", value=aft.description, inline=False)

                    func.time_print("貼圖新增")
                    await self.guild_log_channel.send(embed=embed, stickers=[aft])
                    return
            
            for bef in before:
                if bef not in after:

                    emoji = self.guild.get_emoji(int(bef.emoji))

                    embed = discord.Embed(title="貼圖刪除", timestamp=t.datetime.now(), color=0x00DB00)
                    embed.add_field(name="名稱", value=bef.name, inline=True)
                    embed.add_field(name="相關表符", value=emoji, inline=True)
                    embed.add_field(name="簡介", value=bef.description, inline=False)

                    func.time_print("貼圖刪除")
                    await self.guild_log_channel.send(embed=embed)
                    return
                
            embed = discord.Embed(title="貼圖編輯", timestamp=t.datetime.now(), color=0x00DB00)

            for bef, aft in zip(before, after):
                if (bef.name != aft.name) or (bef.emoji != aft.emoji) or (bef.description != aft.description):

                    if bef.name != aft.name:
                        embed.add_field(name="原始名稱", value=bef.name, inline=False)
                        embed.add_field(name="更新名稱", value=aft.name, inline=False)

                    if bef.emoji != aft.emoji:
                        bef_emoji = self.guild.get_emoji(int(bef.emoji))
                        aft_emoji = self.guild.get_emoji(int(aft.emoji))
                        embed.add_field(name="原始相關表符", value=bef_emoji, inline=False)
                        embed.add_field(name="更新相關表符", value=aft_emoji, inline=False)

                    if bef.description != aft.description:
                        embed.add_field(name="原始簡介", value=bef.description, inline=False)
                        embed.add_field(name="更新簡介", value=aft.description, inline=False)

                    func.time_print("貼圖編輯")
                    await self.guild_log_channel.send(embed=embed, stickers=[aft])
                    return

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_guild_stickers_update", e)


    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        try:
            embed = discord.Embed(title="身份組創建", description=role.mention, timestamp=t.datetime.now(), color=0x0000E3)
            embed.add_field(name="身份組名稱", value=role.name, inline=False)
            self.guild_log_channel.send(embed=embed)
            func.time_print("身份組創建")

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_guild_role_create", e)


    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        try:
            embed = discord.Embed(title="身份組刪除", description=role.mention, timestamp=t.datetime.now(), color=0x0000E3)
            embed.add_field(name="身份組名稱", value=role.name, inline=False)
            self.guild_log_channel.send(embed=embed)
            func.time_print("身份組刪除")
        
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_guild_role_delete", e)


    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            embeds = []

            if before.nick != after.nick:

                embed1 = discord.Embed(title="伺服器暱稱更新", description=before.mention, timestamp=t.datetime.now(), color=0x5A5AAD)
                embed1.set_author(name=before.name, icon_url=before.display_avatar.url)
                embed1.add_field(name="原始暱稱", value=before.nick, inline=False)
                embed1.add_field(name="更新暱稱", value=after.nick, inline=False)

                embeds.append(embed1)

            if before.roles != after.roles:

                embed2 = discord.Embed(title="身份組更新", description=before.mention, timestamp=t.datetime.now(), color=0x5A5AAD)
                embed2.set_author(name=before.name, icon_url=before.display_avatar.url)

                for after_role in after.roles:
                    if after_role not in before.roles:

                        embed2.add_field(name="新增", value=after_role.mention, inline=False)

                        func.time_print(f"身份組新增:{after_role} 成員:{before}")

                for before_role in before.roles:
                    if before_role not in after.roles:

                        embed2.add_field(name="移除", value=before_role.mention, inline=False)
                        
                        func.time_print(f"身份組移除:{before_role} 成員:{before}")

                embeds.append(embed2)

            if before.guild_avatar != after.guild_avatar:

                embed3 = discord.Embed(title="伺服器頭像更新", description=before.mention, timestamp=t.datetime.now(), color=0x5A5AAD)
                embed3.set_author(name=before.name, icon_url=before.display_avatar.url)
                embed3.set_thumbnail(url=after.display_avatar.url)

                embeds.append(embed3)

            if embeds:
                await self.member_log_channel.send(embeds=embeds)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_member_update", e)


    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        try:
            embeds = []

            if before.name != after.name:

                embed1 = discord.Embed(title="使用者名稱更新", description=before.mention, timestamp=t.datetime.now(), color=0xAE57A4)
                embed1.set_author(name=before.name, icon_url=before.display_avatar.url)
                embed1.add_field(name="原始名稱", value=before.name, inline=False)
                embed1.add_field(name="更新名稱", value=after.name, inline=False)

                embeds.append(embed1)

            if before.global_name != after.global_name:

                embed2 = discord.Embed(title="顯示名稱更新", description=before.mention, timestamp=t.datetime.now(), color=0xAE57A4)
                embed2.set_author(name=before.name, icon_url=before.display_avatar.url)
                embed2.add_field(name="原始名稱", value=before.global_name, inline=False)
                embed2.add_field(name="更新名稱", value=after.global_name, inline=False)

                embeds.append(embed2)

            if before.avatar != after.avatar:

                embed3 = discord.Embed(title="頭像更新", description=before.mention, timestamp=t.datetime.now(), color=0xAE57A4)
                embed3.set_author(name=before.name, icon_url=before.display_avatar.url)
                embed3.set_thumbnail(url=after.display_avatar.url)

                embeds.append(embed3)

            if embeds:
                await self.member_log_channel.send(embeds=embeds)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_user_update", e)


async def setup(bot: MyBot):
    await bot.add_cog(log(bot))