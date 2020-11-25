"""Embed creator and formatter"""

from typing import Optional
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
import asyncio

from utils import util_moderation

def check_perm_kick(ctx):
    return ctx.author.guild_permissions.kick_members

def check_junior(ctx):
    junior = ctx.bot.settings.get(ctx.guild.id, {})\
        .get("rank_junior_mod_role_id")
    return junior in [i.id for i in ctx.author.roles]
    
def check_senior(ctx):
    senior = ctx.bot.settings.get(ctx.guild.id, {})\
        .get("rank_senior_mod_role_id")
    return senior in [i.id for i in ctx.author.roles]

def check_admin(ctx):
    admin = ctx.bot.settings.get(ctx.guild.id, {})\
        .get("rank_admin_role_id")
    return admin in [i.id for i in ctx.author.roles]

def member_rank(bot, guild_id, member):
    if not hasattr(member, "roles"):
        return 0
    junior = bot.settings.get(guild_id, {})\
        .get("rank_junior_mod_role_id")
    senior = bot.settings.get(guild_id, {})\
        .get("rank_senior_mod_role_id")
    admin = bot.settings.get(guild_id, {})\
        .get("rank_admin_role_id")
    member_roles = [i.id for i in member.roles]
    if admin in member_roles: return 3
    elif senior in member_roles: return 2
    elif junior in member_roles: return 1
    else: return 0

def can_affect(bot, guild_id, member1, member2):
    member1 = member_rank(bot, guild_id, member1)
    member2 = member_rank(bot, guild_id, member2)
    return member1 > member2


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hierarchy = {
            "rank_junior_mod_role_id": 1,
            "rank_senior_mod_role_id": 2,
            "rank_admin_role_id": 3,
        }
        self.unmuter.start()

    def cog_unload(self):
        self.unmuter.cancel()

    @commands.check_any(
        commands.check(check_junior),
        commands.check(check_senior),
        commands.check(check_admin),
    )
    @commands.command(
        name="mute", 
        brief="Mutes the target member",
        help="Mutes the target member (by mention or ID) for specified amount of hours or indefinitely - until someone unmutes them. Only usable by mods. Only works if there's a mute role set for this server!",
    )
    async def mute(self, ctx, member: discord.Member, hours=0):
        if can_affect(self.bot, ctx.guild.id, ctx.author, member):
            mute_role = self.bot.settings.get(ctx.guild.id, {})\
                .get("rank_mute_role_id")
            mute_role = ctx.guild.get_role(mute_role)
            await member.add_roles(mute_role)
            if not mute_role:
                raise commands.RoleNotFound(mute_role)
            if hours:
                await util_moderation.mute(
                    self.bot, ctx.guild.id, member.id, hours
                )
        else:
            raise commands.MissingPermissions(("higher rank than the target",))

    @commands.check_any(
        commands.check(check_junior),
        commands.check(check_senior),
        commands.check(check_admin),
    )
    @commands.command(
        name="unmute", 
        brief="Unmutes the target member",
        help="Unmutes the target member (by mention or ID). Only usable by mods. Only works if there's a mute role set for this server!",
    )
    async def unmute(self, ctx, member: discord.Member):
        if can_affect(self.bot, ctx.guild.id, ctx.author, member):
            mute_role = self.bot.settings.get(ctx.guild.id, {})\
                .get("rank_mute_role_id")
            mute_role = ctx.guild.get_role(mute_role)
            await member.remove_roles(mute_role)
            await util_moderation.unmute(
                self.bot, ctx.guild.id, member.id
            )
        else:
            raise commands.MissingPermissions(("higher rank than the target",))
    
    @commands.check_any(
        commands.check(check_junior),
        commands.check(check_senior),
        commands.check(check_admin),
    )
    @commands.command(
        name="kick", 
        brief="Kicks the target member",
        help="Kicks the target member (by mention or ID). Only usable by mods. You can also specify the reason",
    )
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if can_affect(self.bot, ctx.guild.id, ctx.author, member):
            await member.kick(reason=reason)
        else:
            raise commands.MissingPermissions(("higher rank than the target",))

    @commands.check_any(
        commands.check(check_senior),
        commands.check(check_admin),
    )
    @commands.command(
        name="ban", 
        brief="Bans the target member",
        help="Bans the target member (by mention or ID). Only usable by mods. You can specify how many days of target member's messages must be purged (up to 7). You can also specify the reason",
    )
    async def ban(
        self, ctx, member: discord.Member, days: Optional[int]=0, *, reason=None
    ):
        days = max(0, min(days, 7))
        if can_affect(self.bot, ctx.guild.id, ctx.author, member):
            await member.ban(reason=reason, delete_message_days=days)
        else:
            raise commands.MissingPermissions(("higher rank than the target",))

    @commands.check_any(
        commands.check(check_senior),
        commands.check(check_admin),
    )
    @commands.command(
        name="unban", 
        brief="Unbans the target user",
        help="Unbans the target user (by mention or ID). Only usable by mods. You can also specify the reason",
    )
    async def unban(
        self, ctx, member: discord.User, *, reason=None
    ):
        if can_affect(self.bot, ctx.guild.id, ctx.author, member):
            await ctx.guild.unban(member, reason=reason)
        else:
            raise commands.MissingPermissions(("higher rank than the target",))
        
    @tasks.loop(minutes=5.0)
    async def unmuter(self):
        members_to_umnute = await fetch_for_unmute(self.bot)
        # Get the guids, members and mute role objects
        for guild_id, user_id in members_to_umnute:
            mute_role_id = self.bot.settings.get(guild_id, {})\
                .get("rank_mute_role_id")
            guild = self.bot.get_guild(guild_id)
            member = guild.get_member(user_id)
            role = guild.get_role(mute_role_id)
            # Remove the mute roles
            await member.remove_roles(role)

    @unmuter.before_loop
    async def before_unmuter(self):
        """Sleeping until the full minute"""
        await self.bot.wait_until_ready()
        await asyncio.sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_minute = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
        await asyncio.sleep((next_minute - now).total_seconds())

def setup(bot):
    bot.add_cog(Moderation(bot))