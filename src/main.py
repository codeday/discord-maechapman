import traceback
import logging
from os import getenv

import discord
import discord.ext.commands as commands
import gspread
from discord import message


intents = discord.Intents.default()
intents.members = True
BOT_TOKEN = getenv("BOT_TOKEN", None)
bot = commands.Bot(command_prefix='m', intents=intents)


@bot.event
async def on_ready():
    print('Ready')

initial_cogs = [
    "cogs.send"
]
loaded_cogs = []

# Here we load our extensions(cogs) listed above in [initial_extensions].
failed_cogs = []
for cog in initial_cogs:
    # noinspection PyBroadException
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded extension {cog}")
        loaded_cogs.append(cog)
    except Exception as e:
        failed_cogs.append(f'''Failed to load extension {cog}.
Traceback: {traceback.format_exc()}''')
        logging.exception(
            f"Failed to load extension {cog}.", exc_info=traceback.format_exc()
        )

bot.run(BOT_TOKEN, bot=True, reconnect=True)
