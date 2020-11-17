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
        brief="Sets message tracking on or off",
        help="Switches message tracking on or off. It will save info about who posted and how much"
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
        brief="Sets reaction tracking on or off",
        help="Switches reaction tracking on or off. It will save who reacted, with what emoji and to whose message"
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
        brief="Sets voice tracking on or off",
        help="Switches voice tracking on or off. It will save who talked in voice with how many other members"
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
        brief="Sets games tracking on or off",
        help="Switches games tracking on or off. It will save who played what"
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