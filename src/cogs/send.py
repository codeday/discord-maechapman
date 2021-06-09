from datetime import datetime
from src.credentials import credentials

import gspread
from discord.ext import commands, tasks


class SendCog(commands.Cog, name="Send"):
    def __init__(self, bot):
        self.bot = bot
        self.records = []
        self.check.start()
        self.update.start()
        self.gc = gspread.service_account_from_dict(credentials)
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
        for index, self.record in enumerate(self.records):
            timestamp = datetime.today().strftime("%m/%d/%Y %H:%M")
            if self.record['Posted'] == 'FALSE':
                print(timestamp)
                if str(self.record['Time']) in timestamp:
                    message_channel = await self.bot.fetch_channel(int(self.record['ChannelID']))
                    await message_channel.send(str(self.record['Announcement']))
                    announcement_cell = self.worksheet.find(str(self.record['Announcement']))
                    announcement_row = announcement_cell.row
                    self.worksheet.update_cell(announcement_row, 5, "TRUE")


                continue


def setup(bot):
    bot.add_cog(SendCog(bot))
