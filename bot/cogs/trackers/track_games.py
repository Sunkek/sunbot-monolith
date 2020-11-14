"""This cog stores messages to the database and does various
activity statistics tracking. Mostly made for APoC."""

import discord
from discord.ext import commands
from datetime import date, datetime

from utils import util_trackers

class TrackGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}
        self.ignore = ("scrivener", "youtube", "spotify", "foobar2000")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Activity changed, not bot, setting on
        try:
            if all((
                before.activities != after.activities,
                not after.bot,
                self.bot.settings.get(after.guild.id, {}).get("track_games")
            )):
                before_game = None
                after_game = None
                # Getting the game before the member changed his activity
                for activity in before.activities:
                    if all((
                        activity.type == discord.ActivityType.playing,
                        hasattr(activity, "application_id")
                    )):
                        before_game = activity
                        break
                # Getting the game after the member changed his activity
                for activity in after.activities:
                    if all((
                        activity.type == discord.ActivityType.playing,
                        hasattr(activity, "application_id")
                    )):
                        after_game = activity
                        break
                print(before_game)
                print(after_game)
                # If started playing
                if after_game and not before_game:
                    if after_game.name.lower() not in self.ignore:
                        self.sessions[before.id] = (
                            after_game.name, 
                            datetime.utcnow()
                        )
                print(self.sessions)
                # If done playing
                elif not after_game and before_game:
                    game = self.sessions.pop(after.id, (None,))
                    if before_game.name == game[0]:
                        played = int((datetime.utcnow()-game[1]).total_seconds())
                        if played > 0:
                            print(game, duration)
                            await util_trackers.add_game(
                                self.bot, 
                                user_id=before.id,
                                game=game[0],
                                duration=played,
                                period=date.today()
                            )
        except Exception as e:
            print(e)
            print(type(e))

def setup(bot):
    bot.add_cog(TrackGames(bot))