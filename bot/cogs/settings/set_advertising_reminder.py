"""Setting util for advertising reminder system"""

import discord
from discord.ext import commands, tasks

from utils import util_settings

AD_PLATFORMS = [
    "disboard", "disforge", "discordme", "discordservers", "topgg", "top.gg"
]

class SetAdReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="setadreminderchannel", 
        aliases=["setadchannel", "sarc"],
        brief="Set up a channel for notifications",
        help="Sets up the specified channel as advertising reminder feed. To reset, provide no channel",
    )
    async def setadreminderchannel(self, ctx, channel: discord.TextChannel=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            ad_reminder_channel_id=channel.id if channel else None,
        )
              
    @commands.command(
        name="setadreminderrole", 
        aliases=["setadrole", "sarr"],
        brief="Sets up the role to ping on each remind",
        help="Sets up the role to ping on advertising reminder notifications",
    )
    async def setadreminderrole(self, ctx, role: discord.Role=None):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            ad_reminder_role_id=role.id if role else None,
        )
       
    @commands.command(
        name="adremind", 
        alises=["ar"],
        brief="Starts/stops advertising reminder",
        help=f"Starts or stops reminding to bump/post on the supported advertising platforms. They currently include: `{', '.join(AD_PLATFORMS)}`",
    )
    async def adremind(self, ctx, platform):
        platform = platform.lower()
        if platform not in AD_PLATFORMS:
            raise commands.BadArgument
        if platform == "disboard":
            value = not self.bot.settings\
                .get(ctx.guild.id, {}).get("ad_reminder_disboard", False)
            await util_settings.change_guild_setting(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_disboard=value,
            )
        elif platform == "disforge":    
            value = not self.bot.settings\
                .get(ctx.guild.id, {}).get("ad_reminder_disforge", False)
            await util_settings.change_guild_setting(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_disforge=value,
            )     
        elif platform == "discordme":
            value = not self.bot.settings\
                .get(ctx.guild.id, {}).get("ad_reminder_discordme", False)
            await util_settings.change_guild_setting(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_discordme=value,
            )
        elif platform == "discordservers":    
            value = not self.bot.settings\
                .get(ctx.guild.id, {}).get("ad_reminder_discordservers", False)
            await util_settings.change_guild_setting(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_discordservers=value,
            )
        elif platform in ("topgg", "top.gg"):     
            value = not self.bot.settings\
                .get(ctx.guild.id, {}).get("ad_reminder_topgg", False)
            await util_settings.change_guild_setting(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_topgg=value,
            )

def setup(bot):
    bot.add_cog(SetAdReminder(bot))
