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
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            track_messages=value,
        )
        
    @commands.command(
        name="settrackreactions", 
        aliases=["str"],
        description="Sets reaction tracking on or off.",
    )
    async def settrackreactions(self, ctx):
        value = not self.bot.settings\
            .get(ctx.guild.id, {}).get("track_reactions", False)
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            track_reactions=value,
        )

    @commands.command(
        name="settrackvoice", 
        aliases=["stv"],
        description="Sets voice tracking on or off.",
    )
    async def settrackvoice(self, ctx):
        value = not self.bot.settings\
            .get(ctx.guild.id, {}).get("track_voice", False)
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            track_voice=value,
        )

    @commands.command(
        name="settrackgames", 
        aliases=["stg"],
        description="Sets games tracking on or off.",
    )
    async def settrackgames(self, ctx):
        value = not self.bot.settings\
            .get(ctx.guild.id, {}).get("track_games", False)
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            track_games=value,
        )
        

def setup(bot):
    bot.add_cog(SetTrackers(bot))