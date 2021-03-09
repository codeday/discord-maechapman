from datetime import date

import gspread
import discord
from discord import client, message
from discord.ext import commands, tasks



class SendCog(commands.Cog, name="Send"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='m')
    async def check(self, ctx):
        gc = gspread.service_account(filename='service_account.json')
        sheet = gc.open('Discord Announcements')
        worksheet = sheet.get_worksheet(0)
        list_of_dicts = worksheet.get_all_records()
        await ctx.send(list_of_dicts)

def setup(bot):
    bot.add_cog(SendCog(bot))
