"""Initial settings loadup"""

import discord
from discord.ext import commands


class SettingsInitial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings on_ready triggered")
    


def setup(bot):
    bot.add_cog(Settings(bot))