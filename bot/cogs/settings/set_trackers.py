import discord
from discord.ext import commands
from typing import Optional

from utils import util_settings

class SetTrackers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
        
    @commands.command(
        name="settrackmessages", 
        aliases=["stm"],
        description="Sets message tracking on or off.",
    )
    async def settrackmessages(self, ctx):
        value = not self.bot.settings\
            .get(ctx.guild.id, {}).get("track_messages", False)
        await settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            track_messages=value,
        )
        

def setup(bot):
    bot.add_cog(SetTrackers(bot))