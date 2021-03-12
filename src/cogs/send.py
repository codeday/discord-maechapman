from datetime import datetime
import gspread
import discord
from discord import client, message
from discord.ext import commands, tasks


class SendCog(commands.Cog, name="Send"):
    def __init__(self, bot):
        self.bot = bot
        self.records = []
        self.check.start()
        self.update.start()
        self.gc = gspread.service_account(filename='./service_account.json')
        self.sheet = self.gc.open('Discord Announcements')
        self.worksheet = self.sheet.get_worksheet(0)

    def cog_unload(self):
        self.update.cancel()
        self.check.cancel()

    @tasks.loop(minutes=30)
    async def check(self):
        print('Updating')
        self.records = self.worksheet.get_all_records()

    @tasks.loop(seconds=60)
    async def update(self):
        print("Checking")
        for index, record in enumerate(self.records):
            try:
                if record['Posted'] == 'FALSE':
                    now = datetime.today()
                    announcement_time = datetime.strptime(record['Time'], '%m/%d/%Y %H:%M:%S')
                    if now >= announcement_time:
                        message_channel = await self.bot.fetch_channel(int(record['ChannelID']))
                        await message_channel.send(str(record['Announcement']))
                        self.records[index]['Posted'] = 'TRUE'
                        announcement_row = self.worksheet.find(str(record['Announcement ID'])).row
                        self.worksheet.update_cell(row=announcement_row, col=5, value='TRUE')
            except ValueError:
                pass


def setup(bot):
    bot.add_cog(SendCog(bot))
