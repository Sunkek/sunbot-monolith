"""Setting util for advertising reminder system"""

from datetime import datetime, timedelta
from asyncio import sleep

import discord
from discord.ext import tasks, commands

from utils import util_users, utils


class Actualizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.actualize.start()

    def cog_unload(self):
        self.actualize.cancel()
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Give the verified role if they passed the discord verification
        if before.pending != after.pending:
            verification = self.bot.settings.get(
                after.guild.id, {}
            ).get("rank_basic_member_role_verification", False)
            if verification:
                role = self.bot.settings.get(
                    after.guild.id, {}
                ).get("rank_basic_member_role_id")
                await after.add_roles(after.guild.get_role(role))
                # Send the prepared welcome message, if there is any
                channel = self.bot.settings.get(after.guild.id, {}).get("welcome_message_channel_id", 0)
                text = self.bot.settings.get(after.guild.id, {}).get("verification_message_text")
                embed = self.bot.settings.get(after.guild.id, {}).get("verification_message_embed")
                channel = after.guild.get_channel(channel)
                if channel and (text or embed):
                    await utils.send_welcome_or_leave(channel, text, embed, after)

    @tasks.loop(hours=24.0)
    async def actualize(self):
        """Promote or demote the members according 
        to their activity and join date"""
        for guild, settings in self.bot.settings.items():
            # Grab the roles and their requirements
            guild = self.bot.get_guild(guild)
            base_member = settings.get("rank_basic_member_role_id")
            base_member = guild.get_role(base_member)
            active_member = settings.get("rank_active_member_role_id")
            active_member = guild.get_role(active_member)
            active_member_days = settings.get("rank_active_member_required_days")
            active_member_activity = settings.get("rank_active_member_required_activity")
            junior_mod = settings.get("rank_junior_mod_role_id")
            junior_mod = guild.get_role(junior_mod)
            junior_mod_days = settings.get("rank_junior_mod_required_days")
            junior_mod_activity = settings.get("rank_junior_mod_required_activity")
            senior_mod = settings.get("rank_senior_mod_role_id")
            senior_mod = guild.get_role(senior_mod)
            admin = settings.get("rank_admin_role_id")
            admin = guild.get_role(admin)
            # Fetch the list of members eligible for each rank by their activity
            active_member_eligible = await util_users.fetch_users_by_days_and_activity(
                self.bot, guild, active_member_days, active_member_activity
            )
            active_member_eligible = [i[0] for i in active_member_eligible]
            junior_mod_eligible = await util_users.fetch_users_by_days_and_activity(
                self.bot, guild, junior_mod_days, junior_mod_activity
            )
            junior_mod_eligible = [i[0] for i in junior_mod_eligible]
            # Iterate over all members to edit their roles
            for member in [i for i in guild.members if not i.bot]:
                # Admin check
                if admin in member.roles:
                    continue
                # Senior mod check
                elif senior_mod in member.roles:
                    continue
                # Junior mod check
                elif junior_mod in member.roles:
                    if member.id not in junior_mod_eligible:
                        await member.remove_roles(junior_mod)
                        await member.add_roles(active_member)
                # Active member check
                elif active_member in member.roles:
                    if member.id not in active_member_eligible:
                        await member.remove_roles(active_member)
                        await member.add_roles(base_member)
                # Base member check
                elif base_member in member.roles:
                    if member.id in active_member_eligible:
                        await member.add_roles(active_member)

    '''@actualize.before_loop
    async def before_actualize(self):
        """Sleeping until the full hour"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())'''

def setup(bot):
    bot.add_cog(Actualizer(bot))
