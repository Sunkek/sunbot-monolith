"""This cog stores messages to the database and does various
activity statistics tracking. Mostly made for APoC."""

import discord
from discord.ext import commands
from datetime import date

from utils import util_trackers

class TrackMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # I don't want to save info about DMs and webhooks
        if message.guild and message.guild.get_member(message.author.id) and \
            not message.author.bot:
            
            if self.bot.settings.get(message.guild.id, {})\
                .get("track_messages", False):

                await trackers.add_message(
                    self.bot, 
                    guild_id=message.guild.id,
                    channel_id=message.channel.id,
                    user_id=message.author.id,
                    postcount=1,
                    attachments=len(message.attachments),
                    words=len(message.content.split()),
                    period=date.today()
                )        

def setup(bot):
    bot.add_cog(TrackMessages(bot))