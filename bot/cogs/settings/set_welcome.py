"""Setting util for uncategorizable things"""
import json

import discord
from discord.ext import commands
from typing import Optional

from utils import util_settings, utils


class SetWelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
        
    @commands.command(
        name="setwelcomechannel", 
        aliases=["swc"],
        brief="Set welcome, leave and verification messages channel",
        help="Sets up the channel where welcome, verification and leave messages will be sent.",
    )
    async def setwelcomechannel(
        self, ctx, 
        channel:Optional[discord.TextChannel]=None
    ):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_message_channel_id=channel.id if channel else None,
        )

    @commands.command(
        name="setwelcomemessage", 
        aliases=["swm"],
        brief="Sets up the welcome text",
        help=f"Sets up the welcome text message which is sent when a new member joins the server. Available placeholders:\n{utils.MESSAGE_PLACEHOLDERS}",
    )
    async def setwelcomemessage(self, ctx, text=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_message_text=text,
        )
        
    @commands.command(
        name="setwelcomeembed", 
        aliases=["swe"],
        brief="Sets up the welcome embed",
        help=f"Sets up the welcome embed which is sent when a new member joins the server. You should build a dummy embed with `Embedder` and then copy it with this command. Available placeholders:\n{utils.MESSAGE_PLACEHOLDERS}",
    )
    async def setwelcomeembed(
        self, ctx,
        channel: Optional[discord.TextChannel]=None, 
        message_id: Optional[int]=0
    ):
        channel = channel or ctx.channel
        message = await channel.fetch_message(message_id)
        embed = message.embeds[0].to_dict() if message.embeds else None
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_message_embed=json.dumps(embed),
        )
             
    @commands.command(
        name="setleavemessage", 
        aliases=["slm"],
        brief="Sets up the leave text",
        help=f"Sets up the leave text message which is sent when a member leaves the server. Available placeholders:\n{utils.MESSAGE_PLACEHOLDERS}",
    )
    async def setleavemessage(self, ctx, text=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            leave_message_text=text,
        )
        
    @commands.command(
        name="setleaveembed", 
        aliases=["sle"],
        brief="Sets up the leave embed",
        help=f"Sets up the leave embed which is sent when a member leaves the server. You should build a dummy embed with `Embedder` and then copy it with this command. Available placeholders:\n{utils.MESSAGE_PLACEHOLDERS}",
    )
    async def setleaveembed(
        self, ctx,
        channel: Optional[discord.TextChannel]=None, 
        message_id: Optional[int]=0
    ):
        channel = channel or ctx.channel
        message = await channel.fetch_message(message_id)
        embed = message.embeds[0].to_dict() if message.embeds else None
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            leave_message_embed=json.dumps(embed),
        )   

def setup(bot):
    bot.add_cog(SetWelcome(bot))