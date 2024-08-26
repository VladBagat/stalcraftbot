from discord import Interaction, app_commands
from Methods.functions import process_date
from Methods.API_requests import retrieve_online
from discord.ext import commands

class Interactive(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Retrieve online function
    @app_commands.command(name="online", description="Узнать онлайн выбранного игрока")
    async def fetch_online(self, interaction: Interaction, player: str) -> None:
        try:
            online = retrieve_online(player)
            message = process_date(online, player)
        except ValueError:
            message = 'Игрок не найден'
        
        await interaction.response.send_message(message)


async def setup(bot):
    await bot.add_cog(Interactive(bot))