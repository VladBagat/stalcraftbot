import discord
from api_key import discord_key
from discord.ext import commands
import StalcraftBot.main as stalcraft

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def fetch_online(ctx):
    stalcraft.retrieve_login()

client.run(discord_key)