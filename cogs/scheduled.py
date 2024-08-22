from discord import Interaction, app_commands, ui, ButtonStyle
from discord.ui import View
from Methods.database.database_requests import fetch_hiatus, insert_hiatus
from Methods.functions import parse_nickname
from discord.ext import commands, tasks
from asyncio import gather
from datetime import time

class Scheduled(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hiatus_message.start() 

    #Function for dealing with errors
    async def error_handler(self, obj, interaction):
        if isinstance(obj, Exception):
            await interaction.response.send_message('Не удалось определить пользователя', ephemeral=True, delete_after=10)
            return 
          
    @tasks.loop(time=time(hour=22, minute=18))
    async def hiatus_message(self):
        await self.bot.get_channel(1274462709165068289).send(
            content='Чтобы отметить пропуск, нажмите на кнопку. Повторное нажатие снимает пропуск', 
            view=HiatusButton(bot=self.bot))

class HiatusButton(View):
    #Create a questionary about hiatus 
    def __init__(self, bot, *, timeout: int = 1800):
        super().__init__(timeout=timeout)
        self.user_list = {}
        self.last_message = None
        self.last_user = None
        self.bot = bot
    
    def create_hiatus_response_message(self, user_id):

        hiatus_num, on_hiatus = self.user_list.get(f'{user_id}')
        
        if not on_hiatus:
            on_hiatus = True
            hiatus_num -= 1
            message = f'Пропускаю. Осталось пропусков: **{hiatus_num}**'
            
        else:
            on_hiatus = False
            hiatus_num += 1
            message = f'Не пропускаю. Осталось пропусков: **{hiatus_num}**'
            
        self.user_list[f'{user_id}'] = (hiatus_num, on_hiatus)
        return message

    async def initiate_user(self, interaction):
        #Prepairing user data
        user_nick = interaction.user.nick

        try:
            user_nickname = parse_nickname(user_nick)
        except ValueError as e:
            await self.error_handler(e, interaction)

        #Pool a DB connection
        conn = self.bot.pool.getconn()

        #Fetch data from DB
        try:
            hiatus_num, on_hiatus = fetch_hiatus(conn, user_nickname)
        except Exception as e:
            await self.error_handler(e, interaction)
        finally:
            self.bot.pool.putconn(conn)

        on_hiatus = bool(on_hiatus) 

        return hiatus_num, on_hiatus


    @ui.button(label='Отпуск', emoji='🙏', style=ButtonStyle.blurple)
    async def hiatus(self, interaction: Interaction, button: ui.Button):
        user_id = interaction.user.id

        try: 
            temp = self.user_list[f'{user_id}']
            message = self.create_hiatus_response_message(user_id)

        except KeyError:
            hiatus_num, on_hiatus = await self.initiate_user(interaction)
            self.user_list.update({f"{user_id}":(hiatus_num, on_hiatus)})
            message = self.create_hiatus_response_message(user_id)

        tasks = []

        tasks.append(interaction.response.send_message(message, ephemeral=True, delete_after=30))
    
        if self.last_message and self.last_user == user_id:
            tasks.append(self.last_message.delete())
        else:
            pass

        await gather(*tasks)

        self.last_message = await interaction.original_response()   
        self.last_user = user_id 

async def setup(bot):
    await bot.add_cog(Scheduled(bot))

    