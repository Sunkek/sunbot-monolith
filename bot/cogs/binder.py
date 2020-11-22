import discord
from discord.ext import commands

from datetime import datetime, timedelta
from pycountry import countries
from bs4 import BeautifulSoup
from typing import Optional

from utils import util_users


class Binder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(
        brief="Add your info to the bot",
        help="Adds information to your profile in this bot's database. Use without value to reset.", 
        aliases = ["b"], 
        invoke_without_command=False,
    )
    async def bind(self, ctx):
        pass

    @bind.command(
        brief="Adds your birthday date",
        help="Adds the birthday date to your entry in the database. It will be used in the birthday feed, if one is set up for a server you're in.", 
        name="birthday",
    )
    async def bind_birthday(self, ctx, birthday=None):
        if birthday:
            birthday = datetime.strptime(birthday, "%d/%m/%Y")
            if datetime.now() - birthday > timedelta(days=365*100):
                raise commands.BadArgument
            birthday = birthday.strftime("%Y-%m-%d")
            print(birthday)
        await util_users.change_user_info(self.bot, ctx.author.id, birthday=birthday)

    @bind.command(
        brief="Add your country",
        help="Adds the country to your entry in the database. Use the official name or 2 or 3 letter code", 
        name="country"
    )
    async def bind_country(self, ctx, *, country="reset"):
        # Check the country name
        if country != "reset":
            country = countries.lookup(country) 
            if country:
                country = country.name
            else:
                raise commands.BadArgument
        await util_users.change_user_info(self.bot, ctx.author.id, country=country)
                
    @bind.command(
        brief="Add your steam",
        help="Adds the steam profile to your entry in the database. Use the link to your profile.", 
        name="steam"
    )
    async def bind_steam(self, ctx, *, steam="reset"):
        # Bring the link to universal format
        if steam != "reset":
            steam = steam.rstrip("/").split("/")
            steam_id = steam[-1]
            if not steam_id.isdigit() or steam[-2] != "profiles":
                url = f"https://steamcommunity.com/id/{steam_id}/?xml=1"
                async with self.bot.web.get(url) as resp:
                    raw_user = await resp.text()
                    soup = BeautifulSoup(raw_user, 'lxml-xml')
                    steam_id = soup.find('steamID64').string
        await util_users.change_user_info(self.bot, ctx.author.id, steam=steam_id)
                

def setup(bot):
    bot.add_cog(Binder(bot))