import datetime
from dotenv import load_dotenv
import gspread
import discord
from discord import client, message
from discord.ext import commands, tasks


class SendCog(commands.Cog, name="Send"):
    def __init__(self, bot):
        self.bot = bot
        self.events = []
        self.update.start()

    def cog_unload(self):
        self.update.cancel()

    @commands.command(name='m')
    async def check(self, ctx):
        load_dotenv()
        gc = gspread.service_account(filename='service_account.json')
        sheet = gc.open('Discord Announcements')
        worksheet = sheet.get_worksheet(0)
        list_of_dicts = worksheet.get_all_records()
        await ctx.send(list_of_dicts)

    @tasks.loop(seconds=60)
    async def update(self):
        print("Updating Variable")
        gc = gspread.service_account(filename='service_account.json')
        sheet = gc.open('Discord Announcements')
        worksheet = sheet.get_worksheet(0)
        records = worksheet.get_all_records()
        self.events = records
        for record in records:
            print(records)
            print(record['Time'])
            (timestamp) = str(datetime.datetime.today())
            print(str(timestamp))
            if record['Posted'] == 'FALSE':
                if str(record['Time']) in timestamp:
                    message_channel = await self.bot.fetch_channel(int(record['ChannelID']))
                    await message_channel.send(str(record['Announcement']))
                    announcement_cell = worksheet.find(str(record['Announcement']))
                    announcement_row = announcement_cell.row
                    worksheet.update_cell(announcement_row, 5, "TRUE")
                    print(announcement_row)
                continue


def setup(bot):
    bot.add_cog(SendCog(bot))
