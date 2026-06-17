from dotenv import load_dotenv
import os
import sys
import Define.Functions as func
from Define.Classes import MyBot
import asyncio


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


settings = func.read_json("settings")


bot = MyBot()

@bot.event
async def on_ready():
    try:
        func.time_print("online")
        await bot.get_channel(settings['id']['channel']['bot']['panel']).send("online")
    except Exception as e:
        print(e)


# 終端機指令讀取函式
async def stdin_reader():
    # 獲取 event loop
    loop = asyncio.get_event_loop()

    while True:
        # 讀取終端機輸入
        line = (await loop.run_in_executor(None, sys.stdin.readline)).strip()

        # 忽略空值
        if not line:
            continue
        
        # 將指令和參數分離
        args = line.split()
        cmd = args.pop(0)

        # 如果沒有參數就跳過
        if not args:
            continue

        # load/reload/unload 指令
        try:
            if cmd == "l":
                await bot.load_extension(f"Cogs.{args[0]}")
                func.time_print(f"Load {args[0]}.py")
                await bot.tree.sync()

            elif cmd == "rl":
                await bot.reload_extension(f"Cogs.{args[0]}")
                func.time_print(f"Reload {args[0]}.py")
                await bot.tree.sync()

            elif cmd == "ul":
                await bot.unload_extension(f"Cogs.{args[0]}")
                func.time_print(f"Unload {args[0]}.py")
                await bot.tree.sync()
            
        except Exception as e:
            func.time_print(f"Error\n{e}")


async def main():
    try:
        async with bot:
            asyncio.create_task(stdin_reader())
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