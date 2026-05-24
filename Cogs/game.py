import discord
from discord import ui, ButtonStyle, Interaction
from discord.ext import tasks
from Define.Classes import MyBot, MyCog, MyView
from Define.CommandsGroup import GameCommandsGroup
import Define.Functions as func
import random


settings = func.read_json("settings")
game_data = func.read_json("game_data")
game_data_dirty = False


# 骰子
class Dice(MyView):
    def __init__(self, *, timeout=180, user_id):
        super().__init__(timeout=timeout, user_id=user_id)
        self.roll_count = 0
        self.dice_count: int
        self.result_log: list[dict] = []

        self.log_page = -1
        self.log_list: list[list[str]] = []

        self.state = "menu"

        self.roll_button = ui.Button(label="繼續擲", style=ButtonStyle.blurple)
        self.roll_button.callback = self.roll_dice
        self.show_log_button = ui.Button(label="查看紀錄")
        self.show_log_button.callback = self.show_log
        self.prev_page_button = ui.Button(label="◀上一頁")
        self.prev_page_button.callback = lambda i: self.flip_page(i, False)
        self.next_page_button = ui.Button(label="下一頁▶")
        self.next_page_button.callback = lambda i: self.flip_page(i, True)

    def update_view(self):
        self.clear_items()

        if self.state == "play":
            self.add_item(self.roll_button)
            self.add_item(self.show_log_button)

        elif self.state == "log":
            self.add_item(self.roll_button)
            self.add_item(self.prev_page_button)
            self.add_item(self.next_page_button)


    async def flip_page(self, interaction: Interaction, mode: bool):
        # false上一頁，true下一頁
        if mode:
            self.log_page += 1
        else:
            self.log_page -= 1
        await self.show_log(interaction)

    async def show_log(self, interaction: Interaction):
        try:
            self.state = "log"

            # 第一次執行時設置顯示用紀錄清單
            if self.log_page == -1:
                self.log_page = 0
                all_logs = [f"{log['result']} {log['count']}" for log in reversed(self.result_log)]
                self.log_list = [all_logs[i : i + 10] for i in range(0, len(all_logs), 10)]

            # 將翻頁按鈕disable
            self.prev_page_button.disabled = (self.log_page <= 0)
            self.next_page_button.disabled = (self.log_page + 1 >= len(self.log_list))

            embed = interaction.message.embeds[0].clear_fields()
            for log_str in self.log_list[self.log_page]:
                embed.add_field(name="", value=log_str, inline=False)

            self.update_view()
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.show_log", e)

    async def roll_dice(self, interaction: discord.Interaction):
        try:
            self.state = "play"
            self.roll_count += 1

            # 如果是在查看紀錄的頁面按下此按鈕，將紀錄頁碼歸零並清空顯示用紀錄清單
            if self.log_page != -1:
                self.log_page = -1
                self.log_list.clear()

            # 生成並紀錄這次的結果
            emoji = game_data['dice']['emoji']
            result_str = "".join(f"\n{random.choice(emoji)}" if num == 10 else random.choice(emoji) for num in range(self.dice_count))
            self.result_log.append(
                {
                    "count": self.roll_count,
                    "result": result_str
                }
            )
            if len(self.result_log) > 100:
                del self.result_log[0]
                # self.result_log.pop(0)

            embed = interaction.message.embeds[0].clear_fields()
            embed.description = f"你總共擲了 {self.roll_count} 次"
            embed.add_field(name="本次結果", value=result_str)
            self.update_view()
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.roll_dice", e)

    # 選擇要擲幾顆骰子的下拉式選單
    number_list = [discord.SelectOption(label=str(num + 1), value=str((num + 1))) for num in range(20)]
    @ui.select(options=number_list, placeholder="選擇你要擲的顆數")
    async def number_select(self, interaction: discord.Interaction, select: ui.Select):
        try:
            self.dice_count = int(select.values[0])
            await self.roll_dice(interaction)
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.number_select", e)

# 骰子挑戰
class DiceChallenge(MyView):
    def __init__(self, *, timeout=180, user_id):
        super().__init__(timeout=timeout, user_id=user_id)
        # 預設玩家資料
        player_data = game_data['player'].setdefault(
            str(user_id),
            {}
        ).setdefault(
            "dice",
            {
                "total_challenge_count": 0,
                "dice_count": 2,
                "roll_count": {
                    "2": 0
                }
            }
        )
        self.total_challenge_count: int = player_data['total_challenge_count']
        self.dice_count: int = player_data['dice_count']
        self.roll_count: dict = player_data['roll_count']

        self.state = "playing"

    def save_data(self):
        global game_data_dirty
        game_data['player'][str(self.user_id)]['dice'] = {
            "total_challenge_count": self.total_challenge_count,
            "dice_count": self.dice_count,
            "roll_count": self.roll_count
        }
        game_data_dirty = True

    def update_view(self):
        for child in self.children:
            if isinstance(child, ui.Button) and child.custom_id == "show_log":
                child.disabled = (self.state == "log")

    @ui.button(label="擲", style=ButtonStyle.blurple)
    async def roll(self, interaction: discord.Interaction, button: ui.Button):
        try:
            self.state = "playing"
            # 總挑戰次數以及當前階段挑戰次數+1
            self.total_challenge_count += 1
            self.roll_count[str(self.dice_count)] += 1

            results = [random.randint(0, 5) for _ in range(self.dice_count)]
            # set會去掉重複值，用以檢查結果是否相同
            same_flag = (len(set(results)) == 1)
            result_str = "".join(game_data['dice']['emoji'][index] for index in results)

            embed = interaction.message.embeds[0].clear_fields()
            embed.add_field(name="本次結果", value=result_str)

            if same_flag:
                embed.description = f"### 恭喜你完成 {self.dice_count} 顆骰子的挑戰\n你在此階段挑戰了 {self.roll_count[str(self.dice_count)]} 次"
                self.dice_count += 1
                self.roll_count[str(self.dice_count)] = 0
            else:
                embed.description = f"### {self.dice_count} 顆\n你在此階段挑戰了 {self.roll_count[str(self.dice_count)]} 次"

            self.save_data()
            self.update_view()
            await interaction.response.edit_message(embed=embed, view=self)     

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.roll", e)

    @ui.button(label="查看紀錄", custom_id="show_log")
    async def show_log(self, interaction: discord.Interaction, button: ui.Button):
        try:
            self.state = "log"

            embed = interaction.message.embeds[0].clear_fields()
            embed.description = "### 紀錄"
            embed.add_field(name="目前階段", value=f"**{self.dice_count} 顆：**{self.roll_count[str(self.dice_count)]} 次", inline=False)
            embed.add_field(name="總挑戰次數", value=f"{self.total_challenge_count} 次", inline=False)

            log_str = "\n".join(f"**{count} 顆：**{self.roll_count[str(count)]} 次" for count in range(2, self.dice_count))
            embed.add_field(name="已完成的挑戰", value=log_str , inline=False)

            self.update_view()
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.show_log", e)

# 二選一遊戲
class RedOrBlue(MyView):
    def __init__(self, *, timeout=180, user_id):
        super().__init__(timeout=timeout, user_id=user_id)
        # 預設玩家資料
        player_data = game_data['player'].setdefault(
            str(user_id),
            {}
        ).setdefault(
            "red_or_blue",
            {
                "choose_count": 0,
                "success_count": 0,
                "highest_level": 1
            }
        )
        self.choose_count: int = player_data['choose_count']
        self.success_count: int = player_data['success_count']
        self.highest_level: int = player_data['highest_level']

        self.now_level: int
        self.right_button: bool  # 紅色False，藍色True

        self.start_button = ui.Button(label="開始遊戲", style=ButtonStyle.green)
        self.start_button.callback = self.start
        self.restart_button = ui.Button(label="重新開始", style=ButtonStyle.green)
        self.restart_button.callback = self.start
        self.show_log_button = ui.Button(label="查看紀錄")
        self.show_log_button.callback = self.show_log
        # 按鈕標籤使用零寬字元U+200B
        self.red_button = ui.Button(label="​", style=ButtonStyle.red)
        self.red_button.callback = lambda i: self.check_choice(i, False)
        self.blue_button = ui.Button(label="​", style=ButtonStyle.blurple)
        self.blue_button.callback = lambda i:self.check_choice(i, True)
        # self.show_ranking_button = ui.Button(label="查看排名", row=1)
        # self.show_ranking_button.callback = self.show_ranking
        
        self.state = "menu"
        self.update_view()


    def save_data(self):
        global game_data_dirty
        game_data['player'][str(self.user_id)]['red_or_blue'] = {
            "choose_count": self.choose_count,
            "success_count": self.success_count,
            "highest_level": self.highest_level
        }
        game_data_dirty = True

        # flag = False
        # for index, player in game_data['red_or_blue']['ranking']:
        #     if player['user_id'] == self.user_id and player['level'] >= self.highest_level:


        #         game_data['red_or_blue']['ranking'].insert(
        #             index,
        #             {
        #                 "user_id": self.user_id,
        #                 "level": self.highest_level
        #             }
        #         )
        #         flag = True

    def update_view(self):
        self.right_button = random.choice([True, False])
        self.clear_items()

        if self.state == "menu":
            self.add_item(self.start_button)
            self.add_item(self.show_log_button)
            # self.add_item(self.show_ranking_button)

        elif self.state == "playing":
            self.add_item(self.red_button)
            self.add_item(self.blue_button)

        elif self.state == "game_over":
            self.add_item(self.restart_button)
            self.add_item(self.show_log_button)
            # self.add_item(self.show_ranking_button)

    async def start(self, interaction: discord.Interaction):
        try:
            self.state = "playing"
            self.now_level = 1
            self.update_view()

            embed = interaction.message.embeds[0].clear_fields()
            embed.description = "### 第 1 關\n抵達機率：1/1"
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.start", e)

    async def check_choice(self, interaction: discord.Interaction, choice: bool):
        try:
            self.choose_count += 1
            embed = interaction.message.embeds[0].clear_fields()

            if choice == self.right_button:
                self.success_count += 1
                self.now_level += 1

                denominator: int = 2 ** (self.now_level - 1)
                embed.description = f"### 第 {self.now_level} 關\n抵達機率：1/{denominator}"

                if self.now_level > self.highest_level:
                    self.highest_level = self.now_level
                    embed.add_field(name="", value="你突破自己的記錄了！")

            else:
                self.state = "game_over"
                embed.add_field(name="", value="**GAME OVER**")

            self.update_view()
            self.save_data()
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.check_choice", e)

    async def show_log(self, interaction: discord.Interaction):
        try:
            embed = interaction.message.embeds[0].clear_fields()
            embed.description = "### 紀錄"
            embed.add_field(name="總選擇次數", value=self.choose_count, inline=False)
            embed.add_field(name="正確次數", value=self.success_count)
            embed.add_field(name="錯誤次數", value=self.choose_count - self.success_count)
            embed.add_field(name="最佳紀錄", value=f"第 {self.highest_level} 關\n抵達機率：1/{2 ** (self.highest_level - 1)}", inline=False)
            await interaction.response.edit_message(embed=embed)
        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.show_log", e)

    # async def show_ranking(self, interaction: discord.Interaction):
    #     try:
    #         embed = interaction.message.embeds[0].clear_fields()
    #         embed.description = "### 排名"
    #         for count, player in enumerate(game_data['red_or_blue']['ranking']):
    #             embed.add_field(name="", value=f"玩家：<@{player['user_id']}>\n紀錄：第 {player['level']} 關", inline=False)
    #             if count >= 24:
    #                 break
    #         await interaction.response.edit_message(embed=embed)
    #     except Exception as e:
    #         self.report_error(__file__, f"{self.__class__.__name__}.show_ranking", e)

# 擲硬幣
class CoinToss(MyView):
    def __init__(self, *, timeout=180, user_id):
        super().__init__(timeout=timeout, user_id=user_id)
        self.toss_count = 0
        self.heads_count = 0
        self.tails_count = 0

    @ui.button(label="擲！", style=ButtonStyle.blurple)
    async def toss(self, interaction: discord.Interaction, button: ui.Button):
        try:
            self.toss_count += 1
            coin_index = random.choice([0, 1])
            if bool(coin_index):
                self.heads_count += 1
            else:
                self.tails_count += 1
            
            embed = interaction.message.embeds[0]
            embed.description = f"### 你總共擲了 {self.toss_count} 次\n 正面 {self.heads_count} 次\n反面 {self.tails_count} 次"
            embed.set_image(url=f"{settings['image']['coin'][coin_index]['url']}.png")

            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            self.report_error(__file__, f"{self.__class__.__name__}.toss", e)


class game(MyCog):
    def __init__(self, bot: MyBot):
        super().__init__(bot)

    def cog_load(self):
        self.minute_loop.start()

    def cog_unload(self):
        self.minute_loop.cancel()

        global game_data_dirty
        if game_data_dirty:
            func.write_json("game_data", game_data)
            game_data_dirty = False

    @tasks.loop(minutes=1)
    async def minute_loop(self):
        try:
            # 每分鐘存檔
            global game_data_dirty
            if game_data_dirty:
                func.write_json("game_data", game_data)
                game_data_dirty = False
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.minute_loop", e)


    gameCommandsGroup = GameCommandsGroup()

    @gameCommandsGroup.command(name="dice", description="擲骰子")
    async def dice(self, interaction: discord.Interaction):
        try:
            view = Dice(user_id=interaction.user.id)
            embed = discord.Embed(title="擲骰子", description="準備好了就擲吧！", color=0x9F35FF)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.dice", e)

    @gameCommandsGroup.command(name="dice-challenge", description="擲骰子挑戰，希望你能在這無止盡的挑戰中找到一點樂趣")
    async def dice_challenge(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="骰子挑戰", description="無止盡的擲骰子\n擲出的所有骰子點數相同即可進到下一階段", color=0x9F35FF)
            view = DiceChallenge(user_id=interaction.user.id)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.dice_challenge", e)

    @gameCommandsGroup.command(name="coin-toss", description="擲硬幣")
    async def coin_toss(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="擲硬幣", description="50%的機率，擲吧！", color=0x9F35FF)
            view = CoinToss(user_id=interaction.user.id)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.coin_toss", e)

    @gameCommandsGroup.command(name="red-or-blue", description="二選一遊戲")
    async def red_or_blue(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="二選一遊戲", description="每道關卡會有兩個按鈕\n按下正確的按鈕才可以通往下一關", color=0x9F35FF)
            view = RedOrBlue(user_id=interaction.user.id)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await self.report_error(__file__, f"{self.__class__.__name__}.red_or_blue", e)


async def setup(bot: MyBot):
    await bot.add_cog(game(bot))