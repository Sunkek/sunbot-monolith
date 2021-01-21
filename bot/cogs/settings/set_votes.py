"""Setting util for rank vote settings"""

import discord
from discord.ext import commands
from discord.ext.commands import Greedy
from typing import Optional

from utils import util_settings


class SetVotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="setvotechannel", 
        aliases=["svc"],
        brief="Set up a channel for votes",
        help="Sets up the specified channel as vote feed. To reset, provide no channel",
    )
    async def setvotechannel(self, ctx, channel: discord.TextChannel=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_channel_id=channel.id if channel else None,
        )

    @commands.command(
        name="setjuniormodvotemonths", 
        aliases=["sjmvm",],
        brief="Sets up the months of junior mod votes",
        help="Sets up the months of junior mod votes. Pass a sequence of numbers from 1 to 12 to select the months. It will add or remove the specified months",
    )
    async def setjuniormodvotemonths(self, ctx, months: Greedy[int]):
        for month in months:
            if month < 1 or month > 12:
                raise commands.BadArgument
        await util_settings.change_guild_setting_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="vote_junior_mod_months",
            targets=months,
        )
        
    @commands.command(
        name="setjuniormodvoteday", 
        aliases=["sjmvd",],
        brief="Sets up the day of junior mod votes",
        help="Sets up the day of junior mod votes. Pass a number from 1 to 20 (yes, 20). The vote will start on the specified day and end 5 days later.",
    )
    async def setjuniormodvoteday(self, ctx, day: int):
        if day < 1 or day > 20:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_junior_mod_day=day,
        )        
        
    @commands.command(
        name="setjuniormodvotelimit", 
        aliases=["sjmvl",],
        brief="Sets up the limit for junior mods",
        help="Sets up the limit for max amount of vote-picked junior mods. Pass a number from 1 to 50.",
    )
    async def setjuniormodvotelimit(self, ctx, limit: int):
        if limit < 1 or limit > 50:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_junior_mod_limit=limit,
        )     

    @commands.command(
        name="setseniormodvotemonths", 
        aliases=["ssmvm",],
        brief="Sets up the months of senior mod votes",
        help="Sets up the months of senior mod votes. Pass a sequence of numbers from 1 to 12 to select the months. It will add or remove the specified months",
    )
    async def setseniormodvotemonths(self, ctx, months: Greedy[int]):
        for month in months:
            if month < 1 or month > 12:
                raise commands.BadArgument
        await util_settings.change_guild_setting_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="vote_senior_mod_months",
            targets=months,
        )
                
    @commands.command(
        name="setseniormodvoteday", 
        aliases=["ssmvd",],
        brief="Sets up the day of senior mod votes",
        help="Sets up the day of senior mod votes. Pass a number from 1 to 20 (yes, 20). The vote will start on the specified day and end 5 days later.",
    )
    async def setseniormodvoteday(self, ctx, day: int):
        if day < 1 or day > 20:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_senior_mod_day=day,
        )      

    @commands.command(
        name="setseniormodvotelimit", 
        aliases=["ssmvl",],
        brief="Sets up the limit for senior mods",
        help="Sets up the limit for max amount of vote-picked senior mods. Pass a number from 1 to 50.",
    )
    async def setseniormodvotelimit(self, ctx, limit: int):
        if limit < 1 or limit > 50:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_senior_mod_limit=limit,
        )     
        
    @commands.command(
        name="setadminvotemonths", 
        aliases=["savm",],
        brief="Sets up the months of admin votes",
        help="Sets up the months of admin votes. Pass a sequence of numbers from 1 to 12 to select the months. It will add or remove the specified months",
    )
    async def setadminvotemonths(self, ctx, months: Greedy[int]):
        for month in months:
            if month < 1 or month > 12:
                raise commands.BadArgument
        await util_settings.change_guild_setting_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="vote_admin_months",
            targets=months,
        )
                
    @commands.command(
        name="setadminvoteday", 
        aliases=["savd",],
        brief="Sets up the day of admin votes",
        help="Sets up the day of admin mod votes. Pass a number from 1 to 20 (yes, 20). The vote will start on the specified day and end 5 days later.",
    )
    async def setadminvoteday(self, ctx, day: int):
        if day < 1 or day > 20:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_admin_day=day,
        )       

    @commands.command(
        name="setadminvotelimit", 
        aliases=["savl",],
        brief="Sets up the limit for admins",
        help="Sets up the limit for max amount of vote-picked admins. Pass a number from 1 to 50.",
    )
    async def setadminsvotelimit(self, ctx, limit: int):
        if limit < 1 or limit > 50:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            vote_admins_limit=limit,
        )     


def setup(bot):
    bot.add_cog(SetVotes(bot))