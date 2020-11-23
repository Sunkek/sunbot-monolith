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
    async def showsettings(self, ctx, *, search: str=""):
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
                title=f"Current settings for {ctx.guild.name}",
                color=ctx.author.color,
                description=desc or "No custom settings yet!"
            )
            # Sort by field value length for better looks
            fields = []
            fields.append(("Activity", activity))
            fields.append(("Ranks", ranks))
            fields.append(("Trackers", trackers))
            fields.append(("Ad Reminder", ad_reminder))
            fields = [i for i in fields if i[1]]
            fields = sorted(fields, key=lambda i: i[1])
            for i in fields:
                embed.add_field(name=i[0], value=i[1])
        else:
            desc = util_settings.format_settings(
                settings, ctx, 
                include=[search.lower().replace(" ", "_")], 
                ignore=[]
            )
            embed = discord.Embed(
                title=f"Current `{search}` settings for {ctx.guild.name}",
                color=ctx.author.color,
                description=desc or "Nothing found!"
            )

        await ctx.send(embed=embed)
                       

def setup(bot):
    bot.add_cog(Settings(bot))