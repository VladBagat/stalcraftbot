from discord import Intents
from discord.ext import commands
from Methods.database.database_requests import connect_to_database
from Methods.database.database_setup import initiate_database
from keys import keys
import os

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents, extensions):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.extensions_list = extensions
        self.pool = connect_to_database()

    async def setup_hook(self):
        # Load the cogs
        for cog in self.extensions_list:
            try:
                await self.load_extension(cog)
                print(f"{cog} was loaded.")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")

        # Sync the commands
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord')


if __name__ == "__main__":
    intents = Intents.default()
    intents.message_content = True
    extens = ['cogs.interactive', 'cogs.scheduled', 'cogs.test']

    bot = MyBot(command_prefix='/', intents=intents, extensions=extens)

    initiate_database()

    if os.getenv('heroku'):
        keys.load_env_keys()
    else:
        keys.load_loc_keys()

    bot.run(keys.discord_key)

    