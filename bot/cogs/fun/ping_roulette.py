import discord
from discord.ext import commands
from typing import Optional
from random import sample

from utils import util_fun


class PingRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="pingroulette", 
        aliases=["pr"],
        brief="Root command",
        help="The root ping roulette command. Use with subcommands!\n\nThis is a luck game. Server admins start the game by using `pingroulette spin`, which gives 3 random members ping roulette charges. They then can opt-out of the game or use their charge to spin the roulette again.",
        invoke_without_command=True,
    )
    async def pingroulette(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.bot.get_command("help"), target="pingroulette")
    
    @commands.cooldown(1, 60*10, type=commands.BucketType.guild)
    @pingroulette.command(
        name="spin",
        aliases=["s"],
        brief="Pings 3 random members",
        help="Spend your ping roulette charge to ping 3 random members."
    )
    async def pingroulette_spin(self, ctx):
        ok = await util_fun.spend_pr_charge(
            self.bot, ctx.author.id, ctx.guild.id
        )
        if ok or ctx.author.guild_permissions.administrator:
            opted_out = await util_fun.opted_out_of_pr(self.bot, ctx.guild.id)
            print(opted_out)
            members = [i for i in ctx.guild.members if not i.bot and i.id not in opted_out]
            members = sample(members, 3)
            e = discord.Embed(
                title="Ping Roulette",
                description="Congratulations! You have won the ping roulette! It means that now you have one more ping roulette charge. Use the `help pingroulette` command to see your options.",
                color=ctx.author.color,
            )
            channel = ctx.guild.get_channel(
                self.bot.settings.get(ctx.guild.id, {}).get("ping_roulette_channel")
            )
            pings = [i.mention for i in members]
            pings = "\n".join(pings)
            await channel.send(pings, embed=e)

            for member in members:
                await util_fun.give_pr_charge(self.bot, member.id, ctx.guild.id)
        else:
            e = discord.Embed(
                title="Ping Roulette",
                description="You need at least one ping roulette charge to spin it!",
                color=ctx.author.color,
            )
            await ctx.channel.send(embed=e)


    @pingroulette.command(
        name="out",
        aliases=["o"],
        brief="Opt-out of the ping roulette",
        help="Opt-out of the ping roulette. Only works if you have at least one PR charge."
    )
    async def pingroulette_out(self, ctx):
        e = discord.Embed(
            title="Ping Roulette Opt-Out",
            color=ctx.author.color,
        )
        charges = await util_fun.fetch_charges(
            self.bot, ctx.author.id, ctx.guild.id
        )
        if charges > 0:
            await util_fun.opt_out_of_pr(self.bot, ctx.author.id, ctx.guild.id)
            e.description = f"{ctx.author.mention} won't be targeted in the ping roulette on this server."
        else:
            e.description = f"{ctx.author.mention} can't opt-out of the ping roulette on this server, because they don't hve PR charges! Win the roulette to opt-out."
        await ctx.send(embed=e)

    @pingroulette.command(
        name="charges",
        aliases=["c"],
        brief="Shows your ping roulette charges",
        help="Shows how many ping roulette charges you have."
    )
    async def pingroulette_charges(self, ctx, target: discord.Member=None):
        target = target or ctx.author
        charges = await util_fun.fetch_charges(
            self.bot, target.id, ctx.guild.id
        )
        e = discord.Embed(
            title="Ping Roulette Charges",
            description=f"{target.mention} has **{charges or 0}** ping roulette charges.",
            color=ctx.author.color,
        )
        await ctx.send(embed=e)

    @pingroulette.command(
        name="list",
        aliases=["l"],
        brief="Lists members with ping roulette charges",
        help="Shows the members with at least one ping roulette charge."
    )
    async def pingroulette_list(self, ctx):
        members = await util_fun.fetch_active_members(self.bot, ctx.guild.id)
        members = [ctx.guild.get_member(i).display_name for i in members]
        members = "\n".join(members)
        e = discord.Embed(
            title="Ping Roulette Active Members",
            description=f"These members have at least one active ping roulette charge:\n\n{members}",
            color=ctx.author.color,
        )
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(PingRoulette(bot))
