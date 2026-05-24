import discord
from discord.ext import commands
import Define.Functions as func
import os
from pathlib import Path


settings = func.read_json("settings")


class MyBot(commands.Bot):
    @property
    def guild(self):
        return self.get_guild(settings['id']['guild'])
    
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
    
    async def load_extensions(self):
        for filename in os.listdir("./Cogs"):
            try:
                if filename.endswith(".py"):
                    await self.load_extension(f"Cogs.{filename[:-3]}")
                    func.time_print(f"Load {filename}")

            except Exception as e:
                func.time_print(f"Load {filename} failed")
                print(e)
    
    async def setup_hook(self):
        # 載入所有Cog
        await self.load_extensions()
        # 載入斜線指令
        slash = await self.tree.sync()
        func.time_print(f"Load slash commands: {slash}")
        

class MyCog(commands.Cog):
    @property
    def guild(self):
        return self.bot.guild
    
    @property
    def panel_channel(self):
        return self.guild.get_channel(settings['id']['channel']['bot']['panel'])
    
    def __init__(self, bot: MyBot):
        self.bot = bot

    async def report_error(self, file_path: str, function_name: str, exception: Exception):
        path = Path(file_path)
        func.time_print(f"Error: {path.stem}.{function_name}\n{exception}")
        await self.panel_channel.send(f"Error: {path.stem}.{function_name}")


class MyView(discord.ui.View):
    def __init__(self, *, timeout = 180, user_id: int):
        super().__init__(timeout=timeout)
        self.user_id = user_id

    # 不讓指令使用者以外的人使用按鈕
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            return True
        else:
            await interaction.response.send_message(content="你不是此指令的使用者，無法使用按鈕", ephemeral=True)
            return False
        
    def report_error(self, file_path: str, function_name: str, exception: Exception):
        path = Path(file_path)
        func.time_print(f"Error: {path.stem}.{function_name}\n{exception}")


class MyModal(discord.ui.Modal):
    def report_error(self, file_path: str, function_name: str, exception: Exception):
        path = Path(file_path)
        func.time_print(f"Error: {path.stem}.{function_name}\n{exception}")