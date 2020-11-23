"""This cog stores voice chat activity to the database and does various
activity statistics tracking."""

import discord
from discord.ext import commands, tasks
from datetime import date

from utils import util_trackers


class TrackVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_check.start()

    def cog_unload(self):
        self.voice_check.cancel()

    @tasks.loop(seconds=60) 
    async def voice_check(self):
        for guild in self.bot.guilds:
            if self.bot.settings.get(guild.id, {}).get("track_voice"):
                for channel in guild.voice_channels:
                    people = [i for i in channel.members if not i.bot]
                    for member in people:
                        await util_trackers.add_voice(
                            self.bot, 
                            guild_id=guild.id,
                            channel_id=channel.id,
                            user_id=member.id,
                            members=len(channel.members),
                            count=1,
                            period=date.today()
                        )
                        
                        # Add activity points, if set
                        if len(people) < 2:
                            continue
                        per_minute = self.bot.settings.get(guild.id, {})\
                            .get("activity_per_voice_minute", 0)
                        per_member = self.bot.settings.get(guild.id, {})\
                            .get("activity_multi_per_voice_member", 1)  
                        from_voice = per_minute * per_member ** (len(people) - 2)
                        if from_voice:
                            await util_trackers.add_activity(
                                self.bot, 
                                guild_id=guild.id,
                                channel_id=channel.id,
                                user_id=member.id,
                                period=date.today(),
                                from_voice=from_voice,
                            )   

def setup(bot):
    bot.add_cog(TrackVoice(bot))