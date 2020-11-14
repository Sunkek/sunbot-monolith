from utils.utils import int_convertable

SELECT_TABLE_NAMES = """
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
"""
CREATE_GUILDS_TABLE = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id bigint PRIMARY KEY,

    track_messages boolean DEFAULT 'false',
    track_reactions boolean DEFAULT 'false'
);
"""
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    guild_id bigint,
    channel_id bigint,
    user_id bigint,
    postcount integer,
    attachments smallint,
    words integer,
    period date,
    PRIMARY KEY (guild_id, channel_id, user_id, period)
);
"""
CREATE_REACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS reactions (
    guild_id bigint,
    channel_id bigint,
    giver_id bigint,
    receiver_id bigint,
    emoji varchar(100),
    count smallint,
    period date,
    PRIMARY KEY (guild_id, channel_id, giver_id, receiver_id, emoji, period)
);
"""
CREATE_VOICE_TABLE = """
CREATE TABLE IF NOT EXISTS voice (
    guild_id bigint,
    channel_id bigint,
    user_id bigint,
    members smallint,
    count smallint,
    period date,
    PRIMARY KEY (guild_id, channel_id, user_id, period)
);
"""
CREATE_GAMES_TABLE = """
CREATE TABLE IF NOT EXISTS games (
    user_id bigint,
    game varchar(100),
    duration integer,
    period date,
    PRIMARY KEY (user_id, game, period)
);
"""

def format_setting(records):
    """Change a list of records into a dict of settings per guild id"""
    result = {i["guild_id"]: {
        k: v for k, v in i.items() if k != "guild_id"
    } for i in records}
    return result

async def read_settings(connection_pool):
    """Read bot settings from the database. 
    Create missing tables if there are any."""
    settings = dict()
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            # Create tables if they don't exist
            tables = await connection.fetch(SELECT_TABLE_NAMES)
            tables = [i["table_name"] for i in tables]
            if "guilds" not in tables:
                await connection.execute(CREATE_GUILDS_TABLE)
            if "messages" not in tables:
                await connection.execute(CREATE_MESSAGES_TABLE)
            if "reactions" not in tables:
                await connection.execute(CREATE_REACTIONS_TABLE)
            if "voice" not in tables:
                await connection.execute(CREATE_VOICE_TABLE)
            if "games" not in tables:
                await connection.execute(CREATE_GAMES_TABLE)
            # Fetch the settings
            settings = await connection.fetch("SELECT * FROM guilds")
            settings = format_setting(settings)
    return settings
        
async def change_guild_setting(bot, guild_id, **kwargs):
    """Change guild settings"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            guild = bot.settings.setdefault(guild_id, {})
            for k, v in kwargs.items():
                res = await connection.execute(
                    # TODO Editing the query string is dangerous, check later
                    f"UPDATE guilds SET {k} = $1 WHERE guild_id = $2;", 
                    v, guild_id
                )
                if " 0" in res:
                    await connection.execute(
                    # TODO Editing the query string is dangerous, check later
                    f"INSERT INTO guilds(guild_id, {k}) VALUES ($1, $2);", 
                    guild_id, v
                )
                if v == "reset": guild[k] = None
                else: guild[k] = v
    
def format_settings_key(string):
    result = string.lower().replace("activity_", "").replace("track_", "")
    result = result.replace("ad_reminder_", "").replace("verification_", "")
    result = result.replace("rank_", "")
    result = result.lstrip("_").replace("_id", "").replace("_", " ").capitalize()
    return f'`{result}`'
    
def format_settings_value(guild, value):
    if type(value) == list:
        result = []
        for i in sorted(value):
            formatted_value = ""
            if int_convertable(i):
                formatted_value = guild.get_channel(int(i))
                if not formatted_value:
                    formatted_value = guild.get_role(int(i))
                if not formatted_value:
                    formatted_value = guild.get_member(int(i))
                if formatted_value:
                    formatted_value = formatted_value.mention
            if not formatted_value:
                formatted_value = str(i)
            result.append(formatted_value)
        result = ", ".join(result)
    else:
        result = ""        
        if int_convertable(value) and not type(value) == bool:
            result = guild.get_channel(int(value))
            if not result:
                result = guild.get_role(int(value))
            if not result:
                result = guild.get_member(int(value))
            if result:
                result = result.mention
        elif type(value) == dict or type(value) == list:
            result = "Set"
        elif value == True:
            result = "On"
        if not result:
            result = value
    return result

def format_settings(settings, ctx, include=[], ignore=[]):
    return "\n".join([
        f"{format_settings_key(key)}: \
            {format_settings_value(ctx.guild, value)}"
        for key, value in settings.items()
        if value \
            and any([i in key for i in include] if include else [True]) \
            and all([i not in key for i in ignore])])