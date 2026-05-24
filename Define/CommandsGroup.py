import discord
import Define.Functions as func


settings = func.read_json("settings")


class MyCommandGroup(discord.app_commands.Group):
    # 新增指令時將覆蓋相同名稱的舊指令
    def add_command(self, command, /, *, override = True):
        return super().add_command(command, override=override)
    
    async def interaction_check(self, interaction: discord.Interaction):
        # 如果是公開指令
        
        if interaction.command.extras.get("public"):
            return True
        
        # 限制指令只能被管理員使用
        admin_ids = {settings['id']['role']['admin'], settings['id']['role']['sub_admin']}
        if any(role.id in admin_ids for role in interaction.user.roles):
            return True
        await interaction.response.send_message(content="只有管理員能使用此指令", ephemeral=True)
        return False
    
    # 預設指令的extras
    def command(self, *, name = ..., description = ..., nsfw = False, auto_locale_strings = True, extras = {"public": True}):
        return super().command(name=name, description=description, nsfw=nsfw, auto_locale_strings=auto_locale_strings, extras=extras)
    

# 遊戲指令
class GameCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="game", description="遊戲指令")

    # 限制指令只能在遊戲指令頻道和後台使用
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.channel_id == settings['id']['channel']['bot']['game'] or interaction.channel_id == settings['id']['channel']['bot']['panel']:
            return True
        else:
            await interaction.response.send_message(content=f"此指令只能在 <#{settings['id']['channel']['bot']['game']}> 使用", ephemeral=True)
            return False


# 訊息指令
class MessageCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="message", description="訊息指令")


# 語音頻道指令
class VcCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="voice-channel", description="語音頻道指令")


# 設定指令
class SettingsCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="settings", description="設定指令")


# youtube設定指令
class YoutubeCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="youtube", description="youtube設定指令")


# 功能指令
class FunctionCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="func", description="功能指令")

class ConvertCommandsGroup(MyCommandGroup):
    def __init__(self):
        super().__init__(name="convert", description="換算指令")