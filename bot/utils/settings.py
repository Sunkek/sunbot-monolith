SELECT_TABLE_NAMES = """
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
"""
CREATE_GUILDS_TABLE = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id bigint PRIMARY KEY,

    track_messages boolean DEFAULT 'false'
);"""

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
            # Fetch the settings
            settings = await connection.fetch("SELECT * FROM guilds")
            settings = format_setting(settings)
    print(settings)
    return settings
        
async def change_guild_setting(bot, guild_id, **kwargs):
    """Change guild settings"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            args = [(k, v, guild_id) for k,v in kwargs.items()]
            print(args)
            await connection.executemany(
                "UPDATE guilds SET $1 = $2 WHERE guild_id = $3;", args
            )
            guild = bot.settings.setdefault(guild_id, {})
            for key, value in kwargs.items():  
                if value == "reset": guild[key] = None
                else: guild[key] = value