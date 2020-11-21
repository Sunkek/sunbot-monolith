"""Setting util for advertising reminder system"""

from datetime import datetime, timedelta
from asyncio import sleep

import discord
from discord.ext import commands, tasks

AD_PLATFORMS = [
    "disboard", "disforge", "discordme", "discordservers", "topgg", "top.gg"
]


class SetAdReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ad_reminder.start()
        self.d_bumped = dict()

    def cog_unload(self):
        self.ad_reminder.cancel()

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 302050872383242240:
            if "Bump done" in message.embeds[0].description:
                if self.bot.settings.get(message.guild.id, {})\
                    .get("ad_reminder_disboard", False):

                    self.d_bumped[message.guild.id] = datetime.now()
                    await sleep(60*60*2)
                    embed = discord.Embed(
                        title="Advertising Reminder",
                        color=message.guild.me.color
                    )
                    embed.add_field(
                        name='Disboard',
                        value=f'`every 2 hours`\nBump at [WEBSITE](https://disboard.org/server/{message.guild.id}) \nor with <@302050872383242240>:\n`!d bump`'
                    )
                    channel = self.bot.settings.get(
                        message.guild.id, {}
                    ).get("ad_reminder_channel_id")
                    channel = message.guild.get_channel(channel)
                    role = self.bot.settings.get(
                        message.guild.id, {}
                    ).get("ad_reminder_role_id")
                    role = message.guild.get_role(role)
                    await channel.send(
                        content=role.mention if role else None, embed=embed
                    )


    @tasks.loop(hours=1.0)
    async def ad_reminder(self):
        """Remind server admins to advertise when it's allowed"""
        for guild, settings in self.bot.settings.items():
            if settings["ad_reminder_channel_id"]:
                guild = self.bot.get_guild(int(guild))
                embed = discord.Embed(
                    title="Advertising Reminder",
                    color=guild.me.color
                )
                # Disboard - every 2 hours
                if settings["ad_reminder_disboard"] and datetime.now().hour % 2 == 0:
                    if datetime.now() > self.d_bumped.get(
                        guild.id,  datetime(2000, 1, 1)
                    ) + timedelta(hours=2):
                        embed.add_field(
                            name='Disboard',
                            value=f'`every 2 hours`\nBump at [WEBSITE](https://disboard.org/server/{guild.id}) \nor with <@302050872383242240>:\n`!d bump`'
                        )
                # Disforge - every 3 hours
                if settings["ad_reminder_disforge"] and datetime.now().hour % 3 == 0:
                    embed.add_field(
                        name='Disforge',
                        value=f'`every 3 hours`\nBump at [WEBSITE](https://disforge.com/dashboard)'
                    )
                # Discord.me
                if settings["ad_reminder_discordme"] and datetime.now().hour % 6 == 0:
                    embed.add_field(
                        name='Discord.me',
                        value=f'`every 6 hours`\nBump at [WEBSITE](https://discord.me/dashboard)'
                    )
                # discordservers
                if settings["ad_reminder_discordservers"] and datetime.now().hour % 12 == 0:
                    embed.add_field(
                        name="discordservers",
                        value=f'`every 12 hours`\nBump at [WEBSITE](https://discordservers.com/panel/{guild.id}/bump)'
                    )
                # top.gg
                if settings["ad_reminder_topgg"] and datetime.now().hour % 12 == 0:
                    embed.add_field(
                        name="top.gg",
                        value=f'`every 12 hours`\nBump at [WEBSITE](https://top.gg/servers/{guild.id}/vote)'
                    )                

                if embed.fields:
                    role = guild.get_role(int(settings["ad_reminder_role_id"]))
                    await guild.get_channel(
                        int(settings["ad_reminder_channel_id"])
                    ).send(content=role.mention if role else None, embed=embed)

    @ad_reminder.before_loop
    async def before_ad_reminder(self):
        """Sleeping until the full hour"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        await sleep((next_hour - now).total_seconds())

def setup(bot):
    bot.add_cog(SetAdReminder(bot))
