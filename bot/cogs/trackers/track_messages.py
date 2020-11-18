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

                await util_trackers.add_message(
                    self.bot, 
                    guild_id=message.guild.id,
                    channel_id=message.channel.id,
                    user_id=message.author.id,
                    postcount=1,
                    attachments=len(message.attachments),
                    words=len(message.content.split()),
                    period=date.today()
                )   

            # Add activity points, if set
            min_words = self.bot.settings.get(message.guild.id, {})\
                .get("activity_min_message_words", 0) 
            words = len(message.content.split())
            if words < min_words:
                return
            per_word = self.bot.settings.get(message.guild.id, {})\
                .get("activity_multi_per_word", 1) 
            per_message = self.bot.settings.get(message.guild.id, {})\
                .get("activity_per_message", 0) 
            per_attachment = self.bot.settings.get(message.guild.id, {})\
                .get("activity_per_attachment", 0) 
            from_text = per_message * per_word**min(words-min_words, 100)
            from_attachments = per_attachment * len(message.attachments)
            if from_text or from_attachments:
                await util_trackers.add_activity(
                    self.bot, 
                    channel_id=message.channel.id,
                    from_text=from_text,
                    from_attachments=from_attachments,
                    period=date.today()
                )   

def setup(bot):
    bot.add_cog(TrackMessages(bot))