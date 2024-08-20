import discord
from discord import app_commands
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

#Update hiatus status
@bot.tree.command(name='Hiatus', description='Опубликовать опрос о пропусках')
async def hiatus_post(ctx):
    await ctx.send('Sigma')

bot.run(discord_key)