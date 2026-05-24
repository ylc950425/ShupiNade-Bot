import discord
from discord.ext import commands
from Define.Classes import MyBot, MyCog
import Define.Functions as func


settings = func.read_json("settings")


message_id_set = {
    func.get_message_id(reaction_role['message_url'])
    for reaction_role in settings['reaction_role']
}


class reaction(MyCog):

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        try:
            if payload.message_id not in message_id_set:
                return
            
            if payload.member.bot:
                return
            
            for reaction_role in settings['reaction_role']:
                message_id = func.get_message_id(reaction_role['message_url'])

                if payload.message_id == message_id and str(payload.emoji) == reaction_role['reaction']:
                    message = await self.guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    role = self.guild.get_role(reaction_role['role_id'])
                    
                    await message.add_reaction(payload.emoji)

                    if reaction_role['role_id'] == settings['id']['role']['basic']:
                        await message.remove_reaction(payload.emoji, payload.member)

                    await payload.member.add_roles(role)
            
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_raw_reaction_add", e)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        try:
            if payload.message_id not in message_id_set:
                return
            
            # 刪除反應的payload不會有member，要自己取得
            member = self.guild.get_member(payload.user_id)
            if member.bot:
                return
            
            for reaction_role in settings['reaction_role']:
                message_id = func.get_message_id(reaction_role['message_url'])

                if payload.message_id == message_id and str(payload.emoji) == reaction_role['reaction']:
                    if reaction_role['role_id'] == settings['id']['role']['basic']:
                        return

                    
                    role = self.guild.get_role(reaction_role['role_id'])

                    await member.remove_roles(role)

        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.on_raw_reaction_remove", e)
        

async def setup(bot: MyBot):
    await bot.add_cog(reaction(bot))