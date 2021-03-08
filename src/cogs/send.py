import gspread
import discord
from discord.ext import commands


class SendCog(commands.Cog, name="Send"):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(SendCog(bot))
