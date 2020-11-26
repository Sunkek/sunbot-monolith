from utils.utils import int_convertable

SELECT_TABLE_NAMES = """
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
"""
CREATE_GUILDS_TABLE = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id bigint PRIMARY KEY,

    birthday_feed_channel_id bigint,

    track_messages boolean DEFAULT 'false',
    track_reactions boolean DEFAULT 'false',
    track_voice boolean DEFAULT 'false',
    track_games boolean DEFAULT 'false',

    activity_per_message smallint,
    activity_min_message_words smallint,
    activity_multi_per_word double precision,
    activity_per_attachment smallint,
    activity_cooldown smallint,
    activity_per_reaction smallint,
    activity_per_voice_minute smallint,
    activity_multi_per_voice_member double precision,
    activity_channels_x0 bigint[],
    activity_channels_x05 bigint[],
    activity_channels_x2 bigint[],
    
    rank_mute_role_id bigint,
    rank_basic_member_role_id bigint,
    rank_basic_member_role_auto boolean DEFAULT 'false'
    rank_active_member_role_id bigint,
    rank_active_member_required_days smallint,
    rank_active_member_required_activity smallint,
    rank_junior_mod_role_id bigint,
    rank_junior_mod_required_days smallint,
    rank_junior_mod_required_activity smallint,
    rank_senior_mod_role_id bigint,
    rank_senior_mod_required_days smallint,
    rank_senior_mod_required_activity smallint,
    rank_admin_role_id bigint,
    rank_admin_required_days smallint,
    rank_admin_required_activity smallint,

    ad_reminder_channel_id bigint,
    ad_reminder_role_id bigint,
    ad_reminder_disboard boolean DEFAULT 'false',
    ad_reminder_disforge boolean DEFAULT 'false',
    ad_reminder_discordme boolean DEFAULT 'false',
    ad_reminder_discordservers boolean DEFAULT 'false',
    ad_reminder_topgg boolean DEFAULT 'false',

    welcome_message_channel_id bigint,
    welcome_message_text varchar(2000),
    welcome_message_embed varchar(6000),
);
"""
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id bigint PRIMARY KEY,
    birthday date,
    steam varchar(2000),
    country varchar(50)
);
"""
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    guild_id bigint REFERENCES guilds(guild_id),
    channel_id bigint,
    user_id bigint REFERENCES users(user_id),
    postcount integer,
    attachments smallint,
    words integer,
    period date,
    PRIMARY KEY (guild_id, channel_id, user_id, period)
);
"""
CREATE_REACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS reactions (
    guild_id bigint REFERENCES guilds(guild_id),
    channel_id bigint,
    giver_id bigint REFERENCES users(user_id),
    receiver_id bigint REFERENCES users(user_id),
    emoji varchar(100),
    count smallint,
    period date,
    PRIMARY KEY (guild_id, channel_id, giver_id, receiver_id, emoji, period)
);
"""
CREATE_VOICE_TABLE = """
CREATE TABLE IF NOT EXISTS voice (
    guild_id bigint REFERENCES guilds(guild_id),
    channel_id bigint,
    user_id bigint REFERENCES users(user_id),
    members smallint,
    count smallint,
    period date,
    PRIMARY KEY (guild_id, channel_id, user_id, members, period)
);
"""
CREATE_GAMES_TABLE = """
CREATE TABLE IF NOT EXISTS games (
    user_id bigint REFERENCES users(user_id),
    game varchar(100),
    duration integer,
    period date,
    PRIMARY KEY (user_id, game, period)
);
"""
CREATE_ACTIVITY_TABLE = """
CREATE TABLE IF NOT EXISTS activity (
    user_id bigint REFERENCES users(user_id),
    guild_id bigint REFERENCES guilds(guild_id),
    period date,
    from_text bigint DEFAULT 0,
    from_attachments bigint DEFAULT 0,
    from_reactions bigint DEFAULT 0,
    from_voice bigint DEFAULT 0,
    PRIMARY KEY (user_id, guild_id, period)
);
"""
CREATE_PING_ROULETTE_TABLE = """
CREATE TABLE IF NOT EXISTS ping_roulette (
    user_id bigint REFERENCES users(user_id),
    guild_id bigint REFERENCES guilds(guild_id),
    charges smallint,
    won smallint,
    plays bool DEFAULT true,
    PRIMARY KEY (user_id, guild_id)
);
"""
CREATE_MUTED_TABLE = """
CREATE TABLE IF NOT EXISTS muted (
    guild_id bigint REFERENCES guilds(guild_id),
    user_id bigint REFERENCES users(user_id),
    start timestamp,
    duration smallint,
    PRIMARY KEY (guild_id, user_id)
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
            if "users" not in tables:
                await connection.execute(CREATE_USERS_TABLE)
            if "messages" not in tables:
                await connection.execute(CREATE_MESSAGES_TABLE)
            if "reactions" not in tables:
                await connection.execute(CREATE_REACTIONS_TABLE)
            if "voice" not in tables:
                await connection.execute(CREATE_VOICE_TABLE)
            if "games" not in tables:
                await connection.execute(CREATE_GAMES_TABLE)
            if "activity" not in tables:
                await connection.execute(CREATE_ACTIVITY_TABLE)
            if "ping_roulette" not in tables:
                await connection.execute(CREATE_PING_ROULETTE_TABLE)
            if "muted" not in tables:
                await connection.execute(CREATE_MUTED_TABLE)
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

async def change_guild_setting_list(bot, guild_id, setting, targets):
    settings = bot.settings.get(guild_id, dict())
    was_set = settings.get(setting, list()) or list()
    new_elements = set(targets).difference(was_set)
    new_setting = {
        setting: list(set(was_set).difference(targets).union(new_elements))
    }
    await change_guild_setting(bot, guild_id, **new_setting)

def format_settings_key(input_string):
    replace_pairs = [
        ("activity_", ""), ("track_", ""), ("ad_reminder_", ""), 
        ("verification_", ""), ("rank_", ""),
        ("junior", "jr"), ("senior", "sr"), ("required", "req"),
        ("message", "msg"), ("channel", "chnl"), ("member", "mbr"), 
        ("_id", ""), ("_", " "),
    ]
    for before, after in replace_pairs:
        input_string = input_string.replace(before, after)
    input_string = input_string.lstrip(" ").capitalize()
    return f'`{input_string}`'
    
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
        elif type(value) == dict or type(value) == list or \
            str(value).startswith("{") and str(value).endswith("}"):
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