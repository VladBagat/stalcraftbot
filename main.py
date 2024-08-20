import discord
from discord import Interaction
from discord.ui import View, Button, button
from discord.ext import commands
from api_key import discord_key
from Methods.API_requests import retrieve_login
from Methods.functions import process_date

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


class HiatusView(View):

    def __init__(self, user_id):
        super().__init__()
        self.hiatus_num = 2
        self.user_id = user_id
        self.msg = None 

    @button(label='Пропускаю', emoji='💤', style=discord.ButtonStyle.danger)
    async def hiatus_post(self, interaction: Interaction, button: Button):
        is_hiatus = False

        if button.style == discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.danger
            self.hiatus_num += 1
            is_hiatus = False
            await interaction.response.edit_message(view=self)
            
        else:
            button.style = discord.ButtonStyle.success
            self.hiatus_num -= 1
            is_hiatus = True
            await interaction.response.edit_message(view=self)

            if self.msg is None:
                self.msg = await interaction.followup.send(content=f"Пропуск засчитан. Оставшееся количество пропусков: {self.hiatus_num}", ephemeral=True)
            else:
                await self.msg.edit(content=f"Пропуск засчитан. Оставшееся количество пропусков: {self.hiatus_num}")

        if is_hiatus:    
            await self.msg.edit(content=f"Пропуск засчитан. Оставшееся количество пропусков: {self.hiatus_num}")
            
        else:
            await self.msg.edit(content=f"Пропуск отменён. Оставшееся количество пропусков: {self.hiatus_num}")
            

@bot.tree.command(name='hiatus', description='Опубликовать опрос о пропусках')
async def hiatus_command(interaction: discord.Interaction):
    view = HiatusView(user_id=interaction.user.id)
    await interaction.response.send_message('Нажмите на кнопку, чтобы отметить пропуск.', view=view)



bot.run(discord_key)