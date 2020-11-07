"""My Discord bot, made to automate the boring admin work
and to track server statistics."""

import os
from random import choice, seed
from datetime import datetime

import discord 
from discord.ext import commands
from asyncpg import create_pool
from aiohttp import ClientSession, TCPConnector
from socket import AF_INET
from asyncio import TimeoutError

from utils.settings import read_settings


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("sb ", "Sb ", "SB "), 
    сase_insensitive=True,
    chunk_guilds_at_startup=True  # Slows launch, especially for lots of guilds
)
# Remove the default help command because there will be a custom one
bot.remove_command("help")
# Create bot variables
bot.web = None
bot.db = None
bot.settings = None
bot.error_titles = (
    "No", "Nope", "I don't think so", "Not gonna happen", "Nah", "Not likely", 
    "Fat chance", "Fuck you", "Good try, asshole", "No way", 
    "Did you really think I would do that?", "Do this shit yourself",
)
# Read cog names
cogs = []
for (dirpath, dirnames, filenames) in os.walk(f"{os.getcwd()}/cogs/"):
    if "__pycache__" not in dirpath:
        # Get relative cog path, strip the .py extension 
        # and replace slashes with dots for cog import
        cogs += [
            os.path.join(dirpath, file).replace(
                f"{os.getcwd()}/",
                ""
            ).replace(".py", "").replace("/", ".") .replace("\\", ".") 
            for file in filenames if "pycache" not in file
        ]
        
@bot.event
async def on_ready():
    # Create web client session
    if not bot.web:
        bot.web = ClientSession(
            loop=bot.loop,
            connector=TCPConnector( 
                family=AF_INET,  # https://github.com/aio-libs/aiohttp/issues/2522#issuecomment-354454800
                ssl=False, 
                ),
            )
    # Create the database connection pool
    if not bot.db:
        bot.db = await create_pool(
            loop=bot.loop,
            database=os.environ.get("SQL_DATABASE"),
            user=os.environ.get("SQL_USER"), 
            password=os.environ.get("SQL_PASSWORD"),
            host=os.environ.get("SQL_HOST"),
            port=os.environ.get("SQL_PORT"),
        )
    # Read saved settings from the DB
    if not bot.settings:
        bot.settings = await read_settings(bot.db)
    # Load cogs
    if not bot.cogs:
        for cog in cogs:
            try:
                if cog not in bot.cogs.values():
                    bot.load_extension(cog)
            except Exception as e:
                print(f"Error on loading {cog}:\n{e}")
            else:
                print(f"Cog {cog} loaded")
    await bot.change_presence(activity=discord.Game(name=("sb ")))
    print(f"{bot.user} online")
    print(datetime.now())

@bot.event 
async def on_message(message):
    await bot.wait_until_ready()
    # Ping reee
    if bot.user.mentioned_in(message):
        await message.add_reaction("a:ping:456710949215272981")  # The emoji is from apoc
    # Without this it will ignore all commands
    if not message.author.bot:
        await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    await ctx.message.add_reaction("👌")

@bot.event 
async def on_command_error(ctx, error):
    """Command error handler"""
    await ctx.message.add_reaction("✋")
    seed()  # Refresh random seed just in case
    embed = discord.Embed(
        title=choice(bot.error_titles),
        color=ctx.author.color
    )
    if isinstance(error, commands.CommandNotFound):
        embed.description = "There is no such command."
        return await ctx.send(embed=embed)
    if ctx.command.description:
        embed.add_field(
            name="Command help", 
            value=ctx.command.description,
            inline=False
        )
    if isinstance(error, TimeoutError):
        embed.description = "You took too long to reply."
    elif isinstance(error, commands.MissingPermissions):
        embed.description = (
            "You are missing permissions to use this "
            f"command: **{error.missing_perms[0]}**."
        )
    elif isinstance(error, commands.BadArgument):
        embed.description = "Something is wrong with the arguments."
        if ctx.command.description:
            embed.add_field(
                name="Command help", 
                value=ctx.command.description,
                inline=False
            )
    else:
        embed.description = "Something went wrong."
        embed.add_field(
            name="Error", 
            value=error,
            inline=False
        )
    await ctx.send(embed=embed)

@commands.check(commands.is_owner())
@bot.command(description=f"`reload <cog name>` - reloads the specified cog")
async def reload(ctx, *, ext):
    cog = f"cogs.{ext}"
    try:
        bot.unload_extension(cog)
    except commands.ExtensionNotLoaded:
        pass
    bot.load_extension(cog)

@commands.check(commands.is_owner())
@bot.command(description=f"`sql <query>` - runs the provided SQL")
async def sql(ctx, *, query):
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            result = await connection.execute(query)
    embed = discord.Embed(
        title="SQL ran",
        description=result or "No output",
        color=ctx.author.color
    )
    await ctx.send(embed=embed)

bot.run(os.environ.get("DISCORD_TOKEN"))