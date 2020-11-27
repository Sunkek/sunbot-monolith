import json

import discord
from discord.ext import commands, tasks

from utils import utils

async def send_welcome_or_leave(channel, text, embed, member):
    text = utils.format_message(text, guild=member.guild, user=member)
    print(text)
    embed = discord.Embed.from_dict(
        utils.format_message(json.loads(embed), guild=member.guild, user=member)
    )
    print(embed)
    if embed:
        await channel.send(content=text, embed=embed)
    elif text:
        await channel.send(text)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends the initial welcome message"""
        channel = self.bot.settings.get(member.guild.id, {}).get("welcome_message_channel_id", 0)
        text = self.bot.settings.get(member.guild.id, {}).get("welcome_message_text")
        embed = self.bot.settings.get(member.guild.id, {}).get("welcome_message_embed")
        channel = member.guild.get_channel(channel)
        if channel and (text or embed):
            await send_welcome_or_leave(channel, text, embed, member)
            
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Sends the leave message"""
        channel = self.bot.settings.get(member.guild.id, {}).get("welcome_message_channel_id", 0)
        text = self.bot.settings.get(member.guild.id, {}).get("leave_message_text")
        embed = self.bot.settings.get(member.guild.id, {}).get("leave_message_embed")
        channel = member.guild.get_channel(channel)
        if channel and (text or embed):
            await send_welcome_or_leave(channel, text, embed, member)
            
    @commands.command(
        brief="Displays the current welcome message", 
        help="Displays the current welcome message. Add `parse` to see how it would be parsed", 
        name='displaywelcome',
        aliases = ["dw"]
    )
    async def displaywelcome(self, ctx, parse=""):
        text = self.bot.settings.get(ctx.guild.id, {}).get("welcome_message_text")
        embed = self.bot.settings.get(ctx.guild.id, {}).get("welcome_message_embed")
        if (text or embed) and parse:
            await send_welcome_or_leave(ctx.channel, text, embed, ctx.author)
        elif embed:
            await ctx.send(text, embed=discord.Embed.from_dict(json.loads(embed)))
        elif text:
            await ctx.send(text)
        else:
            raise commands.UserInputError(message="No welcome message set!")
    
    @commands.command(
        brief="Displays the current leave message", 
        help="Displays the current leave message. Add `parse` to see how it would be parsed", 
        name='displayleave',
        aliases = ["dl"]
    )
    async def displayleave(self, ctx, parse=""):
        text = self.bot.settings.get(ctx.guild.id, {}).get("leave_message_text")
        embed = self.bot.settings.get(ctx.guild.id, {}).get("leave_message_embed")
        if (text or embed) and parse:
            return await send_welcome_or_leave(ctx.channel, text, embed, ctx.author)
        elif embed:
            await ctx.send(text, embed=discord.Embed.from_dict(json.loads(embed)))
        elif text:
            await ctx.send(text)
        else:
            raise commands.UserInputError(message="No leave message set!")
def setup(bot):
    bot.add_cog(Welcome(bot))