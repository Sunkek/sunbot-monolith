import discord
from discord.ext import commands, tasks

from random import shuffle

        
class SecretSanta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=60*60, type=commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.command(
        brief="Assigns secret Santas",
        help="Randomly pairs people who reacted to the target message with 🎅 and sends the givers DMs with their receivers. Also sends a list of pairs to the channel where you typed this command so you could control the event",
        aliases=["santa"]
    ) 
    async def secretsanta(
        self, ctx, 
        channel: discord.TextChannel, 
        message_id: int,
    ):
        try:
            # Make a list of participants
            message = await channel.fetch_message(message_id)
            givers = []
            for reaction in message.reactions:
                if reaction.emoji == "🎅":
                    givers = await reaction.users().flatten()
                    break
            if len(givers) < 2:
                raise commands.BadArgument
            # Make pairs of givers and receivers
            receivers = givers.copy()
            while any([g == r for g, r in zip(givers, receivers)]):
                shuffle(receivers)
            # Send DMs to the givers with their receivers
            link = (
                f"https://discordapp.com/channels/"
                f"{ctx.guild.id}/{channel.id}/{message_id}"
            )
            for g, r in zip(givers, receivers):
                desc = (
                    f"You have been assigned to be a secret Santa "
                    f"for {r.mention} ({r.display_name}) on {ctx.guild.name} "
                    f"because you reacted [here]({link})!"
                )
                e = discord.Embed(
                    title=f"Secret Santa on {ctx.guild.name}",
                    description=desc,
                    color=discord.Colour.red(),
                )
                await ctx.author.send(embed=e)  # Change it to DM givers!
            # Send a list of pairs to the command invoke channel
            desc = "\n".join([
                f"{g.mention} - {r.mention}" 
                for g, r in zip(givers, receivers)
            ])
            e = discord.Embed(
                title="Secret Santa Pairs",
                color=ctx.author.color,
                description=desc
            )
            await ctx.send(embed=e)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(SecretSanta(bot))