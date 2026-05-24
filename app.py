import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import Define.Functions as func
from Define.Classes import MyBot
import asyncio


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


settings = func.read_json("settings")


# bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot = MyBot()


@bot.event
async def on_ready():
    try:
        func.time_print("online")
        await bot.get_channel(settings['id']['channel']['bot']['panel']).send("online")
    except Exception as e:
        print(e)


@bot.command()
async def load(ctx: commands.Context, filename):
    try:
        await bot.load_extension(f'Cogs.{filename}')
        await ctx.send("Done")
        func.time_print(f"Load {filename}")

        await bot.tree.sync()

    except Exception as e:
        await ctx.send("Error")
        func.time_print(f"Load {filename} failed")
        print(e)
        

@bot.command()
async def unload(ctx: commands.Context, filename):
    try:
        await bot.unload_extension(f"Cogs.{filename}")
        await ctx.send("Done")
        func.time_print(f"Unload {filename}")

        await bot.tree.sync()

    except Exception as e:
        await ctx.send("Error")
        func.time_print(f"Unload {filename} failed")
        print(e)


@bot.command()
async def reload(ctx: commands.Context, filename):
    try:
        await bot.reload_extension(f"Cogs.{filename}")
        await ctx.send("Done")
        func.time_print(f"Reload {filename}")

        await bot.tree.sync()

    except Exception as e:
        await ctx.send("Error")
        func.time_print(f"Reload {filename} failed")
        print(e)


async def main():
    try:
        async with bot:
            await bot.start(TOKEN)
    except asyncio.CancelledError:
        print("bot中斷")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
    finally:
        print("bot關閉")