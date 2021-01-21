"""Automated server staff votes"""

from datetime import datetime, timedelta
from asyncio import sleep

import discord
from discord.ext import tasks, commands

from utils import util_users


class Votes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.votes.start()

    def cog_unload(self):
        self.votes.cancel()

    @tasks.loop(hours=24.0)
    async def votes(self):
        """Run the votes for server staff"""
        for guild, settings in self.bot.settings.items():
            now = datetime.now()
            guild = self.bot.get_guild(guild)
            vote_channel = guild.get_channel(settings.get("vote_channel_id"))
            if not vote_channel: continue

            active_member = guild.get_role(settings.get("rank_active_member_role_id"))
            junior_mod = guild.get_role(settings.get("rank_junior_mod_role_id"))
            # Determine which votes trigger

            # JM vote
            junior_mod_vote_day = settings.get("vote_junior_mod_day")
            junior_mod_vote_months = settings.get("vote_junior_mod_months")
            junior_mod_vote_limit = settings.get("vote_junior_mod_limit")
            if now.day == junior_mod_vote_day and \
                now.month in junior_mod_vote_months:
                print("Junior mod vote start!")
                junior_mod_days = settings.get("rank_junior_mod_required_days")
                junior_mod_activity = settings.get("rank_junior_mod_required_activity")
                # Find eligible members    
                members = await util_users.fetch_users_by_days_and_activity(
                    self.bot, guild, junior_mod_days, junior_mod_activity
                )
                # Post a list of them to the vote channel
                e = discord.Embed(
                    title=f"Junior mod vote start {now.year}/{now.month}",
                    description="\n".join(m.mention for m in members),
                    color=guild.me.color
                )
                e.add_field(
                    name="Terms",
                    value=(
                        "The vote is anonymous. React to this message with ☑️ to receive your form.\n"
                        "It's possible to get promoted, demoted or keep your rank.\n"
                        "Make sure to vote for yourself if you want to get promoted.\n"
                        "Only memebers with at least 25% of max upvotes get promoted.\n"
                        f"The max number of {junior_mod.mention} that can be vote-picked is {junior_mod_vote_limit}.\n"
                        f"Only members with {active_member.mention} role can vote here."
                    )
                )
                vote_msg = await vote_channel.send(embed=e)
                await vote_msg.add_reaction("☑️")
                # DM eligible voters the bulletins
            elif now.day == junior_mod_vote_day + 5 and \
                now.month in junior_mod_vote_months:
                print("Junior mod vote end!")
                # Count the votes
                # Declare the results and implement them
            
            # SM vote
            senior_mod_vote_day = settings.get("vote_senior_mod_day")
            senior_mod_vote_months = settings.get("vote_senior_mod_months")
            if now.day == senior_mod_vote_day and \
                now.month in senior_mod_vote_months:
                print("Senior mod vote start!")
                # Find eligible members    
                # Post a list of them to the vote channel
                # DM eligible voters the bulletins
            elif now.day == senior_mod_vote_day + 5 and \
                now.month in senior_mod_vote_months:
                print("Senior mod vote end!")
                # Count the votes
                # Declare the results and implement them
            
            # A vote
            admin_vote_day = settings.get("vote_admin_day")
            admin_vote_months = settings.get("vote_admin_months")
            if now.day == admin_vote_day and \
                now.month in admin_vote_months:
                print("Admin vote start!")
                # Find eligible members    
                # Post a list of them to the vote channel
                # DM eligible voters the bulletins
            elif now.day == admin_vote_day + 5 and \
                now.month in admin_vote_months:
                print("Admin vote end!")
                # Count the votes
                # Declare the results and implement them
    
    # Enable this when the cog is functional
    '''@votes.before_loop
    async def before_votes(self):
        """Sleeping until the given time"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())'''


def setup(bot):
    bot.add_cog(Votes(bot))
