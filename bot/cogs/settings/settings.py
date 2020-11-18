import discord
from discord.ext import commands
from typing import Optional

from utils import util_settings


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="showsettings", 
        aliases=['settings', 'checksettings', 'ss'],
        brief="Shows current settings for this server",
        help="Shows current settings for this server"
    )
    async def showsettings(self, ctx, search: str=""):
        settings = self.bot.settings.get(ctx.guild.id, {})
        if not search:
            activity = util_settings.format_settings(
                settings, ctx, include=["activity_"], ignore=[]
            )
            ranks = util_settings.format_settings(
                settings, ctx, include=["rank_"], ignore=[]
            )
            trackers = util_settings.format_settings(
                settings, ctx, include=["track_"], ignore=[]
            )
            ad_reminder = util_settings.format_settings(
                settings, ctx, include=["ad_reminder_"], ignore=[]
            )
            verification = util_settings.format_settings(
                settings, ctx, include=["verification_"], ignore=[]
            )
            welcome = util_settings.format_settings(
                settings, ctx, include=["welcome_", "leave_"], ignore=[]
            )
            desc = util_settings.format_settings(
                settings, ctx, include=[], ignore=[
                    "track_", "activity_", "ad_reminder_", "verification_", 
                    "welcome_", "leave_", "rank_"
                ],
            )
            embed = discord.Embed(
                title=f"Current{} settings for {ctx.guild.name}",
                color=ctx.author.color,
                description=desc or "No custom settings yet!"
            )
            if activity: embed.add_field(name="Activity", value=activity)
            if ranks: embed.add_field(name="Ranks", value=ranks)
            if trackers: embed.add_field(name="Trackers", value=trackers)
            if ad_reminder: embed.add_field(name="Ad Reminder", value=ad_reminder)
            if verification: embed.add_field(name="Verification", value=verification)
            if welcome: embed.add_field(name="Welcome/Leave", value=welcome)
        else:
            desc = util_settings.format_settings(
                settings, ctx, include=search, ignore=[]
            )
            embed = discord.Embed(
                title=f"Current `{search}` settings for {ctx.guild.name}",
                color=ctx.author.color,
                description=desc or "Nothing found!"
            )

        await ctx.send(embed=embed)
                       

def setup(bot):
    bot.add_cog(Settings(bot))