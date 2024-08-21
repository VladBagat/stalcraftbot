import discord
from discord import Interaction
from discord.ui import View, Button, button
from discord.ext import commands
from api_key import discord_key
from Methods.API_requests import retrieve_login
from Methods.functions import process_date
from asyncio import gather

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

#State confirmation
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#Retrieve online function
@bot.tree.command(name="online", description="Узнать онлайн выбранного игрока")
async def fetch_online(interaction: discord.Interaction, player: str):
    online = retrieve_login(player)

    message = process_date(online, player)

    await interaction.response.send_message(message)

#Create a questionary about hiatus 
class HiatusButton(View):
    def __init__(self, *, timeout: int = 1800):
        super().__init__(timeout=timeout)
        self.user_list = {}
        self.last_message = None
        self.last_user = None
    
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

    @discord.ui.button(label='Отпуск', emoji='🙏', style=discord.ButtonStyle.blurple)
    async def hiatus(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_id = interaction.user.id

        try: 
            temp = self.user_list[f'{user_id}']
            
            message = self.create_hiatus_response_message(user_id)

        except KeyError:
            self.user_list.update({f"{user_id}":(2, False)})

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
        
@bot.tree.command(name='hiatus', description='Запустить опрос о пропусках')
async def hiatus_message(interaction: discord.Interaction):
    await interaction.response.send_message(view=HiatusButton())

bot.run(discord_key)