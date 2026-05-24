import discord
from discord import ui, app_commands, Interaction
from discord.ext import commands
from Define.Classes import MyBot, MyCog
from Define.CommandsGroup import SettingsCommandsGroup, MessageCommandsGroup, FunctionCommandsGroup, ConvertCommandsGroup, VcCommandsGroup
import Define.Functions as func
import emoji
import asyncio


settings = func.read_json("settings")


# 服務台確認面板
class ReportCheckView(ui.View):
    def __init__(self, *, timeout = 180, report_channel: discord.TextChannel):
        super().__init__(timeout=timeout)
        self.report_channel = report_channel
        
    async def create_report_thread(self, interaction: discord.Interaction,  thread_name: str | None = None):

        await interaction.response.defer()

        for child in self.children:
            if isinstance(child, ui.Button):
                child.disabled = True

        embed = interaction.message.embeds[0]

        if thread_name != None:

            thread_report = await self.report_channel.create_thread(name=thread_name, auto_archive_duration=4320)

            message = f"{interaction.user.mention}\n<@&{settings['id']['role']['admin']}>"
            if settings['id']['role']['sub_admin']:
                message += f"\n<@&{settings['id']['role']['sub_admin']}>"
            await thread_report.send(content=message)

            embed.description = f'隱藏討論串已建立\n請至{thread_report.mention}'

        else:
            embed.description = '已取消動作'

        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=self)

    @ui.button(label='確定', style=discord.ButtonStyle.green)
    async def button3(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_report_thread(interaction, str(interaction.user))

    @ui.button(label='取消', style=discord.ButtonStyle.red)
    async def button4(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_report_thread(interaction)

# 身份組領取設定面板
class ReactionRoleView(ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot):
        super().__init__(timeout=timeout)
        self.bot = bot

    @ui.button(label="新增", row=0, style=discord.ButtonStyle.green)
    async def add(self, interaction: discord.Interaction, button: ui.Button):
        try:
            await interaction.response.send_modal(ReactionRoleAddModal(bot=self.bot))
        except Exception as e:
            await func.report_error("slash.ReactionRoleView.add", e)

    @ui.button(label="刪除", row=0, style=discord.ButtonStyle.red)
    async def remove(self, interaction: discord.Interaction, button: ui.Button):
        try:
            await interaction.response.send_modal(ReactionRoleRemoveModal(bot=self.bot))
        except Exception as e:
            await func.report_error("slash.ReactionRoleView.remove", e)

# 身份組領取: 新增
class ReactionRoleAddModal(ui.Modal):
    def __init__(self, *, title = "新增身份組領取", timeout = None, bot: commands.Bot):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot

    role = ui.Label(text="身份組", component=ui.RoleSelect(required=True))
    emoji = ui.Label(
        text = "反應表符",
        description = "自訂emoji需要用完整格式，如 <:my_emoji:1317099578557726770>",
        component = ui.TextInput()
    )
    message_url = ui.Label(text="訊息URL", component=ui.TextInput(style=discord.TextStyle.paragraph))
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            message_url: str = self.message_url.component.value
            emoji_str: str = self.emoji.component.value
            role: discord.Role = self.role.component.values[0]

            # 檢查訊息URL是否存在
            try:
                message_id = func.get_message_id(message_url)
                channel_id = func.get_channel_id(message_url)
                await self.bot.get_channel(channel_id).fetch_message(message_id)
            except:
                await interaction.response.send_message(content="訊息URL錯誤", ephemeral=True)
                return
            
            # 檢查表情符號格式是否正確
            if not emoji.is_emoji(emoji_str) and not func.is_custom_emoji(emoji_str):
                await interaction.response.send_message(content="表符格式錯誤", ephemeral=True)
                return

            reaction_role_dict = {
                "role_id": role.id,
                "reaction": emoji_str,
                "message_url": message_url
            }
            settings['reaction_role'].append(reaction_role_dict)
            func.write_json("settings", settings)
            await self.bot.reload_extension("Cogs.reaction")

            panel_embed = interaction.message.embeds[0].add_field(
                name = f"{emoji_str}",
                value = f"<@&{role.id}>\n{message_url}"
            )
            embed = discord.Embed(title="設定完成", color=0x00BB00)
            embed.add_field(name="身份組", value=role.mention)
            embed.add_field(name="反應表符", value=emoji_str)
            embed.add_field(name="訊息URL", value=message_url)
            await interaction.response.edit_message(embed=panel_embed)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await func.report_error("slash.ReactionRoleAddModal.on_submit", e)

# 身份組領取: 刪除
class ReactionRoleRemoveModal(ui.Modal):
    def __init__(self, *, title = "刪除身份組領取", timeout = None, bot: commands.Bot):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        guild = bot.get_guild(settings['id']['guild'])
    
        self.delete_target = ui.Label(
            text = "刪除目標",
            component = ui.Select(
                options = [
                    discord.SelectOption(
                        label = guild.get_role(reaction_role['role_id']).name,
                        emoji = reaction_role['reaction'],
                        value = count
                    )
                    for count, reaction_role in enumerate(settings['reaction_role'])
                ]
            )
        )
        self.add_item(self.delete_target)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            delete_index = int(self.delete_target.component.values[0])
            reaction_role = settings['reaction_role'].pop(delete_index)
            func.write_json("settings", settings)
            await self.bot.reload_extension("Cogs.reaction")

            panel_embed = interaction.message.embeds[0].remove_field(delete_index)
            embed = discord.Embed(title="刪除完成", color=0xFF0000)
            embed.add_field(name="身份組", value=f"<@&{reaction_role['role_id']}>")
            embed.add_field(name="反應表符", value=reaction_role['reaction'])
            embed.add_field(name="訊息URL", value=reaction_role['message_url'])
            await interaction.response.edit_message(embed=panel_embed)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await func.report_error("slash.ReactionRoleRemoveModal.on_submit", e)


class slash(MyCog):
    def __init__(self, bot: MyBot):
        super().__init__(bot)
        # cmd1 = app_commands.ContextMenu(name="忘記切輸入法轉換器", callback=self.to_zhuyin)
        # self.bot.tree.add_command(cmd1)

    # def cog_unload(self):
    #     self.bot.tree.remove_command(self.test.name, type=discord.AppCommandType.message)

    # async def to_zhuyin(self, interaction: discord.Interaction, message: discord.Message):
    #     content = message.content.lower()
    #     zhuyin = "ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦ ˊˇˋ˙"
    #     not_zhuyin = "1qaz2wsxedcrfv5tgbyhnujm8ik,9ol.0p;/- 6347"
    #     for count, nz in enumerate(not_zhuyin):
    #         content = content.replace(nz, zhuyin[count])
    #     await interaction.response.send_message(content)

    settingsCommandsGroup = SettingsCommandsGroup()
    messageCommandsGroup = MessageCommandsGroup()
    vcCommandsGroup = VcCommandsGroup()
    functionCommandsGroup = FunctionCommandsGroup()

    convertCommandsGroup = ConvertCommandsGroup()
    functionCommandsGroup.add_command(convertCommandsGroup)


    @settingsCommandsGroup.command(name="reaction-role", description="【Admin Only】身份組領取設定", extras={"public": False})
    async def reaction_role(self, interaction: Interaction):
        try:
            embed = discord.Embed(title="身份組領取設定面板", color=0xFFDC35)
            for reaction_role in settings['reaction_role']:
                embed.add_field(
                    name = f"{reaction_role['reaction']}",
                    value = f"<@&{reaction_role['role_id']}>\n{reaction_role['message_url']}"
                )
            view = ReactionRoleView(bot=self.bot)
            await interaction.response.send_message(embed=embed, view=view)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.reaction_role", e)
    

    @messageCommandsGroup.command(name="send", description="【Admin Only】傳送訊息", extras={"public": False})
    async def send(self, interaction: Interaction, 頻道: discord.TextChannel | discord.Thread, 訊息內容: str):
        try:
            channel = 頻道
            message = 訊息內容
            
            await channel.send(content=message)
            await interaction.response.send_message(content="已發送訊息", ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.send", e)

    @messageCommandsGroup.command(name="edit", description="【Admin Only】編輯訊息", extras={"public": False})
    async def edit(self, interaction: Interaction, 訊息連結: str, 訊息內容: str):
        try:
            try:
                message_id = func.get_message_id(訊息連結)
                channel_id = func.get_channel_id(訊息連結)

                channel = self.guild.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                
            except:
                await interaction.response.send_message(content='訊息連結錯誤', ephemeral=True)
                return
            
            channel = self.guild.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            
            await message.edit(content=訊息內容)
            await interaction.response.send_message(content='已編輯訊息', ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.edit", e)

    @messageCommandsGroup.command(name="credit", description="【Admin Only】發送Credit嵌入訊息", extras={"public": False})
    async def credit(self, interaction: Interaction, 圖片連結: str, 作者: str, 來源連結: str, 備註: str | None = None):
        try:
            maker = 作者.replace("\\n", "\n")
            resource = 來源連結.replace("\\n", "\n")
            
            embed = discord.Embed(
                title="表符出處",
                color=0x71e5ff
            )
            embed.set_thumbnail(url=圖片連結)
            embed.add_field(name="作者", value=maker, inline=True)
            embed.add_field(name="來源連結", value=resource, inline=True)
            if 備註:
                other = 備註.replace("\\n", "\n")
                embed.add_field(name="備註", value=other, inline=False)

            await interaction.channel.send(embed=embed)
            await interaction.response.send_message(content="已發送訊息", ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.credit", e)


    @vcCommandsGroup.command(name="connect", description="將bot加入語音頻道")
    async def connect_vc(self, interaction: Interaction, 語音頻道: discord.VoiceChannel):
        try:
            vc_channel = 語音頻道
            await vc_channel.connect(reconnect=False)
            await interaction.response.send_message("已連接語音頻道", ephemeral=True)

        except asyncio.TimeoutError:
            await interaction.response.send_message("超時，無法連接", ephemeral=True)
        except discord.ClientException:
            await interaction.response.send_message("已經在一個語音頻道中", ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.connect_vc", e)

    @vcCommandsGroup.command(name="disconnect", description="將bot退出語音頻道")
    async def disconnect_vc(self, interaction: Interaction):
        try:
            if self.guild.voice_client:
                await self.guild.voice_client.disconnect()
                message = "已退出語音頻道"
            else:
                message = "非連接語音頻道狀態"

            await interaction.response.send_message(message, ephemeral=True)

        except asyncio.TimeoutError:
            await interaction.response.send_message("超時，無法退出", ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.disconnect_vc", e)


    @convertCommandsGroup.command(name="temperature", description="溫度單位轉換")
    async def temperature(self, interaction: Interaction, 攝氏溫標: str | None = None, 華氏溫標: str | None = None, 絕對溫標: str | None = None):
        try:
            inputs = {
                "°C": 攝氏溫標,
                "°F": 華氏溫標,
                "K": 絕對溫標
            }
            given = {k: v for k, v in inputs.items() if v is not None}

            if len(given) != 1:
                msg = "請輸入一個參數" if len(given) < 1 else "最多只能輸入一個參數"
                return await interaction.response.send_message(msg, ephemeral=True)

            try:
                unit, t = list(given.items())[0]
                temperature = float(t)
                # 統一轉換為攝氏
                if unit == "°C":
                    celsius = temperature
                elif unit == "°F":
                    celsius = (temperature - 32) * 5 / 9
                else:
                    celsius = temperature - 273.15

                if celsius < -273.15:
                    return await interaction.response.send_message("溫度不可小於絕對零度", ephemeral=True)
                
                results = {
                    "°C": round(celsius, 2),
                    "°F": round(celsius * 9 / 5 + 32, 2),
                    "K": round(celsius + 273.15, 2)
                }
                
                msg = "\n".join(f"**{v} {k}**" if k == unit else f"{v} {k}" for k, v in results.items())
                embed = discord.Embed(title="溫度轉換", description=msg, color=0xACD6FF)
                await interaction.response.send_message(embed=embed)

            except ValueError:
                await interaction.response.send_message("請輸入數字", ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.temperature", e)

    # @convertCommandsGroup.command(name="number-base", description="數字系統轉換")
    # async def number_base(self, interaction: Interaction, 二進制數: str | None = None, 八進制數: str | None = None,
    #                       十進制數: str | None = None, 十六進制數: str | None = None):
    #     try:
    #         pass
    #     except Exception as e:
    #         await self.report_error(__file__, f"{self.__class__.__name__}.number_base", e)


    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        try:
            if "custom_id" in interaction.data:
                if interaction.data['custom_id'] == "report":

                    await interaction.response.defer()

                    report_channel = self.guild.get_channel(settings['id']['channel']['report'])
                    view = ReportCheckView(report_channel=report_channel)

                    embed = discord.Embed(title="確認創建")

                    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_interaction", e)


    @commands.command()
    async def set_report(self, ctx: commands.Context):
        try:
            embed = discord.Embed(
                title='🛎️充電站服務台🛎️',
                description='若您需要「**提供意見**、**檢舉**、**申請宣傳項目**、**詢問伺服器相關問題**」\n可以按下按鈕創建專屬頻道跟管理員交談',
                color=0xF9F900
            )
            embed.add_field(name='', value='-# ※ 請勿濫用此功能', inline=False)

            view = ui.View()
            button = ui.Button(label='📩開啟專屬頻道', custom_id='report')
            view.add_item(button)

            await ctx.channel.send(embed=embed, view=view)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.set_report", e)


async def setup(bot: MyBot):
    await bot.add_cog(slash(bot))