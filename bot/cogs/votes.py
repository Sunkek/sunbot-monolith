"""Automated server staff votes"""

from datetime import datetime, timedelta
from asyncio import sleep
from re import sub

import discord
from discord.ext import tasks, commands

from utils import util_users, util_user_stats, utils


class Votes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.numbers = {
            1:':1icon:658633333051228161', 2:':2icon:658633333692956673',
            3:':3icon:658633334255124480', 4:':4icon:658633333625847809',
            5:':5icon:658633333877637130', 6:':6icon:658633334217244682',
            7:':7icon:658633334288678922', 8:':8icon:658633334234152980',
            9:':9icon:658633334234021898', 10:':10icon:658633333919711235',
            11:':11icon:658633333395423242', 12:':12icon:658633334158524417',
            13:':13icon:658633334028763137', 14:':14icon:658633333688893444',
            15:':15icon:658633334171238410', 16:':16icon:658633334049734677',
            17:':17icon:658633333688893464', 18:':18icon:658633334141747200',
            19:':19icon:658633334183821322', 20:':20icon:658633334338879518',
            21:':21icon:658633334192341022', 22:':22icon:658633333911322624',
            23:':23icon:658633334036889613', 24:':24icon:658633334167175179',
            25:':25icon:658633334250930189', 26:':26icon:658633334234152981',
            27:':27icon:658633334556983317', 28:':28icon:658633334704046080',
            29:':29icon:658633334263644161', 30:':30icon:658633334548725780',
            31:':31icon:658633334456451082', 32:':32icon:658633334418702357',
            33:':33icon:658633334284484619', 34:':34icon:658633334540468244',
            35:':35icon:658633334695395351', 36:':36icon:658633334506913806',
            37:':37icon:658633334473228288', 38:':38icon:658633334208856085',
            39:':39icon:658633334347268137', 40:':40icon:658633334368370700',
            41:':41icon:658633334439542785', 42:':42icon:658633334490136587',
            43:':43icon:658633334473359370', 44:':44icon:658633334527623168',
            45:':45icon:658633334548856844', 46:':46icon:658633334489874462',
            47:':47icon:658633334527754260', 48:':48icon:658633334787932180',
            49:':49icon:658633334422896651', 50:':50icon:658633334288678913',
        }
        self.votes.start()

    def cog_unload(self):
        self.votes.cancel()

    @commands.Cog.listener() 
    async def on_raw_reaction_add(self, payload):
        # If ☑️, vote period and the voter has at least the active member role
        if str(payload.emoji) != "☑️":
            return
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        settings = self.bot.settings.get(guild.id)
        if message.author != guild.me or voter.bot:
            return
        now = datetime.now()
        junior_mod_vote_day = settings.get("vote_junior_mod_day")
        junior_mod_vote_months = settings.get("vote_junior_mod_months")
        senior_mod_vote_day = settings.get("vote_senior_mod_day")
        senior_mod_vote_months = settings.get("vote_senior_mod_months")
        admin_vote_day = settings.get("vote_admin_day")
        admin_vote_months = settings.get("vote_admin_months")
        voter = guild.get_member(payload.user_id)
        if not any((
            junior_mod_vote_day and junior_mod_vote_months and \
            junior_mod_vote_day <= now.day <= junior_mod_vote_day + 5 and \
            now.month in junior_mod_vote_months,
            senior_mod_vote_day and senior_mod_vote_months and \
            senior_mod_vote_day <= now.day <= senior_mod_vote_day + 5 and \
            now.month in senior_mod_vote_months,
            admin_vote_day and admin_vote_months and \
            admin_vote_day <= now.day <= admin_vote_day + 5 and \
            now.month in admin_vote_months,
        )):
            await message.remove_reaction('☑️', voter)
        active_member = guild.get_role(settings.get("rank_active_member_role_id"))
        junior_mod = guild.get_role(settings.get("rank_junior_mod_role_id"))
        senior_mod = guild.get_role(settings.get("rank_senior_mod_role_id"))
        if active_member not in voter.roles and \
            junior_mod not in voter.roles and \
            senior_mod not in voter.roles:
            await message.remove_reaction('☑️', voter)
        # Fetch the candidate list from the vote start message
        raw_candidates = message.embeds[0].description.split("\n")
        candidates = []
        for m in raw_candidates:
            m_id = sub("[^0-9]", "", m)
            m = guild.get_member(m_id) or await self.bot.fetch_user(m_id)
            print(m.display_name)

        # Build new embed(s) and send it(them) to the voter

    @tasks.loop(hours=24.0)
    async def votes(self):
        """Run the votes for server staff"""
        for guild, settings in self.bot.settings.items():
            now = datetime.now()
            guild = self.bot.get_guild(guild)
            vote_channel = guild.get_channel(settings.get("vote_channel_id"))
            if not vote_channel: continue

            active_member = guild.get_role(settings.get("rank_active_member_role_id"))
            junior_mod = guild.get_role(settings.get("rank_junior_mod_role_id"))
            senior_mod = guild.get_role(settings.get("rank_senior_mod_role_id"))
            admin = guild.get_role(settings.get("rank_admin_role_id"))
            # Determine which votes trigger

            # JM vote
            junior_mod_vote_day = settings.get("vote_junior_mod_day")
            junior_mod_vote_months = settings.get("vote_junior_mod_months")
            junior_mod_vote_limit = settings.get("vote_junior_mod_limit")
            if junior_mod_vote_day and junior_mod_vote_months and \
                now.day == junior_mod_vote_day and \
                now.month in junior_mod_vote_months:
                
                junior_mod_days = settings.get("rank_junior_mod_required_days")
                junior_mod_activity = settings.get("rank_junior_mod_required_activity")
                # Find eligible members    
                members = await util_users.fetch_users_by_days_and_activity(
                    self.bot, guild, junior_mod_days, junior_mod_activity
                )
                members = [
                    m for m in members 
                    if senior_mod not in m.roles
                    and admin not in m.roles
                ]
                activities = [
                    int(await util_user_stats.fetch_average_activity(
                        self.bot, guild.id, m.id, days_back=60
                    )) for m in members
                ]
                table = zip(activities, [f"`{m.mention}" for m in members])
                table = list(zip(*sorted(table, key=lambda t: -t[0])))
                table[0] = [f"`{i}" for i in table[0]]
                table = utils.format_columns(
                    table, 
                    headers=("`ACTIVITY", "MEMBER`")
                )
                # Post a list of them to the vote channel
                e = discord.Embed(
                    title=f"Junior mod vote start {now.year}/{now.month}",
                    description=table,
                    color=guild.me.color
                )
                e.add_field(
                    name="Terms",
                    value=(
                        "The vote is anonymous. React to this message with ☑️ to receive your form.\n"
                        "It's possible to get promoted, demoted or keep your current rank.\n"
                        "Make sure to vote for yourself if you want to get promoted.\n"
                        "Only members with at least 25% of max possible upvotes get promoted.\n"
                        f"The max number of {junior_mod.mention} that can be vote-picked is {junior_mod_vote_limit}.\n"
                        f"Only members with {active_member.mention} or higher role can vote here.\n"
                        "The vote results will be published in 5 days."
                    )
                )
                vote_msg = await vote_channel.send(embed=e)
                await vote_msg.add_reaction("☑️")
                # DM eligible voters the bulletins
            elif junior_mod_vote_day and junior_mod_vote_months and \
                now.day == junior_mod_vote_day + 5 and \
                now.month in junior_mod_vote_months:
                print("Junior mod vote end!")
                # Count the votes
                # Declare the results and implement them
            
            # SM vote
            senior_mod_vote_day = settings.get("vote_senior_mod_day")
            senior_mod_vote_months = settings.get("vote_senior_mod_months")
            if senior_mod_vote_day and senior_mod_vote_months and \
                now.day == senior_mod_vote_day and \
                now.month in senior_mod_vote_months:
                print("Senior mod vote start!")
                # Find eligible members    
                # Post a list of them to the vote channel
                # DM eligible voters the bulletins
            elif senior_mod_vote_day and senior_mod_vote_months and \
                now.day == senior_mod_vote_day + 5 and \
                now.month in senior_mod_vote_months:
                print("Senior mod vote end!")
                # Count the votes
                # Declare the results and implement them
            
            # A vote
            admin_vote_day = settings.get("vote_admin_day")
            admin_vote_months = settings.get("vote_admin_months")
            if admin_vote_day and admin_vote_months and \
                now.day == admin_vote_day and \
                now.month in admin_vote_months:
                print("Admin vote start!")
                # Find eligible members    
                # Post a list of them to the vote channel
                # DM eligible voters the bulletins
            elif admin_vote_day and admin_vote_months and \
                now.day == admin_vote_day + 5 and \
                now.month in admin_vote_months:
                print("Admin vote end!")
                # Count the votes
                # Declare the results and implement them
    
    # Enable this when the cog is functional
    '''@votes.before_loop
    async def before_votes(self):
        """Sleeping until the given time"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())'''


def setup(bot):
    bot.add_cog(Votes(bot))
