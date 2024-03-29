"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from discord.ext.commands import Greedy
from typing import Optional

from utils import util_settings


class SetRanks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
        
    @commands.command(
        name="setmuterole", 
        aliases=["smr",],
        brief="Sets up the mute role",
    )
    async def setmuterole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_mute_role_id=role.id if role else None,
        )

    @commands.group(
        name="setbasicmemberrole", 
        aliases=["sbmr",],
        invoke_without_command=True,
        brief="Sets up the basic member role",
        help="Sets up the basic member role. To give this role to all joining members, type `setbasicmemberrole auto`",
    )
    async def setbasicmemberrole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_basic_member_role_id=role.id if role else None,
        )

    @setbasicmemberrole.command(
        name="auto", 
        aliases=["a",],
        brief="Switches auto-assigning this role",
        help="Switches auto-assigning this role to all joining members on or off.",
    )
    async def setbasicmemberrole_auto(self, ctx):
        # Check if the basic member sole is set
        basic_member = self.bot.settings\
            .get(ctx.guild.id, {}).get("rank_basic_member_role_id")
        if not basic_member:
            e = discord.Embed(
                title="No basic member role set!",
                description="Set the basic member role first!",
                color=ctx.author.color,
            )
            return await ctx.send(embed=e)
        value = not self.bot.settings\
            .get(ctx.guild.id, {}).get("rank_basic_member_role_auto", False)
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_basic_member_role_auto=value,
        )

    @setbasicmemberrole.command(
        name="verification", 
        aliases=["v",],
        brief="Switches assigning this role passing discord verification",
        help="Switches assigning this role on member passing discord verification to all joining members on or off.",
    )
    async def setbasicmemberrole_verification(self, ctx):
        # Check if the basic member sole is set
        basic_member = self.bot.settings\
            .get(ctx.guild.id, {}).get("rank_basic_member_role_id")
        if not basic_member:
            e = discord.Embed(
                title="No basic member role set!",
                description="Set the basic member role first!",
                color=ctx.author.color,
            )
            return await ctx.send(embed=e)
        value = not self.bot.settings\
            .get(ctx.guild.id, {}).get("rank_basic_member_role_verification", False)
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_basic_member_role_verification=value,
        )

    @commands.group(
        name="setactivememberrole", 
        aliases=["samr",],
        invoke_without_command=True,
        brief="Sets up the active member role",
        help="Sets up the active member role. This role is assigned to those who have enough activity points and were on the server long enough.",
    )
    async def setactivememberrole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_active_member_role_id=role.id if role else None,
        )

    @setactivememberrole.command(
        name="days", 
        aliases=["d",],
        brief="Sets up how many days on server is required",
        help="Sets up the amount of days a member must be on your server to have the active member role. Max 2 000",
    )
    async def setactivememberrole_days(self, ctx, days: int=0):
        if days > 2000 or days < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_active_member_required_days=days or None,
        )
        
    @setactivememberrole.command(
        name="activity", 
        aliases=["a",],
        brief="Sets up how much activity is required",
        help="Sets up the amount of average activity per day a member must get in the set required days or previous month to have the active member role. Max 30 000",
    )
    async def setactivememberrole_activity(self, ctx, activity: int=0):
        if activity > 30000 or activity < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_active_member_required_activity=activity,
        )
        
    @commands.group(
        name="setjuniormodrole", 
        aliases=["sjmr",],
        invoke_without_command=True,
        brief="Sets up the junior moderator role",
        help="Sets up the junior moderator role. This role is assigned through the votes to those who have enough activity points and were on the server long enough.",
    )
    async def setjuniormodrole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_junior_mod_role_id=role.id if role else None,
        )

    @setjuniormodrole.command(
        name="days", 
        aliases=["d",],
        brief="Sets up how many days on server is required",
        help="Sets up the amount of days a member must be on your server to have the junior oderator role. Max 2 000",
    )
    async def setjuniormodrole_days(self, ctx, days: int=0):
        if days > 2000 or days < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_junior_mod_required_days=days or None,
        )
        
    @setjuniormodrole.command(
        name="activity", 
        aliases=["a",],
        brief="Sets up how much activity is required",
        help="Sets up the amount of average activity per day a member must get in the set required days or previous month to have the junior oderator role. Max 30 000",
    )
    async def setjuniormodrole_activity(self, ctx, activity: int=0):
        if activity > 30000 or activity < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_junior_mod_required_activity=activity,
        )
        
    @commands.group(
        name="setseniormodrole", 
        aliases=["ssmr",],
        invoke_without_command=True,
        brief="Sets up the senior moderator role",
        help="Sets up the senior moderator role. This role is assigned through the votes to those who have enough activity points and were on the server long enough.",
    )
    async def setseniormodrole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_senior_mod_role_id=role.id if role else None,
        )

    @setseniormodrole.command(
        name="days", 
        aliases=["d",],
        brief="Sets up how many days on server is required",
        help="Sets up the amount of days a member must be on your server to have the senior oderator role. Max 2 000",
    )
    async def setseniormodrole_days(self, ctx, days: int=0):
        if days > 2000 or days < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_senior_mod_required_days=days or None,
        )
        
    @setseniormodrole.command(
        name="activity", 
        aliases=["a",],
        brief="Sets up how much activity is required",
        help="Sets up the amount of average activity per day a member must get in the set required days or previous month to have the senior oderator role. Max 30 000",
    )
    async def setseniormodrole_activity(self, ctx, activity: int=0):
        if activity > 30000 or activity < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_senior_mod_required_activity=activity,
        )
        
    @commands.group(
        name="setadminrole", 
        aliases=["sar",],
        invoke_without_command=True,
        brief="Sets up the senior moderator role",
        help="Sets up the senior moderator role. This role is assigned through the votes to those who have enough activity points and were on the server long enough.",
    )
    async def setadminrole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_admin_role_id=role.id if role else None,
        )

    @setadminrole.command(
        name="days", 
        aliases=["d",],
        brief="Sets up how many days on server is required",
        help="Sets up the amount of days a member must be on your server to have the senior oderator role. Max 2 000",
    )
    async def setadminrole_days(self, ctx, days: int=0):
        if days > 2000 or days < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_admin_required_days=days or None,
        )
        
    @setadminrole.command(
        name="activity", 
        aliases=["a",],
        brief="Sets up how much activity is required",
        help="Sets up the amount of average activity per day a member must get in the set required days or previous month to have the senior oderator role. Max 30 000",
    )
    async def setadminrole_activity(self, ctx, activity: int=0):
        if activity > 30000 or activity < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_admin_required_activity=activity,
        )


def setup(bot):
    bot.add_cog(SetRanks(bot))