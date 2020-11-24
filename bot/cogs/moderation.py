"""Embed creator and formatter"""

import discord
from discord.ext import commands

from typing import Optional

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

    @commands.has_permissions(kick_members=True)
    @commands.command(
        name="mute", 
        brief="Mutes the target member",
        help="Mutes the target member (by mention or ID) for specified amount of hours or indefinitely - until someone unmutes them. Only usable by mods and those with kick permissions",
    )
    async def mute(self, ctx, member: discord.Member, hours=0):
        if can_affect(self.bot, ctx.guild.id, ctx.author, member):
            # Unfinished
            pass
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

def setup(bot):
    bot.add_cog(Moderation(bot))