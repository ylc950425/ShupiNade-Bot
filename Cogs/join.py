import discord
from discord.ext import commands
from Define.Classes import MyBot, MyCog
import Define.Functions as func
import datetime as t


settings = func.read_json("settings")

rule_channel_id: int = settings['id']['channel']['rule']
welcome_message: str = settings['welcome_message']

member_counter_enable: bool = settings['functions']['member_counter']['enable']
member_counter_str: str = settings['functions']['member_counter']['name']


class join(MyCog):

    async def count(self):
        try:
            name = member_counter_str.format(member_count=self.guild.member_count)
            func.time_print(f"伺服器人數：{self.guild.member_count}")
            await self.guild.get_channel(settings['id']['channel']['member_count']).edit(name=name)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.count", e)

    async def welcome(self, member: discord.Member):
        try:
            message = welcome_message.format(member=member.mention, guild=member.guild.name, rule_channel=f"<#{rule_channel_id}>")
            
            func.time_print(f"{member} 加入伺服器")
            await self.guild.get_channel(settings['id']['channel']['welcome']).send(content=message)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.welcome", e)

    async def leave(self, member: discord.Member):
        try:
            embed = discord.Embed(title="成員退出", description=f"{member.mention}離開伺服器", timestamp=t.datetime.now(), color=0x71e5ff)
            embed.set_author(name=member, icon_url=member.display_avatar)

            if member.joined_at:
                utc_time = member.joined_at
                time_stamp = f"<t:{int(utc_time.timestamp())}:F>（<t:{int(utc_time.timestamp())}:R>）"
                embed.add_field(name="加入時間", value=time_stamp, inline=False)

            sentence = ""
            for role in member.roles:
                if role.name == "@everyone":
                    continue
                sentence += f"{role.mention}\n"
            embed.add_field(name="身份組", value=sentence, inline=False)

            func.time_print(f"{member} 退出伺服器")
            await self.guild.get_channel(settings['id']['channel']['log']['guild']).send(embed=embed)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.leave", e)


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            # 忽略測試帳號: YLC(偽物)
            if member.id == 1262974538522824714:
                return
            
            if member_counter_enable:
                await self.count()

            await self.welcome(member)
            
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_member_join", e)


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            # 忽略測試帳號: YLC(偽物)
            if member.id == 1262974538522824714:
                return
            
            if member_counter_enable:
                await self.count()
            
            await self.leave(member)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_member_remove", e)


async def setup(bot: MyBot):
    await bot.add_cog(join(bot))