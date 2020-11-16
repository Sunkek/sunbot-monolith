import discord
from discord.ext import commands
from typing import Optional

from utils import util_settings


class PingRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="pingroulette", 
        aliases=["pr"],
        description="Spends your ping roulette charge, pings 3 random members and gives them a ping roulette charge. \nTo opt-out, type `pingroulette out`. \nTo spend your charge, type `pingroulette spin`. \nTo check your unspent charges, type `pingroulette charges`. \nTo see the list of members with unspent charges, type `pingroulette list`.",
        invoke_without_command=True,
    )
    async def pingroulette(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.bot.get_command("help"), target="pingroulette")
            "ctx.author.guild_permissions.administrator"

def setup(bot):
    bot.add_cog(PingRoulette(bot))