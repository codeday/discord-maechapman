from os import getenv

import discord
import discord.ext.commands as commands

intents = discord.Intents.default()
intents.members = True
BOT_TOKEN = getenv("BOT_TOKEN", None)
bot = commands.Bot(command_prefix='m', intents=intents)


@bot.event
async def on_ready():
    print('Ready')


bot.run(BOT_TOKEN, bot=True, reconnect=True)
