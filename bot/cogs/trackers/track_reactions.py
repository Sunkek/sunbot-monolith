"""This cog stores reactions to the database and does various
activity statistics tracking."""

import discord
from discord.ext import commands
from datetime import date
from emoji import UNICODE_EMOJI

from utils import util_trackers


class TrackReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignore_emoji = ["⏮️", "⏪", "⏩", "⏭️"]
    
    async def save_reaction(self, payload, count):
        # I don't want to save info about DMs with the bot
        if payload.guild_id:
            if self.bot.settings.get(payload.guild_id, {}).get("track_reactions"):
                guild = self.bot.get_guild(payload.guild_id)
                channel = guild.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                # Not the topchart scrollers please
                if message.embeds and str(payload.emoji) in self.ignore_emoji:
                    return
                giver = guild.get_member(payload.user_id)
                receiver = message.author
                if giver.bot or giver == receiver: 
                    return
                if str(payload.emoji) in UNICODE_EMOJI or str(payload.emoji) == "☑️":  # "☑️" isn't in UNICODE_EMOJI?
                    # Stripping skintones and other modifiers
                    try:
                        emoji = str(bytes(str(payload.emoji), "utf-8")[:4], "utf-8")[0]
                    except UnicodeDecodeError:
                        emoji = str(payload.emoji)
                else: 
                    # Just turn it into string
                    emoji = str(payload.emoji).split(":")
                    emoji = f"{emoji[0]}:_:{emoji[2]}"

                await util_trackers.add_reaction(
                    self.bot, 
                    guild_id=guild.id,
                    channel_id=channel.id,
                    giver_id=giver.id,
                    receiver_id=receiver.id,
                    emoji=emoji,
                    count=count,
                    period=date.today()
                )

        
    @commands.Cog.listener() 
    async def on_raw_reaction_add(self, payload):
        await self.save_reaction(payload, 1)

    @commands.Cog.listener() 
    async def on_raw_reaction_remove(self, payload):
        await self.save_reaction(payload, -1)
        

def setup(bot):
    bot.add_cog(TrackReactions(bot))