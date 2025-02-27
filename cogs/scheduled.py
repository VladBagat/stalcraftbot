from discord import Interaction, app_commands, ui, ButtonStyle
from discord.ui import View
from Methods.database.database_requests import fetch_hiatus, update_hiatus, daily_online_hiatus, update_clan_members, increment_player_penalty, reset_hiatus_status, fetch_players_with_penalty
from Methods.API_requests import *
from Methods.functions import parse_nickname
from discord.ext import commands, tasks
from asyncio import gather
from datetime import datetime, timezone, timedelta, time

class Scheduled(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hiatus_message.start()
        self.update_user_hiatus.start()
        self.check_player_online.start()
        self.reset_hiatus.start()
        self.hiatus_view = HiatusButton(bot=self.bot)

    @tasks.loop(time=time(hour=00, minute=00))
    async def reset_hiatus(self):
        if datetime.today().weekday() == 0:
            penalty_channel_id = 1289661974862368798

            channel = self.bot.get_channel(penalty_channel_id)

            if channel == None:
                raise ValueError('Penalty channel not found')
            
            result = self.bot.database_request(fetch_players_with_penalty) #[('ArtemNaw', 100000), ...]

            result = [(name[0].replace("'", ''), name[1]) for name in result]

            result = [f'{name[0]} должен {name[1]}\n\n' for name in result]

            final_message = ''.join(result)

            await channel.send(final_message)

            self.bot.database_request(reset_hiatus_status)


    @tasks.loop(time=time(hour=11, minute=00))
    async def hiatus_message(self):
        self.bot.database_request(update_clan_members)

        await self.bot.get_channel(1283514404733714494).send(
            content='Чтобы отметить пропуск, нажмите на кнопку. Повторное нажатие снимает пропуск', 
            view=self.hiatus_view)

    @tasks.loop(time=time(hour=18, minute=00))
    async def update_user_hiatus(self):
        print(self.hiatus_view.user_list.values())

        self.bot.database_request(update_hiatus, list(self.hiatus_view.user_list.values()))

    @tasks.loop(time=time(hour=18, minute=9))
    async def check_player_online(self):

        database_responce = self.bot.database_request(daily_online_hiatus) or [] #Handles None return

        players = []
        on_hiatus = []

        for user_data in database_responce:
            players.append(user_data[0])
            on_hiatus.append(user_data[1])

        online_times = [retrieve_online(name) for name in players]

        converted_online_times = [datetime.strptime(online_time, r"%Y-%m-%dT%H:%M:%S.%fZ") for online_time in online_times]

        aware_online_times = [naive.replace(tzinfo=timezone.utc) for naive in converted_online_times]

        end_time = datetime.now(tz=timezone.utc)

        start_time = end_time - timedelta(minutes=10)    

        was_on_cw = [end_time >= aware_online_time >= start_time for aware_online_time in aware_online_times]

        late_players = []

        for i in range(len(players)):
            if not was_on_cw[i] and not on_hiatus[i]:
                late_players.append(players[i])

        self.bot.database_request(increment_player_penalty, late_players)

        self.bot.skip = False #Resets skip status for the day

        penalty_channel_id = 1289661974862368798

        channel = self.bot.get_channel(penalty_channel_id)

        final_message = ' '.join(late_players)

        await channel.send(final_message)

    #Function for dealing with errors
    async def error_handler(self, obj, interaction):
        if isinstance(obj, Exception):
            await interaction.response.send_message('Не удалось определить пользователя', ephemeral=True, delete_after=10)
            return 

class HiatusButton(View):
    #Create a questionary about hiatus 
    def __init__(self, bot, *, timeout: int = 28800):
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
            hiatus_num, on_hiatus = self.bot.database_request(fetch_hiatus, user_nickname)
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