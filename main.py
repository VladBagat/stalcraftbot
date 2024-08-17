import discord
from discord import app_commands
from discord.ext import commands
from Stalcraft.api_key import discord_key
from Stalcraft.main import retrieve_login

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="online")
async def fetch_online(interaction: discord.Interaction):
    online = retrieve_login()
    await interaction.response.send_message(online)

bot.run(discord_key)