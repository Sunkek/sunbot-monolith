"""Embed creator and formatter"""

import discord
from discord.ext import commands

from typing import Optional

def check_perm_kick(ctx):
    return ctx.author.guild_permissions.kick_members

def check_junior(ctx):
    junior = ctx.bot.settings.get(ctx.guild.id, {})\
        .get("rank_junior_mod_role_id")
    return junior in [i.id for i in ctx.author.id.roles]
    
def check_senior(ctx):
    senior = ctx.bot.settings.get(ctx.guild.id, {})\
        .get("rank_senior_mod_role_id")
    return senior in [i.id for i in ctx.author.id.roles]

def check_admin(ctx):
    admin = ctx.bot.settings.get(ctx.guild.id, {})\
        .get("rank_admin_role_id")
    return admin in [i.id for i in ctx.author.id.roles]


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
        junior = self.bot.settings.get(message.guild.id, {})\
            .get("rank_junior_mod_role_id")
        senior = self.bot.settings.get(message.guild.id, {})\
            .get("rank_senior_mod_role_id")
        admin = self.bot.settings.get(message.guild.id, {})\
            .get("rank_admin_role_id")
        if admin in [i.id for i in ctx.author.roles]:
            # Unfinished
            pass

    @commands.check_any(check_perm_kick, check_junior, check_senior, check_admin)
    @commands.command(
        name="kick", 
        brief="Kicks the target member",
        help="Kicks the target member (by mention or ID). Only usable by mods and/or those with kick permissions. You can also specify the reason",
    )
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason)


def setup(bot):
    bot.add_cog(Moderation(bot))