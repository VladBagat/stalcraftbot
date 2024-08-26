from discord import Interaction, app_commands, ui, ButtonStyle
from discord.ui import View
from Methods.database.database_requests import fetch_hiatus, update_hiatus, daily_online_hiatus
from Methods.functions import parse_nickname
from discord.ext import commands, tasks
from asyncio import gather
from datetime import time

class Scheduled(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hiatus_message.start()
        self.update_user.start()
        self.check_hiatus.start()
        self.hiatus_view = HiatusButton(bot=self.bot)
                  
    @tasks.loop(time=time(hour=9, minute=00))
    async def hiatus_message(self):
        await self.bot.get_channel(1274462709165068289).send(
            content='Чтобы отметить пропуск, нажмите на кнопку. Повторное нажатие снимает пропуск', 
            view=self.hiatus_view)

    @tasks.loop(time=time(hour=18, minute=00))
    async def update_user(self):
        print(self.hiatus_view.user_list.values())
        with self.bot.pool.getconn() as conn:
            update_hiatus(conn, list(self.hiatus_view.user_list.values()))

    @tasks.loop(time=time(hour=18, minute=10))
    async def check_hiatus(self):
        with self.bot.pool.getconn() as conn:
            results = daily_online_hiatus(conn)
        print(results)
    
    #Function for dealing with errors
    async def error_handler(self, obj, interaction):
        if isinstance(obj, Exception):
            await interaction.response.send_message('Не удалось определить пользователя', ephemeral=True, delete_after=10)
            return 
    
class HiatusButton(View):
    #Create a questionary about hiatus 
    def __init__(self, bot, *, timeout: int = 1800):
        super().__init__(timeout=timeout)
        self.user_list = {}
        self.last_message = None
        self.last_user = None
        self.bot = bot
    
    def create_hiatus_response_message(self, user_id):

        hiatus_num, on_hiatus, user_nickname = self.user_list.get(f'{user_id}')
        
        if not on_hiatus and hiatus_num >= 1:
            on_hiatus = 1
            hiatus_num -= 1
            message = f'Пропускаю. Осталось пропусков: **{hiatus_num}**'
        elif on_hiatus:
            on_hiatus = 0
            hiatus_num += 1
            message = f'Не пропускаю. Осталось пропусков: **{hiatus_num}**'
        else:
            message = f'У вас не осталось пропусков'
            
        self.user_list[f'{user_id}'] = (hiatus_num, on_hiatus, user_nickname)

        print('User list in response message', self.user_list)
        return message

    async def initiate_user(self, interaction):
        #Prepairing user data
        user_nick = interaction.user.nick

        try:
            user_nickname = parse_nickname(user_nick)
        except ValueError as e:
            await self.error_handler(e, interaction)     

        #Fetch data from DB
        try:
            with self.bot.pool.getconn() as conn:
                hiatus_num, on_hiatus = fetch_hiatus(conn, user_nickname)
        except Exception as e:
            await self.error_handler(e, interaction)

        print('Data in user initialization', hiatus_num, on_hiatus, user_nickname)
        
        return hiatus_num, on_hiatus, user_nickname

    @ui.button(label='Отпуск', emoji='🙏', style=ButtonStyle.blurple)
    async def hiatus(self, interaction: Interaction, button: ui.Button):
        user_id = interaction.user.id

        try: 
            temp = self.user_list[f'{user_id}']
            message = self.create_hiatus_response_message(user_id)

        except KeyError:
            hiatus_num, on_hiatus, user_nickname = await self.initiate_user(interaction)
            self.user_list.update({f"{user_id}":(hiatus_num, on_hiatus, user_nickname)})
            print('User list in initiation process', self.user_list)
            message = self.create_hiatus_response_message(user_id)

        tasks = []

        tasks.append(interaction.response.send_message(message, ephemeral=True, delete_after=120))
    
        if self.last_message and self.last_user == user_id:
            tasks.append(self.last_message.delete())
        else:
            pass

        await gather(*tasks)

        self.last_message = await interaction.original_response()   
        self.last_user = user_id        
        
async def setup(bot):
    await bot.add_cog(Scheduled(bot))

    