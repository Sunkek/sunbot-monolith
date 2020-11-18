"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from discord.ext.commands import Greedy
from typing import Union

from utils import util_settings


class SetActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
               
    @commands.command(
        name="setactivitypermessage", 
        aliases=["sapm"],
        brief="Sets base activity per message",
        help="Sets the amount of activity points members get for each message. Max is `100`",
    )
    async def setactivitypermessage(self, ctx, activity: int=0):
        if activity > 100 or activity < 0:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_message=activity,
        )
               
    @commands.command(
        name="setactivityminmessagewords", 
        aliases=["sammw"],
        brief="Sets minimum words for activity",
        help="Sets the minimum amount of words required for a message to reward activity points. Max `20`",
    )
    async def setactivityminmessagewords(self, ctx, words: int=0):
        if words > 20 or words < 0:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_min_message_words=words,
        )

    @commands.command(
        name="setactivitymultiplierperword", 
        aliases=["sampw"],
        brief="Sets multiplier per word",
        help="Each message activity points will be multiplied for this value as many times as there are words in the message. Min `1`, max `1.5`",
    )
    async def setactivitymultiplierperword(self, ctx, multiplier: float=1):
        if multiplier > 1.5 or multiplier < 1:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_multi_per_word=multiplier,
        )

    @commands.command(
        name="setactivityperattachment", 
        aliases=["sapa"],
        brief="Sets activity for attachment",
        help="Sets the amount of activity points rewarded for sent attachments. Max `300`",
    )
    async def setactivityperattachment(self, ctx, activity: int=0):
        if activity > 300 or activity < 0:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_attachment=activity,
        )

    @commands.command(
        name="setactivitycooldown", 
        aliases=["sacd"],
        brief="Sets amount of time between activity rewards",
        help="Sets the amount of seconds that must pass between activity point rewards for each member. Max `3600` (1 hour)",
    )
    async def setactivitycooldown(self, ctx, seconds: int=0):
        if seconds > 3600 or seconds < 0:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_cooldown=seconds,
        )

    @commands.command(
        name="setactivityperreaction", 
        aliases=["sapr"],
        brief="Sets activity for reaction",
        help="Sets the amount of activity points rewarded for given reactions. Max `100`",
    )
    async def setactivityperreaction(self, ctx, activity: int=0):
        if activity > 100 or activity < 0:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_reaction=activity,
        )

    @commands.command(
        name="setactivitypervoiceminute", 
        aliases=["sapvm"],
        brief="Sets activity for a minute in voice",
        help="Sets the amount of activity points rewarded for a minute in voice chat. Loners in voice don't get points. Max `100`",
    )
    async def setactivitypervoiceminute(self, ctx, activity: int=0):
        if activity > 100 or activity < 0:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_voice_minute=activity,
        )

    @commands.command(
        name="setactivitymultiplierpervoicemember", 
        aliases=["sampvm"],
        brief="Sets multiplier per member in voice",
        help="Each voice activity points will be multiplied for this value as many times as there are members in the chat. Min `1`, max `1.5`",
    )
    async def setactivitymultiplierpervoicemember(self, ctx, multiplier: float=1):
        if multiplier > 1.5 or multiplier < 1:
            raise commands.BadArgument
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_multi_per_voice_member=multiplier,
        )
        
    @commands.command(
        name="setactivitychannelx0", 
        aliases=["sac0"],
        brief="Switch channels to/from x0 activity multiplier",
        help="Add or remove the selected channel(s) to/from the list of channels which reward no activity points. You can mention text channels or use their IDs, but for voice channels it's only IDs",
    )
    async def setactivitychannelx0(
        self, ctx, channels:Greedy[Union[discord.TextChannel, int]]
    ):
        targets = [ch.id if type(ch) != int else ch for ch in channels]
        await util_settings.change_guild_setting_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="activity_channels_x0",
            targets=targets,
        )
        
    @commands.command(
        name="setactivitychannelx05", 
        aliases=["sac05"],
        brief="Switch channels to/from x0.5 activity multiplier",
        help="Add or remove the selected channel(s) to/from the list of channels which reward 1/2 of all activity points. You can mention text channels or use their IDs, but for voice channels it's only IDs",
    )
    async def setactivitychannelx05(
        self, ctx, channels:Greedy[Union[discord.TextChannel, int]]
    ):
        targets = [ch.id if type(ch) != int else ch for ch in channels]
        await util_settings.change_guild_setting_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="activity_channels_x05",
            targets=targets,
        )
        
    @commands.command(
        name="setactivitychannelx2", 
        aliases=["sac2"],
        brief="Switch channels to/from x2 activity multiplier",
        help="Add or remove the selected channel(s) to/from the list of channels which reward double activity points. You can mention text channels or use their IDs, but for voice channels it's only IDs",
    )
    async def setactivitychannelx2(
        self, ctx, channels:Greedy[Union[discord.TextChannel, int]]
    ):
        targets = [ch.id if type(ch) != int else ch for ch in channels]
        await util_settings.change_guild_setting_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="activity_channels_x2",
            targets=targets,
        )
        

def setup(bot):
    bot.add_cog(SetActivity(bot))